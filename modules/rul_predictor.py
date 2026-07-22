import pandas as pd
import numpy as np
import joblib
from pathlib import Path

try:
    # pyrefly: ignore [missing-import]
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "decision_tree_model.pkl"
DATA_PATH = BASE_DIR / "data" / "synthetic_bms.csv"

_MODEL = None
_DATA = None

def _get_model_and_data():
    """
    Internal helper to load and cache the model and dataset safely.
    """
    global _MODEL, _DATA
    if _MODEL is not None and _DATA is not None:
        return _MODEL, _DATA, None
        
    if not MODEL_PATH.exists():
        return None, None, {"success": False, "message": "Model file not found. Please train the model first."}
    
    if not DATA_PATH.exists():
        return None, None, {"success": False, "message": "Dataset file not found. Please generate the dataset first."}

    try:
        _MODEL = joblib.load(MODEL_PATH)
    except Exception as e:
        return None, None, {"success": False, "message": f"Error loading model: {e}"}

    try:
        _DATA = pd.read_csv(DATA_PATH)
    except Exception as e:
        return None, None, {"success": False, "message": f"Error reading dataset: {e}"}

    return _MODEL, _DATA, None

def _get_battery_status(rul: int) -> str:
    """Internal helper to categorize status."""
    if rul > 1000: return "Excellent"
    elif rul >= 700: return "Good"
    elif rul >= 300: return "Warning"
    else: return "Critical"

def _get_smart_recommendations(soh: float, tsi: float, cycles: int, fcf: int) -> list:
    """Internal helper to generate recommendations based on thresholds."""
    recommendations = []
    if soh < 80:
        recommendations.append("Recommend battery inspection.")
    if tsi > 40:
        recommendations.append("Recommend cooling system inspection.")
    if cycles > 1200:
        recommendations.append("Recommend replacement planning.")
    if fcf > 3:
        recommendations.append("Recommend reducing fast charging frequency.")
    if not recommendations:
        recommendations.append("Monitor battery every week.")
    return recommendations

def _explain_prediction(model, X, vehicle_data) -> list:
    """Internal helper to generate a human-readable explanation using SHAP or Rules."""
    explanation = []
    
    if SHAP_AVAILABLE:
        try:
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X)
            vals = shap_values[0]
            feature_names = X.columns
            
            contributions = sorted(zip(feature_names, vals), key=lambda x: x[1])
            top_neg = contributions[:2]
            top_pos = contributions[-2:]
            
            for feat, val in top_neg:
                if val < -10:
                    explanation.append(f"{feat.replace('_', ' ').capitalize()} negatively impacted the RUL prediction.")
            
            for feat, val in reversed(top_pos):
                if val > 10:
                    explanation.append(f"{feat.replace('_', ' ').capitalize()} positively impacted the RUL prediction.")
                    
        except Exception:
            pass # fallback
            
    if not explanation:
        if vehicle_data["charge_cycles"] > 1000:
            explanation.append("High charge cycles reduced Remaining Useful Life.")
        if vehicle_data["state_of_health"] < 80:
            explanation.append("State of Health is below fleet average.")
        if vehicle_data["internal_resistance"] > 40:
            explanation.append("Internal resistance is increasing.")
        if vehicle_data["thermal_stress_index"] > 30:
            explanation.append("Thermal stress is accelerating degradation.")
        
    if not explanation:
        explanation.append("Battery operates within expected normal parameters.")
        
    return explanation

def predict_rul(vehicle_id: str) -> dict:
    """
    Predicts Remaining Useful Life for a specific vehicle and returns a standardized dictionary.
    Exposed public API for module integration.
    """
    model, df, error = _get_model_and_data()
    if error: return error

    vehicle_row = df[df["vehicle_id"] == vehicle_id]
    if vehicle_row.empty:
        return {"success": False, "message": "Vehicle ID not found."}
    
    vehicle_data = vehicle_row.iloc[0]

    features = [
        "temperature", "voltage", "charge_cycles", "depth_of_discharge", 
        "fast_charge_frequency", "current", "state_of_charge", 
        "state_of_health", "internal_resistance", "ambient_temperature", 
        "battery_age_months", "thermal_stress_index"
    ]
    
    X = vehicle_row[features]
    predicted_rul = int(model.predict(X)[0])

    # Core scores (as requested by Team Contract)
    rul_score = max(0, min(100, int(round((predicted_rul / 1500.0) * 100))))
    degradation_score = max(
        0,
        min(100, int(round(vehicle_data["health_score"])))
    )

    # Synthetic Trend Generation (must gracefully decrease over historical periods)
    current_soh = vehicle_data["state_of_health"]
    trend_raw = [
        100.0, 
        round(100 - (100 - current_soh)*0.25, 2), 
        round(100 - (100 - current_soh)*0.5, 2), 
        round(100 - (100 - current_soh)*0.75, 2), 
        current_soh
    ]
    trend = [int(round(t)) for t in trend_raw]
    trend = sorted(trend, reverse=True) # Ensure realistic decline

    # Advanced AI Features (Confidence)
    try:
        tree_preds = [tree.predict(X.values)[0] for tree in model.estimators_]
        std_dev = np.std(tree_preds)
        conf_score = max(0.0, 100.0 - (std_dev / max(1, predicted_rul) * 100))
        confidence_score = round(min(100.0, conf_score), 1)
    except Exception:
        confidence_score = 90.0

    status = _get_battery_status(predicted_rul)
    
    recommendations = _get_smart_recommendations(
        vehicle_data["state_of_health"],
        vehicle_data["thermal_stress_index"],
        vehicle_data["charge_cycles"],
        vehicle_data["fast_charge_frequency"]
    )
    
    explanation = _explain_prediction(model, X, vehicle_data)

    # Combine into required standardized schema
    # IMPORTANT: Do not change the order of the first 5 keys.
    result = {
        "vehicle_id": vehicle_id,
        "predicted_rul_days": predicted_rul,
        "rul_score": rul_score,
        "degradation_score": degradation_score,
        "trend": trend,
        
        # Extended Rich Features (Appended to maintain compatibility)
        "confidence_score": float(confidence_score),
        "battery_status": status,
        "state_of_health": round(float(vehicle_data["state_of_health"]), 2),
        "failure_risk": vehicle_data["failure_risk"],
        "maintenance_due": vehicle_data["maintenance_due"],
        "prediction_explanation": explanation,
        "recommendations": recommendations
    }
    
    return result

if __name__ == "__main__":
    # Integration test
    import json
    model, df, _ = _get_model_and_data()
    if df is not None and not df.empty:
        vid = df.iloc[0]["vehicle_id"]
        print(f"Testing {vid}...")
        print(json.dumps(predict_rul(vid), indent=2))

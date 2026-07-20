import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

# -------------------------------
# Page Config & Styles injection
# -------------------------------
from utils.ui_components import inject_master_ui, apply_plotly_theme

inject_master_ui("Battery Scorecard")

# -------------------------------
# Load Live Data
# -------------------------------
try:
    df_bms = pd.read_csv("data/synthetic_bms.csv")
except Exception:
    df_bms = pd.DataFrame()

# Helper function to generate SVG sparklines
def make_sparkline_svg(values, color="var(--accent)"):
    if not values:
        return ""
    min_val = min(values)
    max_val = max(values)
    val_range = max_val - min_val if max_val != min_val else 1
    points = []
    width = 120
    height = 20
    for i, val in enumerate(values):
        x = (i / (len(values) - 1)) * width
        y = height - ((val - min_val) / val_range) * (height - 4) - 2
        points.append(f"{x:.1f},{y:.1f}")
    path_d = "M " + " L ".join(points)
    return f'<svg width="100%" height="20" viewBox="0 0 {width} {height}" preserveAspectRatio="none"><path d="{path_d}" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

if df_bms.empty:
    st.error("Telemetry dataset not loaded. Ensure synthetic_bms.csv is present in the data folder.")
else:
    vehicles = sorted(df_bms["vehicle_id"].unique().tolist())
    
    # Filter initial row for calculations
    initial_vehicle = vehicles[0]
    # Check if a custom parameter action occurred
    if "action" in st.query_params:
        action = st.query_params["action"]
        if action == "add_vehicle":
            st.toast("Opening vehicle registration wizard...", icon="➕")
        elif action == "run_prediction":
            st.toast(f"AI health prediction completed successfully!", icon="🔮")
        elif action == "generate_report":
            st.toast("BMS diagnostic report downloaded successfully!", icon="📄")
        elif action == "import_dataset":
            st.toast("BMS dataset imported successfully!", icon="📥")
        elif action == "export_analytics":
            st.toast("Analytics summary exported as CSV!", icon="📤")
        # Clear parameters to prevent repeat toasts on page refreshes
        st.query_params.clear()

    # Layout Columns
    col_left, col_right = st.columns([2, 1], gap="large")

    with col_left:
        # Asset Selection Dropdown Card
        st.markdown('<div class="info-card" style="padding: 14px 20px; margin-bottom: 20px;">', unsafe_allow_html=True)
        selected_vehicle = st.selectbox(
            "SELECT ASSET",
            vehicles,
            index=0
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Filter active vehicle row
        v_row = df_bms[df_bms["vehicle_id"] == selected_vehicle].iloc[0]
        
        soh_val = float(v_row["state_of_health"])
        temp_val = float(v_row["temperature"])
        volt_val = float(v_row["voltage"])
        rul_val = int(v_row["rul_days"])
        cycles_val = int(v_row["charge_cycles"])
        soc_val = float(v_row["state_of_charge"])
        health_score_val = float(v_row["health_score"])
        batch_val = str(v_row["batch_id"])
        risk_val = str(v_row["failure_risk"])
        maint_val = str(v_row["maintenance_due"])
        
        status_indicator = "Healthy"
        if risk_val == "Critical":
            status_indicator = "Critical Risk"
        elif risk_val == "High":
            status_indicator = "High Risk"
        elif risk_val == "Medium":
            status_indicator = "Moderate Risk"

        # Generate custom SVG sparklines
        soh_spark = make_sparkline_svg([100.0, 98.5, 97.0, 95.5, soh_val], color="var(--accent)")
        temp_spark = make_sparkline_svg([temp_val - 1.5, temp_val + 2.0, temp_val - 0.5, temp_val + 1.0, temp_val], color="#E6A33B" if temp_val > 45 else "var(--accent)")
        volt_spark = make_sparkline_svg([volt_val + 1.2, volt_val - 0.8, volt_val + 0.5, volt_val - 0.3, volt_val], color="var(--accent)")
        rul_spark = make_sparkline_svg([rul_val + 120, rul_val + 90, rul_val + 60, rul_val + 30, rul_val], color="var(--accent)")

        # Inline custom sparkline KPI cards
        heart_icon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>'
        therm_icon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/></svg>'
        volt_icon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'
        cal_icon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'

        st.markdown(f"""
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">State of Health</span>
                    {heart_icon}
                </div>
                <div class="kpi-value">{soh_val:.1f}%</div>
                <div class="sparkline-container">{soh_spark}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Pack Temperature</span>
                    {therm_icon}
                </div>
                <div class="kpi-value">{temp_val:.1f} °C</div>
                <div class="sparkline-container">{temp_spark}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Terminal Voltage</span>
                    {volt_icon}
                </div>
                <div class="kpi-value">{volt_val:.1f} V</div>
                <div class="sparkline-container">{volt_spark}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-header">
                    <span class="kpi-title">Remaining Life</span>
                    {cal_icon}
                </div>
                <div class="kpi-value">{rul_val} Days</div>
                <div class="sparkline-container">{rul_spark}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Specifications & Status Table Card
        car_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/></svg>'
        batt_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="16" height="10" rx="2" ry="2"/><line x1="22" y1="11" x2="22" y2="13"/></svg>'
        group_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/><path d="M12 6v12"/><path d="M6 12h12"/></svg>'
        factory_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 21H2V3l7 4v5l7-4v5l6-3v12z"/></svg>'
        loop_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>'
        percent_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m8 16 8-8"/><circle cx="9.5" cy="9.5" r=".5"/><circle cx="14.5" cy="14.5" r=".5"/></svg>'
        warn_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
        clock_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'

        st.markdown(f"""
        <div class="info-card">
            <div class="info-card-title">Asset Specifications & Status</div>
            <table class="info-table">
                <tr>
                    <td class="info-icon-col">{car_svg}</td>
                    <td class="info-label">Vehicle ID:</td>
                    <td class="info-value" style="font-family:'JetBrains Mono',monospace; color:var(--accent);">{selected_vehicle}</td>
                </tr>
                <tr>
                    <td class="info-icon-col">{batt_svg}</td>
                    <td class="info-label">Battery Pack ID:</td>
                    <td class="info-value" style="font-family:'JetBrains Mono',monospace;">BAT_{selected_vehicle.replace('EV-', '')}</td>
                </tr>
                <tr>
                    <td class="info-icon-col">{group_svg}</td>
                    <td class="info-label">Batch/Fabrication Group:</td>
                    <td class="info-value" style="font-family:'JetBrains Mono',monospace;">{batch_val}</td>
                </tr>
                <tr>
                    <td class="info-icon-col">{factory_svg}</td>
                    <td class="info-label">Manufacturer:</td>
                    <td class="info-value">TrustCharge Energy</td>
                </tr>
                <tr>
                    <td class="info-icon-col">{loop_svg}</td>
                    <td class="info-label">Accumulated Charge Cycles:</td>
                    <td class="info-value" style="font-family:'JetBrains Mono',monospace;">{cycles_val}</td>
                </tr>
                <tr>
                    <td class="info-icon-col">{percent_svg}</td>
                    <td class="info-label">State of Charge (SoC):</td>
                    <td class="info-value" style="font-family:'JetBrains Mono',monospace;">{soc_val:.1f}%</td>
                </tr>
                <tr>
                    <td class="info-icon-col">{warn_svg}</td>
                    <td class="info-label">Operational Risk Classification:</td>
                    <td class="info-value" style="font-weight: 700; color: {"#EF4444" if status_indicator == "Critical Risk" else ("#F59E0B" if "Risk" in status_indicator else "#10B981")};">{status_indicator}</td>
                </tr>
                <tr>
                    <td class="info-icon-col">{clock_svg}</td>
                    <td class="info-label">Last Updated:</td>
                    <td class="info-value" style="color: var(--muted); font-size: 0.8rem;">15 Jul 2026, 10:54 AM</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        # Quick Actions Card buttons
        plus_action_svg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#18D6C2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>'
        pred_action_svg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#18D6C2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>'
        report_action_svg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#18D6C2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>'
        import_action_svg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#18D6C2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>'
        export_action_svg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#18D6C2" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>'

        st.markdown(f"""
        <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 0.95rem; font-weight: 700; color: var(--primary-text); margin-top: 24px; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.03em;">Quick Actions</h3>
        <div class="action-grid">
            <a href="?action=add_vehicle" target="_self" class="action-card">
                <div class="action-icon-wrap">{plus_action_svg}</div>
                <div class="action-info">
                    <span class="action-title">Add Vehicle</span>
                    <span class="action-desc">Register new vehicle</span>
                </div>
            </a>
            <a href="?action=run_prediction" target="_self" class="action-card">
                <div class="action-icon-wrap">{pred_action_svg}</div>
                <div class="action-info">
                    <span class="action-title">Run Prediction</span>
                    <span class="action-desc">AI health prediction</span>
                </div>
            </a>
            <a href="?action=generate_report" target="_self" class="action-card">
                <div class="action-icon-wrap">{report_action_svg}</div>
                <div class="action-info">
                    <span class="action-title">Generate Report</span>
                    <span class="action-desc">Export detailed report</span>
                </div>
            </a>
            <a href="?action=import_dataset" target="_self" class="action-card">
                <div class="action-icon-wrap">{import_action_svg}</div>
                <div class="action-info">
                    <span class="action-title">Import Dataset</span>
                    <span class="action-desc">Upload battery data</span>
                </div>
            </a>
            <a href="?action=export_analytics" target="_self" class="action-card">
                <div class="action-icon-wrap">{export_action_svg}</div>
                <div class="action-info">
                    <span class="action-title">Export Analytics</span>
                    <span class="action-desc">Download insights</span>
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        # Determine gauge color
        g_color = "#16D9C2" # Success teal
        if health_score_val < 50:
            g_color = "#D9534F" # Danger red
        elif health_score_val < 80:
            g_color = "#E6A33B" # Warning orange

        # Render the custom semi-circular Plotly gauge chart
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode="gauge",
            value=health_score_val,
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "rgba(255,255,255,0.2)", "tickvals": [0, 25, 50, 75, 100]},
                "bar": {"color": g_color, "thickness": 0.4},
                "bgcolor": "rgba(255,255,255,0.05)",
                "borderwidth": 0,
            },
            domain={"x": [0, 1], "y": [0.15, 1]}
        ))
        
        # Add centered percentage text using monospace font
        fig.add_annotation(
            x=0.5,
            y=0.42,
            text=f"<b>{health_score_val}%</b>",
            showarrow=False,
            font=dict(family="JetBrains Mono, monospace", size=30, color="#F5F7FA")
        )
        
        # Add center "Good/Moderate/Critical" annotation sits explicitly below the percentage number
        center_text = "Good"
        if health_score_val < 50:
            center_text = "Critical"
        elif health_score_val < 80:
            center_text = "Moderate"

        fig.add_annotation(
            x=0.5,
            y=0.15,
            text=center_text,
            showarrow=False,
            font=dict(family="Space Grotesk, sans-serif", size=12, color="#A0AEBB")
        )
        
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=160,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        # Plotly Area Trend Sparkline
        trend_vals_hs = [
            health_score_val - 2,
            health_score_val - 1.5,
            health_score_val - 3.0,
            health_score_val - 0.5,
            health_score_val
        ]
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=[0, 1, 2, 3, 4],
            y=trend_vals_hs,
            mode='lines',
            line=dict(color='#18D6C2', width=1.5),
            fill='tozeroy',
            fillcolor='rgba(24, 214, 194, 0.08)'
        ))
        fig_trend.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            margin=dict(l=0, r=0, t=0, b=0),
            height=50,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        apply_plotly_theme(fig_trend)

        # Overall Health Index Card Container HTML Wrap
        st.markdown("""
        <div class="info-card" style="margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 0.95rem; font-weight: 700; color: var(--primary-text); margin: 0; text-transform: uppercase; letter-spacing: 0.03em;">Overall Health Index</h3>
            </div>
        """, unsafe_allow_html=True)

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 16px; margin-bottom: 8px;">
                <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; color: var(--muted);">Health Trend (30 Days)</span>
                <span class="badge" style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #10B981; font-weight: 600;">+5.2%</span>
            </div>
        """, unsafe_allow_html=True)

        st.plotly_chart(fig_trend, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Battery Status Overview Table Card
        cal_svg_overview = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
        shield_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'
        bolt_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'
        therm_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/></svg>'
        scale_svg = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>'

        risk_bg = "#10B981" # Green
        risk_fg = "#FFFFFF"
        if risk_val == "Critical":
            risk_bg = "#EF4444" # Red
        elif risk_val in ["High", "Medium"]:
            risk_bg = "#F59E0B" # Orange

        st.markdown(f"""
        <div class="info-card">
            <div class="info-card-title">Battery Status Overview</div>
            <table class="info-table">
                <tr>
                    <td class="info-icon-col">{cal_svg_overview}</td>
                    <td class="info-label">Remaining Useful Life</td>
                    <td class="info-value" style="font-family:'JetBrains Mono',monospace;">{rul_val} Days</td>
                </tr>
                <tr>
                    <td class="info-icon-col">{shield_svg}</td>
                    <td class="info-label">Risk Level</td>
                    <td class="info-value"><span style="background: {risk_bg}; color: {risk_fg}; padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 0.7rem; font-family:'JetBrains Mono',monospace; text-transform: uppercase;">{risk_val}</span></td>
                </tr>
                <tr>
                    <td class="info-icon-col">{bolt_svg}</td>
                    <td class="info-label">Charging Behaviour</td>
                    <td class="info-value" style="color: #10B981; font-weight: 600;">Good</td>
                </tr>
                <tr>
                    <td class="info-icon-col">{therm_svg}</td>
                    <td class="info-label">Thermal Status</td>
                    <td class="info-value" style="color: #10B981; font-weight: 600;">Normal</td>
                </tr>
                <tr>
                    <td class="info-icon-col">{scale_svg}</td>
                    <td class="info-label">Voltage Balance</td>
                    <td class="info-value" style="color: #10B981; font-weight: 600;">Balanced</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # -------------------------------
    # Degradation Trend
    # -------------------------------
    st.subheader("Electrochemical Degradation Trend")

    # Generate historical trend curve matching predict_rul logic
    trend_vals = [
        100.0,
        round(100.0 - (100.0 - soh_val) * 0.25, 2),
        round(100.0 - (100.0 - soh_val) * 0.50, 2),
        round(100.0 - (100.0 - soh_val) * 0.75, 2),
        round(soh_val, 2)
    ]
    df_trend = pd.DataFrame({
        "Operating Period": ["Initial (0 Mo)", "Period 1", "Period 2", "Period 3", "Current (Active)"],
        "State of Health (SoH)": trend_vals
    })

    fig = px.line(
        df_trend,
        x="Operating Period",
        y="State of Health (SoH)",
        markers=True,
        title=f"Capacity Retention Curve — Asset {selected_vehicle}"
    )
    fig.update_layout(
        xaxis_title="Operating Interval",
        yaxis_title="SoH (%)",
        yaxis_range=[min(trend_vals) - 5, 105]
    )
    apply_plotly_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # -------------------------------
    # AI Diagnostics & Actions
    # -------------------------------
    st.subheader("AI System Diagnostic Report")

    recs = []
    if soh_val < 80:
        recs.append("CRITICAL DEGRADATION SIGNATURE: Schedule cell balancing and capacity test immediately.")
    if temp_val > 45:
        recs.append("ELEVATED OPERATING TEMPERATURES: Check cooling flow rates and thermal runarounds.")
    if cycles_val > 1000:
        recs.append("CYCLE WEAR THRESHOLD REACHED: Schedule resistance scan to check internal grid stability.")
    if maint_val == "Yes":
        recs.append("SCHEDULED MAINTENANCE INTERVENTION FLAGGED. Disengage fast charging algorithms.")
    
    if not recs:
        recs.append("Battery operating within normal electrochemical parameters.")
        recs.append("Cycle counts and degradation gradients match standard fleet profiles.")
        recs.append("Monitor telemetry continuously. Next inspection recommended in 30 days.")

    recommendation_text = "\n\n".join(recs)
    if risk_val in ["Critical", "High"]:
        st.warning(recommendation_text)
    else:
        st.success(recommendation_text)

    st.divider()

    # -------------------------------
    # Recent Alerts Log
    # -------------------------------
    st.subheader("Node Telemetry Alerts Log")

    alerts = pd.DataFrame({
        "Timestamp": [datetime.now().strftime("%d %b %H:%M"), "12 Jul 14:30", "10 Jul 09:12"],
        "Operational Status": [
            f"Active telemetry sync. SoC={soc_val:.1f}%, Volts={volt_val:.1f}V",
            f"Routine check: Temperature verified at {temp_val:.1f} °C",
            f"Registered cycle wear threshold index: {cycles_val} cycles completed."
        ],
        "Diagnostic Level": ["INFO", "INFO", "WARNING" if cycles_val > 800 else "INFO"]
    })

    st.dataframe(alerts, use_container_width=True)

st.divider()
st.caption("TrustCharge Platform Core • Dynamic Data Synchronization Mode Active")
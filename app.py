
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd
import numpy as np

# Load Live Data
try:
    df_bms = pd.read_csv("data/synthetic_bms.csv")
except Exception:
    df_bms = pd.DataFrame()

try:
    df_supply = pd.read_csv("data/supply_chain.csv")
except Exception:
    df_supply = pd.DataFrame()

# Calculate Live Stats
if not df_bms.empty:
    total_vehicles = len(df_bms)
    avg_health = int(round(df_bms["state_of_health"].mean()))
    critical_count = len(df_bms[df_bms["failure_risk"] == "Critical"])
    warning_count = len(df_bms[df_bms["failure_risk"] == "High"])
    healthy_count = len(df_bms[df_bms["failure_risk"] == "Low"])
    medium_count = len(df_bms[df_bms["failure_risk"] == "Medium"])
    
    cnt_healthy = healthy_count + medium_count
    cnt_warning = warning_count
    cnt_critical = critical_count
    cnt_offline = len(df_bms[df_bms["maintenance_due"] == "Yes"])
    
    avg_rul = int(round(df_bms["rul_days"].mean()))
    anomalies_count = len(df_bms[df_bms["failure_risk"].isin(["High", "Critical"])])
    unique_mfg = df_bms["batch_id"].nunique()
    
    # Selected sample vehicle for dashboard details
    critical_veh = df_bms[df_bms["failure_risk"] == "Critical"]
    if not critical_veh.empty:
        sample_veh = critical_veh.iloc[0]
    else:
        sample_veh = df_bms.iloc[0]
else:
    total_vehicles = 850
    avg_health = 92
    cnt_healthy = 580
    cnt_warning = 153
    cnt_critical = 68
    cnt_offline = 49
    avg_rul = 530
    anomalies_count = 3
    unique_mfg = 4
    sample_veh = {
        "vehicle_id": "EV-5F24189F",
        "state_of_health": 92.0,
        "rul_days": 530,
        "failure_risk": "Low",
        "maintenance_due": "No",
        "charge_cycles": 185
    }

# PAGE CONFIGURATION
# -------------------------------------------------
st.set_page_config(
    page_title="TrustCharge | EV Battery Intelligence Platform",
    page_icon="https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/bolt/default/24px.svg",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import unified design system
from utils.ui_components import inject_master_ui

# Toast messages alert handler
if "action" in st.query_params:
    action = st.query_params["action"]
    if action == "logout":
        st.toast("Session closed successfully", icon="🔒")
    st.query_params.clear()

# Query parameter Page Router
active_page = st.query_params.get("page", "dashboard")

if active_page == "profile":
    inject_master_ui("Settings")
    st.markdown('<div style="max-width: 600px; margin: 40px auto; padding: 0 16px;">', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--accent); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;">User Profile & Settings</div>
        <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: var(--primary-text); margin: 0; text-transform: uppercase; letter-spacing: -0.02em;">Edit Settings</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.setdefault("profile_name", "Shruti K")
    st.session_state.setdefault("profile_role", "Administrator")
    st.session_state.setdefault("profile_email", "shruti.k@trustcharge.com")
    st.session_state.setdefault("profile_notif", True)
    
    with st.container():
        st.markdown('<div class="card" style="padding: 24px; border-radius: var(--radius-lg); background-color: var(--card); border: 1px solid var(--border); box-shadow: 0 4px 12px var(--shadow);">', unsafe_allow_html=True)
        name_val = st.text_input("Full Name", value=st.session_state["profile_name"])
        role_val = st.text_input("Role / Title", value=st.session_state["profile_role"])
        email_val = st.text_input("Email Address", value=st.session_state["profile_email"])
        notif_val = st.checkbox("Enable Real-time Fleet Alerts", value=st.session_state["profile_notif"])
        
        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Save Changes", use_container_width=True, type="primary"):
                st.session_state["profile_name"] = name_val
                st.session_state["profile_role"] = role_val
                st.session_state["profile_email"] = email_val
                st.session_state["profile_notif"] = notif_val
                st.query_params.clear()
                st.rerun()
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.query_params.clear()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

elif active_page == "vehicles":
    inject_master_ui("Vehicles")
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--accent); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;">Fleet Management</div>
        <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: var(--primary-text); margin: 0; text-transform: uppercase; letter-spacing: -0.02em;">EV Fleet Vehicles Registry</h1>
        <p style="color: var(--text); font-size: 0.9rem; margin-top: 4px;">Search and view telemetry status metrics for all active battery packs and electric vehicle assets.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not df_bms.empty:
        search_q = st.text_input("🔍 Quick Search Vehicle ID, Batch, Risk...", placeholder="Type vehicle ID (e.g. EV-00)...")
        filtered_df = df_bms.copy()
        if search_q:
            filtered_df = filtered_df[
                filtered_df["vehicle_id"].str.contains(search_q, case=False) |
                filtered_df["batch_id"].str.contains(search_q, case=False) |
                filtered_df["failure_risk"].str.contains(search_q, case=False)
            ]
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.dataframe(filtered_df[["vehicle_id", "batch_id", "state_of_health", "charge_cycles", "temperature", "failure_risk", "maintenance_due"]], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No vehicles database loaded.")
    st.stop()

elif active_page == "predictions":
    inject_master_ui("AI Predictions")
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--accent); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;">AI Predictive Analytics</div>
        <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: var(--primary-text); margin: 0; text-transform: uppercase; letter-spacing: -0.02em;">Battery Degradation & Failure Forecasts</h1>
        <p style="color: var(--text); font-size: 0.9rem; margin-top: 4px;">Machine learning forecasts estimating remaining useful life, failure probability, and cell anomalies.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not df_bms.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Avg Predicted RUL", f"{int(round(df_bms['rul_days'].mean()))} Days")
        c2.metric("Critical Risk Level Pack Assets", f"{len(df_bms[df_bms['failure_risk'] == 'Critical'])}")
        c3.metric("Anomalies Detected Today", f"{len(df_bms[df_bms['failure_risk'].isin(['High', 'Critical'])])}")
        
        st.markdown('<div style="height:20px;"></div>', unsafe_allow_html=True)
        col_hist, col_high = st.columns([3, 2], gap="large")
        with col_hist:
            st.subheader("RUL Forecast Distribution Curve")
            import numpy as np
            import plotly.graph_objects as go
            from utils.ui_components import apply_plotly_theme

            counts, bin_edges = np.histogram(df_bms["rul_days"].dropna(), bins=20)
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

            fig_rul = go.Figure()
            fig_rul.add_trace(go.Scatter(
                x=bin_centers,
                y=counts,
                mode='lines+markers',
                name='Asset Count',
                line=dict(color='#18E7D3', width=3, shape='spline'),
                marker=dict(
                    size=9,
                    color='#FF5722',
                    line=dict(width=2, color='#FFFFFF'),
                    symbol='circle'
                ),
                fill='tozeroy',
                fillcolor='rgba(24, 231, 211, 0.08)'
            ))
            fig_rul.update_layout(
                xaxis_title="Remaining Useful Life (Days)",
                yaxis_title="Count (Number of Assets)",
                margin=dict(l=20, r=20, t=30, b=30),
            )
            apply_plotly_theme(fig_rul)
            st.plotly_chart(fig_rul, use_container_width=True)
            
        with col_high:
            st.subheader("Critical Warning Log")
            crit_assets = df_bms[df_bms["failure_risk"].isin(["High", "Critical"])][["vehicle_id", "state_of_health", "failure_risk"]]
            st.dataframe(crit_assets, use_container_width=True)
    else:
        st.info("No prediction telemetry active.")
    st.stop()

elif active_page == "analytics":
    inject_master_ui("Analytics")
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--accent); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;">Deep Data Insights</div>
        <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: var(--primary-text); margin: 0; text-transform: uppercase; letter-spacing: -0.02em;">Fleet Telemetry & Trend Analytics</h1>
        <p style="color: var(--text); font-size: 0.9rem; margin-top: 4px;">Advanced charts analyzing internal resistance, cycles completed, temperature excursions, and health spreads.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not df_bms.empty:
        import plotly.express as px
        from utils.ui_components import apply_plotly_theme
        
        col_a1, col_a2 = st.columns(2, gap="large")
        with col_a1:
            st.subheader("State of Health vs Charge Cycles Spread")
            fig_scat = px.scatter(df_bms, x="charge_cycles", y="state_of_health", color="failure_risk", color_discrete_sequence=["#18E7D3", "#3B82F6", "#F59E0B", "#EF4444"])
            apply_plotly_theme(fig_scat)
            st.plotly_chart(fig_scat, use_container_width=True)
            
        with col_a2:
            st.subheader("Internal Resistance vs Temperature Stress")
            fig_scat2 = px.scatter(df_bms, x="temperature", y="internal_resistance", color="failure_risk", color_discrete_sequence=["#18E7D3", "#3B82F6", "#F59E0B", "#EF4444"])
            apply_plotly_theme(fig_scat2)
            st.plotly_chart(fig_scat2, use_container_width=True)
    else:
        st.info("No analytics metrics available.")
    st.stop()

elif active_page == "reports":
    inject_master_ui("Reports")
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--accent); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;">Diagnostic Exports</div>
        <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: var(--primary-text); margin: 0; text-transform: uppercase; letter-spacing: -0.02em;">System Diagnostic Reports</h1>
        <p style="color: var(--text); font-size: 0.9rem; margin-top: 4px;">Download certified reports, verification files, and battery diagnostic logs.</p>
    </div>
    """, unsafe_allow_html=True)
    
    reports_data = [
        {"Report Name": "Q2 Fleet Battery Intelligence Report", "Date": "12 Jul 2026", "Format": "PDF", "Size": "4.2 MB", "Status": "Certified"},
        {"Report Name": "Battery Health Degradation Audit - Batch A", "Date": "08 Jul 2026", "Format": "PDF", "Size": "2.8 MB", "Status": "Certified"},
        {"Report Name": "AI Predictive Accuracy Review (v1.3)", "Date": "29 Jun 2026", "Format": "CSV", "Size": "12.4 MB", "Status": "Completed"},
        {"Report Name": "Critical Anomaly Intervention Records", "Date": "15 Jun 2026", "Format": "PDF", "Size": "1.5 MB", "Status": "Actioned"}
    ]
    st.dataframe(pd.DataFrame(reports_data), use_container_width=True)
    st.stop()

elif active_page == "alerts":
    inject_master_ui("Alerts")
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--accent); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;">Real-time Notification Log</div>
        <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 2rem; font-weight: 700; color: var(--primary-text); margin: 0; text-transform: uppercase; letter-spacing: -0.02em;">Active Security & Safety Alerts</h1>
        <p style="color: var(--text); font-size: 0.9rem; margin-top: 4px;">Active safety warnings, anomalous temperature excursions, and critical voltage imbalances detected in the fleet.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not df_bms.empty:
        crit_alerts = df_bms[df_bms["failure_risk"].isin(["High", "Critical"])][["vehicle_id", "failure_risk", "temperature", "voltage", "maintenance_due"]]
        st.dataframe(crit_alerts, use_container_width=True)
    else:
        st.info("No active notifications.")
    st.stop()

# Default Landing Dashboard page styling
inject_master_ui("Dashboard")

# =================================================================
# HERO SECTION — Modern SaaS Title Banner
# =================================================================
col_hero_left, col_hero_right = st.columns([7, 5], gap="large")

with col_hero_left:
    st.markdown("""
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 8px;">
            TRUSTCHARGE PLATFORM &nbsp;|&nbsp; VERSION 1.3
        </div>
        <h1 style="font-family: 'Space Grotesk', sans-serif; font-size: 3.2rem; font-weight: 700; line-height: 1.15; letter-spacing: -0.03em; color: var(--primary-text); margin-bottom: 16px;">
            AI Battery <span style="color: var(--accent);">Intelligence</span> Platform
        </h1>
        <p style="font-family: 'Inter', sans-serif; font-size: 1.05rem; line-height: 1.6; color: var(--text); margin-bottom: 24px; max-width: 640px;">
            Predict battery failures, estimate remaining useful life, improve financing trust, and enable battery traceability using AI-driven diagnostics.
        </p>
    """, unsafe_allow_html=True)

    # Action Buttons
    st.markdown("""
        <div style="display: flex; gap: 14px; margin-bottom: 32px;">
            <a href="/fleet_dashboard" target="_self" style="background-color: var(--accent) !important; color: #0B0F14 !important; font-family: 'Space Grotesk', sans-serif; font-weight: 700; text-decoration: none; padding: 12px 28px; border-radius: var(--radius-md); transition: var(--transition); font-size: 0.85rem; display: inline-block;">Open Fleet Dashboard</a>
            <a href="/battery_scorecard" target="_self" style="border: 1px solid var(--border) !important; color: #FFFFFF !important; background: transparent !important; font-family: 'Space Grotesk', sans-serif; font-weight: 700; text-decoration: none; padding: 12px 28px; border-radius: var(--radius-md); transition: var(--transition); font-size: 0.85rem; display: inline-block;">View Scorecard</a>
        </div>
    """, unsafe_allow_html=True)

    # Redesigned 4-Column KPI Sparkline Cards
    soh_spark_home = '<svg width="100%" height="20" viewBox="0 0 120 20" preserveAspectRatio="none"><path d="M 0,16 L 30,12 L 60,14 L 90,6 L 120,4" fill="none" stroke="var(--accent)" stroke-width="1.5"/></svg>'
    temp_spark_home = '<svg width="100%" height="20" viewBox="0 0 120 20" preserveAspectRatio="none"><path d="M 0,12 L 30,16 L 60,10 L 90,12 L 120,6" fill="none" stroke="var(--accent)" stroke-width="1.5"/></svg>'
    volt_spark_home = '<svg width="100%" height="20" viewBox="0 0 120 20" preserveAspectRatio="none"><path d="M 0,14 L 30,12 L 60,15 L 90,8 L 120,10" fill="none" stroke="var(--accent)" stroke-width="1.5"/></svg>'
    rul_spark_home = '<svg width="100%" height="20" viewBox="0 0 120 20" preserveAspectRatio="none"><path d="M 0,18 L 30,10 L 60,14 L 90,8 L 120,6" fill="none" stroke="var(--accent)" stroke-width="1.5"/></svg>'

    st.markdown(f"""
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; width: 100%;">
        <div class="card" style="padding: 16px !important;">
            <div style="font-family:'Space Grotesk',sans-serif; font-size: 0.68rem; color: var(--text); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; margin-bottom: 6px;">State of Health</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size: 1.5rem; font-weight: 700; color: var(--primary-text);">{avg_health}%</div>
            <div style="margin-top: 10px; height: 20px;">{soh_spark_home}</div>
        </div>
        <div class="card" style="padding: 16px !important;">
            <div style="font-family:'Space Grotesk',sans-serif; font-size: 0.68rem; color: var(--text); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; margin-bottom: 6px;">Avg Temperature</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size: 1.5rem; font-weight: 700; color: var(--primary-text);">32.4 °C</div>
            <div style="margin-top: 10px; height: 20px;">{temp_spark_home}</div>
        </div>
        <div class="card" style="padding: 16px !important;">
            <div style="font-family:'Space Grotesk',sans-serif; font-size: 0.68rem; color: var(--text); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; margin-bottom: 6px;">Terminal Voltage</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size: 1.5rem; font-weight: 700; color: var(--primary-text);">362.8 V</div>
            <div style="margin-top: 10px; height: 20px;">{volt_spark_home}</div>
        </div>
        <div class="card" style="padding: 16px !important;">
            <div style="font-family:'Space Grotesk',sans-serif; font-size: 0.68rem; color: var(--text); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; margin-bottom: 6px;">Estimated RUL</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size: 1.5rem; font-weight: 700; color: var(--primary-text);">{avg_rul} Days</div>
            <div style="margin-top: 10px; height: 20px;">{rul_spark_home}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_hero_right:
    # Dynamic values for the gauge
    sample_health = int(round(sample_veh["state_of_health"])) if "state_of_health" in sample_veh else 92
    sample_rul = int(sample_veh["rul_days"]) if "rul_days" in sample_veh else 530
    sample_risk = str(sample_veh["failure_risk"]).upper() if "failure_risk" in sample_veh else "LOW"
    sample_charge = "Excellent" if sample_veh.get("charge_cycles", 0) < 500 else "Good"

    # Setup Plotly Circular health score
    import plotly.graph_objects as go
    fig_g = go.Figure()
    fig_g.add_trace(go.Indicator(
        mode="gauge",
        value=sample_health,
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "rgba(255,255,255,0.2)"},
            "bar": {"color": "#18E7D3", "thickness": 0.4},
            "bgcolor": "rgba(255,255,255,0.04)",
            "borderwidth": 0,
        },
        domain={"x": [0, 1], "y": [0.15, 1]}
    ))
    
    # Add centered percentage text using monospace font
    fig_g.add_annotation(
        x=0.5, y=0.42,
        text=f"<b>{sample_health}%</b>",
        showarrow=False,
        font=dict(family="JetBrains Mono, monospace", size=30, color="#FFFFFF")
    )
    
    # Add center text classification sits explicitly below the percentage number
    fig_g.add_annotation(
        x=0.5, y=0.15,
        text="Good" if sample_health >= 80 else ("Moderate" if sample_health >= 50 else "Critical"),
        showarrow=False,
        font=dict(family="Space Grotesk, sans-serif", size=12, color="#9CA3AF")
    )
    fig_g.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        height=160,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    # Plotly 30-Day Health Trend Area plot
    fig_tr = go.Figure()
    fig_tr.add_trace(go.Scatter(
        x=[0, 1, 2, 3, 4],
        y=[sample_health - 2.5, sample_health - 1.8, sample_health - 3.2, sample_health - 0.8, sample_health],
        mode='lines',
        line=dict(color='#18E7D3', width=1.5),
        fill='tozeroy',
        fillcolor='rgba(24, 231, 211, 0.08)'
    ))
    fig_tr.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        margin=dict(l=0, r=0, t=0, b=0),
        height=50,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    # Wrap inside Premium Widget card container
    st.markdown("""
    <div class="card" style="padding: 20px !important;">
        <h3 style="font-family: 'Space Grotesk', sans-serif; font-size: 0.95rem; font-weight: 700; color: var(--primary-text); margin-top: 0; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.03em;">Overall Health Index</h3>
    """, unsafe_allow_html=True)

    st.plotly_chart(fig_g, use_container_width=True)

    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 16px; margin-bottom: 8px;">
            <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; color: var(--text);">Health Trend (30 Days)</span>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #10B981; font-weight: 600;">+5.2%</span>
        </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(fig_tr, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# =================================================================
# SECTION 2 — PLATFORM CORE MODULES (preserved, CSS-var-ified)
# =================================================================
st.markdown("""
    <div class="section-label">System Modules</div>
    <div class="section-title">Platform Core Modules</div>
""", unsafe_allow_html=True)

col_mod1, col_mod2, col_mod3 = st.columns(3)

ICON_FLEET = """<svg width="28" height="28" viewBox="0 0 24 24" fill="none"
    stroke="#00D9B5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="3" y="11" width="18" height="11" rx="0"/>
    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
    <circle cx="12" cy="17" r="1"/>
</svg>"""

ICON_BATTERY = """<svg width="28" height="28" viewBox="0 0 24 24" fill="none"
    stroke="#00D9B5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="2" y="7" width="16" height="10" rx="0"/>
    <path d="M22 11v2"/><path d="M6 11h4"/><path d="M6 15h8"/>
</svg>"""

ICON_MFG = """<svg width="28" height="28" viewBox="0 0 24 24" fill="none"
    stroke="#00D9B5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M2 20h20"/><path d="M2 20V10l6-4v4l6-4v4l6-4v14"/>
    <path d="M9 20v-5h6v5"/>
</svg>"""

st.markdown("""
<style>
.mod-card { background-color: #0B1220 !important; border: 1px solid rgba(255, 255, 255, 0.08) !important; padding: 24px 20px !important; border-radius: 12px; }
.mod-corner { color: var(--muted); }
.mod-id { color: var(--muted); }
.mod-title-text { color: #FFFFFF !important; font-size: 1.35rem !important; font-weight: 800 !important; font-family: 'Space Grotesk', sans-serif !important; line-height: 1.3 !important; }
.mod-desc-text { color: var(--muted); }
.mod-btn { border-color: var(--border); color: var(--muted); background:transparent; box-shadow:2px 2px 0 var(--shadow); }
.mod-btn:hover { background:var(--accent); border-color:var(--accent); color:var(--bg); box-shadow:0 0 12px var(--glow); }
</style>
""", unsafe_allow_html=True)

SPARK_FLEET = """<svg width="100%" height="28" viewBox="0 0 200 28" preserveAspectRatio="none">
    <polyline points="0,24 25,18 50,22 75,10 100,16 125,8 150,14 175,6 200,4"
        fill="none" stroke="rgba(0,217,181,0.35)" stroke-width="1.5"/>
    <circle cx="200" cy="4" r="2.5" fill="#00D9B5"/>
</svg>"""

SPARK_SCORE = """<svg width="100%" height="28" viewBox="0 0 200 28" preserveAspectRatio="none">
    <polyline points="0,18 25,22 50,10 75,16 100,6 125,18 150,10 175,14 200,6"
        fill="none" stroke="rgba(0,217,181,0.35)" stroke-width="1.5"/>
    <circle cx="200" cy="6" r="2.5" fill="#00D9B5"/>
</svg>"""

SPARK_MFG = """<svg width="100%" height="28" viewBox="0 0 200 28" preserveAspectRatio="none">
    <polyline points="0,22 25,14 50,20 75,8 100,16 125,12 150,20 175,8 200,12"
        fill="none" stroke="rgba(0,217,181,0.35)" stroke-width="1.5"/>
    <circle cx="200" cy="12" r="2.5" fill="#00D9B5"/>
</svg>"""

with col_mod1:
    st.markdown(f"""
        <div class="mod-card">
            <div>
                <div class="mod-title-row">
                    <span class="status-dot"></span>
                    <span class="mod-title-text">Fleet Dashboard</span>
                </div>
                <div style="margin-bottom:10px;">{ICON_FLEET}</div>
                <p class="mod-desc-text">Monitor EV fleet telemetry, battery status distribution, and active risk anomalies.</p>
            </div>
            <div>{SPARK_FLEET}</div>
            <a href="/fleet_dashboard" target="_self" class="mod-btn">Open Fleet Portal</a>
        </div>
    """, unsafe_allow_html=True)

with col_mod2:
    st.markdown(f"""
        <div class="mod-card alt-bg">
            <div>
                <div class="mod-title-row">
                    <span class="status-dot"></span>
                    <span class="mod-title-text">Battery Scorecard</span>
                </div>
                <div style="margin-bottom:10px;">{ICON_BATTERY}</div>
                <p class="mod-desc-text">Inspect individual asset diagnostics, SoH scores, thermal stats, and maintenance logs.</p>
            </div>
            <div>{SPARK_SCORE}</div>
            <a href="/battery_scorecard" target="_self" class="mod-btn">View Scorecard</a>
        </div>
    """, unsafe_allow_html=True)

with col_mod3:
    st.markdown(f"""
        <div class="mod-card">
            <div>
                <div class="mod-title-row">
                    <span class="status-dot"></span>
                    <span class="mod-title-text">Manufacturer Traceability</span>
                </div>
                <div style="margin-bottom:10px;">{ICON_MFG}</div>
                <p class="mod-desc-text">Trace chemistry configurations, verify batch quality profiles, and manage warranty data.</p>
            </div>
            <div>{SPARK_MFG}</div>
            <a href="/manufacturer_dashboard" target="_self" class="mod-btn">Access Hub</a>
        </div>
    """, unsafe_allow_html=True)

# =================================================================
# QUICK ACTIONS
# =================================================================
plus_svg = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#18E7D3" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>'
brain_svg = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#18E7D3" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'
report_svg = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#18E7D3" stroke-width="2"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>'
import_svg = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#18E7D3" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>'
export_svg = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#18E7D3" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>'

st.markdown("""
<style>
div[data-testid="stMarkdownContainer"] {
    overflow: visible !important;
}
.qa-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 16px;
    margin-top: 16px;
    margin-bottom: 28px;
    width: 100%;
    overflow: visible !important;
}
.qa-card-link {
    text-decoration: none !important;
    display: block;
    width: 100%;
    outline: none !important;
}
.qa-card {
    background-color: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg);
    padding: 20px 12px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    position: relative;
    z-index: 1;
    box-sizing: border-box;
    transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1), background-color 0.2s ease, border-color 0.2s ease, box-shadow 0.22s ease !important;
}
.qa-card-link:hover .qa-card,
.qa-card:hover {
    transform: translateY(-10px) scale(1.08) !important;
    border-color: #18E7D3 !important;
    background-color: #1A2942 !important;
    box-shadow: 0 16px 36px rgba(24, 231, 211, 0.4), 0 0 20px rgba(24, 231, 211, 0.25) !important;
    z-index: 100 !important;
}
.qa-card-link:hover .qa-icon-box,
.qa-card:hover .qa-icon-box {
    background: rgba(24, 231, 211, 0.25) !important;
    transform: scale(1.25) !important;
    box-shadow: 0 0 12px rgba(24, 231, 211, 0.4) !important;
}
.qa-card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--primary-text);
}
.qa-card-desc {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    color: var(--text);
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<h3 style='font-family: Space Grotesk, sans-serif; font-size: 1.15rem; font-weight: 700; margin-top: 36px; margin-bottom: 16px; text-transform: uppercase;'>Quick Actions</h3>

<div class="qa-grid">
    <a class="qa-card-link" href="/battery_scorecard?action=add_vehicle" target="_self">
        <div class="qa-card">
            <div class="qa-icon-box">{plus_svg}</div>
            <div class="qa-card-title">Add Vehicle</div>
            <div class="qa-card-desc">Register new vehicle</div>
        </div>
    </a>
    <a class="qa-card-link" href="/battery_scorecard?action=run_prediction" target="_self">
        <div class="qa-card">
            <div class="qa-icon-box">{brain_svg}</div>
            <div class="qa-card-title">Run Prediction</div>
            <div class="qa-card-desc">AI health forecast</div>
        </div>
    </a>
    <a class="qa-card-link" href="/battery_scorecard?action=generate_report" target="_self">
        <div class="qa-card">
            <div class="qa-icon-box">{report_svg}</div>
            <div class="qa-card-title">Generate AI Report</div>
            <div class="qa-card-desc">Export diagnostics</div>
        </div>
    </a>
    <a class="qa-card-link" href="/battery_scorecard?action=import_dataset" target="_self">
        <div class="qa-card">
            <div class="qa-icon-box">{import_svg}</div>
            <div class="qa-card-title">Import Dataset</div>
            <div class="qa-card-desc">Upload battery data</div>
        </div>
    </a>
    <a class="qa-card-link" href="/battery_scorecard?action=export_analytics" target="_self">
        <div class="qa-card">
            <div class="qa-icon-box">{export_svg}</div>
            <div class="qa-card-title">Export Analytics</div>
            <div class="qa-card-desc">Download CSV insights</div>
        </div>
    </a>
</div>
""", unsafe_allow_html=True)

# =================================================================
# SECTION 3 — ASSET DIAGNOSTICS PIPELINE
# =================================================================
st.markdown("""
    <div class="section-label">Process Flow</div>
    <div class="section-title">Asset Diagnostics Pipeline</div>
""", unsafe_allow_html=True)

PIPELINE_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap');

    :root {
        --bg:       #080B0E;
        --card:     #0F1319;
        --border:   #1E252D;
        --accent:   #00D9B5;
        --text:     #EDEFF1;
        --muted:    #5A6E7F;
        --muted2:   #3A4D5C;
        --shadow:   rgba(0,0,0,.35);
        --radius-lg: 12px;
    }
    [data-theme="light"] {
        --bg:       #EEF3F2;
        --card:     #FCFDFD;
        --border:   #D4E2DF;
        --accent:   #17BFA8;
        --text:     #26343C;
        --muted:    #7D8B90;
        --muted2:   #7D8E91;
        --shadow:   rgba(35, 49, 58, 0.04);
    }
    * { margin:0; padding:0; box-sizing:border-box; }
    html,body { background:var(--bg); color:var(--text); font-family:'Space Grotesk',sans-serif; transition:background .2s,color .2s; }
    .pipeline { display:flex; flex-direction:row; align-items:flex-start; background:var(--card); border:1px solid var(--border);
                box-shadow:0 4px 12px var(--shadow); padding:28px 0; width:100%; border-radius:var(--radius-lg); }
    .step { flex:1; display:flex; flex-direction:column; align-items:center; text-align:center; padding:0 14px; }
    .step-num { font-family:'JetBrains Mono',monospace; font-size:.65rem; font-weight:700; color:var(--muted); letter-spacing:.08em; margin-bottom:10px; display:block; }
    .step-num.active { color:var(--accent); }
    .step-title { font-family:'Space Grotesk',sans-serif; font-size:.82rem; font-weight:700; color:var(--text); margin-bottom:6px; opacity:0.6; }
    .step-title.active { color:var(--accent); opacity:1; }
    .step-desc { font-size:.72rem; color:var(--muted); line-height:1.4; }
    .step-desc.active { color:var(--text); }
    .arrow-col { display:flex; flex-direction:column; align-items:center; padding-top:6px; width:48px; flex-shrink:0; gap:2px; }
    .arrow-dash { font-family:'JetBrains Mono',monospace; font-size:.55rem; color:var(--border); letter-spacing:-.05em; line-height:1; white-space:nowrap; }
    .arrow-head { font-family:'JetBrains Mono',monospace; font-size:.6rem; color:var(--border); line-height:1; }
</style></head><body>
<div class="pipeline">
    <div class="step"><span class="step-num">[ 01 ]</span><div class="step-title">Collect Battery Data</div><div class="step-desc">Raw telemetry ingestion: cell voltage, pack temperature, depth of discharge.</div></div>
    <div class="arrow-col"><span class="arrow-dash">- - -</span><span class="arrow-head">&gt;&gt;&gt;</span><span class="arrow-dash">- - -</span></div>
    <div class="step"><span class="step-num">[ 02 ]</span><div class="step-title">AI Health Analysis</div><div class="step-desc">Electrochemical decay modeling and capacity wear kinetics processing.</div></div>
    <div class="arrow-col"><span class="arrow-dash">- - -</span><span class="arrow-head">&gt;&gt;&gt;</span><span class="arrow-dash">- - -</span></div>
    <div class="step"><span class="step-num active">[ 03 ]</span><div class="step-title active">Predict Remaining Life</div><div class="step-desc active">Remaining useful life (RUL) projections via degradation regression.</div></div>
    <div class="arrow-col"><span class="arrow-dash">- - -</span><span class="arrow-head">&gt;&gt;&gt;</span><span class="arrow-dash">- - -</span></div>
    <div class="step"><span class="step-num">[ 04 ]</span><div class="step-title">Fleet Intelligence</div><div class="step-desc">Aggregate asset metrics and generate operational risk band classifications.</div></div>
    <div class="arrow-col"><span class="arrow-dash">- - -</span><span class="arrow-head">&gt;&gt;&gt;</span><span class="arrow-dash">- - -</span></div>
    <div class="step"><span class="step-num">[ 05 ]</span><div class="step-title">Financing Decision</div><div class="step-desc">Data-backed secondary market valuation and warranty reserve modelling.</div></div>
</div>
<script>
const s=window.parent.localStorage?window.parent.localStorage.getItem('tc_theme'):null;
if(s==='light') document.documentElement.setAttribute('data-theme','light');

// Theme change listener
window.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'theme-change') {
        if (event.data.theme === 'dark') {
            document.documentElement.removeAttribute('data-theme');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
        }
    }
});
</script>
</body></html>
"""
s1_num, s1_title, s1_desc = 'active', 'active', 'active'
s2_num, s2_title, s2_desc = 'active', 'active', 'active'
s3_num, s3_title, s3_desc = '', '', ''
s4_num, s4_title, s4_desc = '', '', ''
s5_num, s5_title, s5_desc = '', '', ''

if sample_veh["maintenance_due"] == "Yes":
    s3_num, s3_title, s3_desc = 'active', 'active', 'active'
    s4_num, s4_title, s4_desc = 'active', 'active', 'active'
    s5_num, s5_title, s5_desc = 'warning active', 'warning active', 'warning active'
elif sample_veh["failure_risk"] in ["High", "Critical"]:
    s3_num, s3_title, s3_desc = 'warning', 'warning', 'warning'
    s4_num, s4_title, s4_desc = 'warning active', 'warning active', 'warning active'
    s5_num, s5_title, s5_desc = '', '', ''
else:
    s3_num, s3_title, s3_desc = 'active', 'active', 'active'
    s4_num, s4_title, s4_desc = '', '', ''
    s5_num, s5_title, s5_desc = '', '', ''

pipeline_code = PIPELINE_HTML.replace('[ 01 ]</span><div class="step-title">', f'[ 01 ]</span><div class="step-title {s1_title}">') \
                             .replace('[ 02 ]</span><div class="step-title">', f'[ 02 ]</span><div class="step-title {s2_title}">') \
                             .replace('[ 03 ]</span><div class="step-title active">Predict Remaining Life</div><div class="step-desc active">', f'[ 03 ]</span><div class="step-title {s3_title}">Predict Remaining Life</div><div class="step-desc {s3_desc}">') \
                             .replace('class="step-num active">[ 03 ]', f'class="step-num {s3_num}">[ 03 ]') \
                             .replace('[ 04 ]</span><div class="step-title">', f'[ 04 ]</span><div class="step-title {s4_title}">') \
                             .replace('class="step-num">[ 04 ]', f'class="step-num {s4_num}">[ 04 ]') \
                             .replace('[ 05 ]</span><div class="step-title">', f'[ 05 ]</span><div class="step-title {s5_title}">') \
                             .replace('class="step-num">[ 05 ]', f'class="step-num {s5_num}">[ 05 ]')
components.html(pipeline_code, height=180, scrolling=False)
# =================================================================
# SECTION 4 — DASHBOARD INTELLIGENCE WIDGETS
# =================================================================
st.markdown("""
    <div class="section-label">Live Intelligence</div>
    <div class="section-title">Dashboard Overview</div>
""", unsafe_allow_html=True)

widget_col1, widget_col2 = st.columns(2)

with widget_col1:
    ACTIVITY_HTML = """
    <!DOCTYPE html><html><head><meta charset="utf-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600&family=JetBrains+Mono:wght@400;600&display=swap');

        :root {
            --bg:       #0F1319;
            --border:   #1E252D;
            --accent:   #00D9B5;
            --text:     #EDEFF1;
            --muted:    #5A6E7F;
            --shadow:   rgba(0,0,0,.35);
            --radius-lg: 12px;
            --radius-md: 8px;
        }
        [data-theme="light"] {
            --bg:       #FCFDFD;
            --border:   #D4E2DF;
            --accent:   #17BFA8;
            --text:     #55636B;
            --muted:    #7D8B90;
            --shadow:   rgba(35, 49, 58, 0.04);
        }
        * { margin:0; padding:0; box-sizing:border-box; }
        html,body { background:transparent; color:var(--text); font-family:'Space Grotesk',sans-serif; transition:color .2s; }
        .panel {
            background:var(--bg); border:1px solid var(--border);
            border-radius:var(--radius-lg); box-shadow:0 4px 12px var(--shadow);
            overflow:hidden; transition: background .2s, border-color .2s, box-shadow .2s;
        }
        .panel-header { padding:14px 16px; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; align-items:center; }
        .panel-title { font-family:'Space Grotesk',sans-serif; font-size:.85rem; font-weight:700; color:var(--text); }
        .live-dot { width:6px; height:6px; border-radius:50%; background:var(--accent); box-shadow:0 0 6px var(--accent); animation:pulse 2s infinite; }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.35} }
        .item { display:flex; align-items:flex-start; gap:12px; padding:11px 16px; border-bottom:1px solid var(--border); transition:background .15s; cursor:pointer; }
        .item:hover { background:rgba(24, 191, 168, 0.04); }
        .item:last-child { border-bottom:none; }
        .item-bar { width:2px; flex-shrink:0; background:var(--accent); border-radius:1px; align-self:stretch; opacity:.4; }
        .item-time { font-family:'JetBrains Mono',monospace; font-size:.65rem; color:var(--muted); white-space:nowrap; padding-top:2px; }
        .item-text { font-size:.8rem; color:var(--text); line-height:1.45; }
        .item-badge { display:inline-block; font-family:'JetBrains Mono',monospace; font-size:.58rem; font-weight:700; padding:1px 6px; text-transform:uppercase; letter-spacing:.05em; margin-left:6px; border-radius:12px; }
        .b-ai { color:#3B82F6; background:rgba(59,130,246,.08); border:1px solid rgba(59,130,246,.2); }
        .b-ok { color:#10B981; background:rgba(16,185,129,.08); border:1px solid rgba(16,185,129,.2); }
        .b-warn { color:#F59E0B; background:rgba(245,158,11,.08); border:1px solid rgba(245,158,11,.2); }
    </style></head><body>
    <div class="panel">
        <div class="panel-header">
            <span class="panel-title">Recent Activity</span>
            <span class="live-dot"></span>
        </div>
        %%RECENT_ACTIVITY_ROWS%%
    </div>
    <script>
    const stored = window.parent.localStorage ? window.parent.localStorage.getItem('tc_theme') : null;
    if (stored === 'light') document.documentElement.setAttribute('data-theme','light');
    
    // Theme change listener
    window.addEventListener('message', function(event) {
        if (event.data && event.data.type === 'theme-change') {
            if (event.data.theme === 'dark') {
                document.documentElement.removeAttribute('data-theme');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
            }
        }
    });
    </script>
    </body></html>
    """


    if not df_bms.empty:
        alerts_list = []
        crit_warnings = df_bms[df_bms["failure_risk"].isin(["Critical", "High"])].head(5)
        for idx, row in crit_warnings.reset_index().iterrows():
            time_str = f"{(10 + idx)%24:02d}:{(15 + idx*7)%60:02d}"
            v_id = row["vehicle_id"]
            risk_lbl = row["failure_risk"]
            alerts_list.append(f'<div class="item"><div class="item-bar"></div><span class="item-time">{time_str}</span><div class="item-text">AI predicted failure risk for {v_id} <span class="item-badge b-warn">{risk_lbl}</span></div></div>')
        recent_rows_str = "\n".join(alerts_list)
        dynamic_activity_html = ACTIVITY_HTML.replace('%%RECENT_ACTIVITY_ROWS%%', recent_rows_str)
    else:
        # Fallback rows
        fallback_rows = """
        <div class="item"><div class="item-bar"></div><span class="item-time">10:35</span><div class="item-text">AI predicted battery degradation for VEH-204 <span class="item-badge b-ai">AI</span></div></div>
        <div class="item"><div class="item-bar"></div><span class="item-time">10:22</span><div class="item-text">Fleet Alpha synchronized — 142 assets updated <span class="item-badge b-ok">Sync</span></div></div>
        <div class="item"><div class="item-bar"></div><span class="item-time">09:58</span><div class="item-text">Manufacturer warranty verified: BATCH-007 <span class="item-badge b-ok">Verified</span></div></div>
        <div class="item"><div class="item-bar"></div><span class="item-time">09:30</span><div class="item-text">New dataset imported — 2,400 charge cycles <span class="item-badge b-ok">Import</span></div></div>
        <div class="item"><div class="item-bar"></div><span class="item-time">08:45</span><div class="item-text">Fleet Beta: 3 batteries flagged for maintenance <span class="item-badge b-warn">Alert</span></div></div>
        """
        dynamic_activity_html = ACTIVITY_HTML.replace('%%RECENT_ACTIVITY_ROWS%%', fallback_rows)

    components.html(dynamic_activity_html, height=280, scrolling=False)


with widget_col2:
    HEALTH_HTML = """
    <!DOCTYPE html><html><head><meta charset="utf-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Space+Grotesk:wght@500;700&display=swap');

        :root {
            --bg:       #0F1319;
            --border:   #1E252D;
            --accent:   #00D9B5;
            --text:     #EDEFF1;
            --muted:    #5A6E7F;
            --shadow:   rgba(0,0,0,.35);
            --radius-lg: 12px;
            --gauge-empty: #161B22;
        }
        [data-theme="light"] {
            --bg:       #FCFDFD;
            --border:   #D4E2DF;
            --accent:   #17BFA8;
            --text:     #26343C;
            --muted:    #7D8B90;
            --shadow:   rgba(35, 49, 58, 0.04);
            --gauge-empty: #E7EFEE;
        }
        * { margin:0; padding:0; box-sizing:border-box; }
        html,body { background:transparent; color:var(--text); font-family:'Space Grotesk',sans-serif; transition:color .2s; }
        .panel {
            background:var(--bg); border:1px solid var(--border);
            border-radius:var(--radius-lg); box-shadow:0 4px 12px var(--shadow);
            overflow:hidden; transition: background .2s, border-color .2s, box-shadow .2s;
        }
        .panel-header { padding:14px 16px; border-bottom:1px solid var(--border); }
        .panel-title { font-size:.85rem; font-weight:700; color:var(--text); }
        .body { display:flex; align-items:center; gap:24px; padding:16px; }
        .legend { flex:1; display:flex; flex-direction:column; gap:8px; }
        .leg-row { display:flex; justify-content:space-between; align-items:center; font-family:'JetBrains Mono',monospace; font-size:.65rem; }
        .leg-dot { width:8px; height:8px; display:inline-block; margin-right:6px; border-radius:50%; }
        .leg-val { font-weight:700; color:var(--text); }
        .leg-lbl { color:var(--muted); }
    </style></head><body>
    <div class="panel">
        <div class="panel-header"><span class="panel-title">Battery Health Distribution</span></div>
        <div class="body">
            <svg width="110" height="110" viewBox="0 0 110 110">
                <circle cx="55" cy="55" r="40" fill="none" stroke="var(--gauge-empty)" stroke-width="18"/>
                <circle cx="55" cy="55" r="40" fill="none" stroke="#10B981" stroke-width="18"
                    stroke-dasharray="170.97 80.03" stroke-dashoffset="0" transform="rotate(-90 55 55)"/>
                <circle cx="55" cy="55" r="40" fill="none" stroke="#F59E0B" stroke-width="18"
                    stroke-dasharray="45.24 205.76" stroke-dashoffset="-170.97" transform="rotate(-90 55 55)"/>
                <circle cx="55" cy="55" r="40" fill="none" stroke="#EF4444" stroke-width="18"
                    stroke-dasharray="20.11 230.89" stroke-dashoffset="-216.21" transform="rotate(-90 55 55)"/>
                <circle cx="55" cy="55" r="40" fill="none" stroke="#5A6E7F" stroke-width="18"
                    stroke-dasharray="15.08 235.92" stroke-dashoffset="-236.32" transform="rotate(-90 55 55)"/>
                <text x="55" y="51" font-family="Space Grotesk" font-size="13" font-weight="700" fill="var(--text)" text-anchor="middle">92%</text>
                <text x="55" y="64" font-family="JetBrains Mono" font-size="7" fill="var(--muted)" text-anchor="middle">HEALTHY</text>
            </svg>
            <div class="legend">
                <div class="leg-row"><span><span class="leg-dot" style="background:#10B981;"></span><span class="leg-lbl">Healthy</span></span><span class="leg-val">580</span></div>
                <div class="leg-row"><span><span class="leg-dot" style="background:#F59E0B;"></span><span class="leg-lbl">Warning</span></span><span class="leg-val">153</span></div>
                <div class="leg-row"><span><span class="leg-dot" style="background:#EF4444;"></span><span class="leg-lbl">Critical</span></span><span class="leg-val">68</span></div>
                <div class="leg-row"><span><span class="leg-dot" style="background:#5A6E7F;"></span><span class="leg-lbl">Offline</span></span><span class="leg-val">49</span></div>
            </div>
        </div>
    </div>
    <script>
    const stored = window.parent.localStorage ? window.parent.localStorage.getItem('tc_theme') : null;
    if (stored === 'light') document.documentElement.setAttribute('data-theme','light');
    
    // Theme change listener
    window.addEventListener('message', function(event) {
        if (event.data && event.data.type === 'theme-change') {
            if (event.data.theme === 'dark') {
                document.documentElement.removeAttribute('data-theme');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
            }
        }
    });
    </script>
    </body></html>
    """


    p_h = cnt_healthy / total_vehicles
    p_w = cnt_warning / total_vehicles
    p_c = cnt_critical / total_vehicles
    p_o = cnt_offline / total_vehicles
    
    d_h = p_h * 251.33
    d_w = p_w * 251.33
    d_c = p_c * 251.33
    d_o = p_o * 251.33
    
    o_w = -d_h
    o_c = -(d_h + d_w)
    o_o = -(d_h + d_w + d_c)
    
    health_code = HEALTH_HTML.replace('stroke-dasharray="170.97 80.03" stroke-dashoffset="0"', f'stroke-dasharray="{d_h:.2f} {251.33-d_h:.2f}" stroke-dashoffset="0"') \
                             .replace('stroke-dasharray="45.24 205.76" stroke-dashoffset="-170.97"', f'stroke-dasharray="{d_w:.2f} {251.33-d_w:.2f}" stroke-dashoffset="{o_w:.2f}"') \
                             .replace('stroke-dasharray="20.11 230.89" stroke-dashoffset="-216.21"', f'stroke-dasharray="{d_c:.2f} {251.33-d_c:.2f}" stroke-dashoffset="{o_c:.2f}"') \
                             .replace('stroke-dasharray="15.08 235.92" stroke-dashoffset="-236.32"', f'stroke-dasharray="{d_o:.2f} {251.33-d_o:.2f}" stroke-dashoffset="{o_o:.2f}"') \
                             .replace('>92%</text>', f'>{avg_health}%</text>') \
                             .replace('<span class="leg-val">580</span>', f'<span class="leg-val">{cnt_healthy}</span>') \
                             .replace('<span class="leg-val">153</span>', f'<span class="leg-val">{cnt_warning}</span>') \
                             .replace('<span class="leg-val">68</span>', f'<span class="leg-val">{cnt_critical}</span>') \
                             .replace('<span class="leg-val">49</span>', f'<span class="leg-val">{cnt_offline}</span>')
    components.html(health_code, height=175, scrolling=False)


with widget_col2:
    MAINT_HTML = """
    <!DOCTYPE html><html><head><meta charset="utf-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Space+Grotesk:wght@500;700&display=swap');

        :root {
            --bg:       #0F1319;
            --border:   #1E252D;
            --accent:   #00D9B5;
            --text:     #EDEFF1;
            --muted:    #5A6E7F;
            --shadow:   rgba(0,0,0,.35);
            --radius-lg: 12px;
            --warn:     #F59E0B;
        }
        [data-theme="light"] {
            --bg:       #FCFDFD;
            --border:   #D4E2DF;
            --accent:   #17BFA8;
            --text:     #26343C;
            --muted:    #7D8B90;
            --shadow:   rgba(35, 49, 58, 0.04);
            --warn:     #E6A33B;
        }
        * { margin:0; padding:0; box-sizing:border-box; }
        html,body { background:transparent; color:var(--text); font-family:'Space Grotesk',sans-serif; transition:color .2s; }
        .panel {
            background:var(--bg); border:1px solid var(--border);
            border-radius:var(--radius-lg); box-shadow:0 4px 12px var(--shadow);
            margin-top:8px; overflow:hidden;
            transition: background .2s, border-color .2s, box-shadow .2s;
        }
        .panel-header { padding:11px 14px; border-bottom:1px solid var(--border); font-size:.85rem; font-weight:700; color:var(--text); }
        .m-row { display:flex; justify-content:space-between; align-items:center; padding:10px 14px; border-bottom:1px solid var(--border); }
        .m-row:last-child { border-bottom:none; }
        .m-label { font-size:.8rem; color:var(--text); }
        .m-sub { font-size:.65rem; color:var(--muted); margin-top:2px; }
        .m-date { font-family:'JetBrains Mono',monospace; font-size:.65rem; font-weight:700; padding:2px 8px; border:1px solid var(--warn); color:var(--warn); white-space:nowrap; border-radius:12px; }
    </style></head><body>
    <div class="panel">
        <div class="panel-header">Upcoming Maintenance</div>
        %%MAINTENANCE_ROWS%%
    </div>
    <script>
    const stored = window.parent.localStorage ? window.parent.localStorage.getItem('tc_theme') : null;
    if (stored === 'light') document.documentElement.setAttribute('data-theme','light');
    
    // Theme change listener
    window.addEventListener('message', function(event) {
        if (event.data && event.data.type === 'theme-change') {
            if (event.data.theme === 'dark') {
                document.documentElement.removeAttribute('data-theme');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
            }
        }
    });
    </script>
    </body></html>
    """
    if not df_bms.empty:
        m_list = []
        due_maint = df_bms[df_bms["maintenance_due"] == "Yes"].head(3)
        for idx, row in due_maint.reset_index().iterrows():
            day = 18 + idx*4
            v_id = row["vehicle_id"]
            m_list.append(f'<div class="m-row"><div><div class="m-label">{v_id} — Battery Pack A</div><div class="m-sub">Cycle wear threshold reached: {row["charge_cycles"]} cycles</div></div><span class="m-date">Jul {day}</span></div>')
        maint_rows_str = "\n".join(m_list)
        dynamic_maint_html = MAINT_HTML.replace('%%MAINTENANCE_ROWS%%', maint_rows_str)
    else:
        fallback_m_rows = """
        <div class="m-row"><div><div class="m-label">VEH-204 — Battery Pack A</div><div class="m-sub">Thermal inspection overdue</div></div><span class="m-date">Jul 18</span></div>
        <div class="m-row"><div><div class="m-label">Fleet Beta — Sector 3</div><div class="m-sub">Cycle limit approaching 500</div></div><span class="m-date">Jul 22</span></div>
        <div class="m-row"><div><div class="m-label">VEH-512 — BMS Firmware</div><div class="m-sub">Scheduled patch v4.2.1</div></div><span class="m-date">Jul 30</span></div>
        """
        dynamic_maint_html = MAINT_HTML.replace('%%MAINTENANCE_ROWS%%', fallback_m_rows)

    components.html(dynamic_maint_html, height=158, scrolling=False)


# =================================================================
# SECTION 5 — MANUFACTURER LEADERBOARD
# =================================================================
st.markdown("""
    <div class="section-label">Manufacturer Intelligence</div>
    <div class="section-title">Manufacturer Leaderboard</div>
""", unsafe_allow_html=True)

LEADER_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Space+Grotesk:wght@500;700&display=swap');

    :root {
        --bg:       #0F1319;
        --border:   #1E252D;
        --accent:   #00D9B5;
        --text:     #EDEFF1;
        --muted:    #5A6E7F;
        --shadow:   rgba(0,0,0,.35);
        --radius-lg: 12px;
        --bar-bg:   #161B22;
    }
    [data-theme="light"] {
        --bg:       #FCFDFD;
        --border:   #D4E2DF;
        --accent:   #17BFA8;
        --text:     #26343C;
        --muted:    #7D8B90;
        --shadow:   rgba(35, 49, 58, 0.04);
        --bar-bg:   #E7EFEE;
    }
    * { margin:0; padding:0; box-sizing:border-box; }
    html,body { background:transparent; color:var(--text); font-family:'Space Grotesk',sans-serif; transition:color .2s; }
    .card {
        background:var(--bg); border:1px solid var(--border);
        border-radius:var(--radius-lg); box-shadow:0 4px 12px var(--shadow);
        overflow:hidden; transition: background .2s, border-color .2s, box-shadow .2s;
    }
    table { width:100%; border-collapse:collapse; }
    thead tr { border-bottom:1px solid var(--border); }
    th { padding:14px 16px; text-align:left; font-size:.65rem; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); font-weight:700; }
    td { padding:12px 16px; font-family:'JetBrains Mono',monospace; font-size:.75rem; border-bottom:1px solid var(--border); color:var(--text); }
    tr:last-child td { border-bottom:none; }
    tr:hover td { background:rgba(24, 191, 168, 0.03); }
    .score { font-weight:700; color:var(--accent); }
    .rank { color:var(--muted); font-size:.7rem; font-weight:700; }
    .bar-wrap { width:80px; height:6px; background:var(--bar-bg); display:inline-block; vertical-align:middle; margin-left:8px; border-radius:3px; overflow:hidden; }
    .bar-fill { height:6px; background:var(--accent); border-radius:3px; transition:width .8s ease; }
</style></head><body>
<div class="card">
    <table>
        <thead>
            <tr><th>#</th><th>Manufacturer</th><th>Trust Score</th><th>Avg SoH</th><th>Warranty %</th><th>Prediction Accuracy</th></tr>
        </thead>
            %%LEADER_ROWS%%
        </tbody>
    </table>
</div>
<script>
const s=window.parent.localStorage?window.parent.localStorage.getItem('tc_theme'):null;
if(s==='light') document.documentElement.setAttribute('data-theme','light');

// Theme change listener
window.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'theme-change') {
        if (event.data.theme === 'dark') {
            document.documentElement.removeAttribute('data-theme');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
        }
    }
});
</script>
</body></html>
"""







if not df_bms.empty:
    # Group by batch_id / manufacturer
    mfg_groups = df_bms.groupby("batch_id")
    leader_rows = ""
    rank = 1
    for name, gp in mfg_groups:
        # Let's map batch name nicely
        mfg_name = "TrustCharge Energy" if name == "BATCH_A" else ("VoltCore Systems" if name == "BATCH_B" else ("ElectraPack Ltd." if name == "BATCH_C" else "NovaBattery Corp"))
        avg_soh = gp["state_of_health"].mean()
        avg_trust = gp["health_score"].mean()
        warranty = len(gp[gp["failure_risk"] == "Low"]) / len(gp) * 100
        accuracy = 95.0 - rank * 1.5
        
        leader_rows += f'<tr><td class="rank">{rank:02d}</td><td style="font-family:\'Space Grotesk\',sans-serif; font-weight:600;">{mfg_name}</td><td><span class="score">{avg_trust:.1f}</span><span class="bar-wrap"><span class="bar-fill" style="width:{int(avg_trust)}%"></span></span></td><td>{avg_soh:.1f}%</td><td>{warranty:.1f}%</td><td>{accuracy:.1f}%</td></tr>\n'
        rank += 1
        if rank > 4:
            break
    # fallback default 5th rank if we need 5
    leader_rows += '<tr><td class="rank">05</td><td style="font-family:\'Space Grotesk\',sans-serif; font-weight:600;">IonBridge Intl.</td><td><span class="score">76.8</span><span class="bar-wrap"><span class="bar-fill" style="width:77%"></span></span></td><td>79.3%</td><td>88.2%</td><td>79.1%</td></tr>\n'
    
    dynamic_leader_html = LEADER_HTML.replace('%%LEADER_ROWS%%', leader_rows)
else:
    fallback_leader = """
    <tr><td class="rank">01</td><td style="font-family:'Space Grotesk',sans-serif; font-weight:600;">TrustCharge Energy</td><td><span class="score">98.4</span><span class="bar-wrap"><span class="bar-fill" style="width:98%"></span></span></td><td>94.2%</td><td>99.1%</td><td>96.8%</td></tr>
    <tr><td class="rank">02</td><td style="font-family:'Space Grotesk',sans-serif; font-weight:600;">VoltCore Systems</td><td><span class="score">94.1</span><span class="bar-wrap"><span class="bar-fill" style="width:94%"></span></span></td><td>91.7%</td><td>97.3%</td><td>93.5%</td></tr>
    <tr><td class="rank">03</td><td style="font-family:'Space Grotesk',sans-serif; font-weight:600;">ElectraPack Ltd.</td><td><span class="score">89.7</span><span class="bar-wrap"><span class="bar-fill" style="width:90%"></span></span></td><td>88.5%</td><td>95.0%</td><td>90.2%</td></tr>
    <tr><td class="rank">04</td><td style="font-family:'Space Grotesk',sans-serif; font-weight:600;">NovaBattery Corp</td><td><span class="score">82.3</span><span class="bar-wrap"><span class="bar-fill" style="width:82%"></span></span></td><td>84.1%</td><td>91.4%</td><td>85.6%</td></tr>
    <tr><td class="rank">05</td><td style="font-family:'Space Grotesk',sans-serif; font-weight:600;">IonBridge Intl.</td><td><span class="score">76.8</span><span class="bar-wrap"><span class="bar-fill" style="width:77%"></span></span></td><td>79.3%</td><td>88.2%</td><td>79.1%</td></tr>
    """
    dynamic_leader_html = LEADER_HTML.replace('%%LEADER_ROWS%%', fallback_leader)

components.html(dynamic_leader_html, height=240, scrolling=False)


# =================================================================
# TOAST NOTIFICATIONS (auto-fire on load)
# =================================================================
st.markdown("""
<style>
.toast-container { position:fixed; bottom:90px; right:24px; z-index:99999; display:flex; flex-direction:column; gap:10px; pointer-events:none; }
@keyframes slideIn  { from{opacity:0;transform:translateX(60px)} to{opacity:1;transform:translateX(0)} }
@keyframes slideOut { from{opacity:1;transform:translateX(0)} to{opacity:0;transform:translateX(60px)} }
.toast { font-family:'JetBrains Mono',monospace; font-size:.63rem; font-weight:600; text-transform:uppercase;
         letter-spacing:.08em; background:var(--bg2); border:1px solid var(--border); border-left:3px solid var(--accent);
         color:var(--text); padding:10px 16px; box-shadow:4px 4px 0 var(--shadow);
         min-width:250px; opacity:0; pointer-events:all; }
.toast.in  { animation:slideIn  .3s ease forwards; }
.toast.out { animation:slideOut .35s ease forwards; }
.t-label { color:var(--accent); margin-right:6px; }
</style>
<div class="toast-container" id="toastContainer"></div>
<script>
var toasts=[
    {label:'AI',  text:'Prediction completed for VEH-204'},
    {label:'SYNC',text:'Fleet Alpha imported — 142 assets'},
    {label:'OK',  text:'Manufacturer batch verified'}
];
function showToast(t, delay) {
    setTimeout(function(){
        var el=document.createElement('div');
        el.className='toast';
        el.innerHTML='<span class="t-label">['+t.label+']</span>'+t.text;
        document.getElementById('toastContainer').appendChild(el);
        requestAnimationFrame(function(){ el.classList.add('in'); });
        setTimeout(function(){ el.classList.remove('in'); el.classList.add('out');
            setTimeout(function(){ el.remove(); },400); },4000);
    },delay);
}
toasts.forEach(function(t,i){ showToast(t,(i+1)*2200); });

window.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'show-toast') {
        var label = event.data.label;
        var text = event.data.text;
        if (label === 'USER' && text.includes('Profile')) {
            window.parent.location.href = window.parent.location.pathname + '?page=profile';
            return;
        }
        var container = document.getElementById('toastContainer');
        if (container) {
            var el = document.createElement('div');
            el.className = 'toast in';
            el.innerHTML = '<span class="t-label">[' + label + ']</span> ' + text;
            container.appendChild(el);
            setTimeout(function() {
                el.classList.remove('in');
                el.classList.add('out');
                setTimeout(function() { el.remove(); }, 400);
            }, 4000);
        }
    }
});
</script>
""", unsafe_allow_html=True)

# =================================================================
# FLOATING AI ASSISTANT
# =================================================================
AI_ASSISTANT_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    :root {
        --bg:       #0F1319;
        --border:   #1E252D;
        --accent:   #00D9B5;
        --text:     #EDEFF1;
        --muted:    #5A6E7F;
        --shadow:   rgba(0,0,0,.35);
        --radius-lg: 12px;
        --radius-md: 8px;
        --radius-sm: 6px;
        --chat-bg:  #161B22;
    }
    [data-theme="light"] {
        --bg:       #FCFDFD;
        --border:   #D4E2DF;
        --accent:   #17BFA8;
        --text:     #26343C;
        --muted:    #7D8B90;
        --shadow:   rgba(35, 49, 58, 0.04);
        --chat-bg:  #E7EFEE;
    }
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background:transparent; font-family:'Space Grotesk',sans-serif; overflow:hidden; }
    .fab {
        position:fixed; bottom:20px; right:20px;
        width:52px; height:52px; border-radius:50%;
        background:var(--accent); cursor:pointer; z-index:1000;
        display:flex; align-items:center; justify-content:center;
        box-shadow:0 4px 12px var(--shadow);
        border:none;
        transition:transform .2s ease, box-shadow .2s ease;
    }
    .fab:hover { transform:scale(1.05); box-shadow:0 6px 16px var(--shadow); }
    .fab svg { color: #080B0E; }
    
    .panel {
        position:fixed; bottom:84px; right:20px;
        width:340px; background:var(--bg); border:1px solid var(--border);
        border-radius:var(--radius-lg);
        box-shadow:0 10px 30px var(--shadow); display:none; z-index:999;
        flex-direction:column; max-height:460px; overflow:hidden;
        transition: background .2s, border-color .2s, box-shadow .2s;
    }
    .panel.open { display:flex; }
    .p-header { padding:14px 16px; border-bottom:1px solid var(--border); display:flex; justify-content:space-between; align-items:center; }
    .p-title { font-size:.85rem; font-weight:700; color:var(--text); }
    .p-status { display:flex; align-items:center; gap:6px; font-size:.65rem; color:var(--muted); font-family:'JetBrains Mono',monospace; }
    .p-dot { width:6px; height:6px; border-radius:50%; background:#10B981; }
    .p-close { background:none; border:none; color:var(--muted); cursor:pointer; font-size:14px; padding:0 4px; }
    .p-close:hover { color:var(--accent); }
    .p-body { flex:1; overflow-y:auto; padding:16px; }
    .greet { font-size:.78rem; color:var(--text); margin-bottom:14px; line-height:1.45; }
    .suggestions { display:flex; flex-direction:column; gap:8px; }
    .chip {
        padding:10px 12px; border:1px solid var(--border); font-size:.7rem; color:var(--text);
        cursor:pointer; transition:all .15s; text-align:left; background:var(--chat-bg);
        font-family:'Space Grotesk',sans-serif; border-radius:var(--radius-md);
        display: flex; align-items: center; justify-content: space-between;
    }
    .chip:hover { border-color:var(--accent); color:var(--accent); }
    .chip::after { content: '→'; font-size: .8rem; opacity: 0.5; transition: transform 0.15s; }
    .chip:hover::after { transform: translateX(2px); opacity: 1; }
    
    .p-footer { padding:12px; border-top:1px solid var(--border); display:flex; gap:8px; background: var(--bg); }
    .p-input { flex:1; background:var(--chat-bg); border:1px solid var(--border); color:var(--text); padding:8px 12px;
               font-family:'Space Grotesk',sans-serif; font-size:.75rem; outline:none; border-radius:var(--radius-sm); }
    .p-input:focus { border-color:var(--accent); }
    .p-send { background:var(--accent); border:none; padding:8px 14px; cursor:pointer; color:#080B0E; font-weight:600; font-size:.72rem; font-family:'Space Grotesk',sans-serif; transition:all .15s; border-radius:var(--radius-sm); }
    .p-send:hover { opacity: 0.9; }
</style></head><body>
<div class="fab" onclick="togglePanel()">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 16v-4H8l4-8v4h4l-4 8z" stroke="none" fill="currentColor"/>
    </svg>
</div>
<div class="panel" id="aiPanel">
    <div class="p-header">
        <span class="p-title">TrustCharge AI</span>
        <div style="display:flex;align-items:center;gap:12px;">
            <span class="p-status"><span class="p-dot"></span>Online</span>
            <button class="p-close" onclick="togglePanel()">&#10005;</button>
        </div>
    </div>
    <div class="p-body">
        <div class="greet">Hello. I am the TrustCharge AI assistant. Select a query or type your question below.</div>
        <div class="suggestions">
            <button class="chip">Explain Battery Health Score</button>
            <button class="chip">Predict Remaining Useful Life</button>
            <button class="chip">Generate Maintenance Report</button>
            <button class="chip">Compare Manufacturers by Trust Score</button>
            <button class="chip">Identify Risky Vehicles in Fleet</button>
        </div>
    </div>
    <div class="p-footer">
        <input class="p-input" type="text" placeholder="Ask anything about your fleet..."/>
        <button class="p-send">Send</button>
    </div>
</div>
<script>
function togglePanel() {
    var p = document.getElementById('aiPanel');
    p.classList.toggle('open');
}
document.querySelectorAll('.chip').forEach(function(c) {
    c.addEventListener('click', function() {
        document.querySelector('.p-input').value = this.textContent.trim();
    });
});

const s=window.parent.localStorage?window.parent.localStorage.getItem('tc_theme'):null;
if(s==='light') document.documentElement.setAttribute('data-theme','light');

// Theme change listener
window.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'theme-change') {
        if (event.data.theme === 'dark') {
            document.documentElement.removeAttribute('data-theme');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
        }
    }
});
</script>
</body></html>
"""
components.html(AI_ASSISTANT_HTML, height=500, scrolling=False)



# =================================================================
# FOOTER
# =================================================================
current_year = datetime.now().year
st.markdown(f"""
<div class="footer">
    TrustCharge &nbsp;/&nbsp; National Level Hackathon &nbsp;&nbsp;|&nbsp;&nbsp;
    Enterprise Build v2.0.0 &nbsp;&nbsp;|&nbsp;&nbsp;
    &copy; {current_year} Team TrustCharge
</div>
""", unsafe_allow_html=True)

# =================================================================
# THEME SYNC — Apply localStorage preference on main page load
# =================================================================
st.markdown("""
<script>
(function() {
    try {
        var t = localStorage.getItem('tc_theme');
        if (t === 'light') document.documentElement.setAttribute('data-theme','light');
        else document.documentElement.removeAttribute('data-theme');
    } catch(e) {}
})();
</script>
""", unsafe_allow_html=True)
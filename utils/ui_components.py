import streamlit as st
from datetime import datetime

# SVG Icons
HOME_SVG = '<svg class="nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>'
HEART_SVG = '<svg class="nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>'
GRID_SVG = '<svg class="nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="9"/><rect x="14" y="3" width="7" height="5"/><rect x="14" y="12" width="7" height="9"/><rect x="3" y="16" width="7" height="5"/></svg>'
FACTORY_SVG = '<svg class="nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 21H2V3l7 4v5l7-4v5l6-3v12z"/></svg>'
CAR_SVG = '<svg class="nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/></svg>'
BRAIN_SVG = '<svg class="nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/><path d="M12 6v12"/><path d="M6 12h12"/></svg>'
BAR_SVG = '<svg class="nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>'
REPORTS_SVG = '<svg class="nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>'
BELL_SVG = '<svg class="nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>'
GEAR_SVG = '<svg class="nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>'
LOGOUT_SVG = '<svg class="nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>'
BOLT_LOGO_SVG = '<svg class="logo-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#18E7D3" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="display:inline-block; vertical-align:middle;"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'

def clean_html(html_str: str) -> str:
    return "\n".join([line.strip() for line in html_str.split("\n")])

def inject_master_ui(active_page: str):
    """
    Injects custom styles and layout overrides to transform the Streamlit page
    into a premium enterprise SaaS dashboard.
    """
    
    # Hide Streamlit defaults and layout adjustments
    st.html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap');

        /* ── Unified Color Theme Palette ── */
        :root {
            --bg:               #090C12;
            --main-background:  #090C12;
            --card:             #111827;
            --surface-background: #111827;
            --border:           rgba(255,255,255,0.06);
            --accent:           #18E7D3;
            --accent-hover:     #14cfbd;
            --secondary:        #3B82F6;
            --sidebar:          #0B1220;
            --text:             #9CA3AF;
            --primary-text:     #FFFFFF;
            --muted:            #6B7280;
            --shadow:           rgba(0, 0, 0, 0.3);
            --radius-lg:        14px;
            --radius-md:        10px;
            --radius-sm:        6px;
            --transition:       all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            --success:          #10B981;
            --warn:             #F59E0B;
            --danger:           #EF4444;
        }

        /* ── Streamlit Frame Layout Adjustments ── */
        html, body, main, [data-testid="stAppViewContainer"], section[data-testid="stMain"], .block-container, div[data-testid="stVerticalBlock"] {
            background-color: var(--bg) !important;
            color: var(--primary-text) !important;
            font-family: 'Inter', sans-serif !important;
            transition: var(--transition);
        }

        [data-testid="stHeader"] {
            display: none !important;
        }

        [data-testid="stSidebar"] {
            display: none !important;
        }

        /* ── Main Container Spacing Overrides ── */
        div.block-container {
            padding-top: 136px !important;
            padding-left: 280px !important;
            padding-right: 24px !important;
            padding-bottom: 32px !important;
            max-width: none !important;
            margin: 0 !important;
            height: 100vh !important;
            overflow-y: auto !important;
            box-sizing: border-box !important;
        }

        h1, h2, h3, h4, h5, h6, .section-title {
            color: var(--primary-text) !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
        }

        p, label, span:not(.badge):not(.status-dot):not(.live):not(.warn), .kpi-lbl {
            color: var(--text) !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* Card components styling */
        .card, div[data-testid="stMetric"], div.stAlert {
            background-color: var(--card) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-lg) !important;
            box-shadow: var(--shadow) !important;
            padding: 20px !important;
            transition: var(--transition) !important;
        }
        .card:hover, div[data-testid="stMetric"]:hover {
            border-color: var(--accent) !important;
            transform: translateY(-2px) !important;
        }

        /* Streamlit metric defaults customization */
        div[data-testid="stMetric"] label {
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 0.7rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            color: var(--text) !important;
        }
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            color: var(--primary-text) !important;
        }

        /* Dropdowns/Inputs */
        div[data-baseweb="select"] {
            background-color: var(--card) !important;
            border-radius: var(--radius-md) !important;
            border: 1px solid var(--border) !important;
        }
        div[data-baseweb="select"] > div {
            border-radius: var(--radius-md) !important;
            background-color: transparent !important;
            color: var(--primary-text) !important;
        }

        /* Sidebar Styling (Custom Rendered HTML) */
        .custom-sidebar {
            position: fixed;
            left: 0;
            top: 0;
            bottom: 0;
            width: 260px;
            background: var(--sidebar);
            border-right: 1px solid var(--border);
            z-index: 999999;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 24px 16px;
            box-sizing: border-box;
        }

        .sidebar-logo {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 28px;
            padding-left: 8px;
        }
        .logo-text {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--primary-text);
            letter-spacing: -0.01em;
        }

        .sidebar-nav {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .nav-item {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 14px;
            border-radius: var(--radius-md);
            color: var(--text);
            text-decoration: none;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 0.88rem;
            font-weight: 500;
            transition: var(--transition);
        }
        .nav-item:hover {
            color: var(--accent);
            background: rgba(24, 231, 211, 0.04);
        }
        .nav-item.active {
            color: var(--accent);
            background: rgba(24, 231, 211, 0.06);
            border-left: 3px solid var(--accent);
            border-radius: 0 var(--radius-md) var(--radius-md) 0;
            padding-left: 11px;
            font-weight: 600;
        }

        .sidebar-footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 260px;
            background: #0B1220;
            border-top: 1px solid var(--border);
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            z-index: 10001;
            box-sizing: border-box;
        }
        .user-block {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 4px;
        }
        .user-info {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        .user-name {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--primary-text);
        }
        .user-role {
            font-size: 0.72rem;
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-family: 'JetBrains Mono', monospace;
        }
        .footer-actions {
            display: flex;
            gap: 8px;
        }
        .footer-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            border-radius: var(--radius-sm);
            border: 1px solid var(--border);
            color: var(--text);
            background: rgba(255,255,255,0.02);
            text-decoration: none;
            transition: var(--transition);
        }
        .footer-btn:hover {
            border-color: var(--accent);
            color: var(--accent);
            background: rgba(24, 231, 211, 0.04);
        }

        /* Sticky Top Navbar */
        .custom-navbar {
            position: fixed;
            left: 260px;
            top: 0;
            right: 0;
            height: 72px;
            background: var(--bg);
            border-bottom: 1px solid var(--border);
            z-index: 99999;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 24px;
            box-sizing: border-box;
        }

        .search-wrap {
            display: flex;
            align-items: center;
            gap: 10px;
            background: #111827;
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 8px 14px;
            width: 320px;
            transition: var(--transition);
        }
        .search-wrap:focus-within {
            border-color: var(--accent);
            width: 360px;
        }
        .search-input {
            background: transparent;
            border: none;
            color: var(--primary-text);
            font-size: 0.8rem;
            width: 100%;
            outline: none;
        }
        .search-input::placeholder {
            color: var(--muted);
        }

        .navbar-right {
            display: flex;
            align-items: center;
            gap: 14px;
        }
        .clock-display {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: var(--accent);
            background: rgba(24, 231, 211, 0.04);
            border: 1px solid rgba(24, 231, 211, 0.1);
            padding: 6px 12px;
            border-radius: var(--radius-sm);
        }
        .deploy-btn {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 0.78rem;
            font-weight: 600;
            background: transparent;
            border: 1px solid var(--accent);
            color: var(--accent);
            padding: 7px 16px;
            border-radius: var(--radius-md);
            cursor: pointer;
            transition: var(--transition);
        }
        .deploy-btn:hover {
            background: var(--accent);
            color: #000;
        }
        .nav-bell-wrap {
            position: relative;
        }
        .nav-bell-badge {
            position: absolute;
            top: -2px;
            right: -2px;
            width: 8px;
            height: 8px;
            background: var(--danger);
            border-radius: 50%;
        }

        .navbar-avatar {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: #1A2330;
            border: 1px solid var(--border);
            color: var(--accent);
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            font-size: 0.85rem;
            cursor: pointer;
            transition: var(--transition);
        }
        .navbar-avatar:hover {
            border-color: var(--accent);
        }

        /* Status Strip */
        .status-strip {
            position: fixed;
            left: 260px;
            top: 72px;
            right: 0;
            height: 48px;
            background: #111827;
            border-bottom: 1px solid var(--border);
            z-index: 9999;
            display: flex;
            align-items: center;
            padding: 0 24px;
            gap: 16px;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 0.75rem;
            box-sizing: border-box;
            overflow-x: auto;
            white-space: nowrap;
        }
        .status-strip::-webkit-scrollbar {
            display: none;
        }
        .status-label {
            font-weight: 700;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .status-divider {
            color: rgba(255,255,255,0.1);
        }
        .status-item {
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--text);
        }
        .status-item span {
            font-family: 'JetBrains Mono', monospace;
            color: var(--primary-text);
            font-weight: 600;
        }
        
        /* Table overrides for Stark layout */
        div[data-testid="stDataFrame"] {
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-lg) !important;
            overflow: hidden !important;
            box-shadow: var(--shadow) !important;
        }

        /* Sparkline charts placeholder */
        .spark-svg {
            display: block;
            margin-top: 10px;
        }

        /* Collapse the space occupied by the floating AI assistant iframe */
        div.element-container:has(iframe[srcdoc*="aiPanel"]),
        div.stHtml:has(iframe[srcdoc*="aiPanel"]) {
            position: fixed !important;
            bottom: 0 !important;
            right: 0 !important;
            width: 0 !important;
            height: 0 !important;
            overflow: visible !important;
            z-index: 999999 !important;
            pointer-events: none !important;
        }
        div.element-container:has(iframe[srcdoc*="aiPanel"]) iframe,
        div.stHtml:has(iframe[srcdoc*="aiPanel"]) iframe {
            position: fixed !important;
            bottom: 20px !important;
            right: 20px !important;
            width: 360px !important;
            height: 520px !important;
            border: none !important;
            z-index: 999999 !important;
            pointer-events: all !important;
        }
    </style>
    """)
    
    # Render Left Sidebar
    sidebar_html = f"""
    <div class="custom-sidebar">
        <div>
            <div class="sidebar-logo">
                {BOLT_LOGO_SVG}
                <span class="logo-text">TrustCharge</span>
            </div>
            <div class="sidebar-nav">
                <a href="/" target="_self" class="nav-item {"active" if active_page == "Dashboard" else ""}">
                    {HOME_SVG}
                    Dashboard
                </a>
                <a href="/battery_scorecard" target="_self" class="nav-item {"active" if active_page == "Battery Scorecard" else ""}">
                    {HEART_SVG}
                    Battery Scorecard
                </a>
                <a href="/fleet_dashboard" target="_self" class="nav-item {"active" if active_page == "Fleet Overview" else ""}">
                    {GRID_SVG}
                    Fleet Overview
                </a>
                <a href="/manufacturer_dashboard" target="_self" class="nav-item {"active" if active_page == "Manufacturers" else ""}">
                    {FACTORY_SVG}
                    Manufacturers
                </a>
                <a href="/?page=vehicles" target="_self" class="nav-item {"active" if active_page == "Vehicles" else ""}">
                    {CAR_SVG}
                    Vehicles
                </a>
                <a href="/?page=predictions" target="_self" class="nav-item {"active" if active_page == "AI Predictions" else ""}">
                    {BRAIN_SVG}
                    AI Predictions
                </a>
                <a href="/?page=analytics" target="_self" class="nav-item {"active" if active_page == "Analytics" else ""}">
                    {BAR_SVG}
                    Analytics
                </a>
                <a href="/?page=reports" target="_self" class="nav-item {"active" if active_page == "Reports" else ""}">
                    {REPORTS_SVG}
                    Reports
                </a>
                <a href="/?page=alerts" target="_self" class="nav-item {"active" if active_page == "Alerts" else ""}">
                    {BELL_SVG}
                    Alerts
                </a>
            </div>
        </div>
    </div>
    """
    st.markdown(clean_html(sidebar_html), unsafe_allow_html=True)

    # Render sidebar footer separately to avoid Streamlit code-block escaping
    footer_html = f"""<div class="sidebar-footer"><div class="user-block" style="display:flex;align-items:center;gap:8px;"><div class="user-avatar-circle" style="width:32px;height:32px;border-radius:50%;background:#1A2330;border:1px solid rgba(255,255,255,0.06);color:#18E7D3;display:flex;align-items:center;justify-content:center;font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:0.8rem;flex-shrink:0;">SK</div><div class="user-info"><span class="user-name">Shruti K</span><span class="user-role">Administrator</span></div></div><div class="footer-actions" style="display:flex;gap:8px;margin-top:8px;"><a href="/?page=profile" target="_self" class="footer-btn" title="Settings">{GEAR_SVG}</a><a href="/?action=logout" target="_self" class="footer-btn" style="color:#EF4444;" title="Logout">{LOGOUT_SVG}</a></div></div>"""
    st.markdown(footer_html, unsafe_allow_html=True)
    
    # Render Sticky Top Navbar
    search_icon = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>'
    navbar_html = f"""
    <div class="custom-navbar">
        <div class="search-wrap">
            {search_icon}
            <input type="text" placeholder="Quick Search Assets (e.g., cell, battery)..." class="search-input" />
        </div>
        <div class="nav-right">
            <a href="/?page=profile" target="_self" class="profile-link" style="text-decoration: none; color: inherit;">
                <div class="avatar-circle">SK</div>
                <span class="profile-name">Shruti K</span>
            </a>
        </div>
    </div>
    """
    st.html(navbar_html)
    
    # Render Status Ribbon Bar
    t_now = datetime.now()
    time_str = t_now.strftime("%I:%M %p")
    date_str = t_now.strftime("%d %b %Y")
    
    status_html = f"""
    <div class="status-strip">
        <span class="status-label">[ CURRENT FLEET STATUS ]</span>
        <span class="status-divider">|</span>
        <div class="status-item">ACTIVE VEHICLES: <span id="ticker-active">850</span></div>
        <span class="status-divider">|</span>
        <div class="status-item">BATTERY ASSETS: <span>1,000</span></div>
        <span class="status-divider">|</span>
        <div class="status-item">FLEET UPTIME: <span>99.97%</span></div>
        <span class="status-divider">|</span>
        <div class="status-item">LAST SYNC: <span id="ticker-sync">0.04s</span></div>
        <span class="status-divider">|</span>
        <div class="status-item" style="color: var(--accent); font-weight: 600;" id="status-clock">{time_str}</div>
        <span class="status-divider">|</span>
        <div class="status-item" style="color: var(--muted);">{date_str}</div>
    </div>
    
    <script>
        (function() {{
            function updateClock() {{
                const now = new Date();
                const clockEl = document.getElementById('status-clock');
                if (clockEl) {{
                    let hours = now.getHours();
                    const minutes = String(now.getMinutes()).padStart(2, '0');
                    const ampm = hours >= 12 ? 'PM' : 'AM';
                    hours = hours % 12;
                    hours = hours ? hours : 12;
                    clockEl.textContent = hours + ':' + minutes + ' ' + ampm;
                }}
                
                // Slightly randomize active and sync to simulate live system
                const activeEl = document.getElementById('ticker-active');
                if (activeEl) {{
                    activeEl.textContent = Math.floor(Math.random() * 5) + 848;
                }}
                const syncEl = document.getElementById('ticker-sync');
                if (syncEl) {{
                    syncEl.textContent = (Math.random() * 0.05 + 0.02).toFixed(2) + 's';
                }}
            }}
            setInterval(updateClock, 3000);
        }})();
    </script>
    """
    st.html(status_html)


def apply_plotly_theme(fig):
    """
    Utility to style Plotly charts with transparent backgrounds,
    unified text typography, and clean grids.
    """
    fig.update_layout(
        font_family="Space Grotesk",
        font_color="#9CA3AF",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.04)",
            linecolor="rgba(255,255,255,0.06)",
            tickfont=dict(family="JetBrains Mono", size=10)
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.04)",
            linecolor="rgba(255,255,255,0.06)",
            tickfont=dict(family="JetBrains Mono", size=10)
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(family="Space Grotesk", size=10)
        )
    )
    return fig

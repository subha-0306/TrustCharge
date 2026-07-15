import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------
st.set_page_config(
    page_title="TrustCharge | EV Battery Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =================================================================
# MASTER CSS — CSS Variables for Light/Dark Theme + All Global Styles
# =================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap');

    /* ── Dark Mode (default) ── */
    :root {
        --bg:           #080B0E;
        --bg2:          #0F1319;
        --sidebar:      #0F1319;
        --card:         #0F1319;
        --navbar:       #0F1319;
        --search-bg:    #151B22;
        --border:       #1E252D;
        --border-soft:  #161B22;
        --accent:       #00D9B5;
        --accent-hover: #00BFA2;
        --text:         #9EAEB8;
        --text-title:   #EDEFF1;
        --muted:        #5A6E7F;
        --muted2:       #3A4D5C;
        --warn:         #F59E0B;
        --danger:       #EF4444;
        --success:      #10B981;
        --shadow:       rgba(0, 0, 0, 0.35);
        --hover-bg:     rgba(0, 217, 181, 0.08);
        --selection:    rgba(0, 217, 181, 0.15);
        --radius-lg:    12px;
        --radius-md:    8px;
        --radius-sm:    6px;
        --transition:   all 0.18s ease-in-out;
    }

    /* ── Light Mode overrides (OLA / Ather / Siemens theme) ── */
    [data-theme="light"] {
        --bg:           #EEF3F2;
        --bg2:          #E7EFEE;
        --sidebar:      #DEE9E7;
        --card:         #FCFDFD;
        --navbar:       #F5F8F8;
        --search-bg:    #E7EFEE;
        --border:       #D4E2DF;
        --border-soft:  #D4E2DF;
        --accent:       #17BFA8;
        --accent-hover: #14A692;
        --secondary-accent: #4E7A76;
        --muted-accent: #7D8E91;
        --text-title:   #26343C;
        --text:         #55636B;
        --muted:        #7D8B90;
        --muted2:       #7D8E91;
        --success:      #36A972;
        --warn:         #E6A33B;
        --danger:       #D9534F;
        --shadow:       rgba(35, 49, 58, 0.04);
        --hover-bg:     #F3F8F8;
        --selection:    #DEE9E7;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        transition: var(--transition);
    }

    /* Spacing & Layout overrides */


    div.block-container {
        padding-top: 80px !important;
        padding-bottom: 0px !important;
        padding-left: 32px !important;
        padding-right: 32px !important;
        max-width: 1350px;
        margin: 0 auto;
        display: flex !important;
        flex-direction: column !important;
        min-height: calc(100vh - 80px) !important;
    }

    div[data-testid="stVerticalBlock"] {
        display: flex !important;
        flex-direction: column !important;
        flex-grow: 1 !important;
    }

    /* Push the footer to the bottom */
    div:has(> .footer), div[data-testid="element-container"]:has(> .footer) {
        margin-top: auto !important;
    }

    [data-testid="stHeader"] {
        display: none !important;
    }

    [data-testid="stSidebar"] {
        background-color: var(--sidebar) !important;
        border-right: 1px solid var(--border-soft) !important;
        transition: var(--transition);
    }

    /* Sidebar nav items */
    [data-testid="stSidebarNavLink"] {
        border-radius: var(--radius-md) !important;
        margin: 3px 12px !important;
        padding: 6px 14px !important;
        transition: var(--transition) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 500 !important;
        color: var(--text) !important;
    }
    [data-testid="stSidebarNavLink"]:hover {
        background-color: var(--hover-bg) !important;
        color: var(--accent) !important;
    }
    [data-testid="stSidebarNavLink"][aria-current="page"] {
        background-color: var(--selection) !important;
        color: var(--text-title) !important;
        border-left: 3px solid var(--accent) !important;
        font-weight: 600 !important;
    }

    /* ── CARDS ── */
    .card {
        background-color: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 24px;
        box-shadow: 0 4px 12px var(--shadow);
        transition: var(--transition);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
    }
    .card:hover {
        border-color: var(--accent);
        box-shadow: 0 8px 20px var(--shadow);
    }

    /* ── KPI CARDS ── */
    .kpi-card {
        background-color: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 20px 18px;
        box-shadow: 0 4px 12px var(--shadow);
        height: 100%;
        transition: var(--transition);
    }
    .kpi-card:hover {
        border-color: var(--accent);
        box-shadow: 0 8px 20px var(--shadow);
    }
    .kpi-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.7rem;
        font-weight: 700;
        color: var(--text-title);
        line-height: 1.1;
        margin-bottom: 6px;
        letter-spacing: -0.02em;
        transition: var(--transition);
    }
    .kpi-lbl {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--muted);
        font-weight: 600;
    }
    .kpi-trend {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.6rem;
        color: var(--success);
        margin-top: 4px;
    }

    /* ── BUTTONS ── */
    .btn {
        display: inline-block;
        padding: 10px 24px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.8rem;
        font-weight: 600;
        text-decoration: none !important;
        border-radius: var(--radius-md);
        transition: var(--transition);
        text-align: center;
        cursor: pointer;
    }
    .btn-primary {
        background-color: var(--accent);
        color: var(--bg) !important;
        border: 1px solid var(--accent);
        box-shadow: 0 2px 4px var(--shadow);
    }
    .btn-primary:hover {
        background-color: var(--accent-hover);
        border-color: var(--accent-hover);
        box-shadow: 0 4px 8px var(--shadow);
    }
    .btn-primary:active {
        transform: translateY(0);
    }
    .btn-secondary {
        background-color: transparent;
        border: 1px solid var(--border);
        color: var(--text) !important;
        box-shadow: 0 1px 2px var(--shadow);
    }
    .btn-secondary:hover {
        border-color: var(--accent);
        background-color: var(--hover-bg);
        color: var(--accent) !important;
    }
    .btn-secondary:active {
        transform: translateY(0);
    }
    .btn-full { width: 100%; box-sizing: border-box; }



    /* ── HERO ── */
    .hero-wordmark {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .hero-wordmark::before {
        content: '';
        display: inline-block;
        width: 18px;
        height: 1px;
        background-color: var(--accent);
    }
    .hero-headline {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.2rem;
        font-weight: 700;
        line-height: 1.15;
        letter-spacing: -0.03em;
        color: var(--text-title);
        margin-bottom: 12px;
        transition: var(--transition);
    }
    .hero-headline span { color: var(--accent); }
    .hero-subtitle {
        font-size: 1rem;
        line-height: 1.6;
        color: var(--text);
        margin-bottom: 14px;
        max-width: 620px;
    }

    .section-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: var(--muted);
        margin-top: 40px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-label::after {
        content: '';
        display: block;
        flex: 1;
        height: 1px;
        background-color: var(--border-soft);
    }
    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        margin-top: 6px;
        margin-bottom: 20px;
        letter-spacing: -0.02em;
        color: var(--text-title);
        transition: var(--transition);
    }

    /* ── MODULE CARDS ── */
    .mod-card {
        background-color: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 24px;
        height: 310px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        box-shadow: 0 4px 12px var(--shadow);
        transition: var(--transition);
    }
    .mod-card.alt-bg {
        background-color: var(--bg2);
    }
    .mod-card:hover {
        border-color: var(--accent);
        box-shadow: 0 8px 24px var(--shadow);
        transform: translateY(-2px);
    }
    .mod-corner {
        position: absolute;
        top: 12px;
        right: 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.58rem;
        color: var(--muted);
        letter-spacing: 0.08em;
        transition: var(--transition);
    }
    .mod-card:hover .mod-corner { color: var(--accent); }
    .mod-id {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.58rem;
        color: var(--muted);
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .mod-title-row {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }
    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: var(--accent);
        box-shadow: 0 0 6px var(--accent);
        flex-shrink: 0;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.35; }
    }
    .mod-title-text {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text-title);
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }
    .mod-desc-text {
        font-size: 0.82rem;
        color: var(--text);
        line-height: 1.55;
        margin-bottom: 0;
    }
    .mod-btn {
        display: block;
        width: 100%;
        box-sizing: border-box;
        padding: 9px 16px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: none;
        letter-spacing: 0;
        text-align: center;
        text-decoration: none !important;
        border: 1px solid var(--border);
        background-color: transparent;
        color: var(--text) !important;
        border-radius: var(--radius-md);
        box-shadow: 0 1px 2px var(--shadow);
        transition: var(--transition);
        margin-top: 14px;
    }
    .mod-btn:hover {
        background-color: var(--accent);
        border-color: var(--accent);
        color: var(--bg) !important;
        box-shadow: 0 4px 8px var(--shadow);
        transform: translateY(-1px);
    }
    .mod-btn:active {
        transform: translateY(0);
    }

    /* ── STATUS BADGES ── */
    .badge {
        display: inline-block;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.65rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 12px;
        text-transform: uppercase;
    }
    .badge-healthy  { color: #10B981; background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.2); }
    .badge-warning  { color: #F59E0B; background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.2); }
    .badge-critical { color: #EF4444; background: rgba(239,68,68,0.08);  border: 1px solid rgba(239,68,68,0.2); }
    .badge-online   { color: #00D9B5; background: rgba(0,217,181,0.08);  border: 1px solid rgba(0,217,181,0.2); }
    .badge-processing { color: #3B82F6; background: rgba(59,130,246,0.08); border: 1px solid rgba(59,130,246,0.2); }


    /* ── QUICK ACTIONS ── */
    .qa-bar {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin-bottom: 12px;
    }

    .qa-btn {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.72rem;
        font-weight: 600;
        color: var(--text);
        background: var(--card);
        border: 1px solid var(--border);
        padding: 8px 18px;
        text-transform: none;
        letter-spacing: 0;
        cursor: pointer;
        border-radius: var(--radius-md);
        box-shadow: 0 1px 2px var(--shadow);
        transition: var(--transition);
        text-decoration: none;
        display: inline-block;
    }
    .qa-btn:hover {
        border-color: var(--accent);
        color: var(--accent);
        transform: translateY(-1px);
        box-shadow: 0 2px 6px var(--shadow);
    }
    .qa-btn:active { transform: translateY(0); }
    .qa-btn.primary {
        background: var(--accent);
        color: var(--bg);
        border-color: var(--accent);
        box-shadow: 0 2px 4px var(--shadow);
    }
    .qa-btn.primary:hover {
        background: var(--accent-hover);
        border-color: var(--accent-hover);
        box-shadow: 0 4px 8px var(--shadow);
    }

    /* ── SHIMMER SKELETON ── */
    @keyframes shimmer {
        0%   { background-position: -600px 0; }
        100% { background-position: 600px 0; }
    }
    .skeleton {
        background: linear-gradient(90deg, var(--card) 25%, var(--border-soft) 50%, var(--card) 75%);
        background-size: 600px 100%;
        animation: shimmer 1.4s infinite;
        border-radius: 4px;
    }

    /* ── TICKER ── */
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background-color: var(--bg2);
        border: 1px solid var(--border-soft);
        border-left: 3px solid var(--accent);
        padding: 5px 0;
        margin-top: 6px;
        margin-bottom: 12px;
        border-radius: var(--radius-md);
        transition: var(--transition);
    }
    .ticker-track {
        display: flex;
        width: max-content;
        animation: ticker-scroll 28s linear infinite;
        white-space: nowrap;
    }
    .ticker-item {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 600;
        color: var(--muted);
        padding: 0 36px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .ticker-item .live { color: var(--accent); }
    .ticker-item .warn { color: var(--warn); }
    .ticker-sep { color: var(--border-soft); margin: 0 8px; }

    /* ── FOOTER ── */
    .footer {
        border-top: 1px solid var(--border-soft);
        padding: 16px 0;
        margin-top: 36px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        text-align: center;
        transition: var(--transition);
    }

    /* Sticky Navbar Iframe styles */
    iframe[height="72"] {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 72px !important;
        z-index: 9999 !important;
        border: none !important;
        border-bottom: 1px solid var(--border-soft) !important;
        box-shadow: 0 2px 8px var(--shadow) !important;
    }

    /* ── TOAST NOTIFICATIONS ── */
    .toast-container {
        position: fixed;
        bottom: 90px;
        right: 24px;
        z-index: 99999;
        display: flex;
        flex-direction: column;
        gap: 10px;
        pointer-events: none;
    }
    @keyframes slideIn  { from { opacity:0; transform:translateY(20px); } to { opacity:1; transform:translateY(0); } }
    @keyframes slideOut { from { opacity:1; transform:translateY(0); }   to { opacity:0; transform:translateY(20px); } }
    .toast {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        background-color: var(--bg2);
        border: 1px solid var(--border);
        border-left: 3px solid var(--accent);
        color: var(--text-title);
        padding: 12px 18px;
        border-radius: var(--radius-md);
        box-shadow: 0 4px 16px var(--shadow);
        min-width: 280px;
        animation: slideIn 0.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        pointer-events: all;
        opacity: 0;
        display: flex;
        align-items: center;
    }
    .toast.out { animation: slideOut 0.2s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
    .toast .toast-label { color: var(--accent); margin-right: 8px; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; text-transform: uppercase; }

    h1, h2, h3, h4, h5, h6, .section-title { color: var(--text-title) !important; transition: var(--transition); }
    hr { border-color: var(--border-soft) !important; }
</style>
""", unsafe_allow_html=True)

# =================================================================
# ENTERPRISE NAVBAR — Theme toggle, Search, Notifications, Profile

NAVBAR_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
    * { margin:0; padding:0; box-sizing:border-box; }
    :root {
        --bg:      #080B0E;
        --card:    #0F1319;
        --border:  #1E252D;
        --accent:  #00D9B5;
        --text:    #EDEFF1;
        --muted:   #5A6E7F;
        --shadow:  rgba(0,0,0,.35);
        --navbar:  #0F1319;
        --search-bg: #151B22;
        --radius-lg: 12px;
        --radius-md: 8px;
        --radius-sm: 6px;
    }
    [data-theme="light"] {
        --bg:      #EEF3F2;
        --card:    #FCFDFD;
        --border:  #D4E2DF;
        --accent:  #17BFA8;
        --text:    #55636B;
        --muted:   #7D8B90;
        --shadow:  rgba(35, 49, 58, 0.04);
        --navbar:  #F5F8F8;
        --search-bg: #E7EFEE;
    }
    body { background:var(--navbar); font-family:'Space Grotesk',sans-serif; color:var(--text); transition:background .2s, color .2s; }
    .nav-container {
        display:flex; align-items:center; justify-content:space-between;
        max-width:1350px; margin:0 auto; padding:0 32px; height:72px;
    }
    .nav-left { display:flex; align-items:center; gap:24px; flex:1; }
    .logo { font-size:1.05rem; font-weight:700; color:var(--text); letter-spacing:-0.02em; display:flex; align-items:center; gap:6px; cursor:pointer; text-decoration:none; }
    .logo span { color: var(--accent); }
    .search-wrap {
        width: 380px; display:flex; align-items:center;
        background:var(--search-bg); border:1px solid var(--border);
        padding:8px 14px; gap:8px; border-radius:var(--radius-md);
        transition:all .15s ease-in-out;
        height: 38px;
    }
    .search-wrap:focus-within { border-color:var(--accent); box-shadow:0 0 0 2px rgba(23, 191, 168, 0.15); }
    .search-icon { color:var(--muted); font-size:12px; flex-shrink:0; }
    .search-input {
        flex:1; background:transparent; border:none; outline:none;
        font-family:'Space Grotesk',sans-serif; font-size:0.8rem;
        color:var(--text);
    }
    .search-input::placeholder { color:var(--muted); }
    .nav-right { display:flex; align-items:center; gap:16px; }
    
    /* Deploy Button */
    .deploy-btn {
        background: var(--accent); color: var(--bg) !important; border: none;
        padding: 8px 16px; border-radius: var(--radius-md);
        font-family: 'Space Grotesk', sans-serif; font-size: 0.75rem; font-weight: 600;
        cursor: pointer; display: flex; align-items: center; justify-content: center;
        transition: all .15s ease-in-out;
        box-shadow: 0 2px 4px var(--shadow);
    }
    .deploy-btn:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
    .deploy-btn:active { transform: translateY(0); }

    /* Buttons / icons */
    .nav-btn {
        position:relative; background:var(--card); border:1px solid var(--border);
        width: 38px; height: 38px; border-radius: var(--radius-md);
        cursor:pointer; color:var(--text);
        display: flex; align-items: center; justify-content: center;
        transition:all .15s ease-in-out;
        box-shadow: 0 1px 2px var(--shadow);
    }
    .nav-btn:hover { border-color:var(--accent); color:var(--accent); transform: translateY(-1px); }
    .nav-btn:active { transform: translateY(0); }

    .badge {
        position:absolute; top:-4px; right:-4px;
        min-width:16px; height:16px; border-radius:50%;
        background:#EF4444; color:#FFFFFF;
        font-family:'JetBrains Mono',monospace; font-size:0.55rem; font-weight:700;
        display:flex; align-items:center; justify-content:center; padding: 0 3px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }
    .avatar {
        width:38px; height:38px; border-radius:50%;
        background:var(--card); color:var(--accent);
        font-family:'Space Grotesk',sans-serif; font-size:0.85rem; font-weight:700;
        display:flex; align-items:center; justify-content:center;
        cursor:pointer; border:1px solid var(--border);
        transition:all .15s ease-in-out;
        box-shadow: 0 1px 2px var(--shadow);
    }
    .avatar:hover { border-color:var(--accent); transform: translateY(-1px); }
    
    .theme-btn {
        background:var(--card); border:1px solid var(--border);
        width: 38px; height: 38px; border-radius: var(--radius-md);
        cursor:pointer; color:var(--text);
        display: flex; align-items: center; justify-content: center;
        transition:all .15s ease-in-out;
        box-shadow: 0 1px 2px var(--shadow);
    }
    .theme-btn:hover { border-color:var(--accent); color:var(--accent); transform: translateY(-1px); }

    /* Dropdowns */
    .dropdown {
        position:absolute; top:calc(100% + 8px); right:0;
        background:var(--card); border:1px solid var(--border);
        border-radius: var(--radius-lg);
        min-width:280px; box-shadow:0 10px 30px var(--shadow);
        display:none; z-index:999;
        transform: translateY(10px); opacity: 0;
        animation: slideDown .2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    @keyframes slideDown {
        to { transform: translateY(0); opacity: 1; }
    }
    .dropdown.open { display:block; }
    .dropdown-header {
        font-family:'Space Grotesk',sans-serif; font-size:0.75rem; font-weight:700;
        text-transform:uppercase; letter-spacing:.05em; color:var(--text);
        padding:12px 16px; border-bottom:1px solid var(--border);
        display:flex; justify-content:space-between; align-items:center;
    }
    .dropdown-actions { display:flex; gap:8px; }
    .d-action {
        font-family:'Space Grotesk',sans-serif; font-size:0.68rem; font-weight:600;
        color:var(--accent); cursor:pointer; text-transform:none;
        background:none; border:none;
    }
    .d-action:hover { text-decoration: underline; }
    
    .notif-item {
        padding:12px 16px; border-bottom:1px solid var(--border);
        transition:background .15s; cursor:pointer;
    }
    .notif-item:hover { background:var(--search-bg); }
    .notif-item:last-child { border-bottom:none; }
    .notif-title { font-size:0.75rem; color:var(--text); margin-bottom:4px; font-weight:500; line-height: 1.35; }
    .notif-time  { font-family:'JetBrains Mono',monospace; font-size:0.6rem; color:var(--muted); }
    
    .notif-dot { width:6px; height:6px; border-radius:50%; display:inline-block; margin-right:6px; flex-shrink:0; }
    .notif-dot.alert { background: #EF4444; }
    .notif-dot.warning { background: #F59E0B; }
    .notif-dot.info { background: #3B82F6; }
    .notif-dot.success { background: #10B981; }
    
    .notif-row { display:flex; align-items:flex-start; gap:8px; }
    
    .profile-item {
        padding:10px 16px; display:flex; align-items:center; gap:12px;
        cursor:pointer; transition:background .15s; border-bottom:1px solid var(--border);
        font-size:0.8rem; color:var(--text);
    }
    .profile-item:hover { background:var(--search-bg); color:var(--accent); }
    .profile-item:last-child { border-bottom:none; }
    .pi-icon { color:var(--muted); font-size:14px; width:16px; text-align:center; }
    .profile-item:hover .pi-icon { color:var(--accent); }
    
    svg { display:block; }
    .rel { position:relative; }
</style>
</head><body>
<div class="nav-container">
    <div class="nav-left">
        <!-- Logo & Wordmark -->
        <a class="logo" href="#" target="_self">⚡ <span>TrustCharge</span></a>
        <!-- Search -->
        <div class="search-wrap">
            <svg class="search-icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
            </svg>
            <input class="search-input" type="text" placeholder="Search fleet, battery ID, manufacturer, VIN..."/>
        </div>
    </div>

    <div class="nav-right">
        <!-- Deploy Button -->
        <button class="deploy-btn" onclick="showDeployToast()">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 6px;">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            Deploy
        </button>

        <!-- Theme Toggle -->
        <button class="theme-btn" id="themeBtn" onclick="toggleTheme()" title="Toggle Theme">
            <span id="themeIcon"></span>
        </button>

        <!-- Notification Bell -->
        <div class="rel">
            <button class="nav-btn" onclick="toggleDrop('notifDrop')" title="Notifications">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                </svg>
                <span class="badge" id="notifBadge">5</span>
            </button>
            <div class="dropdown" id="notifDrop">
                <div class="dropdown-header">
                    <span>Notifications</span>
                    <div class="dropdown-actions">
                        <button class="d-action" onclick="markAllRead()">Mark Read</button>
                        <button class="d-action" onclick="clearAll()">Clear All</button>
                    </div>
                </div>
                <div id="notifList">
                    <div class="notif-item"><div class="notif-row"><span class="notif-dot alert"></span><div><div class="notif-title">Battery #204 health dropped below 72%</div><div class="notif-time">2 min ago</div></div></div></div>
                    <div class="notif-item"><div class="notif-row"><span class="notif-dot warning"></span><div><div class="notif-title">Fleet Alpha requires maintenance</div><div class="notif-time">14 min ago</div></div></div></div>
                    <div class="notif-item"><div class="notif-row"><span class="notif-dot info"></span><div><div class="notif-title">AI model generated a new prediction</div><div class="notif-time">1 hr ago</div></div></div></div>
                    <div class="notif-item"><div class="notif-row"><span class="notif-dot success"></span><div><div class="notif-title">Manufacturer batch successfully verified</div><div class="notif-time">3 hr ago</div></div></div></div>
                    <div class="notif-item"><div class="notif-row"><span class="notif-dot info"></span><div><div class="notif-title">Firmware update available for EV-Series 7</div><div class="notif-time">Yesterday</div></div></div></div>
                </div>
            </div>
        </div>

        <!-- User Profile -->
        <div class="rel">
            <div class="avatar" onclick="toggleDrop('profileDrop')">SK</div>
            <div class="dropdown" id="profileDrop">
                <div class="dropdown-header"><span>Shruti K &nbsp;/&nbsp; Admin</span></div>
                <div class="profile-item" onclick="profileAction('Profile')"><span class="pi-icon">&#9679;</span> Profile</div>
                <div class="profile-item" onclick="profileAction('Settings')"><span class="pi-icon">&#9881;</span> Settings</div>
                <div class="profile-item" onclick="profileAction('Appearance')"><span class="pi-icon">&#9728;</span> Appearance</div>
                <div class="profile-item" style="color:#EF4444;" onclick="profileAction('Logout')"><span class="pi-icon" style="color:#EF4444;">&#10006;</span> Logout</div>
            </div>
        </div>
    </div>
</div>

<script>
// Theme system — communicates with parent page via postMessage
const DARK_ICON = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>`;
const MOON_ICON = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
let dark = (window.parent.localStorage.getItem('tc_theme') || 'dark') === 'dark';

function applyTheme() {
    const root = document.documentElement;
    if (dark) {
        root.removeAttribute('data-theme');
        document.getElementById('themeIcon').innerHTML = DARK_ICON;
    } else {
        root.setAttribute('data-theme','light');
        document.getElementById('themeIcon').innerHTML = MOON_ICON;
    }
    // Propagate to parent Streamlit page
    window.parent.document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
    window.parent.localStorage.setItem('tc_theme', dark ? 'dark' : 'light');
    
    // Broadcast to all other iframes
    const frames = window.parent.document.querySelectorAll('iframe');
    frames.forEach(f => {
        try {
            f.contentWindow.postMessage({ type: 'theme-change', theme: dark ? 'dark' : 'light' }, '*');
        } catch(e) {}
    });
}
function toggleTheme() { dark = !dark; applyTheme(); }
applyTheme();

// Dropdowns
function toggleDrop(id) {
    document.querySelectorAll('.dropdown').forEach(d => { if(d.id !== id) d.classList.remove('open'); });
    document.getElementById(id).classList.toggle('open');
}
document.addEventListener('click', function(e) {
    if (!e.target.closest('.rel')) document.querySelectorAll('.dropdown').forEach(d => d.classList.remove('open'));
});

// Notifications
function markAllRead() {
    document.querySelectorAll('.notif-dot').forEach(d => d.style.opacity = '0');
    document.getElementById('notifBadge').textContent = '0';
    showToast('INFO', 'All notifications marked as read');
}
// Clear All
function clearAll() {
    document.getElementById('notifList').innerHTML = '<div style="padding:16px;font-family:Space Grotesk,sans-serif;font-size:0.75rem;color:var(--muted);text-align:center;text-transform:uppercase;letter-spacing:.04em;">No notifications</div>';
    document.getElementById('notifBadge').textContent = '0';
    showToast('INFO', 'Notifications cleared');
}

// Custom event triggers
function showDeployToast() {
    window.parent.postMessage({ type: 'show-toast', label: 'DEPLOY', text: 'Production deployment initiated' }, '*');
}
function profileAction(action) {
    window.parent.postMessage({ type: 'show-toast', label: 'USER', text: action + ' settings accessed' }, '*');
}
function showToast(label, text) {
    window.parent.postMessage({ type: 'show-toast', label: label, text: text }, '*');
}

// Restore theme on load
window.addEventListener('load', function() {
    const stored = window.parent.localStorage.getItem('tc_theme');
    if (stored === 'light') { dark = false; applyTheme(); }
});
</script>
</body></html>
"""
components.html(NAVBAR_HTML, height=72, scrolling=False)
# =================================================================
# TELEMETRY TICKER BAR
# =================================================================
st.markdown("""
<div class="ticker-wrap">
  <div class="ticker-track">
    <span class="ticker-item"><span class="live">[ SYSTEM: ONLINE ]</span></span>
    <span class="ticker-item ticker-sep">|</span>
    <span class="ticker-item">LAST SYNC: <span class="live">0.04ms</span></span>
    <span class="ticker-item ticker-sep">|</span>
    <span class="ticker-item">ACTIVE CONNECTIONS: <span class="live">1,402</span></span>
    <span class="ticker-item ticker-sep">|</span>
    <span class="ticker-item">FLEET UPTIME: <span class="live">99.97%</span></span>
    <span class="ticker-item ticker-sep">|</span>
    <span class="ticker-item">ANOMALIES DETECTED: <span class="warn">03</span></span>
    <span class="ticker-item ticker-sep">|</span>
    <span class="ticker-item">BATTERY ASSETS: <span class="live">850</span></span>
    <span class="ticker-item ticker-sep">|</span>
    <span class="ticker-item">DATA PIPELINE: <span class="live">RUNNING</span></span>
    <span class="ticker-item ticker-sep">|</span>
    <span class="ticker-item">NODE LATENCY: <span class="live">12ms</span></span>
    <span class="ticker-item ticker-sep">|</span>
    <span class="ticker-item"><span class="live">[ SYSTEM: ONLINE ]</span></span>
    <span class="ticker-item ticker-sep">|</span>
    <span class="ticker-item">LAST SYNC: <span class="live">0.04ms</span></span>
    <span class="ticker-item ticker-sep">|</span>
    <span class="ticker-item">ACTIVE CONNECTIONS: <span class="live">1,402</span></span>
    <span class="ticker-item ticker-sep">|</span>
    <span class="ticker-item">FLEET UPTIME: <span class="live">99.97%</span></span>
    <span class="ticker-item ticker-sep">|</span>
    <span class="ticker-item">ANOMALIES DETECTED: <span class="warn">03</span></span>
    <span class="ticker-item ticker-sep">|</span>
    <span class="ticker-item">BATTERY ASSETS: <span class="live">850</span></span>
    <span class="ticker-item ticker-sep">|</span>
    <span class="ticker-item">DATA PIPELINE: <span class="live">RUNNING</span></span>
    <span class="ticker-item ticker-sep">|</span>
    <span class="ticker-item">NODE LATENCY: <span class="live">12ms</span></span>
    <span class="ticker-item ticker-sep">|</span>
  </div>
</div>
""", unsafe_allow_html=True)

# =================================================================
# QUICK ACTIONS BAR
# =================================================================
st.markdown("""
<div class="qa-bar">
    <a href="#" class="qa-btn primary">+ Add Vehicle</a>
    <a href="#" class="qa-btn">Import Dataset</a>
    <a href="#" class="qa-btn">Generate AI Report</a>
    <a href="#" class="qa-btn">Run Prediction</a>
    <a href="#" class="qa-btn">Export Analytics</a>
</div>
""", unsafe_allow_html=True)

# =================================================================
# HERO SECTION — Two-column split layout (preserved exactly)
# =================================================================
col_hero_left, col_hero_right = st.columns([7, 5], gap="large")

with col_hero_left:

    st.markdown("""
        <div class="hero-wordmark">TrustCharge Platform &nbsp;/&nbsp; v1.3.0</div>
        <div class="hero-headline">AI Battery<br><span>Intelligence</span><br>Platform</div>
        <div class="hero-subtitle">
            Predict battery failures, estimate remaining useful life,
            improve financing trust, and enable battery traceability
            using AI-driven electrochemical diagnostics.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="display: flex; gap: 14px; margin-bottom: 16px;">
            <a href="/fleet_dashboard" target="_self" class="btn btn-primary">Open Fleet Dashboard</a>
            <a href="/battery_scorecard" target="_self" class="btn btn-secondary">View Scorecard</a>
        </div>
    """, unsafe_allow_html=True)


    KPI_HTML = """
    <!DOCTYPE html><html><head><meta charset="utf-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Space+Grotesk:wght@600&display=swap');
        :root {
            --bg:       #080B0E;
            --card:     #0F1319;
            --border:   #1E252D;
            --accent:   #00D9B5;
            --text:     #EDEFF1;
            --muted:    #5A6E7F;
            --shadow:   rgba(0, 0, 0, 0.35);
            --radius-lg: 12px;
            --radius-md: 8px;
            --success:  #10B981;
        }
        [data-theme="light"] {
            --bg:       #EEF3F2;
            --card:     #FCFDFD;
            --border:   #D4E2DF;
            --accent:   #17BFA8;
            --text:     #26343C;
            --muted:    #7D8B90;
            --shadow:   rgba(35, 49, 58, 0.04);
            --success:  #36A972;
        }
        * { margin:0; padding:0; box-sizing:border-box; }
        body { background:var(--bg); display:flex; gap:16px; font-family:'JetBrains Mono',monospace; transition:background .2s; }
        .kc {
            flex:1; background:var(--card); border:1px solid var(--border); padding:16px;
            border-radius:var(--radius-lg); box-shadow:0 4px 12px var(--shadow);
            transition:all .2s cubic-bezier(0.4, 0, 0.2, 1); cursor:default;
        }
        .kc:hover { border-color:var(--accent); box-shadow:0 8px 20px var(--shadow); transform:translateY(-2px); }
        .kv { font-size:1.55rem; font-weight:700; color:var(--text); letter-spacing:-.02em; line-height:1.1; margin-bottom:4px; }
        .kv.teal { color:var(--accent); }
        .kl { font-size:0.58rem; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); font-weight:600; }
        .kt { font-size:0.58rem; color:var(--success); margin-top:4px; }
        svg.spark { display:block; margin-top:8px; }
    </style></head><body>
    <div class="kc">
        <div class="kv" id="k1">0</div>
        <div class="kl">Vehicles</div>
        <div class="kt">&#9650; +12 this month</div>
        <svg class="spark" width="100%" height="20" viewBox="0 0 80 20" preserveAspectRatio="none">
            <polyline points="0,16 16,12 32,14 48,6 64,10 80,4" fill="none" stroke="rgba(24, 191, 168, 0.35)" stroke-width="1.5"/>
        </svg>
    </div>
    <div class="kc">
        <div class="kv teal" id="k2">0%</div>
        <div class="kl">Avg Health</div>
        <div class="kt">&#9650; +1.2% vs last week</div>
        <svg class="spark" width="100%" height="20" viewBox="0 0 80 20" preserveAspectRatio="none">
            <polyline points="0,18 16,14 32,16 48,10 64,8 80,4" fill="none" stroke="rgba(24, 191, 168, 0.35)" stroke-width="1.5"/>
        </svg>
    </div>
    <div class="kc">
        <div class="kv" id="k3">0</div>
        <div class="kl">Manufacturers</div>
        <div class="kt">&#9650; +3 onboarded</div>
        <svg class="spark" width="100%" height="20" viewBox="0 0 80 20" preserveAspectRatio="none">
            <polyline points="0,14 16,16 32,10 48,12 64,6 80,8" fill="none" stroke="rgba(24, 191, 168, 0.35)" stroke-width="1.5"/>
        </svg>
    </div>
    <div class="kc">
        <div class="kv" id="k4">0</div>
        <div class="kl">Fleet Tenants</div>
        <div class="kt">&#9650; +2 new</div>
        <svg class="spark" width="100%" height="20" viewBox="0 0 80 20" preserveAspectRatio="none">
            <polyline points="0,18 16,10 32,14 48,8 64,12 80,6" fill="none" stroke="rgba(24, 191, 168, 0.35)" stroke-width="1.5"/>
        </svg>
    </div>
    <script>
    function countUp(id, target, suffix, duration) {
        const el = document.getElementById(id);
        const start = performance.now();
        function step(now) {
            const progress = Math.min((now - start) / duration, 1);
            const ease = 1 - Math.pow(1 - progress, 3);
            el.textContent = Math.round(target * ease) + suffix;
            if (progress < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
    }
    window.addEventListener('load', function() {
        countUp('k1', 850, '+', 1400);
        countUp('k2', 96, '%', 1600);
        countUp('k3', 35, '', 1200);
        countUp('k4', 15, '', 1000);
    });
    // Theme sync
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
    components.html(KPI_HTML, height=130, scrolling=False)

with col_hero_right:

    GAUGE_HTML = """
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
        .card {
            background:var(--bg); border:1px solid var(--border); padding:26px 22px;
            border-radius:var(--radius-lg); box-shadow:0 4px 12px var(--shadow);
            transition: background .2s, border-color .2s, box-shadow .2s;
        }
        .gauge-center { display:flex; justify-content:center; margin-bottom:22px; }
        .divider { border:none; border-top:1px solid var(--border); margin-bottom:0; }
        .gauge-row { display:flex; justify-content:space-between; align-items:center; padding:11px 0; border-bottom:1px solid var(--border); }
        .gauge-row:last-child { border-bottom:none; padding-bottom:0; }
        .gauge-lbl { font-family:'JetBrains Mono',monospace; font-size:.65rem; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); }
        .gauge-val { font-family:'JetBrains Mono',monospace; font-size:.82rem; font-weight:700; color:var(--text); }
        .gauge-tag {
            font-family:'JetBrains Mono',monospace; font-size:.62rem; font-weight:700;
            color:var(--accent); background:rgba(24, 191, 168, 0.08); border:1px solid rgba(24, 191, 168, 0.2);
            padding:2px 8px; letter-spacing:.05em; text-transform:uppercase; border-radius:12px;
        }
        .teal { color:var(--accent); }
    </style></head><body>
    <div class="card">
        <div class="gauge-center">
            <svg width="170" height="170" viewBox="0 0 180 180" xmlns="http://www.w3.org/2000/svg">
                <g stroke="var(--border)" stroke-width="1">
                    <line x1="90" y1="8" x2="90" y2="18" transform="rotate(0   90 90)"/>
                    <line x1="90" y1="8" x2="90" y2="18" transform="rotate(20  90 90)"/>
                    <line x1="90" y1="8" x2="90" y2="18" transform="rotate(40  90 90)"/>
                    <line x1="90" y1="8" x2="90" y2="18" transform="rotate(60  90 90)"/>
                    <line x1="90" y1="8" x2="90" y2="18" transform="rotate(80  90 90)"/>
                    <line x1="90" y1="8" x2="90" y2="18" transform="rotate(100 90 90)"/>
                    <line x1="90" y1="8" x2="90" y2="18" transform="rotate(120 90 90)"/>
                    <line x1="90" y1="8" x2="90" y2="18" transform="rotate(140 90 90)"/>
                    <line x1="90" y1="8" x2="90" y2="18" transform="rotate(160 90 90)"/>
                    <line x1="90" y1="8" x2="90" y2="18" transform="rotate(180 90 90)"/>
                    <line x1="90" y1="8" x2="90" y2="18" transform="rotate(200 90 90)"/>
                    <line x1="90" y1="8" x2="90" y2="18" transform="rotate(220 90 90)"/>
                    <line x1="90" y1="8" x2="90" y2="18" transform="rotate(240 90 90)"/>
                    <line x1="90" y1="8" x2="90" y2="18" transform="rotate(260 90 90)"/>
                    <line x1="90" y1="8" x2="90" y2="18" transform="rotate(280 90 90)"/>
                    <line x1="90" y1="8" x2="90" y2="18" transform="rotate(300 90 90)"/>
                    <line x1="90" y1="8" x2="90" y2="18" transform="rotate(320 90 90)"/>
                    <line x1="90" y1="8" x2="90" y2="18" transform="rotate(340 90 90)"/>
                </g>
                <circle cx="90" cy="90" r="64" fill="none" stroke="var(--gauge-empty)" stroke-width="10"/>
                <circle cx="90" cy="90" r="64" fill="none" stroke="var(--accent)" stroke-width="10"
                        stroke-dasharray="402.12" stroke-dashoffset="32.17" stroke-linecap="butt"
                        transform="rotate(-90 90 90)"/>
                <text x="90" y="83" font-family="Space Grotesk,sans-serif" font-size="30"
                      font-weight="700" fill="var(--text)" text-anchor="middle">92%</text>
                <text x="90" y="102" font-family="JetBrains Mono,monospace" font-size="8"
                      font-weight="600" fill="var(--accent)" text-anchor="middle" letter-spacing="0.12em">FLEET HEALTH</text>
            </svg>
        </div>
        <hr class="divider">
        <div class="gauge-row"><span class="gauge-lbl">Remaining Useful Life</span><span class="gauge-val">530 Days</span></div>
        <div class="gauge-row"><span class="gauge-lbl">Risk Level</span><span class="gauge-tag">LOW</span></div>
        <div class="gauge-row"><span class="gauge-lbl">Charging Behaviour</span><span class="gauge-val teal">Excellent</span></div>
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
    components.html(GAUGE_HTML, height=400, scrolling=False)



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
.mod-card { background-color: var(--card); border: 1px solid var(--border); }
.mod-corner { color: var(--muted); }
.mod-id { color: var(--muted); }
.mod-title-text { color: var(--text); }
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
            <span class="mod-corner">[+]</span>
            <div>
                <div class="mod-id">MOD.01 / FLEET</div>
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
            <span class="mod-corner">[+]</span>
            <div>
                <div class="mod-id">MOD.02 / SCORECARD</div>
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
            <span class="mod-corner">[+]</span>
            <div>
                <div class="mod-id">MOD.03 / TRACE</div>
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
# SECTION 3 — ASSET DIAGNOSTICS PIPELINE
# =================================================================
st.markdown("""
    <div class="section-label">Process Flow</div>
    <div class="section-title">Asset Diagnostics Pipeline</div>
""", unsafe_allow_html=True)

SEGMENT_HTML = """
<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@600;700&display=swap');

    :root {
        --bg:       #080B0E;
        --border:   #1E252D;
        --accent:   #00D9B5;
        --muted:    #5A6E7F;
    }
    [data-theme="light"] {
        --bg:       #EEF3F2;
        --border:   #D4E2DF;
        --accent:   #17BFA8;
        --muted:    #7D8B90;
    }
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background:var(--bg); padding:0 0 12px 0; transition:background .2s; }
    .seg-bar { display:flex; align-items:center; border-bottom:1px solid var(--border); width:100%; }
    .seg-tab { font-family:'JetBrains Mono',monospace; font-size:.68rem; font-weight:700;
               text-transform:uppercase; letter-spacing:.08em; color:var(--muted);
               padding:10px 22px; cursor:pointer; border:none; background:transparent;
               border-bottom:2px solid transparent; margin-bottom:-1px;
               transition:color .15s,border-color .15s; }
    .seg-tab:hover { color:#8B96A0; }
    .seg-tab.active { color:var(--accent); border-bottom:2px solid var(--accent); }
    .seg-sep { font-family:'JetBrains Mono',monospace; font-size:.6rem; color:var(--border); padding:0 4px; user-select:none; }
</style></head><body>
<div class="seg-bar">
    <button class="seg-tab active" onclick="setTab(this)">[ GLOBAL ]</button>
    <span class="seg-sep">|</span>
    <button class="seg-tab" onclick="setTab(this)">[ AT RISK ]</button>
    <span class="seg-sep">|</span>
    <button class="seg-tab" onclick="setTab(this)">[ OFFLINE ]</button>
    <span class="seg-sep">|</span>
    <button class="seg-tab" onclick="setTab(this)">[ CRITICAL ]</button>
</div>
<script>
function setTab(el) { document.querySelectorAll('.seg-tab').forEach(t=>t.classList.remove('active')); el.classList.add('active'); }
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
</script></body></html>
"""
components.html(SEGMENT_HTML, height=52, scrolling=False)

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
components.html(PIPELINE_HTML, height=180, scrolling=False)



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
        <div class="item"><div class="item-bar"></div><span class="item-time">10:35</span><div class="item-text">AI predicted battery degradation for VEH-204 <span class="item-badge b-ai">AI</span></div></div>
        <div class="item"><div class="item-bar"></div><span class="item-time">10:22</span><div class="item-text">Fleet Alpha synchronized — 142 assets updated <span class="item-badge b-ok">Sync</span></div></div>
        <div class="item"><div class="item-bar"></div><span class="item-time">09:58</span><div class="item-text">Manufacturer warranty verified: BATCH-007 <span class="item-badge b-ok">Verified</span></div></div>
        <div class="item"><div class="item-bar"></div><span class="item-time">09:30</span><div class="item-text">New dataset imported — 2,400 charge cycles <span class="item-badge b-ok">Import</span></div></div>
        <div class="item"><div class="item-bar"></div><span class="item-time">08:45</span><div class="item-text">Fleet Beta: 3 batteries flagged for maintenance <span class="item-badge b-warn">Alert</span></div></div>
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
    components.html(ACTIVITY_HTML, height=280, scrolling=False)

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
    components.html(HEALTH_HTML, height=175, scrolling=False)

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
        <div class="m-row"><div><div class="m-label">VEH-204 — Battery Pack A</div><div class="m-sub">Thermal inspection overdue</div></div><span class="m-date">Jul 18</span></div>
        <div class="m-row"><div><div class="m-label">Fleet Beta — Sector 3</div><div class="m-sub">Cycle limit approaching 500</div></div><span class="m-date">Jul 22</span></div>
        <div class="m-row"><div><div class="m-label">VEH-512 — BMS Firmware</div><div class="m-sub">Scheduled patch v4.2.1</div></div><span class="m-date">Jul 30</span></div>
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
    components.html(MAINT_HTML, height=158, scrolling=False)




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
        <tbody>
            <tr><td class="rank">01</td><td style="font-family:'Space Grotesk',sans-serif; font-weight:600;">TrustCharge Energy</td><td><span class="score">98.4</span><span class="bar-wrap"><span class="bar-fill" style="width:98%"></span></span></td><td>94.2%</td><td>99.1%</td><td>96.8%</td></tr>
            <tr><td class="rank">02</td><td style="font-family:'Space Grotesk',sans-serif; font-weight:600;">VoltCore Systems</td><td><span class="score">94.1</span><span class="bar-wrap"><span class="bar-fill" style="width:94%"></span></span></td><td>91.7%</td><td>97.3%</td><td>93.5%</td></tr>
            <tr><td class="rank">03</td><td style="font-family:'Space Grotesk',sans-serif; font-weight:600;">ElectraPack Ltd.</td><td><span class="score">89.7</span><span class="bar-wrap"><span class="bar-fill" style="width:90%"></span></span></td><td>88.5%</td><td>95.0%</td><td>90.2%</td></tr>
            <tr><td class="rank">04</td><td style="font-family:'Space Grotesk',sans-serif; font-weight:600;">NovaBattery Corp</td><td><span class="score">82.3</span><span class="bar-wrap"><span class="bar-fill" style="width:82%"></span></span></td><td>84.1%</td><td>91.4%</td><td>85.6%</td></tr>
            <tr><td class="rank">05</td><td style="font-family:'Space Grotesk',sans-serif; font-weight:600;">IonBridge Intl.</td><td><span class="score">76.8</span><span class="bar-wrap"><span class="bar-fill" style="width:77%"></span></span></td><td>79.3%</td><td>88.2%</td><td>79.1%</td></tr>
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
components.html(LEADER_HTML, height=240, scrolling=False)



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
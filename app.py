import streamlit as st
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

# -------------------------------------------------
# CSS — NEO-BRUTALIST ENGINEERING CONSOLE THEME
# -------------------------------------------------
st.markdown("""
<style>
    /* ── Fonts: Space Grotesk for structural headers, JetBrains Mono for telemetry ── */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background-color: #050505 !important;
        color: #EDEFF1 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* ── Layout: wide, top-padded to clear Streamlit header ── */
    div.block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 1350px;
        margin: 0 auto;
    }

    [data-testid="stHeader"] {
        background-color: rgba(5, 5, 5, 0.92) !important;
        border-bottom: 1px solid #1A2025 !important;
        backdrop-filter: blur(8px);
    }

    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid #1A2025 !important;
    }

    /* ── CARDS — harsh right angles, block shadow, no blur ── */
    .card {
        background-color: #0D1117;
        border: 1px solid #1A2025;
        border-radius: 0px;
        padding: 24px;
        box-shadow: 4px 4px 0px #000000;
        transition: box-shadow 0.12s ease, transform 0.12s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .card:hover {
        border-color: #00D9B5;
        box-shadow: 2px 2px 0px #000000;
        transform: translate(1px, 1px);
    }

    /* ── KPI CARDS — monospace values, square corners ── */
    .kpi-card {
        background-color: #0D1117;
        border: 1px solid #1A2025;
        border-radius: 0px;
        padding: 18px 16px;
        box-shadow: 3px 3px 0px #000000;
        height: 100%;
    }

    .kpi-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.65rem;
        font-weight: 700;
        color: #EDEFF1;
        line-height: 1.1;
        margin-bottom: 6px;
        letter-spacing: -0.02em;
    }

    .kpi-lbl {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #4A5568;
        font-weight: 600;
    }

    /* ── BUTTONS — tactile block toggle, compresses on press ── */
    .btn {
        display: inline-block;
        padding: 12px 28px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        font-weight: 700;
        text-decoration: none !important;
        border-radius: 0px;
        transition: all 0.1s ease;
        text-align: center;
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    .btn-primary {
        background-color: #00D9B5;
        color: #050505 !important;
        border: 1px solid #00D9B5;
        box-shadow: 4px 4px 0px #00877A;
    }

    .btn-primary:hover {
        box-shadow: 2px 2px 0px #00877A;
        transform: translate(2px, 2px);
        background-color: #00c4a3;
    }

    .btn-primary:active {
        box-shadow: 0px 0px 0px #00877A;
        transform: translate(4px, 4px);
    }

    .btn-secondary {
        background-color: transparent;
        border: 1px solid #1A2025;
        color: #4A5568 !important;
        box-shadow: 3px 3px 0px #000000;
    }

    .btn-secondary:hover {
        border-color: #00D9B5;
        color: #00D9B5 !important;
        box-shadow: 1px 1px 0px #000000;
        transform: translate(1px, 1px);
    }

    .btn-full {
        width: 100%;
        box-sizing: border-box;
    }

    /* ── HERO TEXT — structural headers ── */
    .hero-wordmark {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        color: #00D9B5;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .hero-wordmark::before {
        content: '';
        display: inline-block;
        width: 18px;
        height: 1px;
        background-color: #00D9B5;
    }

    .hero-headline {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        line-height: 1.05;
        letter-spacing: -0.03em;
        color: #EDEFF1;
        margin-bottom: 24px;
    }

    .hero-headline span {
        color: #00D9B5;
    }

    .hero-subtitle {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #4A5568;
        margin-bottom: 28px;
        max-width: 620px;
        font-weight: 400;
    }

    /* ── SECTION LABELS ── */
    .section-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        color: #4A5568;
        margin-top: 52px;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .section-label::after {
        content: '';
        display: block;
        flex: 1;
        height: 1px;
        background-color: #1A2025;
    }

    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        margin-top: 8px;
        margin-bottom: 24px;
        letter-spacing: -0.02em;
        color: #EDEFF1;
    }

    /* ── TIMELINE — pipeline steps ── */
    .timeline-container {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        background-color: #0D1117;
        border: 1px solid #1A2025;
        border-radius: 0px;
        padding: 32px 28px;
        margin-bottom: 24px;
        box-shadow: 4px 4px 0px #000000;
        flex-wrap: wrap;
        gap: 0;
    }

    .timeline-step {
        flex: 1;
        min-width: 160px;
        text-align: center;
        padding: 0 12px;
        position: relative;
    }

    .timeline-step:not(:last-child)::after {
        content: '';
        position: absolute;
        right: 0;
        top: 18px;
        width: 1px;
        height: 40px;
        background-color: #1A2025;
    }

    .step-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        color: #00D9B5;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 10px;
        display: block;
    }

    .step-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.88rem;
        font-weight: 600;
        color: #EDEFF1;
        margin-bottom: 6px;
    }

    .step-desc {
        font-size: 0.75rem;
        color: #4A5568;
        line-height: 1.4;
    }

    /* ── MODULE CARD HEADINGS ── */
    .mod-icon {
        margin-bottom: 14px;
        line-height: 1;
    }

    .mod-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        font-weight: 700;
        color: #EDEFF1;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }

    .mod-desc {
        font-size: 0.82rem;
        color: #4A5568;
        line-height: 1.5;
        margin-bottom: 0;
    }

    /* ── GAUGE CARD data rows ── */
    .gauge-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid #1A2025;
    }

    .gauge-row:last-child {
        border-bottom: none;
        padding-bottom: 0;
    }

    .gauge-lbl {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #4A5568;
    }

    .gauge-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        font-weight: 700;
        color: #EDEFF1;
    }

    .gauge-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem;
        font-weight: 700;
        color: #00D9B5;
        background-color: rgba(0, 217, 181, 0.06);
        border: 1px solid rgba(0, 217, 181, 0.25);
        border-radius: 0px;
        padding: 2px 8px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    /* ── GLOBAL OVERRIDES ── */
    h1, h2, h3, h4 { color: #EDEFF1 !important; }
    hr { border-color: #1A2025 !important; }

    /* ── FOOTER ── */
    .footer {
        border-top: 1px solid #1A2025;
        padding: 24px 0;
        margin-top: 64px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        color: #2A333B;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# =================================================================
# HERO SECTION — Two-column split layout
# =================================================================
col_hero_left, col_hero_right = st.columns([7, 5], gap="large")

with col_hero_left:

    # ── Wordmark ──
    st.markdown("""
        <div class="hero-wordmark">TrustCharge Platform &nbsp;/&nbsp; v1.3.0</div>
        <div class="hero-headline">AI Battery<br><span>Intelligence</span><br>Platform</div>
        <div class="hero-subtitle">
            Predict battery failures, estimate remaining useful life,
            improve financing trust, and enable battery traceability
            using AI-driven electrochemical diagnostics.
        </div>
    """, unsafe_allow_html=True)

    # ── Action Buttons ──
    st.markdown("""
        <div style="display: flex; gap: 14px; margin-bottom: 40px;">
            <a href="/fleet_dashboard" target="_self" class="btn btn-primary">
                Open Fleet Dashboard
            </a>
            <a href="/battery_scorecard" target="_self" class="btn btn-secondary">
                View Scorecard
            </a>
        </div>
    """, unsafe_allow_html=True)

    # ── KPI Stats Grid ──
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

    with kpi_col1:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-val">850+</div>
                <div class="kpi-lbl">Vehicles</div>
            </div>
        """, unsafe_allow_html=True)

    with kpi_col2:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-val" style="color: #00D9B5;">96%</div>
                <div class="kpi-lbl">Avg Health</div>
            </div>
        """, unsafe_allow_html=True)

    with kpi_col3:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-val">35</div>
                <div class="kpi-lbl">Manufacturers</div>
            </div>
        """, unsafe_allow_html=True)

    with kpi_col4:
        st.markdown("""
            <div class="kpi-card">
                <div class="kpi-val">15</div>
                <div class="kpi-lbl">Fleet Tenants</div>
            </div>
        """, unsafe_allow_html=True)

with col_hero_right:

    # ── Battery Health Gauge Card ──
    # st.components.v1.html() renders a proper browser iframe — the SVG is parsed
    # directly by the DOM, bypassing Streamlit's Markdown processor entirely.
    # This prevents HTML comments or SVG tags from appearing as raw text.
    import streamlit.components.v1 as components

    GAUGE_HTML = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body {
            background-color: #0D1117;
            color: #EDEFF1;
            font-family: 'JetBrains Mono', monospace;
        }
        .card {
            background-color: #0D1117;
            border: 1px solid #1A2025;
            border-radius: 0px;
            padding: 26px 22px;
            box-shadow: 4px 4px 0px #000000;
        }
        .gauge-center {
            display: flex;
            justify-content: center;
            margin-bottom: 22px;
        }
        .divider {
            border: none;
            border-top: 1px solid #1A2025;
            margin-bottom: 0;
        }
        .gauge-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 11px 0;
            border-bottom: 1px solid #1A2025;
        }
        .gauge-row:last-child { border-bottom: none; padding-bottom: 0; }
        .gauge-lbl {
            font-size: 0.6rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: #4A5568;
        }
        .gauge-val {
            font-size: 0.82rem;
            font-weight: 700;
            color: #EDEFF1;
        }
        .gauge-tag {
            font-size: 0.6rem;
            font-weight: 700;
            color: #00D9B5;
            background-color: rgba(0, 217, 181, 0.06);
            border: 1px solid rgba(0, 217, 181, 0.25);
            border-radius: 0px;
            padding: 2px 8px;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }
        .teal { color: #00D9B5; }
    </style>
    </head>
    <body>
    <div class="card">

        <div class="gauge-center">
            <svg width="170" height="170" viewBox="0 0 180 180" xmlns="http://www.w3.org/2000/svg">
                <g stroke="#1A2025" stroke-width="1">
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
                <circle cx="90" cy="90" r="64" fill="none" stroke="#1A2025" stroke-width="10"/>
                <circle cx="90" cy="90" r="64" fill="none" stroke="#00D9B5" stroke-width="10"
                        stroke-dasharray="402.12" stroke-dashoffset="32.17"
                        stroke-linecap="butt"
                        transform="rotate(-90 90 90)"/>
                <text x="90" y="83" font-family="JetBrains Mono,monospace" font-size="30"
                      font-weight="700" fill="#EDEFF1" text-anchor="middle">92%</text>
                <text x="90" y="102" font-family="JetBrains Mono,monospace" font-size="8"
                      font-weight="600" fill="#00D9B5" text-anchor="middle" letter-spacing="0.18em">FLEET HEALTH</text>
            </svg>
        </div>

        <hr class="divider">

        <div class="gauge-row">
            <span class="gauge-lbl">Remaining Useful Life</span>
            <span class="gauge-val">530 Days</span>
        </div>
        <div class="gauge-row">
            <span class="gauge-lbl">Risk Level</span>
            <span class="gauge-tag">LOW</span>
        </div>
        <div class="gauge-row">
            <span class="gauge-lbl">Charging Behaviour</span>
            <span class="gauge-val teal">Excellent</span>
        </div>

    </div>
    </body>
    </html>
    """
    components.html(GAUGE_HTML, height=400, scrolling=False)

# =================================================================
# SECTION 2 — PLATFORM CORE MODULES
# =================================================================
st.markdown("""
    <div class="section-label">System Modules</div>
    <div class="section-title">Platform Core Modules</div>
""", unsafe_allow_html=True)

col_mod1, col_mod2, col_mod3 = st.columns(3)

# SVG icons: Lucide-style thin-stroke (1.5px), no emojis
ICON_FLEET = """<svg width="28" height="28" viewBox="0 0 24 24" fill="none"
    stroke="#00D9B5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="3" y="11" width="18" height="11" rx="0"/>
    <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
    <circle cx="12" cy="17" r="1"/>
</svg>"""

ICON_BATTERY = """<svg width="28" height="28" viewBox="0 0 24 24" fill="none"
    stroke="#00D9B5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="2" y="7" width="16" height="10" rx="0"/>
    <path d="M22 11v2"/>
    <path d="M6 11h4"/>
    <path d="M6 15h8"/>
</svg>"""

ICON_MFG = """<svg width="28" height="28" viewBox="0 0 24 24" fill="none"
    stroke="#00D9B5" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M2 20h20"/>
    <path d="M2 20V10l6-4v4l6-4v4l6-4v14"/>
    <path d="M9 20v-5h6v5"/>
</svg>"""

# ── Module card HTML is rendered via st.markdown with f-string SVG injection.
# Buttons use a <style> block injected ahead of time to get :hover behaviour.
st.markdown("""
<style>
.mod-card {
    background-color: #0D1117;
    border: 1px solid #333333;
    border-radius: 0px;
    padding: 22px 20px 18px 20px;
    height: 260px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    box-shadow: 4px 4px 0px rgba(0,217,181,0.18);
    transition: box-shadow 0.1s ease, transform 0.1s ease;
}
.mod-card:hover {
    border-color: #00D9B5;
    box-shadow: 2px 2px 0px rgba(0,217,181,0.35);
    transform: translate(1px, 1px);
}
.mod-corner {
    position: absolute;
    top: 10px;
    right: 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: #2A333B;
    letter-spacing: 0.08em;
}
.mod-id {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: #2A333B;
    letter-spacing: 0.12em;
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
    background-color: #00D9B5;
    box-shadow: 0 0 6px #00D9B5;
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
    color: #EDEFF1;
    text-transform: uppercase;
    letter-spacing: 0.02em;
}
.mod-desc-text {
    font-size: 0.80rem;
    color: #5A6475;
    line-height: 1.5;
    margin-bottom: 0;
}
.mod-btn {
    display: block;
    width: 100%;
    box-sizing: border-box;
    padding: 9px 16px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    text-align: center;
    text-decoration: none !important;
    border: 1px solid #444444;
    background-color: transparent;
    color: #8B96A0 !important;
    border-radius: 0px;
    box-shadow: 2px 2px 0px #000000;
    transition: all 0.1s ease;
    margin-top: 14px;
}
.mod-btn:hover {
    background-color: #00D9B5;
    border-color: #00D9B5;
    color: #050505 !important;
    box-shadow: 0px 0px 0px #000000;
    transform: translate(2px, 2px);
}
</style>
""", unsafe_allow_html=True)

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
                <div style="margin-bottom:14px;">{ICON_FLEET}</div>
                <p class="mod-desc-text">Monitor EV fleet telemetry, battery status distribution, and active risk anomalies.</p>
            </div>
            <a href="/fleet_dashboard" target="_self" class="mod-btn">Open Fleet Portal</a>
        </div>
    """, unsafe_allow_html=True)

with col_mod2:
    st.markdown(f"""
        <div class="mod-card">
            <span class="mod-corner">[+]</span>
            <div>
                <div class="mod-id">MOD.02 / SCORECARD</div>
                <div class="mod-title-row">
                    <span class="status-dot"></span>
                    <span class="mod-title-text">Battery Scorecard</span>
                </div>
                <div style="margin-bottom:14px;">{ICON_BATTERY}</div>
                <p class="mod-desc-text">Inspect individual asset diagnostics, SoH scores, thermal stats, and maintenance logs.</p>
            </div>
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
                <div style="margin-bottom:14px;">{ICON_MFG}</div>
                <p class="mod-desc-text">Trace chemistry configurations, verify batch quality profiles, and manage warranty data.</p>
            </div>
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

PIPELINE_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;600;700&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body {
        background-color: #050505;
        color: #EDEFF1;
        font-family: 'Space Grotesk', sans-serif;
    }
    .pipeline {
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        background-color: #0D1117;
        border: 1px solid #333333;
        border-radius: 0px;
        box-shadow: 4px 4px 0px #000000;
        padding: 28px 0;
        width: 100%;
    }
    .step {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 0 14px;
    }
    .step-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 700;
        color: #4A5568;
        letter-spacing: 0.08em;
        margin-bottom: 10px;
        display: block;
    }
    .step-num.active   { color: #00D9B5; }
    .step-title        { font-family: 'Space Grotesk', sans-serif; font-size: 0.82rem; font-weight: 700; color: #6B7280; margin-bottom: 6px; }
    .step-title.active { color: #00D9B5; }
    .step-desc         { font-size: 0.72rem; color: #4A5568; line-height: 1.4; }
    .step-desc.active  { color: #6B7280; }
    /* Arrow connector column */
    .arrow-col {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        padding-top: 6px;
        width: 48px;
        flex-shrink: 0;
        gap: 2px;
    }
    .arrow-dash {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.55rem;
        color: #2A333B;
        letter-spacing: -0.05em;
        line-height: 1;
        white-space: nowrap;
    }
    .arrow-head {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.6rem;
        color: #333333;
        line-height: 1;
    }
</style>
</head>
<body>
<div class="pipeline">

    <div class="step">
        <span class="step-num">[ 01 ]</span>
        <div class="step-title">Collect Battery Data</div>
        <div class="step-desc">Raw telemetry ingestion: cell voltage, pack temperature, depth of discharge.</div>
    </div>

    <div class="arrow-col">
        <span class="arrow-dash">- - -</span>
        <span class="arrow-head">&gt;&gt;&gt;</span>
        <span class="arrow-dash">- - -</span>
    </div>

    <div class="step">
        <span class="step-num">[ 02 ]</span>
        <div class="step-title">AI Health Analysis</div>
        <div class="step-desc">Electrochemical decay modeling and capacity wear kinetics processing.</div>
    </div>

    <div class="arrow-col">
        <span class="arrow-dash">- - -</span>
        <span class="arrow-head">&gt;&gt;&gt;</span>
        <span class="arrow-dash">- - -</span>
    </div>

    <div class="step">
        <span class="step-num active">[ 03 ]</span>
        <div class="step-title active">Predict Remaining Life</div>
        <div class="step-desc active">Remaining useful life (RUL) projections via degradation regression.</div>
    </div>

    <div class="arrow-col">
        <span class="arrow-dash">- - -</span>
        <span class="arrow-head">&gt;&gt;&gt;</span>
        <span class="arrow-dash">- - -</span>
    </div>

    <div class="step">
        <span class="step-num">[ 04 ]</span>
        <div class="step-title">Fleet Intelligence</div>
        <div class="step-desc">Aggregate asset metrics and generate operational risk band classifications.</div>
    </div>

    <div class="arrow-col">
        <span class="arrow-dash">- - -</span>
        <span class="arrow-head">&gt;&gt;&gt;</span>
        <span class="arrow-dash">- - -</span>
    </div>

    <div class="step">
        <span class="step-num">[ 05 ]</span>
        <div class="step-title">Financing Decision</div>
        <div class="step-desc">Data-backed secondary market valuation and warranty reserve modelling.</div>
    </div>

</div>
</body>
</html>
"""
components.html(PIPELINE_HTML, height=180, scrolling=False)

# =================================================================
# FOOTER
# =================================================================
current_year = datetime.now().year
st.markdown(f"""
<div class="footer">
    TrustCharge &nbsp;/&nbsp; National Level Hackathon &nbsp;&nbsp;|&nbsp;&nbsp;
    Neo-Brutalist Build v1.3.0 &nbsp;&nbsp;|&nbsp;&nbsp;
    &copy; {current_year} Team TrustCharge
</div>
""", unsafe_allow_html=True)
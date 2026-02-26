"""
Hidayah AI — Main Application Entry Point
30-Day Ramadan Research Companion

Assembles all UI components, injects Tailwind CSS, and manages the application flow.
Run with: streamlit run app.py
"""

import streamlit as st


st.set_page_config(
    page_title="Hidayah AI — Ramadan Research Companion",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded",
)


from utils.state import init_session_state
from utils.quran_api import fetch_juz_combined, get_surah_info_for_juz
from utils.config import GOLD, MIDNIGHT_BLUE, BG_DARK, JUZ_DATA, AUDIO_MODES
from ui.sidebar import render_sidebar
from ui.header import render_header
from ui.quran_display import render_quran_view
from ui.audio_player import render_audio_player
from ui.chat_panel import render_chat_panel


# ── Initialize Session State ─────────────────────────────────
init_session_state()

# ── Inject Global CSS & Fonts (Tailwind + Custom) ────────────
st.markdown(
    """
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <style>
        /* ── Design Tokens & Variables ────────────────────── */
        :root {{
            --gold: #D4AF37;
            --gold-light: #F3E5AB;
            --bg-dark: #0F172A;
            --glass-bg: rgba(26, 42, 64, 0.7);
            --glass-border: rgba(148, 163, 184, 0.15);
            --sharp-radius: 2px;
            --premium-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        }}

        /* ── Global Reset & Theme ─────────────────────────── */
        [data-testid="stAppViewContainer"] {{
            background-color: var(--bg-dark) !important;
            background-image: 
                radial-gradient(circle at 50% 0%, rgba(26, 42, 64, 1) 0%, rgba(15, 23, 42, 1) 100%),
                url('https://www.transparenttextures.com/patterns/noise-lines.png') !important;
            color: #e2e8f0 !important;
            font-family: 'Inter', sans-serif !important;
        }}

        /* ── Hide Streamlit Default Chrome ─────────────────── */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        .stDeployButton {{display: none;}}
        [data-testid="stDecoration"] {{display: none !important;}}

        /* Transparent top header */
        [data-testid="stHeader"] {{
            background: transparent !important;
        }}

        /* ── Sidebar Toggle (hamburger) ─── */
        [data-testid="collapsedControl"] {{
            visibility: visible !important;
            display: flex !important;
            position: fixed !important;
            top: 0.75rem !important;
            left: 0.75rem !important;
            z-index: 999999 !important;
        }}
        [data-testid="collapsedControl"] button {{
            background: rgba(26, 42, 64, 0.9) !important;
            border: 1px solid rgba(212, 175, 55, 0.4) !important;
            color: var(--gold) !important;
            border-radius: var(--sharp-radius) !important;
            width: 2.5rem !important;
            height: 2.5rem !important;
            padding: 0 !important;
            backdrop-filter: blur(12px) !important;
            box-shadow: var(--premium-shadow) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}
        [data-testid="collapsedControl"] button:hover {{
            transform: translateY(-1px);
            background: rgba(212, 175, 55, 0.1) !important;
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.2) !important;
        }}

        /* ── Sidebar Close (X) button ─────── */
        [data-testid="stSidebarCollapse"] {{
            position: absolute !important;
            top: 0.75rem !important;
            right: 0.75rem !important;
            z-index: 10 !important;
        }}
        [data-testid="stSidebarCollapse"] button {{
            background: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(212, 175, 55, 0.2) !important;
            color: var(--gold) !important;
            border-radius: var(--sharp-radius) !important;
            transition: all 0.2s ease !important;
        }}

        /* ── Main Container Padding ───────────────────────── */
        .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 95rem !important;
        }}

        /* ── Sidebar Styling ───────────────────────────────── */
        [data-testid="stSidebar"] {{
            background: rgba(15, 23, 42, 0.98) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(148, 163, 184, 0.05);
        }}
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
            padding-top: 3.5rem !important;
        }}

        /* ── Premium Glass Panels ─────────────────────────── */
        .glass-panel {{
            background: var(--glass-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: var(--sharp-radius);
            box-shadow: var(--premium-shadow);
            position: relative;
            overflow: hidden;
        }}
        .glass-panel::before {{
            content: "";
            position: absolute;
            inset: 0;
            background: url('https://www.transparenttextures.com/patterns/noise-lines.png');
            opacity: 0.05;
            pointer-events: none;
        }}

        /* ── Responsive Column Control (CRITICAL) ─────────── */
        @media (max-width: 992px) {{
            /* On tablet/mobile, force columns to stack */
            [data-testid="stHorizontalBlock"] {{
                flex-direction: column !important;
                gap: 2rem !important;
            }}
            [data-testid="stColumn"] {{
                width: 100% !important;
            }}
            
            /* Target the Chat Panel Column directly via its unique content */
            [data-testid="stColumn"]:has(.st-key-btn_close_scholar_panel),
            [data-testid="stColumn"]:has([data-testid="stChatInput"]) {{
                position: fixed !important;
                inset: 0 !important;
                width: 100% !important;
                height: 100% !important;
                z-index: 100000 !important;
                background: #0F172A !important;
                padding: 1rem !important;
                overflow-y: auto !important;
                display: block !important;
                animation: slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1) forwards !important;
            }}
        }}

        @keyframes slideUp {{
            from {{ transform: translateY(100%); }}
            to {{ transform: translateY(0); }}
        }}

        /* ── Buttons, Inputs & Micro-interactions ─────────── */
        .stButton > button {{
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid var(--glass-border) !important;
            color: #cbd5e1 !important;
            border-radius: var(--sharp-radius) !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            padding: 0.6rem 1rem !important;
            transition: all 0.3s ease !important;
        }}
        .stButton > button:hover {{
            border-color: var(--gold) !important;
            background: rgba(212, 175, 55, 0.05) !important;
            color: var(--gold) !important;
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.1) !important;
        }}

        /* High Visibility Mode for active verse */
        .active-verse {{
            border-left: 4px solid var(--gold) !important;
            background: rgba(212, 175, 55, 0.05) !important;
        }}

        /* ── Scrollbar (Premium Gold Thin) ────────────────── */
        ::-webkit-scrollbar {{ width: 5px; height: 5px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
        ::-webkit-scrollbar-thumb {{ background: var(--gold); border-radius: 0; }}
        
        /* ── Animations ───────────────────────────────────── */
        @keyframes fadeInSlide {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .animate-reveal {{
            animation: fadeInSlide 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Sidebar ───────────────────────────────────────────────────
render_sidebar()


# ── Fetch Quran Data ──────────────────────────────────────────
current_juz = st.session_state.get("current_juz", 1)

# Fetch data if not already loaded or juz changed
if not st.session_state.ayahs or st.session_state.get("_loaded_juz") != current_juz:
    with st.spinner(f"Loading Juz {current_juz} — {JUZ_DATA.get(current_juz, {}).get('name', '')}..."):
        ayahs = fetch_juz_combined(current_juz)
        st.session_state.ayahs = ayahs
        st.session_state._loaded_juz = current_juz

ayahs = st.session_state.ayahs
current_ayah_index = st.session_state.get("current_ayah_index", 0)


# ── Main Layout: Quran View (left) + Chat Panel (right) ──────
show_chat = st.session_state.get("show_scholar_agent", False)

if show_chat:
    col_main, col_chat = st.columns([3, 2])
else:
    col_main = st.container()
    col_chat = None

with col_main:
    # Header
    render_header(ayahs, current_ayah_index)

    selected_mode = st.selectbox(
        "Choose Audio Language",
        AUDIO_MODES,
        index=AUDIO_MODES.index(st.session_state.get("audio_mode", AUDIO_MODES[0])),
        key="audio_mode_top_select",
    )
    if selected_mode != st.session_state.get("audio_mode"):
        st.session_state.audio_mode = selected_mode
        st.rerun()

    # Audio player (top)
    render_audio_player(ayahs, current_ayah_index)

    # Quran dual-pane display
    render_quran_view(ayahs, current_ayah_index)

if col_chat is not None:
    with col_chat:
        # Scholar Agent chat panel
        render_chat_panel(ayahs)

# ── Global Scroll Lock for Mobile ────────────────────────────
if show_chat:
    st.html(
        """
        <style>
        @media (max-width: 992px) {
            /* Lock the background app view when chat is open on mobile */
            [data-testid="stAppViewContainer"] {
                overflow: hidden !important;
                height: 100vh !important;
                position: fixed !important;
                width: 100% !important;
            }
        }
        </style>
        """
    )

# ── Sync URL Parameters (Smart Resume Persistence) ────────────
# Pushing these to the URL bar allows browsers to intrinsically remember 
# the last read location via their history/autocomplete mechanisms without 
# requiring a dedicated backend database.
st.query_params["juz"] = st.session_state.get("current_juz", 1)
st.query_params["ayah"] = st.session_state.get("current_ayah_index", 0)
st.query_params["mode"] = st.session_state.get("audio_mode", "Arabic (Mishary Rashid)")

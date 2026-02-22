"""
Hidayah AI — Main Application Entry Point
30-Day Ramadan Research Companion

Assembles all UI components, injects Tailwind CSS, and manages the application flow.
Run with: streamlit run app.py
"""

import streamlit as st

# ── Page Config (MUST be first Streamlit call) ────────────────
st.set_page_config(
    page_title="Hidayah AI — Ramadan Research Companion",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Imports ───────────────────────────────────────────────────
from utils.state import init_session_state
from utils.quran_api import fetch_juz_combined, get_surah_info_for_juz
from utils.config import GOLD, MIDNIGHT_BLUE, BG_DARK, JUZ_DATA
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
        /* ── Global Reset & Theme ─────────────────────────── */
        .stApp {{
            background-color: {BG_DARK};
            color: #e2e8f0;
            font-family: 'Inter', sans-serif;
        }}

        /* ── Hide Streamlit Default Chrome ─────────────────── */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        .stDeployButton {{display: none;}}
        [data-testid="stDecoration"] {{display: none !important;}}

        /* Transparent top header — keeps sidebar toggle visible */
        [data-testid="stHeader"] {{
            background: transparent !important;
        }}

        /* ── Sidebar Toggle (hamburger) when sidebar is collapsed ─── */
        [data-testid="collapsedControl"] {{
            visibility: visible !important;
            display: flex !important;
            position: fixed !important;
            top: 0.6rem !important;
            left: 0.6rem !important;
            z-index: 999999 !important;
        }}
        [data-testid="collapsedControl"] button {{
            background: rgba(26, 42, 64, 0.95) !important;
            border: 1px solid rgba(212, 175, 55, 0.4) !important;
            color: {GOLD} !important;
            border-radius: 0.6rem !important;
            width: 2.4rem !important;
            height: 2.4rem !important;
            padding: 0 !important;
            backdrop-filter: blur(12px) !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.25s ease !important;
        }}
        [data-testid="collapsedControl"] button:hover {{
            background: rgba(212, 175, 55, 0.15) !important;
            border-color: {GOLD} !important;
            box-shadow: 0 2px 16px rgba(212, 175, 55, 0.25) !important;
        }}
        [data-testid="collapsedControl"] button svg {{
            stroke: {GOLD} !important;
            width: 1.2rem !important;
            height: 1.2rem !important;
        }}

        /* ── Sidebar Close (X) button inside the sidebar ─────── */
        [data-testid="stSidebarCollapse"] {{
            position: absolute !important;
            top: 0.5rem !important;
            right: 0.5rem !important;
            z-index: 10 !important;
        }}
        [data-testid="stSidebarCollapse"] button {{
            background: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(212, 175, 55, 0.25) !important;
            color: {GOLD} !important;
            border-radius: 0.5rem !important;
            width: 2rem !important;
            height: 2rem !important;
            padding: 0 !important;
            transition: all 0.25s ease !important;
        }}
        [data-testid="stSidebarCollapse"] button:hover {{
            background: rgba(212, 175, 55, 0.15) !important;
            border-color: {GOLD} !important;
        }}
        [data-testid="stSidebarCollapse"] button svg {{
            stroke: {GOLD} !important;
            width: 1rem !important;
            height: 1rem !important;
        }}

        /* Reduce top padding */
        .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 0 !important;
        }}

        /* ── Sidebar Styling ───────────────────────────────── */
        [data-testid="stSidebar"] {{
            background: rgba(26, 42, 64, 0.95) !important;
            backdrop-filter: blur(12px);
            border-right: 1px solid rgba(148, 163, 184, 0.1);
            transition: margin-left 0.3s ease, visibility 0.3s ease !important;
        }}

        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
            padding-top: 2.5rem !important;
        }}

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
            color: #cbd5e1;
        }}

        /* Sidebar buttons */
        [data-testid="stSidebar"] button {{
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(148, 163, 184, 0.1) !important;
            color: #94a3b8 !important;
            border-radius: 0.75rem !important;
            text-align: left !important;
            padding: 0.5rem 0.75rem !important;
            transition: all 0.2s ease !important;
            font-size: 0.85rem !important;
        }}

        [data-testid="stSidebar"] button:hover {{
            background: rgba(255, 255, 255, 0.08) !important;
            border-color: rgba(212, 175, 55, 0.3) !important;
            color: #e2e8f0 !important;
        }}

        /* ── Selectbox Styling ─────────────────────────────── */
        [data-testid="stSidebar"] .stSelectbox > div > div {{
            background: rgba(15, 23, 42, 0.8) !important;
            border: 1px solid rgba(148, 163, 184, 0.2) !important;
            color: #cbd5e1 !important;
            border-radius: 0.5rem !important;
        }}

        /* ── Main Area Buttons ─────────────────────────────── */
        .stButton > button {{
            background: rgba(26, 42, 64, 0.7) !important;
            border: 1px solid rgba(148, 163, 184, 0.15) !important;
            color: #cbd5e1 !important;
            border-radius: 0.5rem !important;
            font-size: 0.8rem !important;
            transition: all 0.2s ease !important;
        }}

        .stButton > button:hover {{
            background: rgba(212, 175, 55, 0.15) !important;
            border-color: rgba(212, 175, 55, 0.3) !important;
            color: {GOLD} !important;
        }}

        /* ── Chat Input Styling ────────────────────────────── */
        [data-testid="stChatInput"] {{
            background: rgba(15, 23, 42, 0.8) !important;
            border: 1px solid rgba(148, 163, 184, 0.15) !important;
            border-radius: 0.75rem !important;
        }}

        [data-testid="stChatInput"] textarea {{
            color: #e2e8f0 !important;
        }}

        /* ── File Uploader ─────────────────────────────────── */
        [data-testid="stFileUploader"] {{
            background: rgba(26, 42, 64, 0.5) !important;
            border: 1px dashed rgba(148, 163, 184, 0.2) !important;
            border-radius: 0.75rem !important;
            padding: 0.5rem !important;
        }}

        [data-testid="stFileUploader"] label {{
            color: #94a3b8 !important;
            font-size: 0.75rem !important;
        }}

        /* ── Scrollbar ─────────────────────────────────────── */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.03);
        }}
        ::-webkit-scrollbar-thumb {{
            background: rgba(212, 175, 55, 0.25);
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: rgba(212, 175, 55, 0.45);
        }}

        /* ── Glass Panel Utility ───────────────────────────── */
        .glass-panel {{
            background: rgba(26, 42, 64, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}

        /* ── Gold Gradient Text ────────────────────────────── */
        .gold-gradient-text {{
            background: linear-gradient(135deg, #D4AF37 0%, #F3E5AB 50%, #D4AF37 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        /* ── Expander & Container Styling ──────────────────── */
        [data-testid="stExpander"] {{
            background: rgba(26, 42, 64, 0.5) !important;
            border: 1px solid rgba(148, 163, 184, 0.1) !important;
            border-radius: 0.75rem !important;
        }}

        .stContainer {{
            background: transparent !important;
        }}

        /* ── Audio Element ─────────────────────────────────── */
        audio {{
            width: 100%;
            height: 2.5rem;
            border-radius: 0.5rem;
        }}

        /* ── Divider ───────────────────────────────────────── */
        hr {{
            border-color: rgba(148, 163, 184, 0.1) !important;
        }}

        /* ── Alert Boxes ───────────────────────────────────── */
        .stSuccess, .stError, .stWarning, .stInfo {{
            background: rgba(26, 42, 64, 0.8) !important;
            border-radius: 0.5rem !important;
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
col_main, col_chat = st.columns([3, 2])

with col_main:
    # Header
    render_header(ayahs, current_ayah_index)

    # Quran dual-pane display
    render_quran_view(ayahs, current_ayah_index)

    # Audio player footer
    render_audio_player(ayahs, current_ayah_index)

with col_chat:
    # Scholar Agent chat panel
    render_chat_panel(ayahs)

"""
Hidayah AI — Session State Management
Initializes and manages all Streamlit session state variables.
"""

import streamlit as st


def init_session_state():
    """Initialize all session state defaults. Reads from URL parameters if available."""
    
    # 1. Parse existing URL parameters (if any)
    qp = st.query_params
    q_juz = qp.get("juz")
    q_ayah = qp.get("ayah")
    q_mode = qp.get("mode")

    initial_juz = int(q_juz) if q_juz and q_juz.isdigit() else 1
    if not (1 <= initial_juz <= 30):
        initial_juz = 1

    initial_ayah = int(q_ayah) if q_ayah and q_ayah.isdigit() else 0
    from utils.config import AUDIO_MODES
    initial_mode = q_mode if q_mode in AUDIO_MODES else "Arabic (Mishary Rashid)"

    defaults = {
        # Navigation
        "current_juz": initial_juz,
        "current_ayah_index": initial_ayah,
        "last_ayah": initial_ayah,
        "_loaded_juz": None,

        # Quran data cache
        "ayahs": [],

        # Audio
        "audio_mode": initial_mode,
        "is_playing": False,

        # Chat
        "chat_history": [],
        "chat_input": "",

        # RAG
        "faiss_index": None,
        "pdf_chunks": [],
        "pdf_embeddings": None,
        "uploaded_pdf_name": None,

        # UI
        "show_settings": False,
        "show_scholar_agent": False,
        "context_open": True,
        "context_tab": "Tafseer",
        "selected_tafseer_source": None,
        "tafsir_language": "en",
        "visible_ayah_window": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

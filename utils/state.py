"""
Hidayah AI — Session State Management
Initializes and manages all Streamlit session state variables.
"""

import streamlit as st


def init_session_state():
    """Initialize all session state defaults if not already set."""
    defaults = {
        # Navigation
        "current_juz": 1,
        "current_ayah_index": 0,
        "last_ayah": 0,
        "_loaded_juz": None,

        # Quran data cache
        "ayahs": [],

        # Audio
        "audio_mode": "Arabic (Mishary Rashid)",
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
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

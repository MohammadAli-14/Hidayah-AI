"""
Hidayah AI — Audio Player Component
Custom Streamlit component that auto-advances and keeps UI synced.
"""

import streamlit as st
from components.audio_player import audio_player


def _build_playlist(ayahs: list[dict], audio_mode: str) -> list[dict]:
    """Build playlist for the frontend component."""
    return [
        {
            "idx": i,
            "url": a.get("audio_url", ""),
            "surah": a.get("surah_name", ""),
            "ayahNum": a.get("number_in_surah", 0),
            "mode": audio_mode,
        }
        for i, a in enumerate(ayahs)
    ]


def render_audio_player(ayahs: list[dict], current_index: int = 0):
    """Render the audio player and sync ayah index from the frontend."""
    if not ayahs:
        return

    audio_mode = st.session_state.get("audio_mode", "Arabic (Mishary Rashid)")
    is_playing = st.session_state.get("is_playing", False)
    idx = min(current_index, len(ayahs) - 1)

    value = audio_player(
        playlist=_build_playlist(ayahs, audio_mode),
        start_index=idx,
        is_playing=is_playing,
        key="audio_player",
    )

    if isinstance(value, dict):
        new_idx = value.get("ayahIndex")
        new_playing = value.get("isPlaying")
        should_rerun = False

        if isinstance(new_idx, (int, float)):
            new_idx = int(new_idx)
            if new_idx != st.session_state.get("current_ayah_index", 0):
                st.session_state.current_ayah_index = new_idx
                st.session_state.last_ayah = new_idx
                should_rerun = True

        if isinstance(new_playing, bool) and new_playing != st.session_state.get("is_playing", False):
            st.session_state.is_playing = new_playing
            should_rerun = True

        if should_rerun:
            st.rerun()

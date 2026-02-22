"""Minimal Streamlit component wrapper for the audio player."""

from pathlib import Path
import streamlit.components.v1 as components

_COMPONENT_DIR = Path(__file__).resolve().parent / "frontend"

_audio_player = components.declare_component(
    "hidayah_audio_player",
    path=str(_COMPONENT_DIR),
)


def audio_player(playlist, start_index=0, is_playing=False, key=None):
    """Render the audio player component and return its latest state."""
    return _audio_player(
        playlist=playlist,
        start_index=start_index,
        is_playing=is_playing,
        key=key,
    )

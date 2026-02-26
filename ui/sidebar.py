"""
Hidayah AI — Sidebar Component
Renders the left sidebar: logo, Juz navigation (30 paras), audio mode selector, Smart Resume button.
"""

import streamlit as st
from utils.config import JUZ_DATA, AUDIO_MODES, LOGO_PATH, GOLD, get_logo_base64


def render_sidebar():
    """Render the full sidebar with logo, Juz navigation, and audio controls."""

    with st.sidebar:
        # ── Logo & Branding ───────────────────────────────────────
        logo_b64 = get_logo_base64()
        if logo_b64:
            st.html(
                f"""
                <div style="text-align:center; padding: 0.5rem 0 0.25rem 0;">
                    <img src="{logo_b64}" style="max-width:100%; border-radius: 0.5rem;" alt="Hidayah AI" />
                </div>
                """
            )
        else:
            st.html(
                f"""
                <div style="text-align:center; padding: 1rem 0;">
                    <h1 style="font-family: 'Playfair Display', serif; color: white; margin:0;">
                        Hidayah<span style="color: {GOLD};">AI</span>
                    </h1>
                    <p style="color: #94a3b8; font-size: 0.75rem; margin-top: 4px;">Research Companion</p>
                </div>
                """
            )

        st.html(
            """
            <div style="text-align:center; padding-bottom: 0.75rem; border-bottom: 1px solid rgba(148,163,184,0.2); margin-bottom: 0.5rem;">
                <p style="color: #94a3b8; font-size: 0.7rem; margin: 0;">30-Day Ramadan Research Companion</p>
            </div>
            """
        )

        # ── Juz Navigation ────────────────────────────────────────
        st.markdown(
            '<p style="font-size:0.7rem; font-weight:700; color:#94a3b8; text-transform:uppercase; '
            'letter-spacing:0.1em; padding: 0 0.5rem; margin-bottom: 0.5rem;">Juz Navigation</p>',
            unsafe_allow_html=True,
        )

        current_juz = st.session_state.get("current_juz", 1)

        for juz_num, juz_info in JUZ_DATA.items():
            is_active = juz_num == current_juz

            if is_active:
                st.html(
                    f"""
                    <div style="
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                        padding: 0.7rem 0.75rem;
                        border-radius: 0.75rem;
                        margin-bottom: 0.35rem;
                        background: rgba(212,175,55,0.12);
                        border: 1px solid rgba(212,175,55,0.45);
                        font-family: Inter, sans-serif;
                    ">
                        <div style="display:flex; align-items:center; gap:0.65rem; min-width:0;">
                            <span style="
                                width: 1.75rem; height: 1.75rem; border-radius: 50%;
                                background: {GOLD}; color: #0F172A; font-weight: 800;
                                display: inline-flex; align-items: center; justify-content: center;
                                font-size: 0.75rem; flex-shrink: 0;
                            ">{juz_num}</span>
                            <span style="
                                color: #f8fafc; font-size: 0.74rem; font-weight: 600;
                                text-transform: uppercase; letter-spacing: 0.04em;
                            ">{juz_info['english']}</span>
                        </div>
                        <span style="
                            font-family: Amiri, serif; color: #ffffff; font-size: 1.05rem;
                            direction: rtl; line-height: 1;
                        ">{juz_info['arabic']}</span>
                    </div>
                    """
                )
            else:
                label = f"{juz_num}. {juz_info['english']}  |  {juz_info['arabic']}"
                if st.button(label, key=f"juz_btn_{juz_num}", use_container_width=True):
                    st.session_state.current_juz = juz_num
                    st.session_state.current_ayah_index = 0
                    st.session_state.last_ayah = 0
                    st.session_state._loaded_juz = None
                    st.session_state.ayahs = []
                    st.session_state.is_playing = False
                    st.rerun()

        # ── Audio Controls ────────────────────────────────────────
        st.markdown("---")
        st.markdown(
            '<p style="font-size:0.7rem; color:#94a3b8; margin-bottom:0.25rem;">Audio Recitation</p>',
            unsafe_allow_html=True,
        )
        current_mode = st.session_state.get("audio_mode", AUDIO_MODES[0])
        st.html(
            f"""
            <div style="
                padding: 0.55rem 0.65rem;
                border: 1px solid rgba(148,163,184,0.16);
                border-radius: 2px;
                background: rgba(15,23,42,0.55);
                margin-bottom: 0.55rem;
                font-family: Inter, sans-serif;
            ">
                <p style="margin:0; color:#e2e8f0; font-size:0.78rem; font-weight:600;">{current_mode}</p>
                <p style="margin:0.15rem 0 0 0; color:#64748b; font-size:0.62rem;">Use top control to change language</p>
            </div>
            """
        )

        # Smart Resume button

        if st.button("▶  Smart Resume", key="smart_resume", use_container_width=True):
            last = st.session_state.get("last_ayah", 0)
            if last > 0:
                st.session_state.current_ayah_index = last
                st.session_state.is_playing = True
                st.rerun()

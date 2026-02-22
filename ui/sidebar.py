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

        # Scrollable Juz list
        current_juz = st.session_state.get("current_juz", 1)

        for juz_num, juz_info in JUZ_DATA.items():
            is_active = juz_num == current_juz

            if is_active:
                # Active Juz — gold highlight (rendered via st.html for div support)
                st.html(
                    f"""
                    <div style="
                        display: flex; align-items: center; padding: 0.6rem 0.75rem;
                        border-radius: 0.75rem; margin-bottom: 0.25rem;
                        background: rgba(212,175,55,0.1); border: 1px solid rgba(212,175,55,0.25);
                        color: {GOLD}; cursor: default; font-family: Inter, sans-serif;
                    ">
                        <span style="
                            display: inline-flex; align-items: center; justify-content: center;
                            width: 1.5rem; height: 1.5rem; border-radius: 50%;
                            background: {GOLD}; color: #0F172A; font-size: 0.7rem; font-weight: 700;
                            margin-right: 0.75rem; flex-shrink: 0;
                        ">{juz_num}</span>
                        <span style="font-size: 0.85rem; font-weight: 500;">{juz_info['name']}</span>
                    </div>
                    """
                )
            else:
                # Inactive Juz — clickable button
                if st.button(
                    f"{juz_num}. {juz_info['name']}",
                    key=f"juz_btn_{juz_num}",
                    use_container_width=True,
                ):
                    st.session_state.current_juz = juz_num
                    st.session_state.current_ayah_index = 0
                    st.session_state.ayahs = []
                    st.rerun()

        # ── Audio Controls ────────────────────────────────────────
        st.markdown("---")
        st.markdown(
            '<p style="font-size:0.7rem; color:#94a3b8; margin-bottom:0.25rem;">Audio Recitation</p>',
            unsafe_allow_html=True,
        )
        audio_mode = st.selectbox(
            "Audio Mode",
            AUDIO_MODES,
            index=AUDIO_MODES.index(st.session_state.get("audio_mode", AUDIO_MODES[0])),
            label_visibility="collapsed",
            key="audio_mode_select",
        )
        st.session_state.audio_mode = audio_mode

        # Smart Resume button

        if st.button("▶  Smart Resume", key="smart_resume", use_container_width=True):
            last = st.session_state.get("last_ayah", 0)
            if last > 0:
                st.session_state.current_ayah_index = last
                st.session_state.is_playing = True
                st.rerun()

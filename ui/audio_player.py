"""
Hidayah AI — Audio Player Component
Full JavaScript-based audio player that survives Streamlit reruns.
Features: continuous playback, auto-advance, speed control, progress bar, waveform animation.
"""

import json
import streamlit as st
import streamlit.components.v1 as components
from utils.config import GOLD, MIDNIGHT_BLUE


def _build_playlist(ayahs: list[dict]) -> list[dict]:
    """Build a JSON-serialisable playlist from ayah data."""
    return [
        {
            "idx": i,
            "url": a.get("audio_url", ""),
            "surah": a.get("surah_name", ""),
            "ayahNum": a.get("number_in_surah", 0),
        }
        for i, a in enumerate(ayahs)
    ]


def render_audio_player(ayahs: list[dict], current_index: int = 0):
    """
    Render a full JS audio player embedded via st.components.v1.html.
    The player lives in an iframe so Streamlit reruns do NOT destroy audio.
    """
    if not ayahs:
        return

    idx = min(current_index, len(ayahs) - 1)
    total = len(ayahs)
    is_playing = st.session_state.get("is_playing", False)
    audio_mode = st.session_state.get("audio_mode", "Arabic (Mishary Rashid)")

    playlist_json = json.dumps(_build_playlist(ayahs))

    # ── Embedded HTML/JS audio player ────────────────────────
    player_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        *{{margin:0;padding:0;box-sizing:border-box}}
        body{{font-family:'Inter',sans-serif;background:transparent;color:#e2e8f0;overflow:hidden}}
        .pw{{background:rgba(26,42,64,0.95);backdrop-filter:blur(12px);border-top:1px solid rgba(212,175,55,0.2);border-radius:0 0 1rem 1rem;position:relative}}
        .jp{{position:absolute;top:0;left:0;right:0;height:3px;background:rgba(148,163,184,0.15);z-index:2}}
        .jpf{{height:100%;background:{GOLD};transition:width .4s ease;position:relative}}
        .jpd{{position:absolute;right:-5px;top:-4px;width:11px;height:11px;border-radius:50%;background:#fff;border:2.5px solid {GOLD};box-shadow:0 1px 4px rgba(0,0,0,.3)}}
        .ir{{display:flex;align-items:center;justify-content:space-between;padding:.65rem 1.25rem .2rem}}
        .np{{display:flex;align-items:center;gap:.6rem}}
        .sl{{color:{GOLD};font-size:.78rem;font-weight:600}}
        .ac{{color:#64748b;font-size:.7rem}}
        .wf{{display:flex;align-items:center;gap:2px;height:1.6rem}}
        .wf .b{{width:3px;border-radius:2px;transition:height .15s ease}}
        .wf.on .b{{animation:wv .6s ease-in-out infinite alternate}}
        @keyframes wv{{0%{{transform:scaleY(.5)}}100%{{transform:scaleY(1.3)}}}}
        .wf .b:nth-child(2){{animation-delay:.08s}}.wf .b:nth-child(3){{animation-delay:.16s}}
        .wf .b:nth-child(4){{animation-delay:.24s}}.wf .b:nth-child(5){{animation-delay:.32s}}
        .wf .b:nth-child(6){{animation-delay:.10s}}.wf .b:nth-child(7){{animation-delay:.18s}}
        .wf .b:nth-child(8){{animation-delay:.26s}}.wf .b:nth-child(9){{animation-delay:.06s}}
        .wf .b:nth-child(10){{animation-delay:.20s}}.wf .b:nth-child(11){{animation-delay:.14s}}
        .wf .b:nth-child(12){{animation-delay:.28s}}.wf .b:nth-child(13){{animation-delay:.04s}}
        .wf .b:nth-child(14){{animation-delay:.22s}}.wf .b:nth-child(15){{animation-delay:.12s}}
        .sr{{display:flex;align-items:center;gap:.5rem;padding:.15rem 1.25rem .3rem}}
        .tl{{font-size:.62rem;color:#94a3b8;min-width:38px;font-variant-numeric:tabular-nums}}
        .st{{flex:1;height:4px;background:rgba(148,163,184,.2);border-radius:2px;cursor:pointer;position:relative}}
        .sf{{height:100%;background:{GOLD};border-radius:2px;position:absolute;left:0;top:0;pointer-events:none}}
        .sth{{width:10px;height:10px;border-radius:50%;background:#fff;border:2px solid {GOLD};position:absolute;top:-3px;pointer-events:none;transition:left .1s linear;box-shadow:0 1px 3px rgba(0,0,0,.3)}}
        .cr{{display:flex;align-items:center;justify-content:center;gap:.8rem;padding:.25rem 1rem .6rem}}
        .cb{{background:rgba(255,255,255,.05);border:1px solid rgba(148,163,184,.15);color:#cbd5e1;border-radius:.5rem;padding:.35rem .9rem;font-size:.78rem;cursor:pointer;transition:all .2s;font-family:'Inter',sans-serif;font-weight:500}}
        .cb:hover{{background:rgba(212,175,55,.15);border-color:rgba(212,175,55,.3);color:{GOLD}}}
        .cb:disabled{{opacity:.35;cursor:default}}
        .cb:disabled:hover{{background:rgba(255,255,255,.05);border-color:rgba(148,163,184,.15);color:#cbd5e1}}
        .pb{{background:rgba(212,175,55,.15)!important;border-color:rgba(212,175,55,.4)!important;color:{GOLD}!important;padding:.4rem 1.4rem;font-size:.85rem;font-weight:600}}
        .pb:hover{{background:rgba(212,175,55,.3)!important}}
        .sp{{color:#94a3b8;font-size:.63rem;text-transform:uppercase;letter-spacing:.05em;border:1px solid rgba(148,163,184,.25);padding:.18rem .55rem;border-radius:.25rem;cursor:pointer;background:transparent;font-family:'Inter',sans-serif;transition:all .2s}}
        .sp:hover{{color:{GOLD};border-color:rgba(212,175,55,.4)}}
        .ml{{font-size:.58rem;color:#475569;text-transform:uppercase;letter-spacing:.08em}}
    </style>
    </head>
    <body>
    <div class="pw">
        <div class="jp"><div class="jpf" id="jF" style="width:{((idx+1)/total*100) if total else 0}%"><div class="jpd"></div></div></div>
        <div class="ir">
            <div class="np">
                <span class="sl" id="sL">Loading...</span>
                <span class="ac" id="aC">–</span>
            </div>
            <div class="wf" id="wF">
                {"".join(f'<div class="b" style="height:{h}px;background:rgba(212,175,55,{o})"></div>' for h,o in [(8,.2),(14,.5),(22,.9),(10,.4),(18,.7),(8,.2),(22,.9),(14,.5),(8,.2),(14,.5),(22,.9),(10,.4),(8,.2),(14,.5),(22,.9)])}
            </div>
            <div style="display:flex;align-items:center;gap:.6rem">
                <span class="ml" id="mL">{audio_mode}</span>
                <button class="sp" id="spB" onclick="cSpd()">1.0x</button>
            </div>
        </div>
        <div class="sr">
            <span class="tl" id="cT">0:00</span>
            <div class="st" id="sT" onclick="skTo(event)">
                <div class="sf" id="sF" style="width:0%"></div>
                <div class="sth" id="sTh" style="left:0%"></div>
            </div>
            <span class="tl" id="dT" style="text-align:right">0:00</span>
        </div>
        <div class="cr">
            <button class="cb" id="pB" onclick="pA()">⏮ Prev</button>
            <button class="cb pb" id="plB" onclick="tP()">▶ Play</button>
            <button class="cb" id="nB" onclick="nA()">Next ⏭</button>
        </div>
    </div>
    <audio id="au" preload="auto"></audio>
    <script>
    const P={playlist_json};
    const T=P.length;
    let ci={idx},ip={'true' if is_playing else 'false'};
    const sp=[0.75,1,1.25,1.5,2];
    let si=1;
    const $=id=>document.getElementById(id);
    const au=$('au'),plB=$('plB'),sL=$('sL'),aC=$('aC'),jF=$('jF'),sF=$('sF'),sTh=$('sTh'),cT=$('cT'),dT=$('dT'),wF=$('wF'),spB=$('spB'),pB=$('pB'),nB=$('nB');

    function fmt(s){{if(!s||isNaN(s))return'0:00';const m=Math.floor(s/60),sec=Math.floor(s%60);return m+':'+(sec<10?'0':'')+sec}}

    function ld(i,ap){{
        if(i<0||i>=T)return;
        ci=i;const it=P[i];
        sL.textContent=it.surah+' : '+it.ayahNum;
        aC.textContent='Ayah '+(i+1)+' of '+T;
        jF.style.width=((i+1)/T*100)+'%';
        pB.disabled=i<=0;nB.disabled=i>=T-1;
        sF.style.width='0%';sTh.style.left='0%';
        cT.textContent='0:00';dT.textContent='0:00';
        if(it.url){{au.src=it.url;au.load();if(ap){{au.play().catch(()=>{{}});sPS(true)}}}}
    }}

    function sPS(p){{ip=p;plB.textContent=p?'⏸ Pause':'▶ Play';p?wF.classList.add('on'):wF.classList.remove('on')}}

    function tP(){{if(!au.src)return;au.paused?(au.play().catch(()=>{{}}),sPS(true)):(au.pause(),sPS(false))}}
    function pA(){{if(ci>0)ld(ci-1,true)}}
    function nA(){{if(ci<T-1)ld(ci+1,true)}}
    function cSpd(){{si=(si+1)%sp.length;au.playbackRate=sp[si];spB.textContent=sp[si]+'x'}}
    function skTo(e){{const r=e.currentTarget.getBoundingClientRect();const p=Math.max(0,Math.min(1,(e.clientX-r.left)/r.width));if(au.duration)au.currentTime=p*au.duration}}

    au.addEventListener('timeupdate',()=>{{if(!au.duration)return;const p=au.currentTime/au.duration*100;sF.style.width=p+'%';sTh.style.left=p+'%';cT.textContent=fmt(au.currentTime)}});
    au.addEventListener('loadedmetadata',()=>{{dT.textContent=fmt(au.duration)}});
    au.addEventListener('ended',()=>{{if(ci<T-1){{ld(ci+1,true)}}else{{sPS(false)}}}});

    document.addEventListener('keydown',e=>{{
        if(e.code==='Space'){{e.preventDefault();tP()}}
        if(e.code==='ArrowLeft')pA();
        if(e.code==='ArrowRight')nA();
    }});

    ld(ci,ip);
    </script>
    </body></html>
    """

    components.html(player_html, height=155, scrolling=False)

    # ── Streamlit-side sync buttons ──────────────────────────
    _handle_player_sync(ayahs, idx, total)


def _handle_player_sync(ayahs: list[dict], current_idx: int, total: int):
    """
    Streamlit-side prev/next + page-sync controls.
    JS player handles continuous playback internally; these buttons update
    Streamlit state so the Quran display panel highlights the correct ayah.
    """
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if current_idx > 0:
            if st.button("⏮ Prev Ayah", key="sync_prev", use_container_width=True):
                st.session_state.current_ayah_index = max(0, current_idx - 1)
                st.session_state.last_ayah = st.session_state.current_ayah_index
                st.session_state.is_playing = True
                st.rerun()

    with col2:
        page_size = 5
        page_num = (current_idx // page_size) + 1
        total_pages = (total + page_size - 1) // page_size
        st.markdown(
            f'<p style="text-align:center;color:#64748b;font-size:0.72rem;margin:0.3rem 0 0 0;">'
            f'Ayah {current_idx + 1} of {total} &nbsp;·&nbsp; Page {page_num} of {total_pages}</p>',
            unsafe_allow_html=True,
        )

    with col3:
        if current_idx < total - 1:
            if st.button("Next Ayah ⏭", key="sync_next", use_container_width=True):
                st.session_state.current_ayah_index = min(total - 1, current_idx + 1)
                st.session_state.last_ayah = st.session_state.current_ayah_index
                st.session_state.is_playing = True
                st.rerun()

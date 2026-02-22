const root = document.getElementById("root");

let playlist = [];
let currentIndex = 0;
let currentSubIndex = 0;
let isPlaying = false;
let audioEl = null;
let nextAudioEl = null;
let initialized = false;

function sendMessage(type, data = {}) {
  window.parent.postMessage(
    {
      isStreamlitMessage: true,
      type,
      ...data,
    },
    "*",
  );
}

function setComponentValue(value) {
  sendMessage("streamlit:setComponentValue", { value });
}

function setFrameHeight(height) {
  sendMessage("streamlit:setFrameHeight", { height });
}

function setComponentReady() {
  sendMessage("streamlit:componentReady", { apiVersion: 1 });
}

function fmt(seconds) {
  if (!seconds || Number.isNaN(seconds)) return "0:00";
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s < 10 ? "0" : ""}${s}`;
}

function renderUI() {
  const item = playlist[currentIndex] || {};
  const total = playlist.length || 1;
  const pct = ((currentIndex + 1) / total) * 100;

  root.innerHTML = `
    <div style="
      background: rgba(26,42,64,0.95);
      border-top: 1px solid rgba(212,175,55,0.2);
      border-radius: 0 0 1rem 1rem;
      padding: 0.75rem 1.5rem 0.6rem 1.5rem;
      position: relative;
      color: #e2e8f0;
    ">
      <div style="position:absolute;top:0;left:0;right:0;height:3px;background:rgba(148,163,184,0.2);">
        <div style="height:100%;width:${pct}%;background:#D4AF37;position:relative;transition:width 0.3s ease;">
          <div style="position:absolute;right:-4px;top:-3px;width:9px;height:9px;border-radius:50%;background:#fff;border:2px solid #D4AF37;"></div>
        </div>
      </div>
      <div style="display:flex;align-items:center;justify-content:space-between;margin-top:0.25rem;">
        <div style="display:flex;align-items:center;gap:0.75rem;min-width:220px;">
          <span style="color:#D4AF37;font-size:0.8rem;font-weight:700;">${item.surah || ""} : ${item.ayahNum || ""}</span>
          <span style="color:#64748b;font-size:0.7rem;">Ayah ${currentIndex + 1} of ${total}</span>
        </div>
        <div style="display:flex;align-items:center;gap:0.5rem;color:#94a3b8;font-size:0.62rem;text-transform:uppercase;letter-spacing:0.05em;">
          ${item.mode || "Arabic (Mishary Rashid)"}
        </div>
      </div>

      <div style="display:flex;align-items:center;gap:0.5rem;margin-top:0.45rem;">
        <span id="curTime" style="font-size:0.62rem;color:#94a3b8;min-width:38px;">0:00</span>
        <div id="seekTrack" style="flex:1;height:4px;background:rgba(148,163,184,0.2);border-radius:2px;cursor:pointer;position:relative;">
          <div id="seekFill" style="height:100%;width:0%;background:#D4AF37;border-radius:2px;"></div>
          <div id="seekThumb" style="width:10px;height:10px;border-radius:50%;background:#fff;border:2px solid #D4AF37;position:absolute;top:-3px;left:0%;"></div>
        </div>
        <span id="durTime" style="font-size:0.62rem;color:#94a3b8;min-width:38px;text-align:right;">0:00</span>
      </div>

      <div style="display:flex;align-items:center;justify-content:center;gap:0.8rem;margin-top:0.5rem;">
        <button id="prevBtn" style="background:rgba(255,255,255,0.05);border:1px solid rgba(148,163,184,0.15);color:#cbd5e1;border-radius:0.5rem;padding:0.35rem 0.9rem;font-size:0.78rem;cursor:pointer;">Prev</button>
        <button id="playBtn" style="background:rgba(212,175,55,0.15);border:1px solid rgba(212,175,55,0.4);color:#D4AF37;border-radius:0.5rem;padding:0.4rem 1.4rem;font-size:0.85rem;font-weight:600;cursor:pointer;">${isPlaying ? "Pause" : "Play"}</button>
        <button id="nextBtn" style="background:rgba(255,255,255,0.05);border:1px solid rgba(148,163,184,0.15);color:#cbd5e1;border-radius:0.5rem;padding:0.35rem 0.9rem;font-size:0.78rem;cursor:pointer;">Next</button>
      </div>
    </div>
  `;

  const prevBtn = document.getElementById("prevBtn");
  const playBtn = document.getElementById("playBtn");
  const nextBtn = document.getElementById("nextBtn");
  const seekTrack = document.getElementById("seekTrack");
  const seekFill = document.getElementById("seekFill");
  const seekThumb = document.getElementById("seekThumb");
  const curTime = document.getElementById("curTime");
  const durTime = document.getElementById("durTime");

  prevBtn.onclick = () => setIndex(currentIndex - 1, true);
  nextBtn.onclick = () => setIndex(currentIndex + 1, true);
  playBtn.onclick = () => togglePlay();

  seekTrack.onclick = (e) => {
    if (!audioEl || !audioEl.duration) return;
    const rect = seekTrack.getBoundingClientRect();
    const pct = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    audioEl.currentTime = pct * audioEl.duration;
  };

  if (audioEl) {
    audioEl.ontimeupdate = () => {
      if (!audioEl.duration) return;
      const pct = (audioEl.currentTime / audioEl.duration) * 100;
      seekFill.style.width = `${pct}%`;
      seekThumb.style.left = `${pct}%`;
      curTime.textContent = fmt(audioEl.currentTime);
    };
    audioEl.onloadedmetadata = () => {
      durTime.textContent = fmt(audioEl.duration);
    };
  }
}

function ensureAudio() {
  if (!audioEl) {
    audioEl = new Audio();
    audioEl.preload = "auto";
    audioEl.onended = () => {
      const currentItem = playlist[currentIndex] || {};
      const currentUrls = currentItem.urls || [];

      // Advance sub-index if there are more translations for this Ayah
      if (currentSubIndex < currentUrls.length - 1) {
        currentSubIndex++;
        const nextSubUrl = currentUrls[currentSubIndex] || "";

        const preloadedSrc = nextAudioEl ? (nextAudioEl.currentSrc || nextAudioEl.src || "") : "";
        if (nextAudioEl && nextSubUrl && preloadedSrc.includes(nextSubUrl)) {
          const prevAudio = audioEl;
          audioEl = nextAudioEl;
          nextAudioEl = prevAudio;
          audioEl.onended = prevAudio.onended;
          isPlaying = true;
          audioEl.play().catch(() => { });
          preloadNextUrl(currentIndex, currentSubIndex + 1);
          renderUI();
          return;
        }

        audioEl.src = nextSubUrl;
        audioEl.load();
        if (isPlaying) {
          audioEl.play().catch(() => { });
        }
        preloadNextUrl(currentIndex, currentSubIndex + 1);
        renderUI();
        return;
      }

      // If no more sub-urls, advance to next Ayah
      currentSubIndex = 0;
      if (currentIndex < playlist.length - 1) {
        const nextIndex = currentIndex + 1;
        const nextItem = playlist[nextIndex] || {};
        const nextUrl = (nextItem.urls && nextItem.urls.length > 0) ? nextItem.urls[0] : "";

        const preloadedSrc = nextAudioEl ? (nextAudioEl.currentSrc || nextAudioEl.src || "") : "";
        if (nextAudioEl && nextUrl && preloadedSrc.includes(nextUrl)) {
          const prevAudio = audioEl;
          audioEl = nextAudioEl;
          nextAudioEl = prevAudio;

          audioEl.onended = prevAudio.onended;
          currentIndex = nextIndex;
          isPlaying = true;
          audioEl.play().catch(() => { });
          preloadNextUrl(currentIndex, 1);
          notifyParent();
          renderUI();
          return;
        }

        // Fallback path when preload is unavailable.
        setIndex(nextIndex, true);
      } else {
        isPlaying = false;
        notifyParent();
        renderUI();
      }
    };
  }

  if (!nextAudioEl) {
    nextAudioEl = new Audio();
    nextAudioEl.preload = "auto";
  }
}

function preloadNextUrl(idx, subIdx) {
  if (!nextAudioEl) return;
  let nextItem = playlist[idx] || {};
  let urls = nextItem.urls || [];

  let targetUrl = "";
  if (subIdx < urls.length) {
    targetUrl = urls[subIdx];
  } else {
    const nextIdx = idx + 1;
    if (nextIdx >= playlist.length) {
      nextAudioEl.removeAttribute("src");
      return;
    }
    nextItem = playlist[nextIdx] || {};
    urls = nextItem.urls || [];
    targetUrl = urls[0] || "";
  }

  if (!targetUrl) {
    nextAudioEl.removeAttribute("src");
    return;
  }

  const currentNextSrc = nextAudioEl.currentSrc || nextAudioEl.src || "";
  if (!currentNextSrc.includes(targetUrl)) {
    nextAudioEl.src = targetUrl;
    nextAudioEl.load();
  }
}

function setIndex(idx, autoplay) {
  if (idx < 0 || idx >= playlist.length) return;
  currentIndex = idx;
  currentSubIndex = 0;
  ensureAudio();
  const item = playlist[currentIndex] || {};
  const targetUrl = (item.urls && item.urls.length > 0) ? item.urls[0] : "";
  if (targetUrl) {
    audioEl.src = targetUrl;
    audioEl.load();
    if (autoplay) {
      audioEl.play().catch(() => { });
      isPlaying = true;
    }
  }
  preloadNextUrl(currentIndex, currentSubIndex + 1);
  notifyParent();
  renderUI();
}

function togglePlay() {
  ensureAudio();
  if (audioEl.paused) {
    audioEl.play().catch(() => { });
    isPlaying = true;
  } else {
    audioEl.pause();
    isPlaying = false;
  }
  notifyParent();
  renderUI();
}

function notifyParent() {
  setComponentValue({
    ayahIndex: currentIndex,
    isPlaying: isPlaying,
  });
}

function onRender(data) {
  if (!data) return;
  playlist = data.playlist || [];
  const startIndex = data.start_index || 0;
  const playFlag = !!data.is_playing;

  ensureAudio();

  // Keep internal audio in sync with server state.
  // Important: on first render currentIndex can already equal startIndex (both 0),
  // so we must still load the source if audioEl has no src yet.
  const previousSrc = audioEl.currentSrc || audioEl.src || "";
  const targetItem = playlist[startIndex] || {};
  const targetUrl = (targetItem.urls && targetItem.urls.length > 0) ? targetItem.urls[0] : "";

  if (currentIndex !== startIndex || !previousSrc || (targetUrl && !previousSrc.includes(targetUrl))) {
    currentIndex = startIndex;
    currentSubIndex = 0;
    if (targetUrl) {
      audioEl.src = targetUrl;
      audioEl.load();
    }
  }

  preloadNextUrl(currentIndex, currentSubIndex + 1);

  if (playFlag && audioEl.paused) {
    audioEl.play().catch(() => { });
    isPlaying = true;
  }
  if (!playFlag && !audioEl.paused) {
    audioEl.pause();
    isPlaying = false;
  }

  renderUI();
  setFrameHeight(root.scrollHeight + 8);
}

window.addEventListener("message", (event) => {
  const message = event.data;
  if (!message || message.type !== "streamlit:render") return;
  onRender(message.args || {});
});

if (!initialized) {
  initialized = true;
  setComponentReady();
  setFrameHeight(220);
}

# /brainstorm - Scholar Agent UI Updates

### Context
The user wants to replace the `HA` text circle icon in the top header and the `🧠` icon in the Scholar Agent chat panel with the main application logo (`Hadayah AI.png`). When the icon is clicked (or shown), it should present the logo consistently.

---

### Option A: Static Logo Update
We simply update `ui/header.py` and `ui/chat_panel.py` to use `get_logo_base64()` and render the logo image instead of the current text/emojis.

✅ **Pros:**
- Direct, simple, and completely aligned with the user request.
- Very fast to implement (just 2 files).
- Maintains the current UI layout but elevates the branding.

❌ **Cons:**
- Doesn't fundamentally change the interaction model (the chat panel is always open).

📊 **Effort:** Low

---

### Option B: Collapsible Chat Panel (Actionable Header Icon)
We update the logo as requested, but we *also* make the logo in the header function as a toggle button. Clicking the logo in the header toggles the visibility of the entire Scholar Agent chat panel.

✅ **Pros:**
- Matches the user's phrasing "when icon of Scholar Agent has been clicked it then appears properly".
- Provides more screen real-estate for the Quran reader when chat is not needed.

❌ **Cons:**
- Streamlit layout columns (`st.columns`) do not support dynamic showing/hiding without triggering a full app re-render and pushing the layout jumpingly. 
- Streamlit's native expanding logic is clunky for side-by-side columns unless using custom component hacks.

📊 **Effort:** High (and clunky UX in Streamlit)

---

### Option C: Modal/Dialog Chat (Actionable Header Icon)
Clicking the logo in the header opens the Scholar Agent inside a centered modal dialog (`@st.dialog`), replacing the side-by-side layout entirely.

✅ **Pros:**
- Cleanest implementation of "clicking an icon to open it".
- Completely frees up the right side of the screen.

❌ **Cons:**
- Breaks the current UX paradigm where the user can read the Quran *while* chatting with the scholar. The dialog blocks the screen.

📊 **Effort:** Medium

---

## � Recommendation

**Option A (Static Logo Update)** is highly recommended. 
Streamlit's layout constraints make toggling entire columns (Option B) jarring, and putting the agent in a modal (Option C) ruins the core experience of reading and researching side-by-side. 

By executing **Option A**, we fulfill the exact visual request: replacing the "HA" and "🧠" placeholders with the beautiful `Hidayah AI.png` logo consistently across both headers, providing a cohesive brand experience exactly as shown in the screenshot intent.

What direction would you like to explore? If you agree, I will run the plan to update those files.

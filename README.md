# Hidayah AI: Ramadan Research Companion 🕌

**Hidayah AI** is a cutting-edge web application designed to make Quranic study and research intuitive, engaging, and accessible. Specifically tailiored as a 30-day companion for Ramadan, it focuses on deep-diving into individual Juz (parts) with modern AI-powered insights.

---

## 🌟 Key Features

- **Interactive Quran Reader:** Beautiful dual-pane view with original Arabic text alongside English (Asad) and Urdu (Jalandhry) translations.
- **Sequential Audio Engine:** A unique playback system that recites Arabic followed immediately by your chosen translation (English or Urdu), using high-quality reciters like Mishary Rashid Alafasy.
- **Scholar Agent (AI Research):** Powered by Google Gemini 1.5 Flash, providing scholarly explanations, historical context, and tafsir for any verse.
- **Contextual Web Research:** Real-time Islamic knowledge retrieval using the Tavily Search API.
- **RAG Document Analysis:** Upload scholarly PDFs and query them directly. The Scholar Agent uses vector search to find answers within your specific documents.
- **Premium UI/UX:** A high-end interface featuring glassmorphism, responsive design, and curated typography (Amiri + Playfair Display).

---

## 🛠️ Installation

To run Hidayah AI locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mohammadali-14/Hidayah-AI.git
   cd Hidayah-AI
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment:**
   Copy `.env.example` to `.env` and add your API keys:
   - `GEMINI_API_KEY`: Obtain from [Google AI Studio](https://aistudio.google.com/)
   - `TAVILY_API_KEY`: Obtain from [Tavily AI](https://tavily.com/)

4. **Launch the app:**
   ```bash
   streamlit run app.py
   ```

---

## 🚀 Deployment (Streamlit Cloud)

Hidayah AI is a optimized for one-click deployment to Streamlit Cloud:

1. Push your code to a GitHub repository.
2. Connect your repo at [share.streamlit.io](https://share.streamlit.io).
3. Set your `app.py` as the main entry point.
4. **Crucial:** Add your `GEMINI_API_KEY` and `TAVILY_API_KEY` to the Streamlit "Secrets" section in the dashboard.

---

## 📜 Technical Stack
- **Framework:** Streamlit (Python)
- **AI Models:** Google Gemini 1.5 Flash & Gemini Embedding
- **Search:** Tavily API
- **Vector DB:** FAISS (In-memory)
- **Data Source:** AlQuran.cloud API

---
**Developed by:** Hidayah AI Team.

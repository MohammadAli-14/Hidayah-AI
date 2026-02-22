"""
Hidayah AI — Configuration & Constants
Loads environment variables, defines model names, color palette, and Juz metadata.
"""

import os
import base64
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# ── Load Environment ──────────────────────────────────────────────
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

# Configure Gemini client globally
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# ── Model Tier Strategy ───────────────────────────────────────────
MODEL_ROUTER = "gemini-2.5-flash-lite"       # Intent classification (fastest)
MODEL_SCHOLAR = "gemini-2.5-pro"             # Scholarly chat & RAG answers (best reasoning)
MODEL_EMBEDDING = "models/text-embedding-004"  # Vector embeddings for FAISS RAG

# ── Design Tokens (from design.instructions.md) ──────────────────
MIDNIGHT_BLUE = "#1a2a40"
BG_DARK = "#0F172A"
GOLD = "#D4AF37"
EMERALD_DEEP = "#064E3B"
EMERALD_LIGHT = "#10B981"
BG_LIGHT = "#F8FAFC"

# ── Logo ──────────────────────────────────────────────────────────
_APP_DIR = Path(__file__).resolve().parent.parent
LOGO_PATH = _APP_DIR / "Hadayah AI.png"


def get_logo_base64() -> str:
    """Return the logo as a base64-encoded data URI for embedding in HTML."""
    try:
        with open(LOGO_PATH, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{data}"
    except FileNotFoundError:
        return ""

# ── AlQuran.cloud API ─────────────────────────────────────────────
QURAN_API_BASE = "https://api.alquran.cloud/v1"
ARABIC_EDITION = "ar.alafasy"       # Mishary Rashid Alafasy (with audio)
ENGLISH_EDITION = "en.asad"         # Muhammad Asad English translation
URDU_EDITION = "ur.jalandhry"       # Maulana Fateh Muhammad Jalandhry

# ── Audio Modes ───────────────────────────────────────────────────
AUDIO_MODES = [
    "Arabic (Mishary Rashid)",
    "Arabic + Urdu Translation",
    "Arabic + English Translation",
]

# ── 30 Juz Metadata ──────────────────────────────────────────────
JUZ_DATA = {
    1:  {"name": "Alif Lam Mim", "surahs": "Al-Fatiha 1 – Al-Baqarah 141"},
    2:  {"name": "Sayaqulu", "surahs": "Al-Baqarah 142 – Al-Baqarah 252"},
    3:  {"name": "Tilka ar-Rusul", "surahs": "Al-Baqarah 253 – Al-Imran 92"},
    4:  {"name": "Lan Tanalu", "surahs": "Al-Imran 93 – An-Nisa 23"},
    5:  {"name": "Wal-Muhsanat", "surahs": "An-Nisa 24 – An-Nisa 147"},
    6:  {"name": "La Yuhibbu-llah", "surahs": "An-Nisa 148 – Al-Ma'idah 81"},
    7:  {"name": "Wa Idha Sami'u", "surahs": "Al-Ma'idah 82 – Al-An'am 110"},
    8:  {"name": "Wa Lau Annana", "surahs": "Al-An'am 111 – Al-A'raf 87"},
    9:  {"name": "Qal al-Mala'", "surahs": "Al-A'raf 88 – Al-Anfal 40"},
    10: {"name": "Wa A'lamu", "surahs": "Al-Anfal 41 – At-Tawbah 92"},
    11: {"name": "Ya'tadhiruna", "surahs": "At-Tawbah 93 – Hud 5"},
    12: {"name": "Wa Ma Min Dabbah", "surahs": "Hud 6 – Yusuf 52"},
    13: {"name": "Wa Ma Ubarri'u", "surahs": "Yusuf 53 – Ibrahim 52"},
    14: {"name": "Rubama", "surahs": "Al-Hijr 1 – An-Nahl 128"},
    15: {"name": "Subhan-alladhi", "surahs": "Al-Isra 1 – Al-Kahf 74"},
    16: {"name": "Qal Alam", "surahs": "Al-Kahf 75 – Ta-Ha 135"},
    17: {"name": "Iqtaraba", "surahs": "Al-Anbiya 1 – Al-Hajj 78"},
    18: {"name": "Qad Aflaha", "surahs": "Al-Mu'minun 1 – Al-Furqan 20"},
    19: {"name": "Wa Qal-alladhina", "surahs": "Al-Furqan 21 – An-Naml 55"},
    20: {"name": "A'man Khalaqa", "surahs": "An-Naml 56 – Al-Ankabut 45"},
    21: {"name": "Utlu Ma Uhiya", "surahs": "Al-Ankabut 46 – Al-Ahzab 30"},
    22: {"name": "Wa Man Yaqnut", "surahs": "Al-Ahzab 31 – Ya-Sin 27"},
    23: {"name": "Wa Mali", "surahs": "Ya-Sin 28 – Az-Zumar 31"},
    24: {"name": "Fa Man Azlamu", "surahs": "Az-Zumar 32 – Fussilat 46"},
    25: {"name": "Ilayhi Yuraddu", "surahs": "Fussilat 47 – Al-Jathiyah 37"},
    26: {"name": "Ha Mim", "surahs": "Al-Ahqaf 1 – Adh-Dhariyat 30"},
    27: {"name": "Qala Fa-ma Khatbukum", "surahs": "Adh-Dhariyat 31 – Al-Hadid 29"},
    28: {"name": "Qad Sami Allahu", "surahs": "Al-Mujadila 1 – At-Tahrim 12"},
    29: {"name": "Tabaraka-lladhi", "surahs": "Al-Mulk 1 – Al-Mursalat 50"},
    30: {"name": "Amma Yatasa'alun", "surahs": "An-Naba 1 – An-Nas 6"},
}


def get_gemini_client() -> genai.Client | None:
    """Return the global Gemini client instance."""
    return client


def get_juz_display_name(juz_num: int) -> str:
    """Return a formatted display string for a Juz number."""
    data = JUZ_DATA.get(juz_num, {})
    return data.get("name", f"Juz {juz_num}")

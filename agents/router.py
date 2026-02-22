"""
Hidayah AI — Intent Router Agent
Uses Gemini 2.5 Flash-Lite for fast intent classification of user queries.
Categories: VERSE_LOOKUP, SCHOLARLY_RESEARCH, PDF_ANALYSIS
"""

from google import genai
from utils.config import MODEL_ROUTER, GEMINI_API_KEY, get_gemini_client

ROUTER_SYSTEM_PROMPT = """You are an intent classifier for an Islamic Quranic research application called Hidayah AI.

Classify the user's query into EXACTLY ONE of these categories. Return ONLY the category name, nothing else.

Categories:
- VERSE_LOOKUP: The user wants to look up, read, or hear a specific verse, surah, or juz. Examples: "Show me verse 255 of Al-Baqarah", "Read Surah Al-Fatiha", "What does ayah 183 say?"
- SCHOLARLY_RESEARCH: The user wants tafsir, fiqh rulings, historical context, scholarly opinions, or general Islamic knowledge. Examples: "Explain the fasting rules", "What do scholars say about...", "Historical context of this verse"
- PDF_ANALYSIS: The user wants to analyze, search, or ask questions about an uploaded PDF document. Examples: "What does the PDF say about...", "Summarize the uploaded document", "Find references to fasting in my PDF"

If unsure, default to SCHOLARLY_RESEARCH."""


def classify_intent(query: str) -> str:
    """
    Classify user intent using Gemini 2.5 Flash-Lite (fastest model).
    Returns one of: VERSE_LOOKUP, SCHOLARLY_RESEARCH, PDF_ANALYSIS
    """
    client = get_gemini_client()
    if not client:
        return "SCHOLARLY_RESEARCH"

    try:
        response = client.models.generate_content(
            model=MODEL_ROUTER,
            contents=query,
            config=genai.types.GenerateContentConfig(
                system_instruction=ROUTER_SYSTEM_PROMPT,
                temperature=0.1,
                max_output_tokens=20,
            ),
        )

        result = response.text.strip().upper()

        # Validate the response is one of the expected categories
        valid_categories = {"VERSE_LOOKUP", "SCHOLARLY_RESEARCH", "PDF_ANALYSIS"}
        if result in valid_categories:
            return result

        # Fuzzy match
        for cat in valid_categories:
            if cat in result:
                return cat

        return "SCHOLARLY_RESEARCH"

    except Exception as e:
        print(f"[Router] Classification error: {e}")
        return "SCHOLARLY_RESEARCH"

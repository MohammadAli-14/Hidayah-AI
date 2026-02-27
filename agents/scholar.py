"""
Hidayah AI — Scholar Agent
Uses Gemini 2.5 Pro for deep scholarly reasoning, tafsir, and research synthesis.
Routes to appropriate data source based on classified intent.
"""

from google import genai
from utils.config import MODEL_SCHOLAR, GEMINI_API_KEY, get_gemini_client
from agents.web_search import search_web
from agents.context_retriever import get_context_bundle_for_window

SCHOLAR_SYSTEM_PROMPT = """You are Hidayah AI, an Islamic scholarly research assistant. You are knowledgeable, respectful, and precise.

Guidelines:
1. Begin responses with "Assalamu Alaykum" when appropriate.
2. Cite sources clearly: Quran verses (Surah:Ayah), Hadith collections, and scholarly names.
3. When discussing fiqh, mention the relevant madhab perspectives where applicable.
4. Use a warm, scholarly tone — like a knowledgeable teacher.
5. If uncertain, say so clearly. Never fabricate scholarly opinions.
6. End with a reminder: "Please verify with qualified scholars for fiqh rulings."
7. Support both English and Urdu — respond in the language the user asks in.
8. When referencing Quranic text, include the Arabic if relevant.

You serve as a bridge between classical Islamic scholarship and modern seekers of knowledge."""


def get_scholar_response(
    query: str,
    intent: str,
    ayahs_context: list[dict] | None = None,
    ayah_window: list[dict] | None = None,
    tafseer_language: str = "en",
    pdf_context: str | None = None,
) -> str:
    """
    Generate a scholarly response using Gemini 2.5 Pro.

    Args:
        query: User's question
        intent: Classified intent (VERSE_LOOKUP, SCHOLARLY_RESEARCH, PDF_ANALYSIS)
        ayahs_context: Current ayahs being viewed (for verse context)
        pdf_context: Retrieved PDF chunks (for RAG answers)

    Returns:
        Formatted response string
    """
    client = get_gemini_client()
    if not client:
        return "⚠️ **Gemini API key not configured.** Please add `GEMINI_API_KEY` to your settings (Secrets on Streamlit Cloud or .env locally)."

    try:
        print(f"📖 [SCHOLAR] Assembling context. Intent: {intent}")
        # Build context based on intent
        context_parts = []
        grounded_sources = []

        if intent == "VERSE_LOOKUP" and (ayah_window or ayahs_context):
            window = ayah_window or ayahs_context or []

            # Provide current verse context
            verses_text = "\n".join(
                f"[{a['surah_name']} {a['number_in_surah']}] Arabic: {a['arabic']}\n"
                f"English: {a['english']}\nUrdu: {a['urdu']}"
                for a in window[:10]  # Limit context size
            )
            context_parts.append(f"Currently viewing these Quranic verses:\n{verses_text}")

            # Retrieve grounded Tafseer + Hadith across visible ayah window
            bundle = get_context_bundle_for_window(
                ayah_window=window[:10],
                tafseer_language=tafseer_language,
            )

            tafsir_context_lines = []
            hadith_context_lines = []
            tafsir_counter = 1
            hadith_counter = 1

            if bundle:
                tafsir_by_ayah = bundle.get("tafsir_by_ayah", {})
                hadith_by_ayah = bundle.get("hadith_by_ayah", {})
                citations = bundle.get("citations", [])

                for ayah_ref, tafsir_items in tafsir_by_ayah.items():
                    for item in tafsir_items[:2]:
                        tafsir_context_lines.append(
                            f"[T{tafsir_counter}] {item['source_name']} ({ayah_ref}, {item.get('language', '').upper()})\n"
                            f"{item['excerpt']}"
                        )
                        tafsir_source = (
                            f"[T{tafsir_counter}] {item['source_name']} | {ayah_ref} | "
                            f"lang:{item.get('language', '').upper()} | canonical:{item.get('canonical_status', 'unverified')}"
                        )
                        if item.get("canonical_url"):
                            tafsir_source += f" — {item['canonical_url']}"
                        grounded_sources.append(tafsir_source)
                        tafsir_counter += 1

                for ayah_ref, hadith_items in hadith_by_ayah.items():
                    for item in hadith_items[:1]:
                        hadith_context_lines.append(
                            f"[H{hadith_counter}] {item['source_name']} ({ayah_ref})\n{item['excerpt']}"
                        )
                        hadith_counter += 1

                for idx, citation in enumerate(citations, start=1):
                    citation_type = citation.get("type", "source")
                    source_name = citation.get("source_name", "Unknown Source")
                    reference = citation.get("reference", "")
                    language = (citation.get("language", "") or "").upper() or "N/A"
                    canonical_status = citation.get("canonical_status", "unverified")
                    canonical_url = citation.get("canonical_url", "")
                    ayah_ref = citation.get("metadata", {}).get("ayah_ref", "")
                    source_rank = citation.get("source_rank", 0)

                    line = (
                        f"type:{citation_type} | id:C{idx} | source:{source_name} | ref:{reference} | "
                        f"ayah:{ayah_ref} | lang:{language} | rank:{source_rank} | canonical:{canonical_status}"
                    )
                    if canonical_url:
                        line += f" | url:{canonical_url}"
                    grounded_sources.append(line)

            if tafsir_context_lines:
                context_parts.append("Authenticated Tafseer Context:\n" + "\n\n".join(tafsir_context_lines[:8]))
            if hadith_context_lines:
                context_parts.append("Related Hadith references:\n" + "\n\n".join(hadith_context_lines[:5]))

        elif intent == "SCHOLARLY_RESEARCH":
            # Fetch web results for additional context
            web_results = search_web(f"Islamic scholarly {query}")
            if web_results:
                web_text = "\n\n".join(
                    f"Source: {r['title']}\nURL: {r['url']}\n{r['content']}"
                    for r in web_results[:3]
                )
                context_parts.append(f"Web research results:\n{web_text}")

        elif intent == "PDF_ANALYSIS" and pdf_context:
            context_parts.append(f"Relevant excerpts from the uploaded PDF:\n{pdf_context}")

        # Assemble the full prompt
        full_prompt = query
        if context_parts:
            context_str = "\n\n---\n\n".join(context_parts)
            full_prompt = f"Context:\n{context_str}\n\n---\n\nUser Question: {query}"

        print(f"🧠 [SCHOLAR] Sending final prompt to {MODEL_SCHOLAR} (Context parts: {len(context_parts)})...")
        response = client.models.generate_content(
            model=MODEL_SCHOLAR,
            contents=full_prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=SCHOLAR_SYSTEM_PROMPT,
                temperature=0.7,
                max_output_tokens=2048,
            ),
        )

        if not response.text:
            return "⚠️ **Scholar Agent error:** The model returned an empty response. This might be due to safety filters or a temporary connection issue."

        print("✨ [SCHOLAR] Response generated successfully.")
        answer = response.text
        if grounded_sources:
            answer += "\n\nSources:\n" + "\n".join(f"- {src}" for src in grounded_sources)
        return answer

    except genai.errors.APIError as e:
        if e.code == 429:
            return "⚠️ **Scholar Agent is currently resting.** Hidayah AI is receiving a high volume of requests. Please wait a moment and try again."
        return f"⚠️ **API Error:** {str(e.message) if hasattr(e, 'message') else str(e)}"
    except Exception as e:
        return f"⚠️ **Scholar Agent error:** An unexpected error occurred. Please try again."

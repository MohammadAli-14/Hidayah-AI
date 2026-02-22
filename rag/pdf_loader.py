"""
Hidayah AI — PDF Loader & Chunker
Extracts text from uploaded PDFs and splits into chunks for RAG.
"""

import io
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract all text from an uploaded PDF file.

    Args:
        pdf_file: Streamlit UploadedFile or file-like object

    Returns:
        Extracted text as a single string
    """
    try:
        reader = PdfReader(pdf_file)
        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text.strip())
        return "\n\n".join(text_parts)
    except Exception as e:
        return f"[PDF extraction error: {str(e)}]"


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping chunks for embedding.

    Args:
        text: Full extracted text
        chunk_size: Approximate number of words per chunk
        overlap: Number of overlapping words between chunks

    Returns:
        List of text chunks
    """
    if not text or text.startswith("[PDF extraction error"):
        return []

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk.strip())
        start = end - overlap  # Overlap for context continuity

    return chunks


def extract_and_chunk(pdf_file, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Full pipeline: Extract PDF text and split into chunks.

    Args:
        pdf_file: Streamlit UploadedFile
        chunk_size: Words per chunk
        overlap: Word overlap between chunks

    Returns:
        List of text chunks ready for embedding
    """
    text = extract_text_from_pdf(pdf_file)
    return chunk_text(text, chunk_size, overlap)

"""
Hidayah AI — Domain Trust Validation
Centralised hostname validation for all external source pipelines.
"""

from urllib.parse import urlparse

# ── Trusted Domains by Category ──────────────────────────────────
HADITH_TRUSTED_DOMAINS = [
    "sunnah.com",
]

SCHOLARLY_TRUSTED_DOMAINS = [
    "sunnah.com",
    "islamqa.info",
    "islamqa.org",
    "quran.com",
    "seekersguidance.org",
    "al-maktaba.org",
    "alquran.cloud",
]

COMMENTARY_DOMAINS = [
    "islamqa.info",
    "islamqa.org",
    "seekersguidance.org",
]


def trusted_host(url: str, allowed_domains: list[str] | None = None) -> str:
    """Return matched trusted host using strict hostname matching, else empty string.

    Args:
        url: URL to validate.
        allowed_domains: Explicit allowlist. Defaults to SCHOLARLY_TRUSTED_DOMAINS.
    """
    if not url:
        return ""
    domains = allowed_domains or SCHOLARLY_TRUSTED_DOMAINS
    try:
        hostname = (urlparse(url).hostname or "").lower().strip()
    except Exception:
        return ""

    if hostname.startswith("www."):
        hostname = hostname[4:]

    for domain in domains:
        normalized = domain.lower().strip()
        if hostname == normalized or hostname.endswith(f".{normalized}"):
            return normalized
    return ""


def is_trusted_scholarly(url: str) -> bool:
    """Check if a URL belongs to a trusted scholarly domain."""
    return bool(trusted_host(url, SCHOLARLY_TRUSTED_DOMAINS))


def is_commentary_source(url: str) -> bool:
    """Check if a URL belongs to a commentary/fatwa site (not primary corpus)."""
    return bool(trusted_host(url, COMMENTARY_DOMAINS))


def classify_source_authority(url: str) -> tuple[str, str, str]:
    """Classify a URL into (source_name, authority, canonical_status).

    Returns:
        Tuple of (source_name, authority_label, canonical_status).
    """
    host = trusted_host(url, SCHOLARLY_TRUSTED_DOMAINS)
    if not host:
        return ("Unknown Source", "Unverified Web Source", "unverified")

    if host == "sunnah.com":
        return ("Sunnah.com", "Hadith Corpus Reference", "domain_verified")
    if host == "quran.com":
        return ("Quran.com", "Verified Tafseer Source", "verified")
    if host == "alquran.cloud":
        return ("AlQuran Cloud", "Quran API Source", "domain_verified")
    if host in {"islamqa.info", "islamqa.org"}:
        return ("IslamQA", "Scholarly Commentary", "unverified")
    if host == "seekersguidance.org":
        return ("SeekersGuidance", "Scholarly Commentary", "unverified")
    if host == "al-maktaba.org":
        return ("Al-Maktaba", "Classical Library", "domain_verified")

    return (host, "Web Source", "unverified")

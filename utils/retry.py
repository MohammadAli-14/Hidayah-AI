"""
Hidayah AI — Retry utility for HTTP requests.
Provides exponential-backoff retry for transient API failures.
"""

import time
import requests
from utils.logger import get_logger

log = get_logger("retry")

_DEFAULT_RETRIES = 2
_DEFAULT_BACKOFF = 0.5  # seconds, doubles each retry


def get_with_retry(
    url: str,
    *,
    headers: dict | None = None,
    params: dict | None = None,
    timeout: int = 15,
    retries: int = _DEFAULT_RETRIES,
    backoff: float = _DEFAULT_BACKOFF,
    label: str = "",
) -> requests.Response:
    """requests.get with automatic retry on transient HTTP errors.

    Retries on: 429 (rate-limit), 500, 502, 503, 504, ConnectionError, Timeout.
    Raises the last exception if all retries are exhausted.
    """
    last_exc: Exception | None = None
    for attempt in range(1, retries + 2):  # retries + 1 total attempts
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=timeout)
            if resp.status_code in (429, 500, 502, 503, 504) and attempt <= retries:
                wait = backoff * (2 ** (attempt - 1))
                log.warning(
                    "%s HTTP %s on attempt %d/%d — retrying in %.1fs",
                    label, resp.status_code, attempt, retries + 1, wait,
                )
                time.sleep(wait)
                continue
            return resp
        except (requests.ConnectionError, requests.Timeout) as exc:
            last_exc = exc
            if attempt <= retries:
                wait = backoff * (2 ** (attempt - 1))
                log.warning(
                    "%s %s on attempt %d/%d — retrying in %.1fs",
                    label, type(exc).__name__, attempt, retries + 1, wait,
                )
                time.sleep(wait)
            else:
                raise
    # Should not reach here, but just in case
    raise last_exc  # type: ignore[misc]

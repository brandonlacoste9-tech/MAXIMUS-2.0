"""
dispatch_bridge.py — MAXIMUS Sovereign Command
Tier-2 Logic: maps natural-language service requests to structured service
types using local LLM inference via Ollama.

Guarantees Digital Sovereignty: every inference call goes to the local Ollama
endpoint — no data leaves Québec soil.
"""

from __future__ import annotations

import logging
import re

import requests

logger = logging.getLogger(__name__)

# Canonical service types for the Québec labour marketplace
SERVICE_TYPES: list[str] = [
    "PLOMBERIE",
    "ÉLECTRICITÉ",
    "MÉNAGE",
    "DÉMÉNAGEMENT",
    "JARDINAGE",
    "RÉPARATION",
    "PEINTURE",
    "AUTRE",
]

# Keyword heuristics used as a fast offline fallback (Tier-1 Reflex)
_KEYWORD_MAP: dict[str, str] = {
    "plomb": "PLOMBERIE",
    "fuit": "PLOMBERIE",
    "tuyau": "PLOMBERIE",
    "robinet": "PLOMBERIE",
    "toilet": "PLOMBERIE",
    "électr": "ÉLECTRICITÉ",
    "electr": "ÉLECTRICITÉ",
    "courant": "ÉLECTRICITÉ",
    # déménagement must precede ménage — "déménager" contains "ménage"
    "déménag": "DÉMÉNAGEMENT",
    "demenag": "DÉMÉNAGEMENT",
    "moving": "DÉMÉNAGEMENT",
    "ménage": "MÉNAGE",
    "menage": "MÉNAGE",
    "nettoyage": "MÉNAGE",
    "clean": "MÉNAGE",
    "jardin": "JARDINAGE",
    "garden": "JARDINAGE",
    "gazon": "JARDINAGE",
    "répar": "RÉPARATION",
    "repar": "RÉPARATION",
    "bris": "RÉPARATION",
    "broken": "RÉPARATION",
    "peind": "PEINTURE",
    "peint": "PEINTURE",
    "paint": "PEINTURE",
}


def _keyword_fallback(text: str) -> str:
    """Tier-1 Reflex: fast keyword heuristic, no network required."""
    lower = text.lower()
    for kw, service in _KEYWORD_MAP.items():
        if kw in lower:
            return service
    return "AUTRE"


def classify_request(
    text: str,
    *,
    ollama_base_url: str = "http://localhost:11434",
    model: str = "mistral",
    system_prompt: str = "",
    timeout: int = 30,
) -> str:
    """
    Tier-2 Logic: classify *text* into a SERVICE_TYPE.

    Sends the request to Ollama for local LLM inference.  Falls back to the
    keyword heuristic if Ollama is unreachable or returns an unexpected answer.

    Parameters
    ----------
    text:             The client's natural-language service description.
    ollama_base_url:  Base URL of the running Ollama server.
    model:            Ollama model name to use (e.g. ``"mistral"``).
    system_prompt:    Override the default dispatch system prompt.
    timeout:          HTTP request timeout in seconds.

    Returns
    -------
    str
        One of the SERVICE_TYPES values (always uppercase).
    """
    if not text or not text.strip():
        return "AUTRE"

    try:
        payload = {
            "model": model,
            "prompt": text.strip(),
            "system": system_prompt,
            "stream": False,
        }
        response = requests.post(
            f"{ollama_base_url}/api/generate",
            json=payload,
            timeout=timeout,
        )
        response.raise_for_status()
        raw: str = response.json().get("response", "").strip()
        # Extract the first all-caps word from the LLM answer
        match = re.search(r"\b([A-ZÀÂÇÉÈÊËÎÏÔÛÙÜŸŒÆ]{2,})\b", raw)
        if match:
            candidate = match.group(1)
            if candidate in SERVICE_TYPES:
                return candidate
        logger.warning("LLM returned unexpected token %r — using fallback.", raw)
    except requests.RequestException as exc:
        logger.warning("Ollama unreachable (%s) — using keyword fallback.", exc)

    return _keyword_fallback(text)

"""
dispatch_bridge.py — MAXIMUS SOVEREIGN COMMAND
Tier-2 Logic Layer: maps natural-language service requests to structured
service types using local LLM inference via Ollama.

Supported service types
-----------------------
PLOMBERIE, ELECTRICITE, DEMENAGEMENT, NETTOYAGE, PEINTURE,
JARDINAGE, MENUISERIE, SERRURIER, INFORMATIQUE, AUTRE
"""

import json
import logging
from typing import Optional

import httpx

from config import OLLAMA_BASE_URL, OLLAMA_MODEL

logger = logging.getLogger(__name__)

# Canonical service catalogue (Quebec labour market)
SERVICE_CATALOGUE: list[str] = [
    "PLOMBERIE",
    "ELECTRICITE",
    "DEMENAGEMENT",
    "NETTOYAGE",
    "PEINTURE",
    "JARDINAGE",
    "MENUISERIE",
    "SERRURIER",
    "INFORMATIQUE",
    "AUTRE",
]

_SYSTEM_PROMPT = (
    "Tu es un assistant de classification de services québécois. "
    "Ton rôle est d'analyser une demande de service en langage naturel "
    "et de retourner UNIQUEMENT le type de service correspondant parmi cette liste:\n"
    + ", ".join(SERVICE_CATALOGUE)
    + "\n\nRègles:\n"
    "- Réponds avec un seul mot en majuscules (ex: PLOMBERIE).\n"
    "- Si la demande n'est pas claire, réponds AUTRE.\n"
    "- Aucune explication, aucun texte supplémentaire."
)


def classify_service(user_message: str, timeout: float = 15.0) -> str:
    """
    Call the local Ollama LLM to classify *user_message* into a service type.

    Parameters
    ----------
    user_message:
        Raw natural-language request from the user (French or English).
    timeout:
        HTTP request timeout in seconds.

    Returns
    -------
    A string from SERVICE_CATALOGUE (defaults to "AUTRE" on any error).
    """
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user_message.strip()},
        ],
        "stream": False,
    }

    try:
        with httpx.Client(base_url=OLLAMA_BASE_URL, timeout=timeout) as client:
            response = client.post("/api/chat", json=payload)
            response.raise_for_status()
            data = response.json()
            raw: str = data["message"]["content"].strip().upper()
    except httpx.HTTPError as exc:
        logger.error("Ollama HTTP error during classification: %s", exc)
        return "AUTRE"
    except (KeyError, json.JSONDecodeError) as exc:
        logger.error("Unexpected Ollama response format: %s", exc)
        return "AUTRE"

    # Normalise: return the first matching catalogue word found in the response
    for service in SERVICE_CATALOGUE:
        if service in raw:
            return service

    logger.warning("LLM returned unrecognised service '%s', defaulting to AUTRE", raw)
    return "AUTRE"


def build_dispatch_summary(user_message: str, service_type: str, user_id: int) -> str:
    """
    Return a human-readable French dispatch summary for internal dashboards.
    """
    return (
        f"🏛️ DISPATCH SOUVERAIN\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"👤 Utilisateur : {user_id}\n"
        f"📋 Demande     : {user_message}\n"
        f"🔧 Service     : {service_type}\n"
        f"━━━━━━━━━━━━━━━━━━━"
    )

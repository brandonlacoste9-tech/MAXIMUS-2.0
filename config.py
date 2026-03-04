"""
config.py — MAXIMUS SOVEREIGN COMMAND
Central configuration loader for all bot modules.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def _require(key: str) -> str:
    """Return env variable or raise a clear error if missing."""
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(
            f"Required environment variable '{key}' is not set. "
            "Copy .env.example to .env and fill in your values."
        )
    return value


# ── Telegram ─────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN: str = _require("TELEGRAM_BOT_TOKEN")

# ── Ollama LLM ───────────────────────────────────────────────
OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "mistral")

# ── Business Identity ────────────────────────────────────────
COMPANY_NAME: str = os.getenv("COMPANY_NAME", "MAXIMUS SOVEREIGN COMMAND")
SUPPORT_USERNAME: str = os.getenv("SUPPORT_USERNAME", "maximus_support")

# ── Lead Logger ──────────────────────────────────────────────
LEADS_DIR: str = os.getenv("LEADS_DIR", "data")

# ── Compliance ───────────────────────────────────────────────
CONSENT_TEXT: str = os.getenv(
    "CONSENT_TEXT",
    (
        "En utilisant ce service, vous consentez à la collecte de données "
        "conformément à la Loi 25 du Québec. / By using this service, you "
        "consent to data collection in accordance with Quebec Law 25."
    ),
)

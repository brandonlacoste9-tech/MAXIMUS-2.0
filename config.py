"""
config.py — MAXIMUS Sovereign Command
Central configuration loader.  Reads from environment variables (populated
from .env via python-dotenv) so no secrets ever touch source control.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- Telegram ---
TELEGRAM_BOT_TOKEN: str = os.environ["TELEGRAM_BOT_TOKEN"]

# --- Ollama (local LLM) ---
OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "mistral")

# --- Business ---
BUSINESS_NAME: str = os.getenv("BUSINESS_NAME", "MAXIMUS")
BUSINESS_TAGLINE: str = os.getenv(
    "BUSINESS_TAGLINE",
    "La Souveraineté Numérique au Service du Travail Québécois",
)

# --- Lead logging ---
LEADS_CSV_PATH: str = os.getenv("LEADS_CSV_PATH", "data/leads.csv")

# --- Dispatch system prompt ---
DISPATCH_SYSTEM_PROMPT: str = os.getenv(
    "DISPATCH_SYSTEM_PROMPT",
    (
        "You are MAXIMUS Dispatch, the AI brain of an autonomous labour marketplace "
        "operating under Québec law (Bill 96 / Law 25). "
        "Your task: analyse a client's natural-language service request written in "
        "French or English and return ONLY a single uppercase service-type keyword "
        "from this list:\n"
        "PLOMBERIE, ÉLECTRICITÉ, MÉNAGE, DÉMÉNAGEMENT, JARDINAGE, "
        "RÉPARATION, PEINTURE, AUTRE\n"
        "Reply with exactly one word. No explanation."
    ),
)

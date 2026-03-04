"""
bot.py — MAXIMUS Sovereign Command
Imperial Telegram Bot — the public face of the 4-pillar AI empire.

4-Tier Intelligence Stack
─────────────────────────
Tier 1 · Reflex  — Instant menu/keyboard responses (this file, ConversationHandler)
Tier 2 · Logic   — Business dispatch (dispatch_bridge.classify_request)
Tier 3 · Worker  — Persistence / dashboard (lead_logger.log_lead)
Tier 4 · Vision  — LLM inference via local Ollama (inside dispatch_bridge)

Run:
    python bot.py
"""

from __future__ import annotations

import logging

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

import config
import dispatch_bridge
import lead_logger

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Conversation states
# ---------------------------------------------------------------------------
MAIN_MENU, AWAITING_SERVICE_DESCRIPTION, AWAITING_TASKER_INFO = range(3)

# ---------------------------------------------------------------------------
# Keyboards
# ---------------------------------------------------------------------------

_MAIN_KEYBOARD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("🔧 Demander un Service", callback_data="dispatch")],
        [InlineKeyboardButton("💼 Devenir Tasker", callback_data="recruit")],
    ]
)

_BACK_KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🏛️ Retour au menu principal", callback_data="main_menu")]]
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_WELCOME = (
    "👑 *Bienvenue chez {name}*\n"
    "_{tagline}_\n\n"
    "Que souhaitez-vous faire aujourd'hui ?"
)

_SERVICE_PROMPT = (
    "✍️ Décrivez votre besoin en quelques mots.\n"
    "_(Ex : « Mon lavabo fuit », « Besoin d'un électricien », « Ménage complet »)_"
)

_SERVICE_CONFIRM = (
    "✅ *Demande enregistrée !*\n\n"
    "📋 Type de service détecté : `{service_type}`\n\n"
    "Un(e) Tasker qualifié(e) vous contactera sous peu. 🚀"
)

_TASKER_PROMPT = (
    "💼 *Rejoignez l'empire MAXIMUS !*\n\n"
    "Envoyez-nous votre *prénom, spécialité et ville* en un seul message.\n"
    "_(Ex : « Marie, Plomberie, Montréal »)_"
)

_TASKER_CONFIRM = (
    "🎉 *Candidature reçue !*\n\n"
    "Nous vous contacterons très prochainement. Bienvenue dans l'empire ! 🏛️"
)


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point — /start command."""
    await update.message.reply_text(
        _WELCOME.format(
            name=config.BUSINESS_NAME,
            tagline=config.BUSINESS_TAGLINE,
        ),
        parse_mode="Markdown",
        reply_markup=_MAIN_KEYBOARD,
    )
    return MAIN_MENU


async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle inline-button presses on the main menu."""
    query = update.callback_query
    await query.answer()

    if query.data == "dispatch":
        await query.edit_message_text(_SERVICE_PROMPT, parse_mode="Markdown")
        return AWAITING_SERVICE_DESCRIPTION

    if query.data == "recruit":
        await query.edit_message_text(_TASKER_PROMPT, parse_mode="Markdown")
        return AWAITING_TASKER_INFO

    if query.data == "main_menu":
        await query.edit_message_text(
            _WELCOME.format(
                name=config.BUSINESS_NAME,
                tagline=config.BUSINESS_TAGLINE,
            ),
            parse_mode="Markdown",
            reply_markup=_MAIN_KEYBOARD,
        )
        return MAIN_MENU

    return MAIN_MENU


async def receive_service_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Tier 2 + 3: classify the request and log the lead."""
    user = update.effective_user
    text = update.message.text

    # Tier 2 — Logic
    service_type = dispatch_bridge.classify_request(
        text,
        ollama_base_url=config.OLLAMA_BASE_URL,
        model=config.OLLAMA_MODEL,
        system_prompt=config.DISPATCH_SYSTEM_PROMPT,
    )

    # Tier 3 — Worker
    lead_logger.log_lead(
        csv_path=config.LEADS_CSV_PATH,
        user_id=user.id,
        username=user.username or user.full_name,
        action="DISPATCH_REQUEST",
        service_type=service_type,
        raw_text=text,
    )

    await update.message.reply_text(
        _SERVICE_CONFIRM.format(service_type=service_type),
        parse_mode="Markdown",
        reply_markup=_BACK_KEYBOARD,
    )
    return MAIN_MENU


async def receive_tasker_application(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Log the Tasker application and confirm."""
    user = update.effective_user
    text = update.message.text

    lead_logger.log_lead(
        csv_path=config.LEADS_CSV_PATH,
        user_id=user.id,
        username=user.username or user.full_name,
        action="TASKER_APPLICATION",
        raw_text=text,
    )

    await update.message.reply_text(
        _TASKER_CONFIRM,
        parse_mode="Markdown",
        reply_markup=_BACK_KEYBOARD,
    )
    return MAIN_MENU


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel and return to main menu."""
    await update.message.reply_text(
        "❌ Action annulée.",
        reply_markup=_BACK_KEYBOARD,
    )
    return ConversationHandler.END


# ---------------------------------------------------------------------------
# App bootstrap
# ---------------------------------------------------------------------------


def build_application() -> Application:
    """Construct and wire the Telegram Application."""
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(main_menu_callback),
            ],
            AWAITING_SERVICE_DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_service_request),
                CallbackQueryHandler(main_menu_callback, pattern="^main_menu$"),
            ],
            AWAITING_TASKER_INFO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_tasker_application),
                CallbackQueryHandler(main_menu_callback, pattern="^main_menu$"),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)
    return app


if __name__ == "__main__":
    application = build_application()
    logger.info("🏛️ MAXIMUS Sovereign Command — bot en ligne. Appuyez sur Ctrl+C pour arrêter.")
    application.run_polling()

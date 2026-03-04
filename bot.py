"""
bot.py — MAXIMUS SOVEREIGN COMMAND
Imperial Telegram Bot Framework

4-Tier Intelligence Stack
--------------------------
Tier 1 — Reflex  : instant menu responses (this file, lead_logger)
Tier 2 — Logic   : dispatch_bridge (LLM classification)
Tier 3 — Worker  : future task-matching engine (Q-MÉTIER / Q-EMPLOIS)
Tier 4 — Vision  : FLOGURU analytics & forecasting layer

Run
---
    python bot.py
"""

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
from dispatch_bridge import classify_service, build_dispatch_summary
from lead_logger import log_interaction

# ── Logging ───────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── Conversation states ───────────────────────────────────────
(
    STATE_MAIN_MENU,
    STATE_AWAITING_SERVICE_DESC,
    STATE_AWAITING_TASKER_INFO,
) = range(3)

# ── Callback data constants ───────────────────────────────────
CB_DISPATCH = "dispatch"
CB_RECRUITMENT = "recruitment"
CB_MAIN_MENU = "main_menu"


# ═══════════════════════════════════════════════════════════════
# Helper: build the main Imperial Menu keyboard
# ═══════════════════════════════════════════════════════════════

def _main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔧 Demander un Service (Dispatch)", callback_data=CB_DISPATCH
                )
            ],
            [
                InlineKeyboardButton(
                    "👷 Devenir Tasker (Recrutement)", callback_data=CB_RECRUITMENT
                )
            ],
        ]
    )


def _back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("⬅️ Menu Principal", callback_data=CB_MAIN_MENU)]]
    )


# ═══════════════════════════════════════════════════════════════
# /start handler
# ═══════════════════════════════════════════════════════════════

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point — display consent notice and Imperial Menu."""
    user = update.effective_user
    log_interaction(
        user_id=user.id,
        username=user.username or "",
        full_name=user.full_name,
        action="/start",
        pillar="MAX",
    )

    welcome = (
        f"👑 *Bienvenue dans {config.COMPANY_NAME}*\n\n"
        f"_{config.CONSENT_TEXT}_\n\n"
        "Que souhaitez-vous faire aujourd'hui ?"
    )
    await update.message.reply_text(
        welcome,
        parse_mode="Markdown",
        reply_markup=_main_menu_keyboard(),
    )
    return STATE_MAIN_MENU


# ═══════════════════════════════════════════════════════════════
# Inline button: Main Menu (return from sub-flows)
# ═══════════════════════════════════════════════════════════════

async def cb_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🏛️ *Menu Principal — MAXIMUS SOVEREIGN COMMAND*\n\n"
        "Choisissez une option :",
        parse_mode="Markdown",
        reply_markup=_main_menu_keyboard(),
    )
    return STATE_MAIN_MENU


# ═══════════════════════════════════════════════════════════════
# DISPATCH FLOW — Demander un Service
# ═══════════════════════════════════════════════════════════════

async def cb_dispatch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt the user to describe their service need."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🔧 *Demander un Service*\n\n"
        "Décrivez votre besoin en quelques mots.\n"
        "_Exemple : « Mon lavabo fuit » ou « J'ai besoin d'un électricien »_",
        parse_mode="Markdown",
        reply_markup=_back_keyboard(),
    )
    return STATE_AWAITING_SERVICE_DESC


async def handle_service_description(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Tier-2 Logic: classify the user's natural-language message,
    log the lead, and return a structured dispatch confirmation.
    """
    user = update.effective_user
    user_message = update.message.text

    # Tier-2: LLM classification
    service_type = classify_service(user_message)

    # Tier-1: log the lead
    log_interaction(
        user_id=user.id,
        username=user.username or "",
        full_name=user.full_name,
        action="DISPATCH",
        raw_message=user_message,
        service_type=service_type,
        pillar="Q-MÉTIER",
    )

    summary = build_dispatch_summary(user_message, service_type, user.id)
    response = (
        f"{summary}\n\n"
        f"✅ Votre demande de *{service_type}* a été enregistrée.\n"
        f"Un Tasker qualifié vous contactera sous peu.\n\n"
        f"Pour toute question : @{config.SUPPORT_USERNAME}"
    )

    await update.message.reply_text(
        response, parse_mode="Markdown", reply_markup=_main_menu_keyboard()
    )
    return STATE_MAIN_MENU


# ═══════════════════════════════════════════════════════════════
# RECRUITMENT FLOW — Devenir Tasker
# ═══════════════════════════════════════════════════════════════

async def cb_recruitment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt the prospective Tasker for their skills."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "👷 *Devenir Tasker — Q-EMPLOIS*\n\n"
        "Indiquez vos compétences et votre zone de service.\n"
        "_Exemple : « Plombier, Montréal, 5 ans d'expérience »_",
        parse_mode="Markdown",
        reply_markup=_back_keyboard(),
    )
    return STATE_AWAITING_TASKER_INFO


async def handle_tasker_info(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Log the Tasker application and confirm registration."""
    user = update.effective_user
    user_message = update.message.text

    log_interaction(
        user_id=user.id,
        username=user.username or "",
        full_name=user.full_name,
        action="RECRUITMENT",
        raw_message=user_message,
        pillar="Q-EMPLOIS",
    )

    await update.message.reply_text(
        "✅ *Candidature reçue !*\n\n"
        f"Merci *{user.first_name}*, votre profil Tasker a été enregistré dans "
        f"*Q-EMPLOIS*.\n\n"
        "Notre équipe examinera votre candidature et vous contactera bientôt.\n\n"
        f"Support : @{config.SUPPORT_USERNAME}",
        parse_mode="Markdown",
        reply_markup=_main_menu_keyboard(),
    )
    return STATE_MAIN_MENU


# ═══════════════════════════════════════════════════════════════
# /help command
# ═══════════════════════════════════════════════════════════════

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🏛️ *MAXIMUS SOVEREIGN COMMAND — Aide*\n\n"
        "• /start — Lancer le menu principal\n"
        "• /help  — Afficher ce message d'aide\n\n"
        f"Support : @{config.SUPPORT_USERNAME}",
        parse_mode="Markdown",
    )


# ═══════════════════════════════════════════════════════════════
# Application bootstrap
# ═══════════════════════════════════════════════════════════════

def build_application() -> Application:
    """Assemble and return the configured Telegram Application."""
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", cmd_start)],
        states={
            STATE_MAIN_MENU: [
                CallbackQueryHandler(cb_dispatch, pattern=f"^{CB_DISPATCH}$"),
                CallbackQueryHandler(cb_recruitment, pattern=f"^{CB_RECRUITMENT}$"),
            ],
            STATE_AWAITING_SERVICE_DESC: [
                CallbackQueryHandler(cb_main_menu, pattern=f"^{CB_MAIN_MENU}$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_service_description),
            ],
            STATE_AWAITING_TASKER_INFO: [
                CallbackQueryHandler(cb_main_menu, pattern=f"^{CB_MAIN_MENU}$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_tasker_info),
            ],
        },
        fallbacks=[CommandHandler("start", cmd_start)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("help", cmd_help))

    return app


def main() -> None:
    logger.info("🏛️ %s — Imperial Bot starting...", config.COMPANY_NAME)
    app = build_application()
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()

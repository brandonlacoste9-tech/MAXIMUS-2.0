import logging
import asyncio
import json
import os
import datetime
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import ollama

# Load Environment Variables from .env
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# --- BUSINESS CONFIGURATION ---
BUSINESS_NAME = os.getenv("BUSINESS_NAME", "🏛️ MAXIMUS SOVEREIGN COMMAND")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:latest")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# --- IMPERIAL INTEGRATIONS ---
from floguru_qemplois_bridge import FloguruDispatchBridge
dispatch_bridge = FloguruDispatchBridge()

# The "Imperial Brain"
BUSINESS_PROMPT = os.getenv("BUSINESS_PROMPT", f"You are the official AI Assistant for {BUSINESS_NAME}.")

def log_lead(user, niche="General"):
    """Save user info to the Lead Command Center logic."""
    lead_file = "leads.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lead_info = f"[{timestamp}] ID: {user.id} | User: @{user.username} | Name: {user.first_name} {user.last_name or ''} | Niche: {niche}\n"
    
    with open(lead_file, "a", encoding="utf-8") as f:
        f.write(lead_info)
    logger.info(f"New lead captured ({niche}): {user.username}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Imperial Greeting with Sovereign Menu."""
    user = update.effective_user
    log_lead(user, "User/Visitor")
    
    keyboard = [
        ["🛠️ Demander un Service", "💼 Devenir Tasker"],
        ["💰 Nos Tarifs", "🏛️ Maximus Empire"],
        ["🤖 Parler à l'IA"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        f"👑 Bienvenue au {BUSINESS_NAME}, {user.first_name}!\n\n"
        "Je suis MAXIMUS. Je coordonne l'économie du travail au Québec.\n"
        "Comment puis-je servir votre souveraineté aujourd'hui ?",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the Imperial Logic."""
    user_text = update.message.text
    user = update.effective_user
    
    # --- Imperial Menu Logic ---
    if user_text == "🛠️ Demander un Service":
        await update.message.reply_text(
            "Décrivez simplement votre problème (ex: 'Mon lavabo fuit' ou 'Besoin d'un électricien').\n"
            "Je vais identifier l'expert parfait pour vous."
        )
        return

    elif user_text == "💼 Devenir Tasker":
        log_lead(user, "Potential Tasker")
        await update.message.reply_text(
            "📍 **PROGRAMME FONDATEUR Q-EMPLOIS**\n\n"
            "Nous recrutons les 50 premiers experts (Plombiers, Électriciens, Menuisiers).\n"
            "• 60 crédits GRATUITS (Valeur 150$)\n"
            "• Priorité sur les leads locaux\n\n"
            "Envoyez votre numéro RBQ ou votre spécialité pour commencer l'enrôlement."
        )
        return

    elif user_text == "💰 Nos Tarifs":
        await update.message.reply_text(
            "Le modèle Maximus est simple :\n"
            "• Clients : Gratuit pour demander.\n"
            "• Pros : Système de crédits par mise en relation.\n"
            "Transparence totale. Pas de commissions cachées."
        )
        return

    elif user_text == "🏛️ Maximus Empire":
        await update.message.reply_text(
            "Maximus est le système d'exploitation de la souveraineté numérique québécoise.\n"
            "Nous construisons un futur où vos données et votre travail vous appartiennent.\n"
            "🌐 [En savoir plus](https://floguru.ai)"
        )
        return

    # --- Natural Language Dispatch Logic ---
    # Try to see if it's a service request using the bridge
    dispatch_result = dispatch_bridge.process_natural_request(user_text)
    
    if isinstance(dispatch_result, dict):
        service = dispatch_result.get('service_type', 'inconnu').upper()
        await update.message.reply_text(
            f"✅ **DÉPÊCHE IMPÉRIALE INITIÉE**\n\n"
            f"J'ai identifié un besoin en : **{service}**.\n"
            "Un de nos experts 'Fondateurs' va être alerté immédiatement.\n"
            "Restez en ligne pour la confirmation."
        )
        log_lead(user, f"Service Request: {service}")
        return

    # --- AI Chat Fallback ---
    logger.info(f"Imperial AI thinking for {user.id}: {user_text}")
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        response = ollama.chat(model=OLLAMA_MODEL, messages=[
            {'role': 'system', 'content': BUSINESS_PROMPT},
            {'role': 'user', 'content': user_text},
        ])
        
        reply_text = response['message']['content']
        await update.message.reply_text(reply_text)
    except Exception as e:
        logger.error(f"Ollama Error: {e}")
        await update.message.reply_text("Le système est en maintenance impériale. Réessayez dans un instant.")

def main():
    """Start the Maximus Imperial Bot."""
    print(f"--- 🏛️ Starting {BUSINESS_NAME} ---", flush=True)
    
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found!")
        return
    
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("👑 Maximus is LIVE. Operation Quebecois Takeover active!", flush=True)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

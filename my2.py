import os
import random
import threading
from fastapi import FastAPI
import uvicorn
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ======================
# FastAPI Health Check (Prevents Render sleep)
# ======================
app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "active", "bot": "CEFR Bot"}

def run_server():
    port = int(os.getenv("PORT", 8000))  # Render-compatible port
    uvicorn.run(app, host="0.0.0.0", port=port)

# ======================
# Bot Configuration
# ======================
TOKEN = "7866049366:AAEpeVkO_7Pi8ikS3hLnWOLGSCGynp2H9g4"  # Replace with token from @BotFather
QUESTIONS_FILE = "part1_questions1.txt"

# Load questions
with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
    QUESTIONS = [line.strip() for line in f if line.strip()]

# ======================
# Bot Handlers
# ======================
def generate_question():
    return random.choice(QUESTIONS), InlineKeyboardMarkup([
        [InlineKeyboardButton("Next Question ➡️", callback_data="next")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question, markup = generate_question()
    await update.message.reply_text(question, reply_markup=markup)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    question, markup = generate_question()
    await query.edit_message_text(question, reply_markup=markup)

# ======================
# Main Execution
# ======================
def main():
    # Start health check server
    threading.Thread(target=run_server, daemon=True).start()
    
    # Initialize bot
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_button, pattern="^next$"))
    
    print("🟢 Bot is running with health checks!")
    application.run_polling()

if __name__ == "__main__":
    main()

import random
import os
import threading
from fastapi import FastAPI
import uvicorn
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Health Check
app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "Part1 Bot is online"}

# Load questions
with open("part1_questions1.txt", "r", encoding="utf-8") as f:
    QUESTIONS = [line.strip() for line in f if line.strip()]

# Config
TOKEN = os.getenv("7866049366:AAEpeVkO_7Pi8ikS3hLnWOLGSCGynp2H9g4")  # Set in Render

def get_question_markup():
    question = random.choice(QUESTIONS)
    button = InlineKeyboardButton("Next question ➡️", callback_data="next_question")
    return question, InlineKeyboardMarkup([[button]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        question, markup = get_question_markup()
        await update.message.reply_text(question, reply_markup=markup)
    except Exception as e:
        await update.message.reply_text("⚠️ Error loading questions. Try again later.")
        print(f"Error: {e}")

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    question, markup = get_question_markup()
    await query.edit_message_text(text=question, reply_markup=markup)

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

def main():
    threading.Thread(target=run_server, daemon=True).start()
    
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button, pattern="^next_question$"))
    print("Bot is running with health checks...")
    app.run_polling()

if __name__ == "__main__":
    main()

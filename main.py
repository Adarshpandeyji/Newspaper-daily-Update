import requests
from bs4 import BeautifulSoup
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram Bot API token
BOT_TOKEN = '6304691403:AAFjHrYRlbf8Z9ysJJ0kgTj5GTLbknvw_5c'

# States for the conversation
SELECTING_NEWSPAPER, SELECTING_DATE = range(2)

def get_today_newspapers():
    try:
        response = requests.get('https://www.dailyepaper.in/news-home/')
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        newspapers = soup.select('.newsdate > a')
        return [newspaper.text.strip() for newspaper in newspapers]
    except Exception as e:
        print("Error fetching newspapers:", e)
        return []

def start(update: Update, _: CallbackContext):
    update.message.reply_text("Welcome to the Daily Newspaper Bot! Type /todaynews to get today's newspaper options.")
    return SELECTING_NEWSPAPER

def todaynews(update: Update, _: CallbackContext):
    available_newspapers = get_today_newspapers()

    if not available_newspapers:
        update.message.reply_text("No newspapers available today.")
        return ConversationHandler.END

    options_text = "\n".join([f"{i + 1}. {newspaper}" for i, newspaper in enumerate(available_newspapers)])
    update.message.reply_text(f"Today's available newspapers:\n{options_text}\n\nPlease choose a newspaper by typing its number.")

    context.user_data['available_newspapers'] = available_newspapers
    return SELECTING_DATE

# The rest of the script remains the same...

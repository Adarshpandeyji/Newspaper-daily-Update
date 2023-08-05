import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram Bot API token
BOT_TOKEN = '6205563150:AAEcvLABRAyg6wgP74GvvKGzDbhzXoiEj8I'
CHANNEL_ID = '@hxzhsvsgsf'  # Replace with your channel username or ID
DAILY_EPAPER_URL = 'https://www.dailyepaper.in/news-home/'  # Website URL where daily newspapers are hosted

def get_newspaper_link():
    response = requests.get(DAILY_EPAPER_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    newspaper_link = soup.select_one('.title > a')['href']
    return newspaper_link

def download_newspaper(link):
    response = requests.get(link)
    response.raise_for_status()
    return response.content

def start(update: Update, _: CallbackContext):
    update.message.reply_text("Welcome to the Daily Newspaper Bot! Type /today to receive today's newspaper.")

def today(update: Update, _: CallbackContext):
    try:
        newspaper_link = get_newspaper_link()
        newspaper = download_newspaper(newspaper_link)
        bot = Bot(token=BOT_TOKEN)
        bot.send_document(chat_id=CHANNEL_ID, document=newspaper, caption="Here's today's newspaper!")
    except Exception as e:
        update.message.reply_text("Sorry, there was an error while fetching the newspaper. Please try again later.")

def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("today", today))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

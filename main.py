import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import CommandHandler, CallbackContext

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram Bot API token
BOT_TOKEN = 'YOUR_BOT_TOKEN'
CHANNEL_ID = '@your_channel_name'  # Replace with your channel username or ID
DAILY_EPAPER_URL = 'https://www.dailyepaper.in/news-home/'  # Website URL where daily newspapers are hosted

def get_today_newspaper_link():
    response = requests.get(DAILY_EPAPER_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    today_newspaper_link = soup.select_one('.newsdate > a')['href']
    return today_newspaper_link

def download_newspaper(link):
    response = requests.get(link)
    response.raise_for_status()
    return response.content

def start(update: Update, _: CallbackContext):
    update.message.reply_text("Welcome to the Daily Newspaper Bot!")

def todaynewspaper(update: Update, _: CallbackContext):
    try:
        today_newspaper_link = get_today_newspaper_link()
        newspaper = download_newspaper(today_newspaper_link)
        bot = Bot(token=BOT_TOKEN)
        bot.send_document(chat_id=CHANNEL_ID, document=newspaper, caption="Today's newspaper!")
    except Exception as e:
        update.message.reply_text("Sorry, there was an error while sending the newspaper. Please try again later.")

def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("todaynewspaper", todaynewspaper))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
    

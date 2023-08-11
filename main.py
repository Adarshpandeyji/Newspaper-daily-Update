import requests
from bs4 import BeautifulSoup
from datetime import datetime, time
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram Bot API token
BOT_TOKEN = '6304691403:AAFjHrYRlbf8Z9ysJJ0kgTj5GTLbknvw_5c'
DAILY_EPAPER_URL = 'https://www.dailyepaper.in/news-home/'  # Website URL where daily newspapers are hosted

def get_newspapers_after_7am():
    try:
        response = requests.get(DAILY_EPAPER_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        newspapers = soup.select('.newsdate > a')
        newspapers_after_7am = []

        for newspaper in newspapers:
            upload_time = newspaper.find_previous(class_='time')  # Assuming the time is included as a class
            if upload_time:
                upload_time = datetime.strptime(upload_time.text.strip(), '%I:%M %p').time()
                if upload_time >= time(7, 0):
                    newspapers_after_7am.append(newspaper['href'])

        return newspapers_after_7am
    except Exception as e:
        print("Error fetching newspapers:", e)
        return []

def start(update: Update, _: CallbackContext):
    update.message.reply_text("Welcome to the Daily Newspaper Bot!")

def todaynews(update: Update, _: CallbackContext):
    newspapers = get_newspapers_after_7am()

    if not newspapers:
        update.message.reply_text("No newspapers available after 7 AM today.")
    else:
        bot = Bot(token=BOT_TOKEN)
        for newspaper_link in newspapers:
            bot.send_message(chat_id=update.effective_chat.id, text=newspaper_link)

def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("todaynews", todaynews))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

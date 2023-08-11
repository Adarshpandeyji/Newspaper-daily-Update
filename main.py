import requests
from bs4 import BeautifulSoup
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram Bot API token
BOT_TOKEN = '6304691403:AAFjHrYRlbf8Z9ysJJ0kgTj5GTLbknvw_5c'

# States for the conversation
SELECTING_NEWSPAPER, SELECTING_DATE = range(2)

def get_today_newspapers():
    response = requests.get('https://www.dailyepaper.in/news-home/')
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    newspapers = soup.select('.newsdate > a')
    return [newspaper.text.strip() for newspaper in newspapers]

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

def select_newspaper(update: Update, context: CallbackContext):
    selected_newspaper_index = int(update.message.text) - 1
    available_newspapers = context.user_data.get('available_newspapers', [])

    if 0 <= selected_newspaper_index < len(available_newspapers):
        selected_newspaper = available_newspapers[selected_newspaper_index]
        context.user_data['selected_newspaper'] = selected_newspaper
        update.message.reply_text(f"You've selected {selected_newspaper}. Please enter the date in the format DD-MM-YYYY.")

        return SELECTING_DATE
    else:
        update.message.reply_text("Invalid selection. Please choose a valid newspaper number.")

def select_date(update: Update, context: CallbackContext):
    selected_date = update.message.text.strip()

    selected_newspaper = context.user_data.get('selected_newspaper')
    newspaper_pdf_link = f"https://www.dailyepaper.in/{selected_newspaper.lower()}/{selected_date}.pdf"

    bot = Bot(token=BOT_TOKEN)
    bot.send_message(chat_id=update.effective_chat.id, text=f"Here's the PDF link for {selected_newspaper} dated {selected_date}:\n{newspaper_pdf_link}")

    return ConversationHandler.END

def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_NEWSPAPER: [CommandHandler('todaynews', todaynews)],
            SELECTING_DATE: [MessageHandler(Filters.text & ~Filters.command, select_date)],
        },
        fallbacks=[],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

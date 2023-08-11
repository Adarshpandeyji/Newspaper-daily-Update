import requests
from bs4 import BeautifulSoup
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram Bot API token
BOT_TOKEN = '6304691403:AAFjHrYRlbf8Z9ysJJ0kgTj5GTLbknvw_5c'
CHANNEL_ID = '@newspapertest'  # Replace with your channel username or ID
DAILY_EPAPER_URL = 'https://www.dailyepaper.in/news-home/'  # Website URL where daily newspapers are hosted

# States for the conversation
SELECTING_PAPER = 1

def get_available_papers():
    response = requests.get(DAILY_EPAPER_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    papers = soup.select('.newsdate > a')
    return [paper['href'] for paper in papers]

def start(update: Update, _: CallbackContext):
    update.message.reply_text("Welcome to the Daily Newspaper Bot! Type /todaynewspaper to receive today's e-paper options.")
    return SELECTING_PAPER

def todaynewspaper(update: Update, context: CallbackContext):
    available_papers = get_available_papers()

    if not available_papers:
        update.message.reply_text("No e-papers available today.")
        return ConversationHandler.END

    options_text = "\n".join([f"{i + 1}. {paper}" for i, paper in enumerate(available_papers)])
    update.message.reply_text(f"Today's available e-papers:\n{options_text}\n\nPlease choose a paper by typing its number.")

    context.user_data['available_papers'] = available_papers
    return SELECTING_PAPER

def select_paper(update: Update, context: CallbackContext):
    selected_paper_index = int(update.message.text) - 1
    available_papers = context.user_data.get('available_papers', [])

    if 0 <= selected_paper_index < len(available_papers):
        selected_paper_link = available_papers[selected_paper_index]
        newspaper = download_newspaper(selected_paper_link)
        bot = Bot(token=BOT_TOKEN)
        bot.send_document(chat_id=CHANNEL_ID, document=newspaper, caption="Here's the selected e-paper!")
    else:
        update.message.reply_text("Invalid selection. Please choose a valid paper number.")

    return ConversationHandler.END

def download_newspaper(link):
    response = requests.get(link)
    response.raise_for_status()
    return response.content

def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_PAPER: [CommandHandler('todaynewspaper', todaynewspaper)],
            MessageHandler(Filters.text & ~Filters.command, select_paper),
        },
        fallbacks=[],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

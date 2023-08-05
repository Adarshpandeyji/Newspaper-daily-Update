import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram Bot API token
BOT_TOKEN = '6095676994:AAHSBNTqxITrrq54Wg7STJzggX0zLEWzQcc'
CHANNEL_ID = '@hxzhsvsgsf'  # Replace with your channel username or ID
DAILY_NEWS_URLS = [
    'https://newsonair.gov.in/hindi/Hindi-Default.aspx#collapseOne',
    'https://newsonair.gov.in/hindi/Hindi-Default.aspx#collapseTwo'
]
DAILY_EPAPER_URL = 'https://www.dailyepaper.in/news-home/'  # Website URL where daily newspapers are hosted

def get_news_headlines():
    news_headlines = []
    for url in DAILY_NEWS_URLS:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = soup.select('.vertical-ticker h4')
        news_headlines.extend([headline.text.strip() for headline in headlines])
    return '\n'.join(news_headlines)

def get_newspaper_link():
    response = requests.get(DAILY_EPAPER_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    newspaper_link = soup.select_one('.title > a')
    if newspaper_link:
        return newspaper_link['href']
    else:
        return None

def download_newspaper(link):
    response = requests.get(link)
    response.raise_for_status()
    return response.content

def main():
    bot = Bot(token=BOT_TOKEN)

    while True:
        try:
            news_headlines = get_news_headlines()
            newspaper_link = get_newspaper_link()

            if newspaper_link:
                newspaper = download_newspaper(newspaper_link)

                # Send news headlines and newspaper as separate messages
                bot.send_message(chat_id=CHANNEL_ID, text="**Today's News Headlines:**\n" + news_headlines, parse_mode="Markdown")
                bot.send_document(chat_id=CHANNEL_ID, document=newspaper, caption="Here's today's newspaper!")
            else:
                print("Newspaper link not found.")
        except Exception as e:
            print("Error while fetching updates:", e)

        # Wait for 24 hours before sending the next update
        time.sleep(24 * 60 * 60)

if __name__ == "__main__":
    main()

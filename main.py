import requests
from bs4 import BeautifulSoup
import re
import os

# URL of the main page
BASE_URL = 'https://www.dailyepaper.in/news-home/'

def download_newspapers(language):
    try:
        url = BASE_URL + language
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        newspapers = soup.find_all('a', href=re.compile(r'\/' + language + r'\/\d{2}-\d{2}-\d{4}'))

        if not newspapers:
            print(f"No newspapers available in {language} today.")
            return

        print(f"Downloading newspapers in {language}...")

        for newspaper in newspapers:
            newspaper_url = newspaper['href']
            response = requests.get(newspaper_url)
            response.raise_for_status()

            # Create a folder for each language
            language_folder = os.path.join(os.getcwd(), language)
            os.makedirs(language_folder, exist_ok=True)

            # Extract the date from the URL and use it as the filename
            filename = os.path.join(language_folder, os.path.basename(newspaper_url)) + '.pdf'

            with open(filename, 'wb') as f:
                f.write(response.content)

            print(f"Downloaded: {filename}")

        print(f"Downloaded all newspapers in {language}.")

    except Exception as e:
        print("Error:", e)

def main():
    languages = ['english', 'hindi', 'telugu', 'tamil']  # Add more languages as needed

    for language in languages:
        download_newspapers(language)

if __name__ == "__main__":
    main()


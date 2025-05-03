import requests
from bs4 import BeautifulSoup
import csv

def scrape_quotes(url="http://quotes.toscrape.com"):
    """
    Scrapes quotes from the given URL and returns a list of dictionaries.
    Also saves the data to a CSV file.
    """
    try:
        # Send HTTP request
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad status codes

        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')

        # Extract data
        quotes_data = []
        for quote in quotes:
            text = quote.find('span', class_='text').get_text(strip=True)
            author = quote.find('small', class_='author').get_text(strip=True)
            quotes_data.append({'text': text, 'author': author})

        # Save to CSV
        with open('quotes.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['text', 'author'])
            writer.writeheader()
            writer.writerows(quotes_data)

        return quotes_data

    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []
    except Exception as e:
        print(f"Error parsing data: {e}")
        return []

if __name__ == "__main__":
    # Test the scraper
    data = scrape_quotes()
    print(data)
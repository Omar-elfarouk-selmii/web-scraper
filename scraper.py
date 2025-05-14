import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse
import os
import time

def get_safe_filename(url):
    """Generate a safe filename from URL"""
    parsed = urlparse(url)
    domain = parsed.netloc.replace(".", "_")
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    return f"scraped_{domain}_{timestamp}.csv"

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

        # Generate unique filename
        filename = get_safe_filename(url)
        
        # Save to CSV
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['text', 'author'])
            writer.writeheader()
            writer.writerows(quotes_data)

        return {'data': quotes_data, 'filename': filename}

    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return {'error': str(e)}
    except Exception as e:
        print(f"Error parsing data: {e}")
        return {'error': str(e)}

def scrape_any_website(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all text content
        text_content = []
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = tag.get_text(strip=True)
            if text:  # Only include non-empty text
                text_content.append({'content': text})

        # Generate unique filename
        filename = get_safe_filename(url)

        # Save to CSV
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['content'])
            writer.writeheader()
            writer.writerows(text_content)

        return {'data': text_content, 'filename': filename}

    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    # Test the scraper
    result = scrape_quotes()
    print(result)
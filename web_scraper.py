from bs4 import BeautifulSoup

# Define the scrape_quotes function
def scrape_quotes(file_path):
    """
    Scrapes quotes and authors from a local HTML file.
    Returns a list of dictionaries with 'author' and 'quote'.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        quotes = soup.find_all('div', class_='quote')
        data = []

        for quote in quotes:
            text = quote.find('span', class_='text').get_text(strip=True)
            author = quote.find('small', class_='author').get_text(strip=True)
            data.append({'author': author, 'quote': text})

        return data

    except Exception as e:
        print(f"Error during scraping: {e}")
        return []

# Example usage
if __name__ == "__main__":
    file_path = r"C:\Users\agerb\OneDrive\Bureau\work\quotes.html"  # Raw string literal
    results = scrape_quotes(file_path)
    for item in results:
        print(f"{item['author']}: {item['quote']}")


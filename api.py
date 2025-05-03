from flask import Flask, jsonify, send_file, request
from scraper import scrape_quotes
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

app = Flask(__name__)

# Rate limiting for security
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

# Cache scraped data
QUOTES_DATA = scrape_quotes()

@app.route('/quotes', methods=['GET'])
@limiter.limit("10 per minute")
def get_all_quotes():
    """Returns all scraped quotes as JSON."""
    return jsonify(QUOTES_DATA)

@app.route('/quotes/<string:author>', methods=['GET'])
@limiter.limit("10 per minute")
def get_quotes_by_author(author):
    """Returns quotes for a specific author (case-insensitive)."""
    if not author or len(author) > 50:  # Input validation
        return jsonify({"message": "Invalid author name."}), 400
    filtered = [q for q in QUOTES_DATA if q['author'].lower() == author.lower()]
    if filtered:
        return jsonify(filtered)
    else:
        return jsonify({"message": "No quotes found for this author."}), 404

@app.route('/scrape', methods=['POST'])
@limiter.limit("5 per minute")
def scrape_url():
    """Scrapes a given URL and returns the data."""
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"message": "URL is required."}), 400
    
    url = data['url']
    if not url.startswith('http://quotes.toscrape.com'):
        return jsonify({"message": "Only quotes.toscrape.com is allowed."}), 403
    
    try:
        quotes = scrape_quotes(url)
        return jsonify(quotes)
    except Exception as e:
        return jsonify({"message": f"Scraping failed: {str(e)}"}), 500

@app.route('/download', methods=['GET'])
def download_csv():
    """Downloads the scraped quotes as a CSV file."""
    if os.path.exists('quotes.csv'):
        return send_file('quotes.csv', as_attachment=True)
    else:
        return jsonify({"message": "No data available to download."}), 404

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, jsonify, send_file, request,render_template
from scraper import scrape_quotes,scrape_any_website
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from pprint import pprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Rate limiting for security
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

# Cache scraped data
QUOTES_DATA = scrape_quotes()
pprint(QUOTES_DATA)
@app.route('/',methods=['GET'])
def get_site():
    return render_template("index.html")


@app.route('/quotes', methods=['post'])
@limiter.limit("10 per minute")
def get_all_quotes():
    """Returns all scraped quotes as JSON."""
    url=request.form['url']
    QUOTES_DATA = scrape_quotes(url)
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
def scrape_url():
    """Scrapes a given URL and returns the data."""
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"message": "URL is required."}), 400
    
    url = data['url']
    if url=="http://quotes.toscrape.com":
        quotes = scrape_quotes(url)
        return jsonify(quotes)
    else:
        # print('"""""""""""""""')

        # url=request.form.get('url')
        # print(url)
        # print('"""""""""""""""')
        try:
            quotes = scrape_any_website(url)
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
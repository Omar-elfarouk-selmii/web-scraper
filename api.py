from flask import Flask, jsonify, send_file, request, render_template
from scraper import scrape_quotes, scrape_any_website
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from pprint import pprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Rate limiting for security
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

@app.route('/', methods=['GET'])
def get_site():
    return render_template("index.html")

@app.route('/quotes', methods=['POST'])
@limiter.limit("10 per minute")
def get_all_quotes():
    """Returns all scraped quotes as JSON."""
    url = request.form['url']
    result = scrape_quotes(url)
    return jsonify(result)

@app.route('/scrape', methods=['POST'])
def scrape_url():
    """Scrapes a given URL and returns the data."""
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"message": "URL is required."}), 400
    
    url = data['url']
    if url == "http://quotes.toscrape.com":
        result = scrape_quotes(url)
    else:
        try:
            result = scrape_any_website(url)
        except Exception as e:
            return jsonify({"message": f"Scraping failed: {str(e)}"}), 500
    
    if 'error' in result:
        return jsonify({"message": f"Scraping failed: {result['error']}"}), 500
    
    # Store the filename in the session
    app.config['LAST_SCRAPED_FILE'] = result.get('filename')
    return jsonify(result)

@app.route('/download', methods=['GET'])
def download_csv():
    """Downloads the most recently scraped file."""
    filename = app.config.get('LAST_SCRAPED_FILE')
    if filename and os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({"message": "No data available to download."}), 404

if __name__ == '__main__':
    app.run(debug=True)
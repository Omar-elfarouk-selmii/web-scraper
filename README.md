# 🕸️ Web Scraper

A Python-based web scraper for collecting and exporting structured data from various websites like **quotes.toscrape.com** and **medium.com**. Built with a simple UI and flexible logic to support multiple sources.

## 🔍 Features

* Extracts quotes, authors, and tags
* CSV export support
* Clean UI (HTML/CSS templates)
* Basic API setup (`api.py`)

## 🗂️ Project Structure

```
📁 static/           → CSS and static files  
📁 templates/        → HTML templates (UI)  
📄 scraper.py        → Main scraping logic  
📄 api.py            → REST API endpoints  
📄 requirements.txt  → Dependencies  
📄 *.csv             → Scraped data output  
```

## ▶️ Usage

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**

   ```bash
   python api.py
   ```

3. Visit the local server to access the UI and start scraping.

## 📎 Notes

* Sample output is saved in `.csv` files
* Educational/demo purposes only — respect website terms of service

## 📄 Resources

* [`Project-security.pdf`](./Project-security.pdf)
* [`Web_scrapper_2_-1.pdf`](./Web_scrapper_2_-1.pdf)



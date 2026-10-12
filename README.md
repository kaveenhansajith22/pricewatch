
# PriceWatch

PriceWatch is a Python portfolio project for automated price monitoring.

## Current Features

- Fetch product listing pages with Requests.
- Extract product names and prices with Beautiful Soup.
- Validate price values.
- Log errors and extraction counts.

## Technology Stack

- Python
- Requests
- Beautiful Soup
- SQLite (planned)
- CSV and Excel exports (planned)
- Automated scheduling (planned)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/pricewatch.git
cd pricewatch
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the scraper

```bash
python scraper.py
```

## Project Status

In development. The current version scrapes a practice website. Database-backed price history, scheduled execution, and reporting are planned.

## Practice Website

[Books to Scrape](https://books.toscrape.com/)

This project is for learning and portfolio demonstration.
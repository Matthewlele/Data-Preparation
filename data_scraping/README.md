## Data Scraper

This project is a web scraping tool designed to extract bicycle product information from the Bike-Discount.de e-commerce website. The scraper consists of two main components: one for collecting product URLs and another for extracting detailed product specifications. The extracted data is formatted as TSV (Tab-Separated Values) for easy analysis and processing.

### Data Structure

**TSV Header:** `URL | title | price | frame | frame_material | wheel_size | maximum_total_weight_allowed | weight`

**Column Descriptions:**
- **URL** - Product URL that was processed
- **title** - Product name
- **price** - Current product price
- **frame** - Bike frame description, frame brand, frame geometry
- **frame_material** - Bike frame material
- **wheel_size** - Bike wheel size
- **maximum_total_weight_allowed** - Maximum allowed system weight (bike + luggage + rider)
- **weight** - Bike weight

### Implementation Overview:

This project consists of two main Python scripts for scraping bicycle product data from Bike-Discount.de:

#### 1. `product_url_scraper.py`
- Scrapes product URLs from category pages
- Implements asynchronous HTTP requests for better performance
- Uses rate limiting to avoid overloading the server (max 3 requests/second, 5 concurrent)
- Accepts command-line argument `--num_pages` to specify how many pages to scrape
- Outputs product URLs to stdout (can be redirected to `urls.txt`)
- Default scrapes 10 pages

#### 2. `product_info_scraper.py`
- Scrapes detailed product information from individual product URLs
- Extracts: title, price, frame details, frame material, wheel size, weight limits, and bike weight
- Reads URLs from a file (specified with `--urls` parameter)
- Implements error handling for failed requests
- Outputs data in TSV format to stdout
- Accepts `--max` parameter to limit number of products to scrape
- Uses the same rate limiting strategy as the URL scraper


### Usage

1. **Extract product URLs:**
   ```bash
   python product_url_scraper.py --num_pages 10 > urls.txt
   ```

2. **Scrape product details:**
   ```bash
   python product_info_scraper.py --urls urls.txt --max 100 > data.tsv
   ```

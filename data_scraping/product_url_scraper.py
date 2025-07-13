import sys
import httpx
import asyncio
import aiometer
import argparse
import functools
from bs4 import BeautifulSoup


sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = 'https://www.bike-discount.de/en/bike'
NUM_PAGES_TO_SCRAPE = 10
TRANSPORT = httpx.AsyncHTTPTransport(retries=3)


def build_urls_to_scrape(base_url=BASE_URL, num_pages_to_scrape=NUM_PAGES_TO_SCRAPE):
    """
    Helper function to build urls for pages to scrape for product urls.
    """
    urls = []
    for i in range(1, num_pages_to_scrape + 1):
        urls.append(f'{base_url}?p={i}')
    return urls


async def scrape_product_url(client, url):
    """
    Scrape the product urls from the urls provided.
    """
    product_urls = []
    response = await client.get(url)
    product_urls += extract_product_urls_from_html(response.text)
    return product_urls


def extract_product_urls_from_html(html):
    """
    Extracts the product urls from the html provided.
    """
    product_urls = []
    soup = BeautifulSoup(html, 'html.parser')
    product_divs = soup.find_all('a', class_='product--image')
    for div in product_divs:
        product_urls.append(div['href'])
    return product_urls

    
async def scrape_product_urls(num_pages=NUM_PAGES_TO_SCRAPE):
    """
    Scrape the product urls from the pages provided.
    """
    urls = build_urls_to_scrape(num_pages_to_scrape=num_pages)
    
    async with httpx.AsyncClient(headers={'User-Agent': 'Mozilla/5.0'}, transport=TRANSPORT) as client:
        async with aiometer.amap(
            functools.partial(scrape_product_url, client),
            urls,
            max_at_once=5, # Limit maximum number of concurrently running tasks.
            max_per_second=3,  # Limit request rate to not overload the server.
        ) as results:
            async for page in results:
                for url in page:
                    print(url)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_pages', help='Number of pages to scrape.', type=int, default=None)
    args = parser.parse_args()
    num_pages = args.num_pages
    if num_pages is None:
        num_pages = NUM_PAGES_TO_SCRAPE
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(scrape_product_urls(num_pages))
    event_loop.close()
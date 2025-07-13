import sys
import httpx
import asyncio
import aiometer
import argparse
import functools
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')
TRANSPORT = httpx.AsyncHTTPTransport(retries=3)


async def scrape_product_info(client,url):
    """
    Scrape the product info from the url provided.
    """
    try:
        response = await client.get(url)
    except httpx.HTTPError as exc:
        return {'error': exc, 'url': url}
    
    if response.status_code != 200:
        return {'error': f'HTTP status code: {response.status_code}', 'url': url}
    
    try:
        product_info = extract_product_info_from_html(response.text)
    except Exception as exc:
        return {'error': 'html scraping failed', 'url': url}

    product_info['url'] = url
    return product_info


async def scrape_product_infos(urls):
    """
    Scrape the product info from the urls provided.
    """
    async with httpx.AsyncClient(headers={'User-Agent': 'Mozilla/5.0'}, transport=TRANSPORT) as client:
        async with aiometer.amap(
            functools.partial(scrape_product_info, client),
            urls,
            max_at_once=3, # Limit maximum number of concurrently running tasks.
            max_per_second=3,  # Limit request rate to not overload the server.
        ) as results:
            async for data in results:
                 if 'error' in data.keys():
                     data = {'url': data['url'], 'title': '', 'price': '', 'frame': '', 'frame_material': '', 'wheel_size': '', 'maximum_total_weight_allowed': '', 'weight': '' }
                 print('\t'.join(data.values()))



# function to extract data from html table and return a dictionary
def extract_product_info_from_html(html):
    """
    Extracts the product info from the html provided.
    """
    product_info = {'url': '', 'title': '', 'price': '', 'frame': '', 'frame_material': '', 'wheel_size': '', 'maximum_total_weight_allowed': '', 'weight': '' }
    soup = BeautifulSoup(html, 'html.parser')
   

    price_span = soup.find('span', id='netz-price')
    if price_span:
        product_info['price'] = price_span.text.strip()

    product_title = soup.find('h1', class_='product--title')
    if product_title:
        product_info['title'] = product_title.text.strip()

    product_info_tables = soup.find_all('table', class_='product--properties-table')
    product_info_rows = []

    if not product_info_tables:
        return product_info
    
    for product_info_table in product_info_tables:
        product_info_rows.extend(product_info_table.find_all('tr'))
    
    if not product_info_rows:
        return product_info

    for row in product_info_rows:
        key = row.find('td', class_='product--properties-label is--bold')
        if not key:
            continue
        key = key.text.strip('  \n:').lower().replace(' ', '_')
        if key in product_info.keys():
            value = row.find('td', class_='product--properties-value')
            if not value:
                continue
            value = value.text.strip()
            product_info[key] = value
  
    return product_info


def load_urls_from_file(url_file, max=1):
    """
    Load urls from file.
    """
    urls = []
    with open(url_file, 'r', encoding='utf-8') as f:
        for i in range(max):
            url = f.readline()
            if not url:
                break
            urls.append(url.strip())
    return urls

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max', help='Number of products to scrape.', type=int, default=None)
    parser.add_argument('--urls', help='File with urls to scrape', type=str, default=None)
    args = parser.parse_args()
    if args.urls is None:
        raise ValueError('Please provide a file with urls to scrape.')
    if args.max is None:
        args.max = 10
    urls = load_urls_from_file(args.urls, args.max)
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(scrape_product_infos(urls))
    event_loop.close()
    

    
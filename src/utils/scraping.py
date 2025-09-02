import re

import requests
from bs4 import BeautifulSoup

from src.core.config import PAGE_URL


def fetch_number_of_sources(page_url: str = PAGE_URL) -> int:
    """
    Fetch the number of STATCAN sources available.

    Parameters
    ----------
    page_url : str, optional
        URL of the STATCAN data page (default: PAGE_URL).

    Returns
    -------
    int
        Total number of sources.
    """
    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, 'lxml')
    result = re.search(r'\((.*?)\)', soup.summary.get_text()).group(1)
    return int(result.replace(',', ''))


def fetch_raw_data(
    url_template: str = 'https://www150.statcan.gc.ca/n1/en/type/data?count={}&p={}-All#all',
    sources_per_page: int = 100,
) -> list[dict]:
    """
    Fetch raw data records from STATCAN.

    Parameters
    ----------
    url_template : str, optional
        URL template for paginated STATCAN data.
    sources_per_page : int, optional
        Number of sources per page (default: 100).

    Returns
    -------
    list[dict]
        List of raw data records.
    """
    total_pages = 1 + fetch_number_of_sources() // sources_per_page
    records = []

    for page_idx in range(total_pages):
        print(f'Parsing Page {page_idx + 1:3} of {total_pages}')
        page = requests.get(url_template.format(sources_per_page, page_idx))
        soup = BeautifulSoup(page.text, 'lxml')
        details_soup = soup.find('details', id='all')
        items = details_soup.find_all('li', {'class': 'ndm-item'})

        for item in items:
            tag_description = item.find('div', class_='ndm-result-description')
            tag_former_id = item.find('div', class_='ndm-result-formerid')
            tag_frequency = item.find('div', class_='ndm-result-freq')
            tag_geo = item.find('div', class_='ndm-result-geo')

            records.append(
                {
                    'title': item.find('div', class_='ndm-result-title').get_text(),
                    'product_id': item.find('div', class_='ndm-result-productid').get_text(),
                    'former_id': tag_former_id and tag_former_id.get_text(),
                    'geo': tag_geo and tag_geo.get_text(),
                    'frequency': tag_frequency and tag_frequency.get_text(),
                    'description': tag_description and tag_description.get_text(),
                    'release_date': item.find('span', class_='ndm-result-date').get_text(),
                    'type': item.find('div', class_='ndm-result-productid').get_text().split(':')[0],
                    'ref': item.a.get('href'),
                }
            )
    print('Parsing Complete')
    return records

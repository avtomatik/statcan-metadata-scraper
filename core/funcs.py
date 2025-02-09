import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

from scraper.settings import ENDPOINT


def get_number_of_sources() -> int:
    """
    Retrieves Number of STATCAN Sources

    Returns
    -------
    int
        Number of STATCAN Sources.

    """
    page = requests.get(ENDPOINT)
    soup = BeautifulSoup(page.text, 'lxml')
    result = re.search(r'\((.*?)\)', soup.summary.get_text()).group(1)
    return int(result.replace(',', ''))


def combine_data(
    url_generic: str = '{ENDPOINT}?count={}&p={}-All#all',
    sources_per_page: int = 100,
) -> list[dict]:
    """
    Collects Data List

    Parameters
    ----------
    url_generic : str, optional
        DESCRIPTION. The default is '{ENDPOINT}?count={}&p={}-All#all'.
    sources_per_page : int, optional
        DESCRIPTION. The default is 100.

    Returns
    -------
    list[dict]

    """
    number_of_sources = get_number_of_sources()
    data_list = []
    for _ in range(1 + number_of_sources // sources_per_page):
        print(
            f'Parsing Page {1 + _:3} Out of {1 + number_of_sources // sources_per_page}'  # noqa: E501
        )
        page = requests.get(url_generic.format(sources_per_page, _))
        soup = BeautifulSoup(page.text, 'lxml')
        details_soup = soup.find('details', id='all')
        items = details_soup.find_all('li', {'class': 'ndm-item'})
        for item in items:
            tag_description = item.find('div', class_='ndm-result-description')
            tag_former_id = item.find('div', class_='ndm-result-formerid')
            tag_frequency = item.find('div', class_='ndm-result-freq')
            tag_geo = item.find('div', class_='ndm-result-geo')

            data_list.append(
                {
                    'title': item.find('div', class_='ndm-result-title').get_text(),  # noqa: E501
                    'product_id': item.find('div', class_='ndm-result-productid').get_text(),  # noqa: E501
                    'former_id': tag_former_id and tag_former_id.get_text(),
                    'geo': tag_geo and tag_geo.get_text(),
                    'frequency': tag_frequency and tag_frequency.get_text(),
                    'description': tag_description and tag_description.get_text(),  # noqa: E501
                    'release_date': item.find('span', class_='ndm-result-date').get_text(),  # noqa: E501
                    'type': item.find(
                        'div',
                        class_='ndm-result-productid'
                    ).get_text().split(':')[0],
                    'ref': item.a.get('href'),
                }
            )
    print('Parsing Complete')
    return data_list


def build_preprocess_dataframe(data_list: list[dict]) -> pd.DataFrame:
    """
    Builds DataFrame from Collected Data List

    Parameters
    ----------
    data_list : list[dict]

    Returns
    -------
    pd.DataFrame

    """
    data = pd.DataFrame.from_dict(data_list)
    data[['id', 'title_only']] = data['title'].str.split(
        pat='. ',
        n=1,
        expand=True
    )
    data['id'] = pd.to_numeric(data['id'].str.replace(',', ''))
    data['release_date'] = pd.to_datetime(
        data['release_date'],
        infer_datetime_format=False
    )
    return data.fillna('None')

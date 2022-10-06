#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 21:59:20 2021

@author: Alexander Mikhailov
"""

# =============================================================================
# STATCAN Sources Metadata Grabber through Web Scraping
# =============================================================================
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_number_of_sources(
        url: str = 'https://www150.statcan.gc.ca/n1/en/type/data'
) -> int:
    """
    Retrieves Number of STATCAN Sources

    Parameters
    ----------
    url : str, optional
        Link. The default is 'https://www150.statcan.gc.ca/n1/en/type/data'.

    Returns
    -------
    int
        Number of STATCAN Sources.

    """
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    result = re.search(r'\((.*?)\)', soup.summary.get_text()).group(1)
    return int(result.replace(',', ''))


def main(
    url_generic: str = 'https://www150.statcan.gc.ca/n1/en/type/data?count=100&p={}-All#all',
    file_name: str = 'stat_can_all.xlsx',
) -> None:
    """
    Builds Resulting DataFrame and Dumps It To Excel File

    Parameters
    ----------
    url_generic : str, optional
        DESCRIPTION. The default is 'https://www150.statcan.gc.ca/n1/en/type/data?count=100&p={}-All#all'.
    file_name : str, optional
        DESCRIPTION. The default is 'stat_can_all.xlsx'.

    Returns
    -------
    None
    """
    number_of_sources = get_number_of_sources()
    data_list = []
    for _ in range(1 + number_of_sources // 100):
        page = requests.get(url_generic.format(_))
        print(f'Parsing Page {1 + _:3} Out of {1 + number_of_sources // 100}')
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
                    'title': item.find('div', class_='ndm-result-title').get_text(),
                    'product_id': item.find('div', class_='ndm-result-productid').get_text(),
                    'former_id': tag_former_id and tag_former_id.get_text(),
                    'geo': tag_geo and tag_geo.get_text(),
                    'frequency': tag_frequency and tag_frequency.get_text(),
                    'description': tag_description and tag_description.get_text(),
                    'release_date': item.find('span', class_='ndm-result-date').get_text(),
                    'type': item.find(
                        'div',
                        class_='ndm-result-productid'
                    ).get_text().split(':')[0],
                    'ref': item.a.get('href'),
                }
            )

    data = pd.DataFrame.from_dict(data_list)
    data[['id', 'title_only']] = data.iloc[:, 0].str.split(
        pat='. ',
        n=1,
        expand=True
    )
    data['id'] = pd.to_numeric(data['id'].str.replace(',', ''))
    data.fillna('None').to_excel(file_name, index=False)


if __name__ == '__main__':
    main()

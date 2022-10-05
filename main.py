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


def get_number_of_sources() -> int:
    '''
    Retrieves Number of STATCAN Sources

    Returns
    -------
    int
        Number of STATCAN Sources.

    '''
    URL = 'https://www150.statcan.gc.ca/n1/en/type/data'
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'lxml')
    result = re.search(r'\((.*?)\)', soup.summary.get_text()).group(1)
    return int(result.replace(',', ''))


def main():
    '''
    Builds Resulting DataFrame and Dumps It To Excel File

    Returns
    -------
    None.
    '''
    FILE_NAME = 'stat_can_all.xlsx'
    number_of_sources = get_number_of_sources()
    data_list = []
    for _ in range(1 + number_of_sources // 100):
        GENERIC_URL = 'https://www150.statcan.gc.ca/n1/en/type/data?count=100&p={}-All#all'
        page = requests.get(GENERIC_URL.format(_))
        print(f'Parsing Page {1+_:3} Out of {1+number_of_sources // 100}')
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
                    'former_id': None if tag_former_id is None else tag_former_id.get_text(),
                    'geo': None if tag_geo is None else tag_geo.get_text(),
                    'frequency': None if tag_frequency is None else tag_frequency.get_text(),
                    'description': None if tag_description is None else tag_description.get_text(),
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
    data.fillna('None').to_excel(FILE_NAME, index=False)


if __name__ == '__main__':
    main()

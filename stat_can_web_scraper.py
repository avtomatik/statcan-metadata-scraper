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
    number_of_sources = get_number_of_sources()
    _data = []
    for _ in range(1+number_of_sources // 100):
        GENERIC_URL = 'https://www150.statcan.gc.ca/n1/en/type/data?count=100&p={}-All#all'
        page = requests.get(GENERIC_URL.format(_))
        print(f'Parcing Page {1+_:3} Out of {1+number_of_sources // 100}')
        soup = BeautifulSoup(page.text, 'lxml')
        details_soup = soup.find('details', id='all')
        items = details_soup.find_all('li', {'class': 'ndm-item'})
        for item in items:
            former_id = item.find('div', class_='ndm-result-formerid')
            geo = item.find('div', class_='ndm-result-geo')
            frequency = item.find('div', class_='ndm-result-freq')
            description = item.find('div', class_='ndm-result-description')
            if former_id:
                former_id = item.find(
                    'div', class_='ndm-result-formerid'
                ).get_text()
            else:
                former_id = None
            if geo:
                geo = item.find('div', class_='ndm-result-geo').get_text()
            else:
                geo = None
            if frequency:
                frequency = item.find(
                    'div', class_='ndm-result-freq'
                ).get_text()
            else:
                frequency = None
            if description:
                description = item.find(
                    'div', class_='ndm-result-description'
                ).get_text()
            else:
                description = None
            _data.append(
                {
                    'title': item.find('div', class_='ndm-result-title').get_text(),
                    'product_id': item.find('div', class_='ndm-result-productid').get_text(),
                    'former_id': former_id,
                    'geo': geo,
                    'frequency': frequency,
                    'description': description,
                    'release_date': item.find('span', class_='ndm-result-date').get_text(),
                    'type': item.find(
                        'div',
                        class_='ndm-result-productid'
                    ).get_text().split(':')[0],
                    'ref': item.a.get('href'),
                }
            )

    data = pd.DataFrame.from_dict(_data)
    data[['id', 'title_only']] = data.iloc[:, 0].str.split(
        pat='. ',
        n=1,
        expand=True
    )
    data['id'] = pd.to_numeric(data['id'].str.replace(',', ''))
    data.fillna('None', inplace=True)
    data.to_excel('stat_can_all.xlsx', index=False)


if __name__ == '__main__':
    main()

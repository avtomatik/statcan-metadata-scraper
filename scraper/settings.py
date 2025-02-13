#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 10:41:27 2025

@author: alexandermikhailov
"""

from pathlib import Path

ALLOWED_DOMAINS = ['www150.statcan.gc.ca']

START_URLS = ['https://www150.statcan.gc.ca/n1/']

URL_ROOT = 'https://www150.statcan.gc.ca/n1/tbl/csv'

ENDPOINT = 'https://www150.statcan.gc.ca/n1/en/type/data'

BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS_DIR = 'data'

DATA_DIR = Path(__file__).resolve().parent.parent.joinpath('data')

# =========================================================================
# This Is Where You Store Your StanCan Archives:
# =========================================================================
STORAGE_DIR = DATA_DIR.joinpath('external')

BOT_NAME = 'statcan_parse'

SPIDER_NAME = 'statcan_spyder'

SPIDER_MODULES = ['statcan_parse.spiders']

NEWSPIDER_MODULE = 'statcan_parse.spiders'

ROBOTSTXT_OBEY = True

FEED_EXPORT_ENCODING = 'utf-8'

FEEDS = {
    'data/statcan_%(time)s.csv': {
        'format': 'csv',
        'fields': {'*': '*'},
        'overwrite': True
    },
}

ITEM_PIPELINES = {
    'statcan_parse.pipelines.PepParsePipeline': 300,
}

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 10:41:27 2025

@author: alexandermikhailov
"""

from pathlib import Path

URL_ROOT = 'https://www150.statcan.gc.ca/n1/tbl/csv'

ENDPOINT = 'https://www150.statcan.gc.ca/n1/en/type/data'

DATA_DIR = Path(__file__).resolve().parent.parent.joinpath('data')

# =========================================================================
# This Is Where You Store Your StanCan Archives:
# =========================================================================
STORAGE_DIR = DATA_DIR.joinpath('external')

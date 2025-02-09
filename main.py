#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 21:59:20 2021

@author: Alexander Mikhailov
"""

# =============================================================================
# STATCAN Sources Metadata Grabber through Web Scraping
# =============================================================================

from datetime import date
from pathlib import Path

from core.funcs import build_preprocess_dataframe, combine_data
from scraper.settings import DATA_DIR


def main(
    file_name: str,
) -> None:
    """
    Main Function to Export Collected DataFrame to Excel File

    Parameters
    ----------
    excel_writer : str, optional
        DESCRIPTION. The default is f'statcan_data_sources-{date.today()}.xlsx'. # noqa: E501

    Returns
    -------
    None

    """
    Path(DATA_DIR).mkdir(exist_ok=True)
    build_preprocess_dataframe(combine_data()).to_excel(
        excel_writer=Path(DATA_DIR).joinpath(file_name),
        index=False
    )


if __name__ == '__main__':
    file_name = f'statcan_data_sources-{date.today()}.xlsx'
    main(file_name)

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

from .core.config import DATA_DIR
from .core.funcs import build_preprocess_dataframe, combine_data


def main(
    file_name: str,
    path_exp: Path = DATA_DIR
) -> None:
    """
    Main Function to Export Collected DataFrame to Excel File

    Parameters
    ----------
    excel_writer : str, optional
        DESCRIPTION. The default is f'stat_can_data_sources-{date.today()}.xlsx'.

    Returns
    -------
    None

    """
    path_exp.mkdir(exist_ok=True)
    build_preprocess_dataframe(combine_data()).to_excel(
        excel_writer=Path(path_exp).joinpath(file_name),
        index=False
    )


if __name__ == '__main__':
    file_name = f'stat_can_data_sources-{date.today()}.xlsx'
    main(file_name)

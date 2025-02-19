# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 21:22:23 2021

@author: Alexander Mikhailov
"""

import os
from pathlib import Path

import pandas as pd
from more_itertools import map_except

from statcan_web_scraper.settings import DATA_DIR, STORAGE_DIR, URL_ROOT


def url_to_archive_name(url: str) -> str:
    """


    Parameters
    ----------
    url : str
        DESCRIPTION.

    Returns
    -------
    str
        DESCRIPTION.

    """
    return f'{url.split("?pid=")[1][:-2]}-eng.zip'


def get_archive_names(file_name: str) -> set[str]:
    """


    Parameters
    ----------
    file_name : str
        DESCRIPTION.

    Returns
    -------
    set[str]
        DESCRIPTION.

    """
    df = pd.read_excel(Path(DATA_DIR).joinpath(file_name))
    return set(map_except(url_to_archive_name, df.loc[:, 'ref'], IndexError))


def main(
    check_option: str,
):
    """


    Parameters
    ----------
    check_option : str
        `snapshots': Check Two Excel Files;
        `downloaded': Check the Latest Excel File Against Downloaded Collection. # noqa: E501

    Returns
    -------
    None.

    """
    # =========================================================================
    # Read File Generated with main() @src/main.py @https://github.com/avtomatik/statcan_web_scraper # noqa: E501
    # =========================================================================

    snapshots_available = sorted(
        filter(lambda _: _.endswith('.xlsx'), os.listdir(Path(DATA_DIR)))
    )

    archive_names_available = get_archive_names(snapshots_available[-1])

    archive_names_seen = get_archive_names(snapshots_available[-2]) \
        if check_option == 'snapshots' \
        else {
        set(
            filter(
                lambda _: _.endswith('-eng.zip'),
                os.listdir(STORAGE_DIR)
            )
        )
    }

    archive_names_to_check = sorted(
        archive_names_available - archive_names_seen
    )
    if archive_names_to_check:
        print('You Might Want to Check Those New Archives:')
        for archive_name in archive_names_to_check:
            print('/'.join((URL_ROOT, archive_name)))
    else:
        print('No New Archives Since the Last Snapshot/Download')


if __name__ == '__main__':
    main('snapshots')

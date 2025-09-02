# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 21:22:23 2021

@author: Alexander Mikhailov
"""


import os
from pathlib import Path

import pandas as pd
from more_itertools import map_except

from .core.config import DATA_DIR, DATA_EXTERNAL_PATH
from .utils.filenames import url_to_archive_name


def get_archive_names(file_name: str, path_src: Path = DATA_DIR) -> set[str]:
    """


    Parameters
    ----------
    file_name : str
        DESCRIPTION.
    path_src : str, optional
        DESCRIPTION. The default is <DATA_DIR>.

    Returns
    -------
    set[str]
        DESCRIPTION.

    """
    df = pd.read_excel(path_src / file_name)
    return set(map_except(url_to_archive_name, df.loc[:, 'ref'], IndexError))


def main(
    check_option: str,
    path_src: Path = DATA_DIR,
    url_root: str = 'https://www150.statcan.gc.ca/n1/tbl/csv',
):
    """


    Parameters
    ----------
    check_option : str
        `snapshots': Check Two Excel Files;
        `downloaded': Check the Latest Excel File Against Downloaded Collection.
    path_src : str, optional
        DESCRIPTION. The default is <DATA_DIR>.
    url_root : str, optional
        DESCRIPTION. The default is 'https://www150.statcan.gc.ca/n1/tbl/csv'.

    Returns
    -------
    None.

    """
    # =========================================================================
    # Read File Generated with main() @src/main.py @https://github.com/avtomatik/statcan_parser
    # =========================================================================

    snapshots_available = sorted(
        filter(lambda _: _.endswith('.xlsx'), os.listdir(path_src))
    )

    archive_names_available = get_archive_names(snapshots_available[-1])

    archive_names_seen = get_archive_names(snapshots_available[-2]) \
        if check_option == 'snapshots' \
        else {
        set(
            filter(
                lambda _: _.endswith('-eng.zip'),
                os.listdir(DATA_EXTERNAL_PATH)
            )
        )
    }

    archive_names_to_check = sorted(
        archive_names_available - archive_names_seen
    )
    if archive_names_to_check:
        print('You Might Want to Check Those New Archives:')
        for archive_name in archive_names_to_check:
            print('/'.join((url_root, archive_name)))
    else:
        print('No New Archives Since the Last Snapshot/Download')


if __name__ == '__main__':
    main('snapshots')

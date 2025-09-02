#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entry point for the STATCAN Sources Metadata Grabber.

This module runs the main export function from core.funcs.

Created on Thu Aug  5 21:59:20 2021

@author: Alexander Mikhailov
"""

import time

from src.utils.io import download_archives
from src.utils.snapshots import check_new_archives

from .core.config import DATA_DIR, INTERVAL_HOURS
from .utils.pipeline import run_pipeline


def main_loop() -> None:
    """
    Blocking main loop: repeat every INTERVAL_HOURS.

    - If < 2 snapshot files >> run_pipeline to create one.
    - If ≥ 2 snapshot files >> check for new archives, download if found.
    """
    while True:
        try:
            snapshot_files = [
                f for f in DATA_DIR.iterdir() if f.suffix == '.xlsx'
            ]

            if len(snapshot_files) < 2:
                print('Less than 2 snapshots found >> running pipeline...')
                run_pipeline()
            else:
                print('Checking for new archives...')
                new_archives = check_new_archives(snapshot_dir=DATA_DIR)
                if new_archives:
                    download_archives(new_archives)

        except Exception as exc:
            # prevent crash >> log and continue loop
            print(f'Error during cycle: {exc}')

        print(f'Sleeping for {INTERVAL_HOURS} hours...\n')
        time.sleep(INTERVAL_HOURS * 3600)


if __name__ == '__main__':
    main_loop()

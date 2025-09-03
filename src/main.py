#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entry point for the STATCAN Sources Metadata Grabber.

This module runs a blocking main loop that:
- Creates snapshot Excel files of STATCAN sources metadata.
- Periodically checks for new archives and downloads them if available.
- Falls back to creating a new snapshot if not enough snapshots exist.
- Supports KeyboardInterrupt (Ctrl+C) to stop the loop cleanly.

Repeats every INTERVAL_HOURS (see config).

Created on Thu Aug  5 21:59:20 2021

@author: Alexander Mikhailov
"""

import time
import traceback

from src.core.config import DATA_DIR, INTERVAL_HOURS
from src.utils.io import download_archives
from src.utils.pipeline import run_pipeline
from src.utils.snapshots import check_new_archives


def main_loop() -> None:
    """
    Blocking main loop: repeat every INTERVAL_HOURS.

    Behavior per cycle:
    1. If fewer than 2 snapshot files exist, run the pipeline to create one.
    2. If 2 or more snapshots exist, check for new archives and download them.
    3. Sleeps INTERVAL_HOURS between cycles.

    KeyboardInterrupt (Ctrl+C) will stop the loop gracefully.
    """
    try:
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
                    else:
                        print('No new archives found.')

            except Exception:
                print('Error during cycle:')
                traceback.print_exc()

            print(f'Sleeping for {INTERVAL_HOURS} hours...\n')
            time.sleep(INTERVAL_HOURS * 3600)

    except KeyboardInterrupt:
        print('\nMain loop stopped by user.')


if __name__ == '__main__':
    main_loop()

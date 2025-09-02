# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 21:22:23 2021

@author: Alexander Mikhailov
"""

from datetime import datetime
from enum import Enum
from pathlib import Path

from openpyxl import load_workbook

from .core.config import DATA_DIR, DATA_EXTERNAL_PATH
from .utils.filenames import url_to_archive_name


class Mode(Enum):
    SNAPSHOTS = 'snapshots'
    DOWNLOADED = 'downloaded'


def extract_archive_names_from_excel(file_path: Path) -> set[str]:
    """
    Extract archive names from the 'ref' column of an Excel file,
    converting URLs to standardized archive filenames.
    """
    archive_names: set[str] = set()
    workbook = load_workbook(file_path, read_only=True)
    sheet = workbook.active

    headers = list(next(sheet.iter_rows(values_only=True)))
    try:
        ref_column_index = headers.index('ref')
    except ValueError as exc:
        raise ValueError("No 'ref' column found in the Excel file") from exc

    for row in sheet.iter_rows(min_row=2, values_only=True):
        url = row[ref_column_index]
        if url is None:
            continue
        try:
            archive_name = url_to_archive_name(url)
            archive_names.add(archive_name)
        except (IndexError, ValueError):
            continue

    return archive_names


def snapshot_sort_key(file_path: Path):
    """
    Extracts date from filename for sorting.
    Expected format: snapshot_YYYY-MM-DD.xlsx
    """
    try:
        date_str = file_path.stem.split('_')[-1]
        return datetime.strptime(date_str, '%Y-%m-%d')
    except Exception:
        # Fallback: lexical sort if parsing fails
        return file_path.name


def get_latest_snapshot_file(snapshot_files: list[Path]) -> Path | None:
    return snapshot_files[-1] if snapshot_files else None


def get_previous_snapshot_file(snapshot_files: list[Path]) -> Path | None:
    return snapshot_files[-2] if len(snapshot_files) >= 2 else None


def main(
    mode: Mode,
    snapshot_dir: Path = DATA_DIR,
    url_base: str = 'https://www150.statcan.gc.ca/n1/tbl/csv',
):
    """
    Compare snapshots or downloaded archive collections.

    Parameters
    ----------
    mode : Mode
        Mode.SNAPSHOTS: Compare two Excel snapshot files.
        Mode.DOWNLOADED: Compare latest Excel snapshot against downloaded
            archives.
    snapshot_dir : Path, optional
        Directory containing snapshot Excel files. Defaults to DATA_DIR.
    url_base : str, optional
        Base URL for StatCan archives.
    """

    snapshot_files = [f for f in snapshot_dir.iterdir() if f.suffix == '.xlsx']
    snapshot_files.sort(key=snapshot_sort_key)

    if not snapshot_files:
        print(f'No snapshot files found in {snapshot_dir}')
        return

    latest_snapshot_file = get_latest_snapshot_file(snapshot_files)
    previous_snapshot_file = (
        get_previous_snapshot_file(snapshot_files)
        if mode == Mode.SNAPSHOTS
        else None
    )

    if mode == Mode.SNAPSHOTS and not previous_snapshot_file:
        print('Not enough snapshots to compare (need at least 2).')
        return

    latest_archives = extract_archive_names_from_excel(latest_snapshot_file)

    if mode == Mode.SNAPSHOTS:
        previous_archives = extract_archive_names_from_excel(
            previous_snapshot_file
        )
    else:
        previous_archives = {
            f.name for f in DATA_EXTERNAL_PATH.iterdir()
            if f.suffix == '.zip' and f.name.endswith('-eng.zip')
        }

    new_archives = sorted(latest_archives - previous_archives)

    if new_archives:
        print('You Might Want to Check These New Archives:')
        for archive_name in new_archives:
            print(f'{url_base}/{archive_name}')
    else:
        print('No New Archives Since the Last Snapshot/Download')


if __name__ == '__main__':
    main(Mode.SNAPSHOTS)

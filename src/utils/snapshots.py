from datetime import datetime
from pathlib import Path

from src.core.config import DATA_DIR, URL_BASE

from .excel import extract_archive_names_from_excel


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


def check_new_archives(
    snapshot_dir: Path = DATA_DIR,
    url_base: str = URL_BASE,
) -> list[str]:
    """Check for new archives between the two latest snapshots."""
    snapshot_files = [f for f in snapshot_dir.iterdir() if f.suffix == '.xlsx']
    snapshot_files.sort(key=snapshot_sort_key)

    latest_snapshot_file = get_latest_snapshot_file(snapshot_files)
    previous_snapshot_file = get_previous_snapshot_file(snapshot_files)

    if not latest_snapshot_file or not previous_snapshot_file:
        print('Not enough snapshots to compare (need at least 2).')
        return []

    latest_archives = extract_archive_names_from_excel(latest_snapshot_file)
    previous_archives = extract_archive_names_from_excel(
        previous_snapshot_file)

    new_archives = sorted(latest_archives - previous_archives)

    if new_archives:
        print('You Might Want to Check These New Archives:')
        for archive_name in new_archives:
            print(f'{url_base}/{archive_name}')
    else:
        print('No New Archives Since the Last Snapshot/Download')

    return new_archives

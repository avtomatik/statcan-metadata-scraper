from pathlib import Path

import pandas as pd
import requests

from src.core.config import DATA_DIR, DATA_EXTERNAL_PATH, URL_BASE


def export_dataframe(
    df: pd.DataFrame,
    file_name: str,
    export_dir: Path = DATA_DIR
) -> None:
    """
    Save DataFrame to an Excel file.

    Parameters
    ----------
    df : pd.DataFrame
    file_name : str
        Name of the Excel file to create.
    export_dir : Path, optional
        Directory where the Excel file will be saved (default: DATA_DIR).
    Returns
    -------
    None
    """
    export_dir.mkdir(parents=True, exist_ok=True)
    output_path = export_dir / file_name
    df.to_excel(output_path, index=False)


def download_archives(
    archive_names: list[str],
    url_base: str = URL_BASE
) -> None:
    """Download new archives into DATA_EXTERNAL_PATH."""
    DATA_EXTERNAL_PATH.mkdir(parents=True, exist_ok=True)

    for archive_name in archive_names:
        url = f'{url_base}/{archive_name}'
        output_path = DATA_EXTERNAL_PATH / archive_name
        print(f'Downloading {url} >> {output_path}')

        resp = requests.get(url)
        resp.raise_for_status()

        with open(output_path, 'wb') as f:
            f.write(resp.content)

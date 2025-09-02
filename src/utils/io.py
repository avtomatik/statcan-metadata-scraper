from pathlib import Path

import pandas as pd

from src.core.config import DATA_DIR


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

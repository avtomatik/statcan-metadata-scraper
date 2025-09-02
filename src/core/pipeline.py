from src.utils.dataframe import make_dataframe, preprocess_dataframe
from src.utils.filenames import get_default_filename
from src.utils.io import export_dataframe
from src.utils.scraping import fetch_raw_data


def run_pipeline(file_name: str | None = None) -> None:
    """
    Run the complete pipeline:
    fetch → make DataFrame → preprocess → export.

    Parameters
    ----------
    file_name : str, optional
        Name of the Excel file (default: from get_default_filename()).

    Returns
    -------
    None
    """
    file_name = file_name or get_default_filename()

    (
        make_dataframe(fetch_raw_data())
        .pipe(preprocess_dataframe)
        .pipe(export_dataframe, file_name)
    )

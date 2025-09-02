from datetime import date


def get_default_filename() -> str:
    """Generate a default Excel file name with today's date."""
    return f'stat_can_data_sources-{date.today()}.xlsx'


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

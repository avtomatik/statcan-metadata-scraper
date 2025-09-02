from datetime import date
from urllib.parse import parse_qs, urlparse


def get_default_filename() -> str:
    """Generate a default Excel file name with today's date."""
    return f'stat_can_data_sources-{date.today()}.xlsx'


def url_to_archive_name(url: str) -> str:
    """
    Convert a URL containing a 'pid' parameter to a standardized archive
    filename.

    Parameters
    ----------
    url : str
        The input URL which should contain a 'pid' query parameter.

    Returns
    -------
    str
        A string representing the archive filename in the format
        '{pid}-eng.zip'.

    Raises
    ------
    ValueError
        If the URL does not contain a 'pid' query parameter or it is empty.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    pid_list = query_params.get('pid')

    if not pid_list or not pid_list[0]:
        raise ValueError(
            f'URL does not contain a valid `pid` parameter: {url}'
        )

    pid = pid_list[0]
    return f'{pid}-eng.zip'

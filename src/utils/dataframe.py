import pandas as pd


def make_dataframe(records: list[dict]) -> pd.DataFrame:
    """
    Convert raw records into a DataFrame without preprocessing.

    Parameters
    ----------
    records : list[dict]

    Returns
    -------
    pd.DataFrame
    """
    return pd.DataFrame.from_dict(records)


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess DataFrame (cleaning and transformations).

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    df = df.copy()

    split_cols = df['title'].str.split(pat='. ', n=1, expand=True)

    df['id'] = pd.to_numeric(
        split_cols[0].str.replace(',', ''),
        errors='coerce'
    )

    if 1 in split_cols.columns:
        df['title_only'] = split_cols[1].fillna(df['title'])
    else:
        df['title_only'] = df['title']

    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

    return df.fillna('None')

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

    df[['id', 'title_only']] = df['title'].str.split(
        pat='. ',
        n=1,
        expand=True,
    )
    df['id'] = pd.to_numeric(df['id'].str.replace(',', ''))
    df['release_date'] = pd.to_datetime(
        df['release_date'], infer_datetime_format=False)

    return df.fillna('None')

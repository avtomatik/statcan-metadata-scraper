#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entry point for the STATCAN Sources Metadata Grabber.

This module runs the main export function from core.funcs.

Created on Thu Aug  5 21:59:20 2021

@author: Alexander Mikhailov
"""

from .core.funcs import (export_dataframe, fetch_raw_data, make_dataframe,
                         preprocess_dataframe)
from .utils.filenames import get_default_filename


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


if __name__ == '__main__':
    run_pipeline()

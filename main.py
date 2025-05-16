#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 21:59:20 2021

@author: Alexander Mikhailov
"""

from datetime import date
from pathlib import Path
from typing import Protocol
import pandas as pd
from core.funcs import build_preprocess_dataframe, combine_data
from statcan_web_scraper.settings import DATA_DIR


class FilePathHandler(Protocol):
    def create_directory(self) -> None:
        ...

    def get_file_path(self, file_name: str) -> Path:
        ...


class LocalFilePathHandler:
    def create_directory(self) -> None:
        Path(DATA_DIR).mkdir(parents=True, exist_ok=True)

    def get_file_path(self, file_name: str) -> Path:
        return Path(DATA_DIR) / file_name


class DataProcessor(Protocol):
    def process(self) -> pd.DataFrame:
        ...


class StatCanDataProcessor:
    def process(self) -> pd.DataFrame:
        return build_preprocess_dataframe(combine_data())


class ExcelExporter:
    def __init__(
        self,
        file_path_handler: FilePathHandler,
        data_processor: DataProcessor
    ) -> None:
        self.file_path_handler = file_path_handler
        self.data_processor = data_processor

    def export(self, file_name: str) -> None:
        self.file_path_handler.create_directory()
        data = self.data_processor.process()
        data.to_excel(
            self.file_path_handler.get_file_path(file_name),
            index=False
        )


def main(file_name: str) -> None:
    file_path_handler = LocalFilePathHandler()
    data_processor = StatCanDataProcessor()
    exporter = ExcelExporter(file_path_handler, data_processor)
    exporter.export(file_name)


if __name__ == '__main__':
    main(f'statcan_data_sources-{date.today()}.xlsx')

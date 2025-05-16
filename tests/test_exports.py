import unittest
from unittest.mock import MagicMock

from main import DataProcessor, ExcelExporter, FilePathHandler


class TestExcelExporter(unittest.TestCase):
    def test_export(self):
        mock_file_path_handler = MagicMock(spec=FilePathHandler)
        mock_data_processor = MagicMock(spec=DataProcessor)
        mock_data_processor.process.return_value = 'mock_data'

        exporter = ExcelExporter(mock_file_path_handler, mock_data_processor)
        exporter.export('test.xlsx')

        mock_file_path_handler.create_directory.assert_called_once()
        mock_data_processor.process.assert_called_once()
        mock_file_path_handler.get_file_path.assert_called_once_with(
            'test.xlsx'
        )


if __name__ == '__main__':
    unittest.main()

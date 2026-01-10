import unittest
from unittest.mock import mock_open, patch, MagicMock, Mock

import pandas as pd
from src.convert_to_xlsx import SaveData


class TestCase(unittest.TestCase):

    def setUp(self):
        self.mock_html = "<html><body>Test</body></html>"
        self.mock_xlsx = b"\x50\x4b\x03\x04\x14\x00\x00\x00\x08\x00"
        self.fake_class = MagicMock()
        self.sd = SaveData()

    def test_read_xlsx_file(self):
        """Тестирование чтения файла html"""
        mock = mock_open(read_data=self.mock_html)
        with patch("builtins.open", mock):
            self.sd.read_file()
            result = self.sd.html_content
        # Проверяем
        self.assertEqual(result, "<html><body>Test</body></html>")

    def test_shorten_url_simple(self):
        """Самый простой рабочий тест - ИСПРАВЛЕННЫЙ"""
        # Настраиваем `__getitem__`, потому что в коде url["href"]
        self.fake_class.__getitem__.return_value = "https://example.com/long-url"

        self.sd.card_models = [self.fake_class]

        # Мокаем pyshorteners
        with patch(
            "src.convert_to_xlsx.pyshorteners.Shortener"
        ) as mock_shortener_class:
            # Упрощенная настройка
            mock_shortener_class.return_value.clckru.short.return_value = (
                "https://clck.ru/123abc"
            )

            # Запускаем метод
            self.sd.shorten_url()

            # Проверяем
            self.assertEqual(self.sd.short_url, ["https://clck.ru/123abc"])
            # Дополнительная проверка
            self.assertEqual(len(self.sd.short_url), 1)

    def test_data_in_list(self):
        """Тестирование объединённых данных в списке"""
        self.sd.name_model = [Mock(text="Товар1")]
        self.sd.card_brand = [Mock(text="Бренд1")]
        self.sd.old_price = [Mock(text="1000")]
        self.sd.new_price = [Mock(text="900")]
        self.sd.short_url = ["https://example.com"]
        self.sd.delivery_date = [Mock(text="1 день")]
        self.sd.rating_model = [Mock(text="4.5")]
        self.sd.number_of_reviews = [Mock(text="100")]

        self.sd.all_products = []

        self.sd.unity_data_in_list()

        self.assertEqual(self.sd.all_products[0]["title_model"], "Товар1")

    @patch("pandas.DataFrame")
    @patch("openpyxl.Workbook")
    def test_convert_to_file_simple(self, mock_wb_class, mock_df_class):
        """Тестирование сохранения в xlsx"""
        # Подготавливаем данные
        self.sd.all_products = [{"title": "Тест"}]

        # Вызываем метод
        self.sd.convert_to_file()

        # Проверяем
        mock_wb_class.assert_called_once()  # Проверяем создание Workbook
        mock_df_class.assert_called_once_with(
            self.sd.all_products
        )  # Проверяем создание DataFrame

    def test_save_to_db(self):
        """Тестирование сохранения данных в БД"""

        # Настраиваем объект
        self.sd.df = Mock()
        self.sd.df.to_sql = Mock()
        self.sd.engine = Mock()

        with patch("logging.info") as mock_log, patch("builtins.print") as mock_print:
            self.sd.save_to_db()

            self.sd.df.to_sql.assert_called_once()

            mock_log.assert_called_with("Данные в БД успешно загружены!")
            mock_print.assert_called_with("Данные успешно собраны и загружены в БД!")

    def test_read_to_xlsx(self):
        """Тестирование чтения файла xlsx"""

        expected_df = pd.DataFrame(
            {
                "title_model": ["Товар1", "Товар2"],
                "brand_model": ["Бренд1", "Бренд2"],
                "price": [1000, 2000],
            }
        )

        with patch("pandas.read_excel", return_value=expected_df) as mock_read_excel:
            with patch("builtins.print"):
                # Вызываем
                self.sd.read_to_xlsx()

                # Проверяем
                mock_read_excel.assert_called_once_with("data/catalog.xlsx")


if __name__ == "__main__":
    unittest.main()

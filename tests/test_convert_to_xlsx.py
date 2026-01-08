import unittest
from unittest.mock import mock_open, patch, MagicMock

from src.convert_to_xlsx import SaveData


class TestCase(unittest.TestCase):

    def setUp(self):
        self.mock_html = "<html><body>Test</body></html>"
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
        # Создаем фейковую ссылку
        fake_url = MagicMock()
        # Настраиваем `__getitem__`, потому что в коде url["href"]
        fake_url.__getitem__.return_value = "https://example.com/long-url"

        self.sd.card_models = [fake_url]

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


if __name__ == "__main__":
    unittest.main()

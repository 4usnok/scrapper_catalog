import os

from src.convert_to_xlsx import main_convert
from src.scrapper_wb import main_scrapper


path_to_file = os.path.exists("data/wildberries.html")
if __name__ == "__main__":
    # Запуск парсера
    if not path_to_file:
        main_scrapper()
        main_convert()
    else:
        main_convert()

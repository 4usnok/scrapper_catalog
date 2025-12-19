import os

import logging

from src.convert_to_xlsx import main_convert
from src.scrapper_wb import main_scrapper

logging.basicConfig(
    level=logging.INFO,
    filename="py_log.log",
    filemode="w",
    encoding="utf-8",
    force=True,
)

path_to_file = os.path.exists("data/wildberries.html")
if __name__ == "__main__":
    # Запуск парсера
    if not path_to_file:
        main_scrapper()
        main_convert()
        logging.info(
            "Создание файла xlxs с названием и ссылками на товар прошло успешно"
        )
    else:
        main_convert()
        logging.info(
            "Создание файла xlxs с названием и ссылками на товар прошло успешно"
        )

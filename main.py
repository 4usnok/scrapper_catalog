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

if __name__ == "__main__":
    main_scrapper()
    main_convert()
    logging.info("Создание файла xlxs с названием и ссылками на товар прошло успешно")

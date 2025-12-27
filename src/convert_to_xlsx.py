import logging
import openpyxl
import pandas as pd
from bs4 import BeautifulSoup

from src.config_db import engine, table_name


class SaveData:

    def __init__(self):
        self.result_title = []
        self.result_href = []
        self.product_container = None
        self.card_titles = None
        self.soup = None
        self.df = None

    def read_file(self):
        """Чтение html файла"""
        with open("data/catalog.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        self.soup = BeautifulSoup(html_content, features="html.parser")
        self.product_container = self.soup.find("div", class_="product-card-list")
        self.card_titles = self.product_container.find_all(
            "a", class_="product-card__link j-card-link j-open-full-product-card"
        )
        logging.info("Чтение html-файла прошло успешно")

    def pars_model(self):
        """Парсинг названий и ссылок моделей"""
        for info_model in self.card_titles:
            self.result_title.append(info_model["aria-label"])
            self.result_href.append(info_model["href"])

    def convert_to_file(self):
        """Сохранение в файл xlsx"""
        # Создаём новый файл(книгу)
        wb = openpyxl.Workbook()
        # Создаём активный лист, куда будем загружать данные
        sheet = wb.active
        # Даём название странице
        sheet.tittle = "Товары"
        # Записываем данные в ячейки
        self.df = pd.DataFrame(
            {
                "title_model": self.result_title,
                "url_model": self.result_href,
            }
        )
        self.df.to_excel("data/catalog.xlsx", index=False)
        logging.info("Создание файла xlxs с отфильтрованными товарами прошло успешно")

    def db_work(self):
        """Сохранение данных в БД"""
        self.df.to_sql(table_name, engine, if_exists="replace", index=False)
        logging.info("Данные в БД успешно загружены!")
        print("Данные успешно собраны и загружены в БД!")

    def read_to_excel_title(self):
        """Чтение файла xlsx"""
        file_path = "data/catalog.xlsx"
        # Читаем файл в DataFrame
        self.df = pd.read_excel(file_path)
        # Выводим первые 5 строк, чтобы проверить данные
        print(self.df.head())


def main_convert():
    pars = SaveData()
    pars.read_file()
    pars.pars_model()
    pars.convert_to_file()
    pars.db_work()
    pars.read_to_excel_title()

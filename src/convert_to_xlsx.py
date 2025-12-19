import logging
import openpyxl
import pandas as pd
from bs4 import BeautifulSoup


class SaveData:

    def __init__(self):
        self.result_title = []
        self.result_href = []

    def read_file(self):
        """Чтение html файла"""
        with open("data/wildberries.html", "r", encoding="utf-8") as f:
            html_content = f.read()

        self.soup = BeautifulSoup(html_content, features="html.parser")
        logging.info("Чтение html-файла прошло успешно")

    def title_model(self):
        """Парсинг названий модели"""
        titles = self.soup.find_all("a", class_="product-card__link")
        for title in titles:
            self.result_title.append(title["aria-label"])

    def href_model(self):
        """Парсинг ссылки на модель"""
        hrefs = self.soup.find_all("a", class_="product-card__link")
        for href in hrefs:
            self.result_href.append(href["href"])

    def convert_to_file(self):
        """Сохранение в файл xlsx"""
        # Создаём новый файл(книгу)
        wb = openpyxl.Workbook()
        # Создаём активный лист, куда будем загружать данные
        sheet = wb.active
        # Даём название странице
        sheet.tittle = "Куртки"
        # Записываем данные в ячейки
        df = pd.DataFrame(
            {
                "Название модели": self.result_title,
                "Ссылка на модель": self.result_href,
            }
        )
        df.to_excel("data/wb_catalog.xlsx", index=False)
        logging.info("Создание файла xlxs с отфильтрованными товарами прошло успешно")

    def read_to_excel_title(self):
        file_path = "data/wb_catalog.xlsx"
        # Читаем файл в DataFrame
        df = pd.read_excel(file_path)
        # Выводим первые 5 строк, чтобы проверить данные
        print(df.head())


def main_convert():
    pars = SaveData()
    pars.read_file()
    pars.title_model()
    pars.href_model()
    pars.convert_to_file()
    pars.read_to_excel_title()

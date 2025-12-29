import logging
import openpyxl
import pandas as pd
from bs4 import BeautifulSoup

from src.config_db import engine, table_name


class SaveData:

    def __init__(self):
        self.all_products = []
        self.product_container = None
        self.card_models = None
        self.old_price = None
        self.new_price = None
        self.soup = None
        self.df = None

    def read_file(self):
        """Чтение html файла"""
        with open("data/catalog.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        self.soup = BeautifulSoup(html_content, features="html.parser")
        self.product_container = self.soup.find("div", class_="product-card-list")
        self.card_models = self.product_container.find_all(
            "a", class_="product-card__link j-card-link j-open-full-product-card"
        )
        self.old_price = self.product_container.find_all("del")
        self.new_price = self.product_container.find_all(
            "ins", class_="price__lower-price wallet-price red-price"
        )
        logging.info("Чтение html-файла прошло успешно")

    def pars_model(self):
        """Парсинг информации моделей"""
        for info_model, old, new in zip(
            self.card_models, self.old_price, self.new_price
        ):
            # Посчитаем скидку
            price_old_str = old.text.replace("\xa0", "")
            price_old_str = price_old_str.replace(" ", "")
            price_old_str = price_old_str.replace("₽", "")
            price_old_int = int(price_old_str)
            price_new_str = new.text.replace("\xa0", "")
            price_new_str = price_new_str.replace(" ", "")
            price_new_str = price_new_str.replace("₽", "")
            price_new_int = int(price_new_str)
            discount_price = (price_old_int - price_new_int) // 100
            if 0 > discount_price:
                discount_price = f"Цена увеличилась на {discount_price * -1}"
            elif discount_price == 0:
                discount_price = "Стоимость не изменилась"
            else:
                discount_price = f"Цена уменьшилась на {discount_price}"

            result_list = {
                "title_model": info_model["aria-label"],
                "old_price": old.text.replace("\xa0", ""),
                "new_price": new.text.replace("\xa0", ""),
                "discount_price": f"{discount_price}%",
                "url_model": info_model["href"],
            }
            self.all_products.append(result_list)

    def convert_to_file(self):
        """Сохранение в файл xlsx"""
        # Создаём новый файл(книгу)
        wb = openpyxl.Workbook()
        # Создаём активный лист, куда будем загружать данные
        sheet = wb.active
        # Даём название странице
        sheet.tittle = "Товары"
        # Записываем данные в ячейки
        self.df = pd.DataFrame(self.all_products)
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

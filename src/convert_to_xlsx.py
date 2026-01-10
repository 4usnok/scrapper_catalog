import logging
import openpyxl
import pandas as pd
import pyshorteners
from bs4 import BeautifulSoup

from src.config_db import engine, table_name


class SaveData:

    def __init__(self):
        self.soup = None
        self.html_content = None
        self.df = None
        self.product_container = None
        self.card_models = None
        self.name_model = None
        self.old_price = None
        self.new_price = None
        self.card_brand = None
        self.delivery_date = None
        self.rating_model = None
        self.original_model = None
        self.number_of_reviews = None
        self.discount_price = None

        self.all_products = []
        self.is_original = []
        self.short_url = []

    def read_file(self):
        """Чтение html файла"""
        with open("data/catalog.html", "r", encoding="utf-8") as f:
            self.html_content = f.read()

    def pars_html(self):
        self.soup = BeautifulSoup(self.html_content, features="html.parser")
        self.product_container = self.soup.find("div", class_="product-card-list")
        self.card_models = self.product_container.find_all(
            "a", class_="product-card__link j-card-link j-open-full-product-card"
        )
        self.name_model = self.product_container.find_all(
            "span", class_="product-card__name"
        )

        self.old_price = self.product_container.find_all("del")
        self.new_price = self.product_container.find_all(
            "ins", class_="price__lower-price wallet-price red-price"
        )
        self.card_brand = self.product_container.find_all(
            "span", class_="product-card__brand"
        )
        self.delivery_date = self.product_container.find_all("span", class_="btn-text")
        self.rating_model = self.product_container.find_all(
            "span", class_="address-rate-mini address-rate-mini--sm"
        )
        self.original_model = self.product_container.find_all(
            "span",
            class_="product-card__original-mark icon-original-check originalMark--b3N5n",
        )
        self.number_of_reviews = self.product_container.find_all(
            "span", class_="product-card__count"
        )
        logging.info("Чтение html-файла прошло успешно")

    def shorten_url(self):
        """Сокращатель ссылок"""
        for url in self.card_models:
            original_href = url["href"]
            self.short_url.append(pyshorteners.Shortener().clckru.short(original_href))

    def unity_data_in_list(self):
        """Сбор информации карточки товара в единый файл"""
        for name, brand, old, new, url, delivery, rating, rev in zip(
            self.name_model,
            self.card_brand,
            self.old_price,
            self.new_price,
            self.short_url,
            self.delivery_date,
            self.rating_model,
            self.number_of_reviews,
        ):
            result_list = {
                "title_model": name.text,
                "brand_model": brand.text,
                "old_price": old.text.replace("\xa0", ""),
                "new_price": new.text.replace("\xa0", ""),
                "url_model": url,
                "delivery_date": delivery.text,
                "rating": rating.text,
                "number_of_rev": rev.text,
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

    def save_to_db(self):
        """Сохранение данных в БД"""
        self.df.to_sql(table_name, engine, if_exists="replace", index=False)
        logging.info("Данные в БД успешно загружены!")
        print("Данные успешно собраны и загружены в БД!")

    def read_to_xlsx(self):
        """Чтение файла xlsx"""
        file_path = "data/catalog.xlsx"
        # Читаем файл в DataFrame
        self.df = pd.read_excel(file_path)
        # Выводим первые 5 строк, чтобы проверить данные
        print(self.df.head())


def main_convert():
    pars = SaveData()
    pars.read_file()
    pars.pars_html()
    pars.shorten_url()
    pars.unity_data_in_list()
    pars.convert_to_file()
    pars.save_to_db()
    pars.read_to_xlsx()

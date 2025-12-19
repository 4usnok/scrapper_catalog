import os
import time

from dotenv import load_dotenv
from logger import logger
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
url = os.getenv("base_url")


class ParsingWB:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = url
        self.settings_webdriver()

    def settings_webdriver(self):
        try:
            # Инициализация WebDriver для Chrome
            self.driver.maximize_window()
            stealth(
                self.driver,
                languages=["ru-Ru", "en"],
                vendor="Google Inc",
                platform="Win64",
                webgl_vendor="Intel Inc",
                renderer="Intel Iris OpenGL Engine",
            )
            return self.driver
        except Exception as e:
            logger.error(e)
            return None

    def search_query(self):
        """Поисковый запрос"""
        self.driver.get(url)
        # ждем появления элемента
        element = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "searchInput"))
        )
        time.sleep(0.5)
        # закрываем рекламное объявление
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        # поисковый запрос
        search_el = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.ID, "searchInput"))
        )
        search_el.send_keys("Куртки")
        search_el.send_keys(Keys.ENTER)
        time.sleep(2)
        return search_el

    def filters_for_reit(self):
        """Фильтрация по рейтингу"""
        elem = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".dropdown-filter__btn.dropdown-filter__btn--all")
            )
        )
        elem.click()
        time.sleep(1)

        # scroll до кнопки с рейтингом и её выбор
        filter_but = self.driver.find_element(
            By.CSS_SELECTOR, ".btn-switch__btn.j-filter-switch"
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", filter_but
        )

        time.sleep(1)
        reit_but = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".btn-switch__btn.j-filter-switch")
            )
        )
        reit_but.click()
        time.sleep(1)

    def filters_for_country(self):
        """Фильтрация по стране производителя"""
        # scroll до выбора страны и клик на Россию
        country_change = self.driver.find_element(
            By.XPATH,
            "//span[contains(@class, 'checkbox-with-text__text') and text()='Россия']/..",
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", country_change
        )
        time.sleep(1)
        country_but = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//span[contains(@class, 'checkbox-with-text__text') and text()='Россия']/..",
                )
            )
        )
        country_but.click()
        time.sleep(1)

    def run_scrapper(self):
        """Запуск скраппера"""
        # применить фильтрацию
        elem = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".filters-desktop__btn-main.btn-main")
            )
        )
        elem.click()
        time.sleep(5)

    def save_html_text(self):
        """Сохраняет html в файл"""
        soup = self.driver.page_source
        with open("data/wildberries.html", "w", encoding="utf-8") as file:
            file.write(soup)
        print("HTML код на обновлённый каталог успешно создан!")


def main_scrapper():
    parser = ParsingWB()
    parser.search_query()
    parser.filters_for_reit()
    parser.filters_for_country()
    parser.run_scrapper()
    parser.save_html_text()

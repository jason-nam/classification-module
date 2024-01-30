import json
import abc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class ProductsScraper(abc.ABC):
    '''Abstract products scraper class
    '''
    def __init__(self, grocery_store_name):
        self.store_name = grocery_store_name
        self.products_list = []

        with open('config.json', 'r') as file:
            self.config = json.load(file)

        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")  # Optional: Run in headless mode
        self.service = Service(ChromeDriverManager().install())

    @abc.abstractmethod
    def get_all_products(self):
        raise NotImplementedError

    @abc.abstractmethod
    def scrape_items(self, driver, base_url):
        raise NotImplementedError
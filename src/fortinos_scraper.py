import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from workflows import execute_workflow
from web_crawler import get_urls
from global_vars import FORTINOS_BASE_URL

from products_scraper import ProductsScraper


class FortinosProductsScraper(ProductsScraper):
    '''Products scraper for Fortinos Grocery Store
    '''
    def __init__(self, grocery_store_name):
        super().__init__(grocery_store_name)

        self.store_name = "Fortinos"

    def _get_url(self):
        # self.driver = webdriver.Chrome(service=self.service, options=self.options)
        base_urls = FORTINOS_BASE_URL
        all_urls = []

        try:
            for base_url in base_urls:
                all_urls = list(set(get_urls(self.driver, base_url)).union(all_urls))
        finally:
            # self.driver.quit()
            pass

        return all_urls

    def get_all_products(self):

        self.driver = webdriver.Chrome(service=self.service, options=self.options)

        base_urls = self._get_url()

        len(base_urls)

        try:
            for base_url in base_urls:
                self.iter_pages(base_url)

                print(f"Total items scraped: {len(self.products_list)}")
            
            for item in self.products_list:
                print(item)

        finally:
            self.driver.quit()

    def iter_pages(self, base_url):
        page_number = 1

        while True:
            url = f"{base_url}?page={page_number}"
            print(f"Scraping {url}")
            items = self.scrape_items(url)

            if not items:
                print(f"No items found on page {page_number}. End of pages reached.")
                break

            print(f'Scraped {len(items)} items')
            self.products_list.extend(item for item in items if item not in self.products_list)
            page_number += 1

    def scrape_items(self, url):
        try:
            self.driver.get(url)
            item_container_class = self.config['stores'][self.store_name]['item_container']
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, item_container_class)))
            item_containers = self.driver.find_elements(By.CLASS_NAME, item_container_class)
        except:
            return None
        
        items = []
        for item in item_containers:            
            brand = self._get_brand(item)
            name = self._get_name(item)
            was_price = self._get_was_price(item)
            price = self._get_price(item)
            product_number = self._get_product_number(item)
            image_url = self._get_image_url(item)

            items.append({
                "store": self.store_name,
                "brand": brand,
                "name": name,
                "price": price,
                "was_price": was_price,
                "product_number": product_number,
                "image_url": image_url
            })
        
        return items
    
    def _get_brand(self, item):
        try:
            workflow_name = "get_product_brand"
            brand = execute_workflow(item, self.config, self.store_name, workflow_name)
        except NoSuchElementException:
            brand = None
        finally:
            return brand
        
    def _get_name(self, item):
        try:
            workflow_name = "get_product_name"
            name = execute_workflow(item, self.config, self.store_name, workflow_name)
        except NoSuchElementException:
            name = None
        finally:
            return name
        
    def _get_was_price(self, item):
        try:
            workflow_name = "get_product_was_price"
            was_price = execute_workflow(item, self.config, self.store_name, workflow_name)
        except NoSuchElementException:
            was_price = None
        finally:
            return was_price
        
    def _get_price(self, item):
        try:
            workflow_name = "get_product_price"
            price = execute_workflow(item, self.config, self.store_name, workflow_name)
        except NoSuchElementException:
            price = None
        finally:
            return price
        
    def _get_product_number(self, item):
        try:
            workflow_name = "get_product_number"
            product_number = execute_workflow(item, self.config, self.store_name, workflow_name)
        except NoSuchElementException:
            product_number = None
        finally:
            return product_number

    def _get_image_url(self, item):
        try:
            workflow_name = "get_product_image_url"
            image_element = execute_workflow(item, self.config, self.store_name, workflow_name)

            self.driver.execute_script("arguments[0].scrollIntoView();", image_element)
            WebDriverWait(self.driver, 5).until(EC.visibility_of(image_element))  # Wait for image to be visible

            image_url = image_element.get_attribute('src')

        except NoSuchElementException:
            image_url = None

        finally:
            if not image_url or 'data:image' in image_url:  # Placeholder images are sometimes encoded in base64
                image_url = image_element.get_attribute('data-src')

        return image_url

    def _download_image(image_url, folder_path, product_number):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        response = requests.get(image_url)
        if response.status_code == 200:
            with open(os.path.join(folder_path, product_number + '.png'), 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to download image for product number {product_number}")


if __name__ == "__main__":
    fortinos_products = FortinosProductsScraper("Fortinos")
    fortinos_products.get_all_products()
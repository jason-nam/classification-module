import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Load configuration
with open('config.json', 'r') as file:
    config = json.load(file)

def get_product_details(sku):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        url = f"https://www.fortinos.ca/search?search-bar={sku}"
        driver.get(url)

        # Wait up to 10 seconds for the elements to be present
        wait = WebDriverWait(driver, 10)
        
        product_brand = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-name__item--brand"))).text
        product_name = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-name__item--name"))).text
        product_price = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "selling-price-list__item__price--now-price__value"))).text
        product_link = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-tile__details__info__name__link")))
        product_href = product_link.get_attribute('href')
        product_href_last_section = product_href.split('/')[-1]

        return {
            "brand": product_brand.strip(),
            "name": product_name.strip(),
            "price": product_price.strip(),
            "product_number": product_href_last_section.strip(),
        }
    finally:
        driver.quit()

# Example usage
sku = "06905212968"
product_info = get_product_details(sku)
print(product_info)
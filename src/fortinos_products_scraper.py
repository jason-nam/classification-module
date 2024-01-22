from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

def get_items_from_subcategory(driver, url):
    # Navigate to the subcategory page
    driver.get(url)
    
    # Wait for the items to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-wbarzq')))
    
    # Find all item containers
    item_containers = driver.find_elements(By.CLASS_NAME, "css-wbarzq")
    
    # List to hold all items
    items = []
    
    # Iterate over all item containers to extract information
    for item in item_containers:
        # Extract the brand, name, price, product number (ID), and image URL
        brand = name = price = product_number = image_url = None

        try:
            brand = item.find_element(By.CSS_SELECTOR, "[data-testid='product-brand']").text.strip()
        except NoSuchElementException:
            pass

        try:
            name = item.find_element(By.CSS_SELECTOR, "[data-testid='product-title']").text.strip()
        except NoSuchElementException:
            pass

        try:
            price = item.find_element(By.CSS_SELECTOR, "[data-testid='price']").text.strip()
        except NoSuchElementException:
            pass
            
        try:
            product_number = item.find_element(By.CSS_SELECTOR, "[data-testid='product-title']").get_attribute('id').strip()
        except NoSuchElementException:
            pass
        
        try:
            image_element = item.find_element(By.CSS_SELECTOR, "[data-testid='product-image'] img")
            image_url = image_element.get_attribute('src').strip()
        except NoSuchElementException:
            pass
        
        items.append({
            "brand": brand,
            "name": name,
            "price": price,
            "product_number": product_number,
            "image_url": image_url
        })
    
    return items

# Set up the Selenium browser instance with Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Optional: Run in headless mode without opening a browser window
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    url = "https://www.fortinos.ca/food/fruits-vegetables/fresh-vegetables/c/28195?page=2"
    items_info = get_items_from_subcategory(driver, url)

    print(len)

    for item in items_info:
        print(item)
finally:
    driver.quit()

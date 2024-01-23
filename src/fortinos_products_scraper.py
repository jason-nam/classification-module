from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

import requests
import os

def download_image(image_url, folder_path, product_number):
    # Create the directory if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Get the image content
    response = requests.get(image_url)
    if response.status_code == 200:
        # Write the image content to a file
        with open(os.path.join(folder_path, product_number + '.png'), 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download image for product number {product_number}")

def get_image_url(image_element):
    # Check if 'src' attribute is available, otherwise fall back to 'data-src' if it's lazy-loaded
    image_url = image_element.get_attribute('src')

    if not image_url or 'data:image' in image_url:  # Placeholder images are sometimes encoded in base64
        image_url = image_element.get_attribute('data-src')

    return image_url

def get_items_from_url(driver, url):
    # Navigate to the subcategory page
    driver.get(url)
    
    # Wait for the items to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-175gnef')))
    
    # Find all item containers
    item_containers = driver.find_elements(By.CLASS_NAME, "css-175gnef")
    
    # List to hold all items
    items = []
    
    # Iterate over all item containers to extract information
    for item in item_containers:
        # Extract the brand, name, price, product number (ID), and image URL
        brand = name = was_price = price = product_number = image_url = None

        try:
            brand = item.find_element(By.CSS_SELECTOR, "[data-testid='product-brand']").text.strip()
        except NoSuchElementException:
            pass

        try:
            name = item.find_element(By.CSS_SELECTOR, "[data-testid='product-title']").text.strip()
        except NoSuchElementException:
            pass

        try:
            was_price = item.find_element(By.CSS_SELECTOR, "[data-testid='was-price']").text.strip()
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
            image_element = item.find_element(By.CSS_SELECTOR, "img.chakra-image")  # Adjusted selector for image
            driver.execute_script("arguments[0].scrollIntoView();", image_element)
            WebDriverWait(driver, 5).until(EC.visibility_of(image_element))  # Wait for image to be visible
            image_url = get_image_url(image_element)
        except NoSuchElementException:
            pass

        items.append({
            "brand": brand,
            "name": name,
            "price": price,
            "was_price": was_price,
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
    url = "https://www.fortinos.ca/food/fruits-vegetables/fresh-vegetables/c/28195?page=1"
    items_info = get_items_from_url(driver, url)

    print(len(items_info))

    for item in items_info:
        if item['image_url']:
            download_image(item['image_url'], 'downloaded_images', item['product_number'])
        print(item)
finally:
    driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from urllib.parse import urljoin
import logging

from global_vars import FORTINOS_BASE_URL


BAD_CHARACTERS = ['?', '#', '=']

logging.basicConfig(level=logging.INFO)

def get_urls(driver, url):
    try:
        driver.get(url)
        WebDriverWait(driver, 40).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

        anchors = driver.find_elements(By.TAG_NAME, "a")
        links = set()

        logging.info(f'Crawling through {url} ...')

        for i in range(len(anchors)):
            try:
                anchor = driver.find_elements(By.TAG_NAME, "a")[i]
                link = anchor.get_attribute('href')
                if (
                    link and url not in link 
                    and '/c/' in link and '?' in link
                ):
                    full_url = urljoin(url, link.split('?')[0] if '?' in link else None)
                    links.add(full_url)
                elif (
                    link and url not in link
                    and not any(char in link for char in BAD_CHARACTERS) 
                    and '/c/' in link
                ):
                    full_url = urljoin(url, link)
                    links.add(full_url)

                # if link and url not in link and not any(char in link for char in BAD_CHARACTERS) and '/c/' in link:
                #     full_url = urljoin(url, link)
                #     links.add(full_url)
            except StaleElementReferenceException:
                continue

        if not links:
            logging.warning(f'No links found at {url}')
        
        logging.info(f'Successfully crawled through {url}')
        return links

    except Exception as e:
        logging.error(f'Error while crawling {url}: {e}')
        return set()


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    base_urls = FORTINOS_BASE_URL
    all_urls = []

    try:
        for base_url in base_urls:
            all_urls = list(set(get_urls(driver, base_url)).union(all_urls))

        for url in all_urls:
            print(url)
    finally:
        driver.quit()

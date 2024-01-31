from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from urllib.parse import urljoin
import logging

from global_vars import FORTINOS_BASE_URL, FORTINOS_AVOID_URL


BAD_CHARACTERS = ['?', '#', '=']

def _setup_logging():
    logging.basicConfig(level=logging.INFO)

def crawl_through_urls(driver, url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

        anchors = driver.find_elements(By.TAG_NAME, "a")
        links = set()

        logging.info(f'Crawling through {url} ...')

        for i in range(len(anchors)):
            try:
                anchor = driver.find_elements(By.TAG_NAME, "a")[i]
                link = anchor.get_attribute('href')

                # if (
                #     link and url not in link 
                #     and '/c/' in link and '?' in link
                # ):
                #     full_url = urljoin(url, link.split('?')[0] if '?' in link else None)
                #     if (full_url in FORTINOS_AVOID_URL):
                #         logging.info(f'Avoided {full_url}')
                #         continue
                #     links.add(full_url)
                #     logging.info(f'Extracted {full_url}')
                    
                if (
                    link and url not in link
                    and not any(char in link for char in BAD_CHARACTERS) 
                    and '/c/' in link
                ):
                    full_url = urljoin(url, link) 
                    if (full_url in FORTINOS_AVOID_URL):
                        logging.info(f'Avoided {full_url}')
                        continue
                    links.add(full_url)
                    logging.info(f'Extracted {full_url}')

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
    _setup_logging()

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    base_urls = FORTINOS_BASE_URL
    all_urls = []

    try:
        for base_url in base_urls:
            all_urls = list(set(crawl_through_urls(driver, base_url)).union(all_urls))

        for url in all_urls:
            print(url)
    finally:
        driver.quit()
else:
    logging.basicConfig(level=logging.WARNING)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

from urllib.parse import urljoin

def get_all_links(driver, url):
    driver.get(url)
    driver.implicitly_wait(10)

    # Get the list of all anchor elements on the page
    anchors = driver.find_elements(By.TAG_NAME, "a")
    links = set()

    # Re-fetch the anchor elements by their index to avoid StaleElementReferenceException
    for i in range(len(anchors)):
        try:
            # Re-locate the anchor element
            anchor = driver.find_elements(By.TAG_NAME, "a")[i]
            link = anchor.get_attribute('href')

            bad_characters = ['?', '#', '=']

            if link and url not in link and not any(char in link for char in bad_characters) and '/c/' in link:
                # Make sure the link is a full URL
                full_url = urljoin(url, link)
                links.add(full_url)
        except StaleElementReferenceException:
            # If the element has gone stale, skip and move to the next
            continue

    return links

# Set up the Selenium browser instance with Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Optional: Run in headless mode without opening a browser window
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    base_url = 'https://www.fortinos.ca/home-and-living/c/27986'
    all_links = get_all_links(driver, base_url)
    for link in all_links:
        print(link)
finally:
    driver.quit()

"""
https://www.fortinos.ca/food/c/27985
https://www.fortinos.ca/home-and-living/c/27986
https://www.fortinos.ca/baby/c/27987
https://www.fortinos.ca/pet-supplies/c/27988
https://www.fortinos.ca/health-beauty/c/27994
"""

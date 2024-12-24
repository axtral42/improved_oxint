from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver=None
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration

# Set up the ChromeDriver service
service = Service('/usr/bin/chromedriver')

# Initialize the WebDriver with options and service
driver = webdriver.Chrome(service=service, options=chrome_options)

def facebook_crawl(link):
    driver.get(link)

    dialog=driver.find_element(By.XPATH,"//div[@role = 'dialog']")
    cross=dialog.find_element(By.XPATH,".//div[@role = 'button']").click()

    driver.save_screenshot('facebook.png')
    return 'facebook.png'


def linkedin_crawl(link):
    pass

def instagram_crawl(link):
    pass

def x_crawl(link):
    pass

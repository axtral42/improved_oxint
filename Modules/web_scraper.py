from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment to run Chrome in headless mode
chrome_prefs = {
    "profile.managed_default_content_settings.images": 2,  # Disable images
    "profile.managed_default_content_settings.stylesheets": 2,  # Disable CSS (optional, if not needed)
    #"profile.managed_default_content_settings.javascript": 2,  # Disable JavaScript (optional, if not needed)
    "profile.managed_default_content_settings.plugins": 2,  # Disable Plugins (optional)
}

chrome_options.add_experimental_option("prefs", chrome_prefs)

# Set up the ChromeDriver service
service = Service('/usr/bin/chromedriver')

# Initialize the WebDriver with options and service
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define WebDriverWait (increase timeout for slow-loading React apps)
wait = WebDriverWait(driver, 30)  # Increase wait time for React content to load

# Navigate to the webpage
driver.get('https://www.instagram.com/anshsharma_')
print("Selenium launched")
time.sleep(20)
# Wait for a specific element that indicates page load (e.g., profile header or username)
# Modify this to wait for an element that uniquely appears after the page fully loads
#wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(@class, 'rhpdm')]")))  # Example XPath for Instagram profile

# Once the page is loaded, we can get the final HTML source of the page
page_source = driver.page_source

# Print the page source or extract text from it
#print(page_source)

# Optional: Extract specific text (e.g., username or bio)
#username = driver.find_element(By.XPATH, "//h1[contains(@class, 'rhpdm')]").text  # Example username
#bio = driver.find_element(By.XPATH, "//div[contains(@class, 'QGPIr')]").text  # Example bio
#print(f"Username: {username}")
#print(f"Bio: {bio}")

# Don't forget to quit the driver after scraping
#driver.quit()

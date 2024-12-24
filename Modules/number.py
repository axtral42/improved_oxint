from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def find_trace(number):
    driver = None
    try:
        # Set up headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration

        # Set up the ChromeDriver service
        service = Service('/usr/bin/chromedriver')

        # Initialize the WebDriver with options and service
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Navigate to the webpage
        driver.get('https://www.findandtrace.com/')
        print("selenium launched")

        # Find the input box (assuming it has an ID attribute)
        input_box = driver.find_element(By.NAME, "mobilenumber")
        print("found")

        # Input data into the input box
        input_box.send_keys(number)
        print("number input")
        # Example of hitting Enter key (optional)
        input_box.send_keys(Keys.RETURN)

        wait = WebDriverWait(driver, 10)
        tables = wait.until(EC.presence_of_all_elements_located((By.ID, "customers")))

        res = []

        # Iterate through each table and extract data
        for table in tables:
            rows = table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                for cell in cells:
                    res.append(cell.text)

        # Creating the dictionary
        result_dict = {res[i]: res[i + 1] for i in range(0, len(res) - 1, 2)}
        clean_dict = {key.rstrip(':') if isinstance(key, str) and key.endswith(':') else key: value for key, value in result_dict.items()}

        return clean_dict

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser if it was initialized
        if driver:
            driver.quit()

def free_carrier_lookup(code, number):
    driver = None
    try:
        # Set up headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
        
        # Set up the ChromeDriver service
        service = Service('/usr/bin/chromedriver')

        # Initialize the WebDriver with options and service
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Navigate to the webpage
        driver.get('https://freecarrierlookup.com/')

        input_box1 = driver.find_element(By.ID, "phonenum")
        input_box1.send_keys(number)

        input_box = driver.find_element(By.ID, "cc")
        input_box.clear()
        input_box.send_keys(code)

        time.sleep(2)

        input_box.send_keys(Keys.RETURN)

        # Submit the form by clicking the Search button
        search_button = driver.find_element(By.XPATH, "//input[@value='Search']")
        driver.execute_script("arguments[0].click();", search_button)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.ID, "search-result")))

        # Extracting data from the search results
        num = driver.find_element(By.CLASS_NAME, "col-sm-6 col-md-8")
        print(num.text)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser if it was initialized
        if driver:
            driver.quit()

def main():
    print(type(7840018950))
    result_dict = find_trace(7840018950)

    if result_dict:
        for key, value in result_dict.items():
            print(f"{key}: {value}\n")

    # carrier lookup not working
    # free_carrier_lookup(91, 9540018950)

if __name__ == "__main__":
    print(find_trace(9082593918))

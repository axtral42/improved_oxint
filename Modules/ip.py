import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key= os.getenv('ip_api')
# Function to get IP info from Shodan
def get_shodan_info(api_key, ip):
    url = f'https://api.shodan.io/shodan/host/{ip}?key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Shodan API request failed with status code {response.status_code}"}

# Function to get IP info from CentralOps without logging in
def get_centralops_info(ip):
    # Set up the WebDriver (Chrome in this case)
    service = Service('/usr/bin/chromedriver')  # Adjust the path to where your ChromeDriver is located
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 10)
    
    try:
        # Navigate to the Domain Dossier page
        driver.get(f'https://centralops.net/co/DomainDossier.aspx?addr={ip}&dom_whois=1')
        
        # Wait for the results to load and grab the HTML
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'pre')))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        results = soup.find_all("pre")
        
        return {"results": [result.text for result in results]}
    finally:
        driver.quit()

# Function to extract location from Shodan data
def extract_location_shodan(shodan_data):
    if 'error' in shodan_data:
        return shodan_data
    location = {
        "country": shodan_data.get('country_name', 'Unknown Country'),
        "city": shodan_data.get('city', 'Unknown City')
    }
    return location

# Function to extract location from CentralOps data
def extract_location_centralops(centralops_data):
    if 'error' in centralops_data:
        return centralops_data
    # Here, parse the location information from the CentralOps data
    # This is an example and might need to be adjusted based on the actual HTML structure
    location = {"country": "Unknown Country", "city": "Unknown City"}
    for result in centralops_data["results"]:
        if "Country" in result:
            location["country"] = result.split("Country:")[1].strip().split()[0]
        if "City" in result:
            location["city"] = result.split("City:")[1].strip().split()[0]
    return location

def ipinfo(ip):

    # Fetch data from Shodan
    shodan_info = get_shodan_info(api_key, ip)
    shodan_location = extract_location_shodan(shodan_info)
    
    return [shodan_info,shodan_location]
    
    #print("Shodan Info:")
    #for i in shodan_location:
    #    print(i,shodan_location[i])

    # Fetch data from CentralOps without logging in
    #centralops_info = get_centralops_info(args.ip)
    #centralops_location = extract_location_centralops(centralops_info)
    #print("CentralOps Info:")
    #print(centralops_info)
    #print("CentralOps Location:")
    #print(centralops_location)

if __name__ == "__main__":
    print(ipinfo("142.250.67.46"))
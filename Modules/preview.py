from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from bs4 import BeautifulSoup
import re
import json


driver=None
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
chrome_options.add_argument("window-size=1920,1080")
# Set up the ChromeDriver service
service = Service('/usr/bin/chromedriver')

# Initialize the WebDriver with options and service
driver = webdriver.Chrome(service=service, options=chrome_options)
search_results=[]
instagram=[]
facebook=[]
linkedin=[]
twitter=[]
email=[]
phonenum=[]
external_link=[]
bio=[]
content=[]

def sm_classify(info):
    sm_class=""
    try:
        if "https" in info:
            if "instagram" in info:
                sm_class="instagram"
                instagram.append(info)
                return sm_class,instagram
            elif "twitter.com" in info:
                sm_class="twitter"
                twitter.append(info)
                return sm_class,twitter
            elif "linkedin" in info:
                sm_class="linkedin"
                linkedin.append(info)
                return sm_class,linkedin
            elif "facebook" in info and "php" not in info:
                sm_class="facebook"
                facebook.append(info)
                return sm_class,facebook
            else:
                sm_class="external_site"
                external_link.append(info)
                return sm_class,external_link
        elif "@" in info:
            sm_class="email"
            email.append(info)
            return sm_class,email
        elif isinstance(eval("1"+info.replace(" ",'')),int):
            sm_class="phonenum"
            phonenum.append(info)
            return sm_class,phonenum
        else:
            
            sm_class="bio"
            bio.append(info)
            return sm_class,bio
    except:
        sm_class="content"
        content.append(info)
        return sm_class,content
    return sm_class

def classify(social_media):
    posts=[]
    profile=[]
    for i in social_media:
        if "reel" not in i and "status" not in i and "post" not in i:
            profile.append(i)
        else:
            posts.append(i)
    classified={}
    for i in profile:
        result=sm_classify(i)
        classified[result[0]]=result[1]
    return classified,posts

def extract_facebook_bio_item(i):
    if "external_url" in i:
        new=i.split('"external_url":')
        text=new[1].split(",")
        text=text[0].replace("\/","/")
    else:    
        new=i.split('"text":')
        text=new[1].split("}")
        text=text[0]
    text=text.replace("\/","/")
    text=text.replace('"','')
    text=text.replace(r'\u0025','%')
    text=text.replace(r'\u0040','@')
    return text

def facebook_crawl(link):
    driver.get(link)

    dialog=driver.find_element(By.XPATH,"//div[@role = 'dialog']")
    cross=dialog.find_element(By.XPATH,".//div[@role = 'button']").click()
    driver.save_screenshot('facebook.png')
    content=driver.page_source
    soup = BeautifulSoup(content, 'html5lib')
    links=soup.find_all("div",class_="x9f619 x1n2onr6 x1ja2u2z xeuugli x1iyjqo2 xs83m0k xjl7jj x1xmf6yo x1emribx x1e56ztr x1i64zmx xnp8db0 x65f84u x1xzczws") #for intro
    #also do for about page, hint: it has a seperate link with /about and many more
    print(links)
    return 'facebook.png'


def linkedin_crawl(link):
    pass

def instagram_crawl(link):
    pass

def x_crawl(link):
    pass

if __name__=="__main__":
    facebook_crawl("https://www.facebook.com/narendramodi/")

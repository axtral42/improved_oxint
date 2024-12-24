import requests
from bs4 import BeautifulSoup

search_results=[]

web_result=search_results[1]

online_presence=web_result

email=search_results[2]

r=requests.get(email[9])
soup=BeautifulSoup(r.content,'html5lib')
print(soup.prettify())
import requests
from bs4 import BeautifulSoup
import re
import json


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
                print("External Link:", info)
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
        #print(classified)
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


headers_dict = {
    "Host": "www.facebook.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Cookie": "datr=iJJ9Z3Dt1R6EsUSpk_c5JHHw; sb=iJJ9ZwN8oNewTyNrs1uvAQv4; wd=1920x503",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-GPC": "1",
    "TE": "trailers"

}



def facebook_extractor(link):
    r=requests.get(link)
    print(r.content)
    #
    soup=BeautifulSoup(r.content,'html5lib')
    
    #intro_card=soup.find(string=re.compile("INTRO_CARD")).text
    
    intro_card=soup.find_all(string="ContextItemDefaultRenderer")
    

    intro_card=intro_card.split("ContextItemDefaultRenderer")
    website_card=intro_card[-1].split("WebsiteContextItemRenderer")
    found=[]
    content={}
    total=[0,0]
    for i in intro_card[0:-1]:
        try:
            found.append(extract_facebook_bio_item(i))
        except:
            pass
    for i in website_card:
        try:
            found.append(extract_facebook_bio_item(i))
        except:
            pass
    for i in found:
        result=sm_classify(i)
        content[result[0]]=result[1]
    return content


if __name__=="__main__":
    print(facebook_extractor("https://www.facebook.com/tandon.rakshit/"))
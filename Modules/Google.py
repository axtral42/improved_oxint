
import requests
import json
from dotenv import load_dotenv
from os import getenv

load_dotenv()
api_key = getenv('g_api_key')
cx = getenv('g_cx')
initial_query=''

dorks={
    'sm': 'site:linkedin.com OR site:twitter.com OR site:instagram.com OR site:facebook.com', #search for social media profiles
    'email': '*.com', #search for email and website
    'gs': '-linkedin.com -twitter.com -instagram.com -facebook.com', #search for information on the internet
    'docs': 'filetype:pdf OR filetype:xlsx OR filetype:docx OR filetype:PPT OR filetype:pptx', #search for related documents
}

#input: name / search string
#output: google search, socialmedia search, image search

def get_google_search_results(api_key, cx, **kwargs):
    # Base URL for Google Custom Search API
    base_url = "https://www.googleapis.com/customsearch/v1"
    
    # Required parameters
    params = {
        'key': api_key,
        'cx': cx
    }
    
    # Include all additional parameters
    params.update(kwargs)
    
    # Construct the URL with the parameters
    response = requests.get(base_url, params=params)
    data = response.json()
    # Check for errors or empty search results
    if 'error' in data:
        print(data)
    elif 'items' not in data:
        print("hi")
        return {"message": "No search results found."}
    else:
        # Extract search results
        search_results = data['items']
        return search_results

# Example usage
def gen_params(name,keywords='',is_famous=False):
    global initial_query
    keywords=keywords+' '
    if is_famous:
        initial_query = f'intitle:"{name}" ' + keywords
    else:
            initial_query = f'intext:"{name}" '+keywords 

    search_params=[f'intitle:"{name}" '+keywords+dorks['sm']]
    search_params.append(f'intext:"{name}"'+dorks["email"])

    for i in list(dorks.values())[2:]:
        search_params.append(initial_query+i)
    return search_params

def Dork(name,keywords='',is_famous=False):

    query=gen_params(name,keywords,is_famous)
    result=[]

    for i in query: 
        search_params={
            'q': i,
        }    
        result.append(get_google_search_results(api_key, cx, **search_params))

    search_params={
            'q': initial_query,
            'searchType' : 'image'
        } 
    result.append(get_google_search_results(api_key, cx, **search_params))
    print("Images done")
    final=[]
    k=0
    for j in result:
        row=[]
        for i in j:
            try:
                
                row.append(i['link'])
            except:
                row.append([])
        
        final.append(row)
    return final

if __name__=='__main__':
    print(Dork("Amit dubey","Cybersecurity"))
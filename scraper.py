import requests
from bs4 import BeautifulSoup
import json


def get_desc(search_string):
    url = search_string
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        result = soup.css.select('header p p')
        return result

def scraper(keyword):
    url = "https://www.arise.tv/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article')
        
        results = []
        
        for article in articles:
            if keyword in article.text.lower():
                title = article.css.select('h3 a')
                img_link = article.css.select('div a img')
                page_link = article.css.select('h3 a')
                date = article.css.select('.date')
                posted_by = article.css.select('a[rel = "author"]')
                desc = article.css.select('p')
                
                #to check whether its an empty array before trying to get the data
                #else it would return an empty string 
                # this is to prevent error of tring reference an index from an empty array
                data = {
                    'title': (title[0]).text if len(title) > 0 else '',
                    'img_link': (img_link[0]).get('src') if len(img_link) > 0 else '',
                    'page_link': (page_link[0]).get('href') if len(page_link) > 0 else '',
                    'date': (date[0]).text if len(date) > 0 else '',
                    'posted_by': (posted_by[0]).text if len(posted_by) > 0 else '',
                }

                search_string = (title[0]).get('href')
                desc = get_desc(search_string)
                data['desc'] = (desc[0]).text if len(desc) > 0 else ''
                
                data_json = json.dumps(data)
                results.append(data_json)
        
        return results
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")
        return []



while(True):
    keyword = (input('Enter your keyword: ')).lower()
    results = scraper(keyword)

    for result in results:
        print(result)
    
    if len(results) == 0:
        print('There are no results that match your search')
        
    retry = input('Press Enter to try again or input q to print ')
    if retry == 'q':
        break


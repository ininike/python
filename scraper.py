import requests
from bs4 import BeautifulSoup

def scraper(keyword):
    url = "https://www.arise.tv/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article')
        results = []
        
        for article in articles:
            if keyword in article.text.lower():
                results.append(article.text.strip())
        
        return results
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")
        return []


while(True):
    keyword = (input('Enter your keyword: ')).lower()
    results = scraper(keyword)
    
    for result in results:
        print('..',result,'..')
        
    if len(results) == 0:
        print('There are no results that match your search')
        
    retry = input('Press Enter to try again or input q to print ')
    if retry == 'q':
        break
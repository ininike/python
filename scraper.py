import multiprocessing
import requests
from bs4 import BeautifulSoup
import json


class Scraper:
    def __init__(self, home_url):
        self.home_url = home_url
    
    def _get_string(self, soup, selector, type):
        if type == 'text':
            return ((soup.css.select(selector))[0]).text 
        if type == 'link':
            return ((soup.css.select(selector))[0]).get('href')
        if type == 'img':
            return ((soup.css.select(selector))[0]).get('src')    
        
    def _get_articles_links(self, link_selector, keyword):
        response = requests.get(self.home_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article')
            links = []
            for article in articles:
                if keyword.lower() in article.text.lower():
                    link = self._get_string(article,link_selector,'link')
                    links.append(link)
            return links
        else:
            return f"Failed to retrieve the website. Status code: {response.status_code}"
        
    def _scrape_article(self, link, selector_dict, queue):
        response = requests.get(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            data = {
                'title': self._get_string(soup,selector_dict['title'],'text'),
                'img_link': self._get_string(soup,selector_dict['img_link'],'img'),
                'page_link': link,
                'date': self._get_string(soup,selector_dict['date'],'text'),
                'posted_by': self._get_string(soup,selector_dict['posted_by'],'text'),
                'desc': self._get_string(soup,selector_dict['desc'],'text')
            }
            data_json = json.dumps(data)
            print(data_json)
            queue.put(data_json)
        else:
            queue.put(f"Failed to retrieve the website({link}). Status code: {response.status_code}") 
    
    def _consumer(self, queue, length):
        results = []
        for _ in range(length):
            results.append(queue.get())
        queue.put(results)
        
    def scrape(self, selector_dict, keyword = ''):
        if __name__ == '__main__':
            multiprocessing.freeze_support()
            multiprocessing.set_start_method('spawn')
            queue = multiprocessing.SimpleQueue()
            
            links = self._get_articles_links(selector_dict['page_link'],keyword)
            if isinstance(links,str):
                return links
            
            c = multiprocessing.Process(target=self._consumer, args=(queue, len(links)))
            c.start()     
            for i in range(len(links)):
                p = multiprocessing.Process(target=self._scrape_article, args=(links[i], selector_dict, queue,))
                p.start() 
            for i in range(len(links)): 
                p.join()        
            c.join(1.0)
            
            results = queue.get()
            if len(results) == 0:
                results = ['There are no results that match your search']
            return results
        

arisenews = Scraper('https://www.arise.tv/')     

selector_dict = {
    'title': 'h1',
    'img_link': '.wp-post-image',
    'page_link': '.img-link',
    'date': '.date',
    'posted_by': 'a[rel = "author"]',
    'desc': 'header p p'
}

results =  arisenews.scrape(selector_dict,'miners') 
print(str(results)) 



        
    
        
        
        
    
    
        
        
    

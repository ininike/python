import multiprocessing
import requests
from bs4 import BeautifulSoup
import json


class AriseTVScraper:
    def __init__(self, home_url):
        self.home_url = home_url
    
    def _get_string(self, soup, selector, type):
        if type == 'text':
            return ((soup.css.select(selector))[0]).text 
        if type == 'link':
            return ((soup.css.select(selector))[0]).get('href')
        if type == 'img':
            return ((soup.css.select(selector))[0]).get('src')    
        
    def _get_articles_links(self,  keyword):
        response = requests.get(self.home_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article')
            links = []
            for article in articles:
                if keyword.lower() in article.text.lower():
                    link = self._get_string(article,'.img-link','link')
                    links.append(link)
            return links
        else:
            return f"Failed to retrieve the website. Status code: {response.status_code}"
        
    def _scrape_article(self, link, queue):
        response = requests.get(link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            data = {
                'title': self._get_string(soup,'h1','text'),
                'img_link': self._get_string(soup,'.wp-post-image','img'),
                'page_link': link,
                'date': self._get_string(soup,'.date','text'),
                'posted_by': self._get_string(soup,'a[rel = "author"]','text'),
                'desc': self._get_string(soup,'header p p','text')
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
        
    def scrape(self, keyword = ''):
        if __name__ == '__main__':
            multiprocessing.freeze_support()
            multiprocessing.set_start_method('spawn')
            queue = multiprocessing.SimpleQueue()
            
            links = self._get_articles_links(keyword)
            if isinstance(links,str):
                return links
            
            c = multiprocessing.Process(target=self._consumer, args=(queue, len(links)))
            c.start()     
            for i in range(len(links)):
                p = multiprocessing.Process(target=self._scrape_article, args=(links[i], queue,))
                p.start() 
            for i in range(len(links)): 
                p.join()        
            c.join(1.0)
            
            results = queue.get()
            if len(results) == 0:
                results = ['There are no results that match your search']
            return results
        

arisenews = AriseTVScraper('https://www.arise.tv/')     

results =  arisenews.scrape('trump') 

if results != None:
    print(str(results)) 



        
    
        
        
        
    
    
        
        
    

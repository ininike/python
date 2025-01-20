import multiprocessing
import requests
from bs4 import BeautifulSoup
import json

# to get all articles
def get_articles():
    url = "https://www.arise.tv/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article')
        return articles
    else:
        print(f"Failed to retrieve the website. Status code: {response.status_code}")
        return []

#collect data on articles  that match the keyword 
def scrape(articles):
    datas = []
    for article in articles:
        if keyword in article.text.lower():
            title = article.css.select('h3 a')
            img_link = article.css.select('div a img')
            page_link = article.css.select('h3 a')
            date = article.css.select('.date')
            posted_by = article.css.select('a[rel = "author"]')
            
            #to check whether its an empty array before trying to get the data
            #else it would return an empty string 
            # this is to prevent error of string reference an index from an empty array
            #desc for now is just a link to the main page where the desc will be retrieved
            data = {
                'title': (title[0]).text if len(title) > 0 else '',
                'img_link': (img_link[0]).get('src') if len(img_link) > 0 else '',
                'page_link': (page_link[0]).get('href') if len(page_link) > 0 else '',
                'date': (date[0]).text if len(date) > 0 else '',
                'posted_by': (posted_by[0]).text if len(posted_by) > 0 else '',
                'desc': (page_link[0]).get('href') if len(page_link) > 0 else ''
            }
            datas.append(data)
    return datas

#get_desc process function to get article description to complete the scraped article data 
# with its corresponding desc and convert it all to json
def get_desc(results_before_desc, i,q):
        x = results_before_desc[i]
        url = x['desc']
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            desc = soup.css.select('header p p')
            x['desc'] = (desc[0]).text if len(desc) > 0 else ''
            x_json = json.dumps(x)
            print(x_json)
            q.put(x_json)
        else:
            print(f"Failed to retrieve the website. Status code: {response.status_code}")
        return []

#consumer process function to read all the json strings in the queue and append to a list           
def consumer(q, results_before_desc):
    results = []
    for x in range(len(results_before_desc)):
        results.append(q.get())
    q.put(results)
    

#main codeblock
if __name__ == '__main__':
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn')
    q = multiprocessing.SimpleQueue()
    
    articles = get_articles()
    while(True):
        keyword = (input('Enter your keyword: ')).lower() 
        results_before_desc = scrape(articles)

        #starting processes
        c = multiprocessing.Process(target=consumer, args=(q,results_before_desc,))
        c.start()     
        for i in range(len(results_before_desc)):
            p = multiprocessing.Process(target=get_desc, args=(results_before_desc,i,q,))
            p.start()  
        p.join()        
        c.join(1.0)
        
        #output
        results = q.get()
        print(f'{len(results)} articles found')
        
        if len(results) == 0:
            print('There are no results that match your search')
            
        retry = input('Press Enter to try again or input q to quit ')
        if retry == 'q':
            c.close()
            quit()

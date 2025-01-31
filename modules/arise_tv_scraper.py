import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json


class AriseTVScraper:
    def __init__(self):
        pass
    
    async def _get_string(self, soup, selector, type):
        if type == 'text':
            return ((soup.select(selector))[0]).text
        if type == 'link':
            return ((soup.select(selector))[0]).get('href')
        if type == 'img':
            return ((soup.select(selector))[0]).get('src')

    async def _fetch(self, session, url):
        try:
            async with session.get(url) as response:
                return await response.text()
        except aiohttp.ClientConnectorError as e:
            print('Connection Error', str(e))
            return ''
            

    async def _get_articles_links(self, session, keyword):
        url = "https://www.arise.tv/"
        content = await self._fetch(session, url)
        soup = BeautifulSoup(content, 'html.parser')
        articles = soup.find_all('article')
        links = []
        for article in articles:
            if keyword.lower() in article.text.lower():
                link = await self._get_string(article, '.img-link', 'link')
                links.append(link)
        return links

    async def _scrape_article(self, session, link):
        content = await self._fetch(session, link)
        soup = BeautifulSoup(content, 'html.parser')
        data = {
            #--------------------------------------
            #This is where you change the selectors
            #--------------------------------------
            'title': await self._get_string(soup, 'h1', 'text'),
            'img_link': await self._get_string(soup, '.wp-post-image', 'img'),
            'page_link': link,
            'date': await self._get_string(soup, '.date', 'text'),
            'posted_by': await self._get_string(soup, 'a[rel = "author"]', 'text'),
            'desc': await self._get_string(soup, 'header p p', 'text')
        }
        return json.dumps(data)

    async def scrape(self, keyword=''):
        async with aiohttp.ClientSession() as session:
            try:
                links = await self._get_articles_links(session, keyword)
            except aiohttp.ClientConnectorError as e:
                print('Connection Error', str(e))
            tasks = [self._scrape_article(session, link) for link in links]
            results = await asyncio.gather(*tasks)
            if not results:
                results = ['There are no results that match your search']
            return results


async def main():
    results = await AriseTVScraper().scrape()
    if results:
        print(results)


if __name__ == '__main__':
    asyncio.run(main())

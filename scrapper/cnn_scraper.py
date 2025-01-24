import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json


class CNNScraper:
    def __init__(self):
        pass
    
    async def _get_string(self, soup, selector, type):
        if type == 'text':
            string = soup.select(selector)
            return ((string[0]).text.strip()).replace('  ','') if len(string) > 0 else None
        if type == 'link':
            string = soup.select(selector)
            return (string[0]).get('href') if len(string) > 0 else None
        if type == 'img':
            string = soup.select(selector)
            return (string[0]).get('src') if len(string) > 0 else None

    async def _fetch(self, session, url):
        try:
            async with session.get(url) as response:
                return await response.text()
        except aiohttp.ClientConnectorError as e:
            print('Connection Error', str(e))
            return ''
            

    async def _get_articles_links(self, session, keyword):
        url = "https://edition.cnn.com"
        content = await self._fetch(session, url)
        soup = BeautifulSoup(content, 'html.parser')
        articles = soup.select('.card')
        links = []
        for article in articles:
            
            if keyword.lower() in article.text.lower():
                link = url + await self._get_string(article, 'a:nth-of-type(1)', 'link')
                links.append(link)
        return links

    async def _scrape_article(self, session, link):
        content = await self._fetch(session, link)
        if content == '':
            return None
        soup = BeautifulSoup(content, 'html.parser')
        data = {
            #--------------------------------------
            #This is where you change the selectors
            #--------------------------------------
            'title': await self._get_string(soup, 'h1', 'text'),
            'img_link': await self._get_string(soup, '.image__dam-img:nth-of-type(1)', 'img'),
            'page_link': link,
            'date': await self._get_string(soup, '.headline__byline-sub-text .timestamp', 'text'),
            'posted_by': await self._get_string(soup, '.byline__name', 'text'),
            'desc': await self._get_string(soup, '.paragraph:nth-of-type(1)', 'text')
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
    results = await CNNScraper().scrape()
    if results:
        print(results)


if __name__ == '__main__':
    asyncio.run(main())
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json


class ChannelsTVScraper:
    def __init__(self):
        pass
    
    async def _get_string(self, soup, selector, type):
        if type == 'text':
            string = soup.select(selector)
            return (string[0]).text if len(string) > 0 else None
        if type == 'link':
            string = soup.select(selector)
            return (string[0]).get('href') if len(string) > 0 else None
        if type == 'img':
            string = soup.select(selector)
            return (string[0]).get('src') if len(string) > 0 else None

    async def _fetch(self, session, url):
        apikey = '4fa3f1c48f1396185b469494f6f16838a7d7aad3'
        params = {
            'url': url,
            'apikey': apikey,
            'premium_proxy': 'true',
        }
        try:
            async with session.get('https://api.zenrows.com/v1/', params = params) as response:
                return await response.text()
        except aiohttp.ClientConnectorError as e:
            print('Connection Error', str(e))
            return ''

    async def _get_articles_links(self, session, keyword):
        url = "https://www.channelstv.com/"
        content = await self._fetch(session, url)
        soup = BeautifulSoup(content, 'html.parser')
        articles = soup.find_all('article')
        links = []
        for article in articles:
            if keyword.lower() in article.text.lower():
                #------------------------------------------------------------
                #This is where you change the home page article link selector
                #------------------------------------------------------------
                link = await self._get_string(article, 'h3 a', 'link')
                links.append(link)
        return links

    async def _scrape_article(self, session, link):
        content = await self._fetch(session, link)
        soup = BeautifulSoup(content, 'html.parser')
        data = {
            #--------------------------------------
            #This is where you change the selectors
            #--------------------------------------
            'title': await self._get_string(soup, '.post-title', 'text'),
            'img_link': await self._get_string(soup, '.wp-post-image', 'img'),
            'page_link': link,
            'date': await self._get_string(soup, '.post-time', 'text'),
            'posted_by': await self._get_string(soup, '.post-author', 'text'),
            'desc': await self._get_string(soup, '.lead', 'text')
        }
        return json.dumps(data)

    async def scrape(self, keyword=''):
        async with aiohttp.ClientSession() as session:
            try:
                links = await self._get_articles_links(session, keyword)
            except aiohttp.ClientConnectorError as e:
                print('Connection Error', str(e))
            tasks = [self._scrape_article(session, link) for link in links if link != None]
            results = await asyncio.gather(*tasks)
            if not results:
                results = ['There are no results that match your search']
            return results


async def main():
    results = await ChannelsTVScraper().scrape('trump')
    if results:
        print(results)


if __name__ == '__main__':
    asyncio.run(main())

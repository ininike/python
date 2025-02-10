import aiohttp
import asyncio
from bs4 import BeautifulSoup

class PFPScraper:
    def __init__(self):
        pass

    async def _fetch(self, session, url):
        print (url)
        try:
            async with session.get(url, allow_redirects=True, headers={'User-Agent': 'python-requests/2.20.0'}) as response:
                return await response.text()
        except:
            return ''
    
    def _filter(self,tag):
        def img_test():
            is_img_tag = tag.name == 'img'
            is_pfp = (class_test() or src_test()) and is_img_tag
            return is_pfp
            
        def div_test():
            is_div_tag = tag.name == 'div' 
            is_pfp = is_div_tag and style_test() and class_test()
            return is_pfp
        
        def meta_test():
            is_meta_tag = tag.name == 'meta'
            is_pfp = is_meta_tag and open_graph_test()
            return is_pfp
        
        test_strings = ['profile', 'avatar', 'user', 'account' ]
        
        def class_test():
            try:
                classes = ''.join(tag['class'])
            except:
                return False
            is_pfp_class = any([True if string in classes else False for string in test_strings]) 
            return is_pfp_class
        
        def src_test():
            try:
                source = tag['src']
            except:
                return False
            is_pfp_source = any([True if string in source else False for string in test_strings])
            return is_pfp_source
                
        def style_test():
            try:
                style = tag['style']
            except:
                return False
            is_pfp_style = 'background-image' in style
            return is_pfp_style
        
        def open_graph_test():
            try:
                og = tag['property']
            except:
                return False
            is_pfp_ogp = ('og:image' == og) or ('og:image:url' == og) or ('og:image:secure_url' == og)
            return is_pfp_ogp
        return img_test() or div_test() or meta_test()
        
    async def _get_url(self, soup):
        pfp = soup.find(self._filter)
        if pfp is None:
            return 'No Image Found'
        if pfp.name == 'img':
            return pfp.get('src')
        if pfp.name == 'div':
            return pfp.get('style')
        if pfp.name == 'meta':
            return pfp.get('content')
        
    async def _scrape_pages(self, session, link):
        content = await self._fetch(session, link['site_url'])
        soup = BeautifulSoup(content, 'html.parser')
        data = {
            'profile_picture': await self._get_url(soup),
        }
        link.update(data)
        return link

    async def _scrape(self, links):
        async with aiohttp.ClientSession() as session: 
            tasks = [self._scrape_pages(session, link) for link in links]
            results = await asyncio.gather(*tasks)
            if not results:
                results = ['There are no results that match your search']
            return results
    
    def scrape(self, links):
        results = asyncio.run(self._scrape(links))
        return results


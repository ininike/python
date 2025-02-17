import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from selenium_recaptcha_solver import RecaptchaSolver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

DOMAIN = "https://www.google.com"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"

class GoogleDorkScrapper:
    def __init__(self):
        """Initialize the Selenium WebDriver once per session to avoid reloading it repeatedly."""
        self.chrome_options = Options()
        # self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--window-size=1920x1080")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument(f"user-agent={USER_AGENT}")
        
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.solver = RecaptchaSolver(self.driver)
        self.executor = ThreadPoolExecutor(max_workers=4)

    def __del__(self):
        """Ensure the WebDriver is properly closed when the object is deleted."""
        self.driver.quit()
        self.executor.shutdown(wait=True)

    def create_search_string(self, search_string: str):
        """Create a search string for Google Dorking."""
        search_string = f'"{search_string} filetype:pdf OR filetype:xlsx OR filetype:docx OR filetype:doc"'
        return search_string
    
    def sort(self, documents: list, search_string: str) -> list:
        """Sort the search results based on relevance."""
        keywords = search_string.split()
        for document in documents:
            score = 0
            for keyword in keywords:
                if keyword in document["preview"].lower():
                    score += 1
            document["score"] = score
        return sorted(documents, key=lambda x: x["score"], reverse=True)
    
    async def search(self, search_string: str, number_of_pages: int) -> list:
        """Search for pdfs based on a query (async)."""
        html_pages = []
        first_page_html = await self.run_in_thread(self.search_html_contents, search_string)
        html_pages.append(first_page_html)
        first_page_url = self.driver.current_url
        for page_number in range(1, number_of_pages):
            next_page_html = await self.run_in_thread(self.search_other_pages, page_number, first_page_url)
            html_pages.append(next_page_html)
        return await self.extract_search_contents(html_pages, search_string)
    
    async def run_in_thread(self, func, *args):
        """Run blocking functions inside a ThreadPoolExecutor asynchronously."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, func, *args)
    
    def search_html_contents(self, search_string: str) -> str | None:
        """Search for the given search string."""
        search_string = self.create_search_string(search_string)
        try:
            self.driver.get(DOMAIN)
            search = self.driver.find_element(By.NAME,'q')
            search.send_keys(search_string)
            search.send_keys(Keys.RETURN)
            time.sleep(2)
            recaptcha_iframe = self.driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
            self.solver.click_recaptcha_v2(iframe=recaptcha_iframe)
            time.sleep(5) 
            return self.driver.page_source
        except Exception as e:
            print(f"Error: {e}")
            return None
        
    def search_other_pages(self, page_number: int, current_url: str) -> str | None:
        """Navigate to the next page of the search results."""
        start = page_number * 10
        try:
            self.driver.get(f"{current_url}&start={start}")
            time.sleep(5)
            return self.driver.page_source
        except Exception as e:
            print(f"Error: {e}")
            return None

    async def extract_search_contents(self, html_pages: list, search_string: str) -> list:
        """Extract search results from the HTML content."""
        if not html_pages:
            return []
        documents = []
        for html in html_pages:
            soup = BeautifulSoup(html, 'html.parser')
            documents_from_page = [
                {
                    "site_url": section.select_one("h3").text.strip(),         
                    "site_name": section.select_one(".VuuXrf").text.strip(), 
                    "document_link": section.select_one("a").get("href"),
                    "preview": section.select_one(".VwiC3b.yXK7lf.p4wth.r025kc.hJNv6b.Hdw6tb").text.strip(),
                }
                for section in soup.select(".g")
            ]
            documents.extend(documents_from_page)
        documents = self.sort(documents, search_string)
        return documents
    
gds = GoogleDorkScrapper()
results = asyncio.run(gds.search(search_string="inioluwa ayotomiwa adenaike",number_of_pages=2))
if results:
    print(results)


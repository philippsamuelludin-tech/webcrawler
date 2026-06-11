import asyncio
import aiohttp
from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup, Tag #type: ignore
from typing import TypedDict


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

def normalize_url(input_url: str) -> str:
    urlobject = urlsplit(input_url)
    url = f"{urlobject.netloc}{urlobject.path}"
    return url.lower().rstrip("/")

def get_heading_from_html(html: str) -> str: 
    text = BeautifulSoup(html, 'html.parser')
    h_tag = text.find("h1")
    if h_tag == None:
        h_tag = text.find("h2")
    return h_tag.get_text(separator=" ", strip=True) if isinstance(h_tag, Tag) else ""

def get_first_paragraph_from_html(html: str) -> str:
    text = BeautifulSoup(html, 'html.parser')
    main_tag = text.find("main")
    if main_tag != None:
        p_tag = main_tag.find("p")
        return p_tag.get_text(strip=True) if isinstance(p_tag, Tag) else ""
    else:
        p_tag = text.find("p")
        return p_tag.get_text(strip=True) if isinstance(p_tag, Tag) else ""
    
def get_urls_from_html(html, base_url):
    text = BeautifulSoup(html, 'html.parser')
    matches = text.find_all("a")
    listofURLs = []
    for match in matches:
        href = match.get("href")
        if href == None:
            continue
        absluteURL = urljoin(base_url, href)
        listofURLs.append(absluteURL)
    return listofURLs

def get_images_from_html(html, base_url):
    text = BeautifulSoup(html, 'html.parser')
    matches = text.find_all("img")
    listofURLs = []
    for match in matches:
        src = match.get("src")
        if src == None:
            continue
        absluteURL = urljoin(base_url, src)
        listofURLs.append(absluteURL)
    return listofURLs

def extract_page_data(html: str, page_url: str):
    u = normalize_url(page_url)
    h = get_heading_from_html(html)
    f = get_first_paragraph_from_html(html)
    l = get_urls_from_html(html, page_url)
    i = get_images_from_html(html, page_url)
    return PageData(url=u, heading=h, first_paragraph=f, outgoing_links=l, image_urls=i)




class AsyncCrawler:
    def __init__(self, base_url, max_concurrency=1, max_pages=5):
        self.base_url = base_url
        domain = urlsplit(base_url)
        self.base_domain = domain.netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()


    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if self.should_stop == True:
                return False
            
            if self.max_pages <= len(self.page_data):
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                for task in self.all_tasks:
                    task.cancel()
                return False

            if normalized_url in self.page_data:
                return False  # Already visited
            
            else:
                self.page_data[normalized_url] = None  # Mark as being processed
                return True  # First visit

    async def get_html(self, url):
        try:
            async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as r:
                if r.status >= 400:
                    raise Exception(f"HTTP Error: {r.status}")
                
                content_type = r.headers.get("content-type", "")
                if "text/html" not in content_type:
                    raise Exception(f"Expected text/html, got {content_type}")
                
                return await r.text()
        except Exception as e:
            raise Exception(f"Network error: {e}")

    async def crawl_page(self, current_url):
        if self.should_stop == True:
            return
        try:
            normalized_url = normalize_url(current_url)
            
            # Check if current_url is on the same domain as base_url
            current_urlobject = urlsplit(current_url)
            if current_urlobject.netloc != self.base_domain:
                return
            
            # Check if it's a new page
            if not await self.add_page_visit(normalized_url):
                return
            
            async with self.semaphore:
                print(f"Crawling: {current_url}")
                try:
                    html = await self.get_html(current_url)
                    pagedata = extract_page_data(html, current_url)
                    
                    async with self.lock:
                        self.page_data[normalized_url] = pagedata
                    
                    urls = get_urls_from_html(html, current_url)
                    
                    tasks = []
                    for url in urls:
                        task = asyncio.create_task(self.crawl_page(url))
                        self.all_tasks.add(task)
                    
                    await asyncio.gather(*tasks)
                except Exception as e:
                    print(f"Error crawling {current_url}: {e}")
        finally:
            # Remove this task from the set when it completes
            current_task = asyncio.current_task()
            if current_task in self.all_tasks:
                self.all_tasks.discard(current_task)

    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data


async def crawl_site_async(base_url, max_concurrency=1, max_pages=5):
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        page_data = await crawler.crawl()
        return page_data
from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup, Tag #type: ignore
from typing import TypedDict
import requests


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

def get_html(url):
    # Wrap in try/except to catch network-level errors (DNS failures, timeouts, etc.)
    try:
        r = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    except Exception as e:
        raise Exception(f"Network error: {e}")

    # Check for HTTP errors (400+)
    if r.status_code >= 400:
        raise Exception(f"HTTP Error: {r.status_code}")

    # Check content-type headers securely
    content_type = r.headers.get("content-type", "")
    if "text/html" not in content_type:
        raise Exception(f"Expected text/html, got {content_type}")

    # Return the string representation of the HTML
    return r.text

def crawl_page(base_url, current_url=None, page_data=None):
    current_urlobject = urlsplit(current_url)
    base_url_object = urlsplit(base_url)
    if current_urlobject.netloc != base_url_object.netloc:
        return
    normURL = normalize_url(current_url)
    if normURL in page_data:
        return
    html = get_html(normURL)
    print(html)
    pagedata = extract_page_data(html, normURL)
    URLs = get_urls_from_html(html, normURL)
    for url in URLs:
        crawl_page(base_url, url, page_data)
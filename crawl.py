from urllib.parse import urljoin, urlsplit
from bs4 import BeautifulSoup, Tag

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
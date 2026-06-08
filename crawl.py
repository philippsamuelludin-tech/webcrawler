from urllib.parse import urlsplit

def normalize_url(input_url):
    urlobject = urlsplit(input_url)
    url = f"{urlobject.netloc}{urlobject.path}"
    return url.lower().rstrip("/")
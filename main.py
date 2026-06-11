import sys
from crawl import get_html, crawl_page

if len(sys.argv) < 2:
    print("no website provided")
    sys.exit(1)
elif len(sys.argv) > 2:
    print("too many arguments provided")
    sys.exit(1)

BASE_URL = sys.argv[1]

print(f"starting crawl of: {BASE_URL}")
crawl_page(BASE_URL)

# print("Script name:", sys.argv[0]) # example.py
# print("Argument:", sys.argv[1])    # -v
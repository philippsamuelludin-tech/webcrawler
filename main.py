import sys
from crawl import get_html

if len(sys.argv) < 2:
    print("no website provided")
    sys.exit(1)
elif len(sys.argv) > 2:
    print("too many arguments provided")
    sys.exit(1)

BASE_URL = sys.argv[1]

print(f"starting crawl of: {BASE_URL}")
html = get_html(BASE_URL)
print(html)

# print("Script name:", sys.argv[0]) # example.py
# print("Argument:", sys.argv[1])    # -v
import sys
import asyncio
from crawl import crawl_site_async

async def main_async():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)

    BASE_URL = sys.argv[1]
    MAX_CONCURRENCY = int(sys.argv[2])
    MAX_PAGES = int(sys.argv[3])

    print(f"starting crawl of: {BASE_URL}")
    page_data = await crawl_site_async(BASE_URL, MAX_CONCURRENCY, MAX_PAGES)

    # Print statistics about collected data
    print(f"\n--- Crawl Complete ---")
    print(f"Total pages found: {len(page_data)}")
    print(f"\nPage Data:")
    for data in page_data.values():
        if data is not None:
            print(f"\nURL: {data['url']}")
            print(f"  Heading: {data['heading']}")
            print(f"  First Paragraph: {data['first_paragraph']}")
            print(f"  Outgoing Links: {len(data['outgoing_links'])}")
            print(f"  Images: {len(data['image_urls'])}")

if __name__ == "__main__":
    asyncio.run(main_async())
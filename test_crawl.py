import unittest
from crawl import get_images_from_html, normalize_url, get_heading_from_html, get_first_paragraph_from_html, get_urls_from_html

class TestCrawl(unittest.TestCase):

    ## TEST: NORMALIZE URL

    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url1(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url2(self):
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url3(self):
        input_url = "www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url4(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)


    ## TEST: GET HEADING FROM HTML

    def test_get_heading_from_html_basic(self):
        input_body = '<html><body><h1>Test Title</h1></body></html>'
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_basic1(self):
        input_body = '''<html><body>
        <h2>Test Title</h2>
        </body></html>'''
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_basic2(self):
        input_body = '''<html>
        <head>
        <title>My First HTML Page</title>
        </head>
        <body>
        <h1>Welcome to HTML</h1>
        <p>This is my first paragraph in HTML.</p>
        <a href="https://www.example.com" target="_blank">Visit Example</a>
        </body>
        </html>'''
        actual = get_heading_from_html(input_body)
        expected = "Welcome to HTML"
        self.assertEqual(actual, expected)

    def test_get_heading_no_tags(self):
        input_body = '<html><body><p>Just a paragraph, no headings here!</p></body></html>'
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_heading_nested_tags(self):
        input_body = '<html><body><h1>Welcome to <span>Boot.dev</span>!</h1></body></html>'
        actual = get_heading_from_html(input_body)
        expected = "Welcome to Boot.dev !"
        self.assertEqual(actual, expected)

    ## TEST GET FIRST PARAGRAPH FROM HTML MAIN PRIORITY

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)


    def test_get_first_paragraph_from_html_main_priority1(self):
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Outside paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority2(self):
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph1.</p>
            </main>
            <main>
                <p>Main paragraph2.</p>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph1."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_empty_tag(self):
        input_body = '<html><body><p>   </p></body></html>'
        # Since we use strip=True, this should result in an empty string
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    ## TEST GET URLS FROM HTML

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/about">About</a><a href="/contact">Contact</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/about", "https://crawler-test.com/contact"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_mixed_and_missing(self):
        input_url = "https://example.com"
        input_body = '<html><body><a href="https://external.com">External</a><a>No href</a><a href="/page">Page</a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://external.com", "https://example.com/page"]
        self.assertEqual(actual, expected)

    ## TEST GET IMAGES FROM HTML
    
    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_multiple(self):
        input_url = "https://example.com"
        input_body = '<html><body><img src="/img1.png"><img src="https://cdn.com/img2.jpg"><img src="images/img3.gif"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://example.com/img1.png", "https://cdn.com/img2.jpg", "https://example.com/images/img3.gif"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_missing_src(self):
        input_url = "https://example.com"
        input_body = '<html><body><img alt="No src"><img src="/valid.png"><img src=""></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://example.com/valid.png", "https://example.com"]
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
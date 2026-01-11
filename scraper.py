import requests
from html.parser import HTMLParser

class SimpleScraper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_heading = False
        self.in_paragraph = False
        self.in_title = False
        
        self.data = {
            "title": "",
            "headings": [],
            "paragraphs": [],
            "links": []
        }

    def handle_starttag(self, tag, attrs):
        if tag in ["h1","h2","h3","h4","h5","h6"]:
            self.in_heading = True
        
        if tag == "p":
            self.in_paragraph = True
        
        if tag == "title":
            self.in_title = True
        
        if tag == "a":
            for attr, val in attrs:
                if attr == "href":
                    self.data["links"].append(val)

    def handle_endtag(self, tag):
        if tag in ["h1","h2","h3","h4","h5","h6"]:
            self.in_heading = False
        
        if tag == "p":
            self.in_paragraph = False
        
        if tag == "title":
            self.in_title = False

    def handle_data(self, text):
        text = text.strip()
        if not text:
            return

        if self.in_title:
            self.data["title"] += text

        if self.in_heading:
            self.data["headings"].append(text)

        if self.in_paragraph:
            self.data["paragraphs"].append(text)


def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        parser = SimpleScraper()
        parser.feed(response.text)
        return parser.data

    except Exception as e:
        return {"error": str(e)}

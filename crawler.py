
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from pymongo import MongoClient


class WebCrawler:
    def __init__(self, start_url, target_h1, db_name, collection_name):
        self.frontier = [start_url]
        self.visited = set()
        self.target_h1 = target_h1
        self.mongo_client = MongoClient("mongodb://localhost:27017/")
        self.db = self.mongo_client[db_name]
        self.collection = self.db[collection_name]

    def retrieve_html(self, url):
        try:
            response = urllib.request.urlopen(url)
            if response.headers.get_content_type() in ["text/html"]:
                return response.read()
        except Exception as e:
            print(f"Failed to retrieve {url}: {e}")
        return None

    def parse_links(self, html, base_url):
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        for anchor in soup.find_all('a', href=True):
            link = urllib.parse.urljoin(base_url, anchor['href'])
            if link.endswith(('.html', '.shtml')) and link not in self.visited:
                links.add(link)
        return links

    def is_target_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        h1 = soup.find('h1', class_="cpp-h1")
        return h1 and self.target_h1 in h1.text

    def store_page(self, url, html):
        self.collection.insert_one({"url": url, "html": html.decode('utf-8')})

    def clear_frontier(self):
        self.frontier = []

    def run(self):
        while self.frontier:
            url = self.frontier.pop(0)
            if url in self.visited:
                continue

            print(f"Visiting: {url}")
            html = self.retrieve_html(url)
            if not html:
                continue

            self.store_page(url, html)
            if self.is_target_page(html):
                print(f"Target page found: {url}")
                self.clear_frontier()
                return

            self.visited.add(url)
            links = self.parse_links(html, urllib.parse.urlparse(url).scheme + "://" + urllib.parse.urlparse(url).netloc)
            self.frontier.extend(links)


if __name__ == "__main__":
    START_URL = "https://www.cpp.edu/sci/computer-science/"
    TARGET_H1 = "Permanent Faculty"
    DB_NAME = "webcrawler"
    COLLECTION_NAME = "pages"

    crawler = WebCrawler(START_URL, TARGET_H1, DB_NAME, COLLECTION_NAME)
    crawler.run()

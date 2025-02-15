import scrapy
# from linkdn.items import Product
from lxml import html

class LinkdnSpider(scrapy.Spider):
    name = "linkdn"
    start_urls = ["https://example.com"]

    def parse(self, response):
        parser = html.fromstring(response.text)
        print("Visited:", response.url)

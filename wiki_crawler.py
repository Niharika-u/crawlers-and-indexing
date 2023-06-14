import scrapy
from scrapy.crawler import CrawlerRunner
from crochet import setup, wait_for
import os
import re


setup()


class Crawl_Wiki(scrapy.Spider):
    name = "cork_wiki"
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Cork_(city)']
    visited_urls = set()

    def parse(self, response):
        # Check if URL has already been visited
        if response.url in self.visited_urls:
            return

        # Add URL to visited set
        self.visited_urls.add(response.url)

        try:
            # create a new file inside the folder
            folder_path = "files"
            title = response.xpath("/html/head/title/text()").get()
            print(title)
            filename = re.sub(r'\W+', '_', title) + '.txt'
            file_path = os.path.join(folder_path, filename)
            # Extract the paragraphs from the page
            paragraphs = response.xpath("//p//text()").getall()

            # Write the paragraphs to a text file
            with open(file_path, 'w', encoding='utf-8') as file:
                for paragraph in paragraphs:
                    file.write(paragraph.strip() + '\n')
            # Extract all internal links from the page
            internal_links = response.xpath("//a/@href").getall()

            # Follow each internal link and recursively parse the linked page
            for link in internal_links:
                if link.startswith('/wiki/'):
                    linked_page = response.urljoin(link)
                    yield scrapy.Request(linked_page, callback=self.parse)

        except Exception as e:
            print(self.logger.error('Error parsing %s', e))


@wait_for(50)
def run_spider():
    crawler = CrawlerRunner()
    d = crawler.crawl(Crawl_Wiki)
    return d


run_spider()




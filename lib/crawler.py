import scrapy
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
import bs4
import re
import json
import os


class RithmLectureSpider(scrapy.Spider):
    """ To run this spider in command line interface:

    >>> rm data.json
    >>> scrapy runspider spider.py -o data.json
    """
    
    name = 'rithm_lecture_spider'

    def __init__(self, cohort='r11'):
        self.start_urls = [f'http://curric.rithmschool.com/{cohort}/lectures/']

    def parse(self, response):
        """Yields an object that parses all scraped information for each lecture note page"""
        for link in response.css('a'):
            href = link.attrib.get('href')
            is_valid_notes_page = href is not None and href != '../' and not href.endswith('.zip')
            if is_valid_notes_page: 
                next_page = response.urljoin(href)
                yield scrapy.Request(next_page, callback=self.create_document)

    def create_document(self, response):
        """Creates a document object for each page"""
        title = response.xpath('//head/title/text()').extract_first()
        page_content = response.css('div #page-content')

        document = self.bs_parse(page_content.extract_first())

        return { 
            "url": response.url,
            "title": title, 
            **document
        }

    def bs_parse(self, raw_html):
        """Grabs all raw detail from a certain page by parsing through BeautifulSoup """
        soup = bs4.BeautifulSoup(raw_html, features='lxml')

        clean = RithmLectureSpider.clean # Just an alias for shorthand

        # Separate html into categories so ElasticSearch can handle each field differently

        # grabs <h1> ... <h6> tags
        headers = [hd.text.strip()
                   for hd in soup.find_all(re.compile('^h[1-6]$'))]

        bullets = [clean(li) for li in soup.find_all('li')]

        p = [clean(p) for p in soup.find_all('p')]

        code_snippets = [clean(pre) for pre in soup.find_all('pre')]

        return {
            "headers": headers,
            "bullets": bullets,
            "text": p,
            "code": code_snippets,
        }

    @staticmethod
    def clean(raw_pre):
        """Cleans raw pre text by stripping new line characters with spaces. """
        return re.sub(r'\n', r' ', raw_pre.get_text(), flags=re.M)

def scrape_cohort_lectures(cohort):
    """Synchronous (blocking) scraping of all lectures. Returns json array of parsed documents """

    # TODO: Add download delays in case of overload 
    temp_file = 'temp.json' 

    process = CrawlerRunner(
        settings={
            'FEED_FORMAT': 'json',
            'FEED_URI': temp_file,
        }
    )

    runner = process.crawl(RithmLectureSpider, cohort=cohort)
    
    # Manual stop callback
    manual_stop_cb = lambda _: reactor.stop()
    runner.addBoth(manual_stop_cb) 
    reactor.run() # This will block the script until it completes

    with open(temp_file) as f:
        data = json.load(f)

    os.remove(temp_file)

    return data

if __name__ == "__main__":
    results = scrape_cohort_lectures(cohort='r12')
    print(results)

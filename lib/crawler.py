import scrapy
from scrapy.crawler import CrawlerRunner
import bs4
import re
import json
import os
import crochet
crochet.setup()


class RithmLectureSpider(scrapy.Spider):
    """ To run this spider in command line interface:
    >>> rm data.json
    >>> scrapy runspider spider.py -o data.json
    """

    name = 'rithm_lecture_spider'

    def __init__(self, cohort='r11'):
        self.start_urls = [f'http://curric.rithmschool.com/{cohort}/lectures/']

    def parse(self, response):
        """Yields an object that parses all scraped information
        for each lecture note page
        :param response: Scrapy response
        :yield: Document object from each URL
        """
        for link in response.css('a'):
            href = link.attrib.get('href')

            is_valid_notes_page = (
                href is not None and href != '../'
                and not href.endswith('.zip')
            )

            if is_valid_notes_page:
                next_page = response.urljoin(href)
                yield scrapy.Request(next_page, callback=self.create_document)

    def create_document(self, response):
        """Creates a document object for each page
        :param response: Scrapy response
        :yield: Document object for the page
        """
        title = response.xpath('//head/title/text()').extract_first()
        page_content = response.css('div #page-content')

        document = self.bs_parse(page_content.extract_first())

        return {
            "url": response.url,
            "title": title,
            **document
        }

    def bs_parse(self, raw_html: str):
        """Grabs all raw detail from a certain page
        by parsing through BeautifulSoup
        :param raw_html: Html as a string
        """
        soup = bs4.BeautifulSoup(raw_html, features='lxml')

        clean = RithmLectureSpider.clean  # Just an alias for shorthand

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
        """Cleans raw pre text by stripping new line characters w/ spaces.
        :param raw_pre: Raw html pre as a string
        """
        return re.sub(r'\n', r' ', raw_pre.get_text(), flags=re.M)


def scrape_cohort_lectures(cohort):
    """Synchronous (blocking) scraping of all lectures.
    Returns json array of parsed documents
    :param cohort: Cohort 'r11', 'r12', 'r13'
    """

    temp_file = 'temp.json'
    _scrape_to_temp(cohort, temp_file)
    with open(temp_file) as f:
        data = json.load(f)

    os.remove(temp_file)

    return data


@crochet.wait_for(timeout=40)
def _scrape_to_temp(cohort, temp_file: str):
    """Crawls with scrapy asynchronously'
    Blocks until timeout or result is returned from the `Twisted` thread.
    :param cohort: Cohort to scrape
    :param temp_file: Name of a tempory file to store
    :return: A `Deferred` with extracted results.
    """

    # Manual removal b/c Scrapy does not overwrite
    try:
        os.remove(temp_file)
    except FileNotFoundError:
        pass

    runner = CrawlerRunner(
        settings={
            'FEED_FORMAT': 'json',
            'FEED_URI': temp_file,
        }
    )

    thread = runner.crawl(RithmLectureSpider, cohort=cohort)
    # TODO: Replace this callback with a logger to update with date
    thread.addCallback(lambda _: print('Done'))
    return thread


if __name__ == "__main__":
    results = scrape_cohort_lectures(cohort='r12')
    print(results)

from time import sleep
from typing import List, Set
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from requests.api import get

from grawt.scraper.base_scraper import BaseScraper
from grawt.scraper.general_scraper import GeneralScraper
from grawt.models import ScrapedArticle

URL_RETRY_DELAY: float = 0.25
MAX_RETRIES: int = 5


class MaxRetriesReached(Exception):
    pass


class Crawler():

    def __init__(self) -> None:
        self._general_scraper = GeneralScraper()
        self._scrapers: List[BaseScraper] = [
            # To be filled
        ]

    def _load_url(self, url: str, retry: int = 0) -> str:
        if retry > MAX_RETRIES:
            raise MaxRetriesReached('Reached maximum amount of retries.')

        try:
            return requests.get(url).text
        except Exception as e:
            print(str(e))
            retry += 1
            sleep(URL_RETRY_DELAY)
            return self._load_url(url, retry)

    def _choose_scraper(self, netloc: str) -> BaseScraper:
        for scraper in self._scrapers:
            if type(scraper).__name__.lower()[:-7] in netloc.lower():
                return scraper
        return self._general_scraper

    def _single_scrape(self, url: str) -> ScrapedArticle:
        raw_html: str = self._load_url(url)
        netloc: str = urlparse(url).netloc
        soup: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
        scraper: BaseScraper = self._choose_scraper(netloc)
        scraped_article: ScrapedArticle = scraper.scrape_article(soup)
        scraped_article.url = url
        return scraped_article

    def _recursive_crawl_site(
        self, 
        url: str, 
        netloc_source: str,
        max_depth: int = 2, 
        depth: int = 0, 
        scraped_articles: Set[ScrapedArticle] = set()
    ) -> ScrapedArticle:
        if depth > max_depth:
            return

        article: ScrapedArticle
        try:
            article: ScrapedArticle = self._single_scrape(url)
        except:
            return

        scraped_articles.add(article)
        depth += 1
        link: str
        for link in article.netloc_links:
            if netloc_source not in link:
                continue
            self._recursive_crawl_site(link, netloc_source=netloc_source, max_depth=max_depth, depth=depth, scraped_articles=scraped_articles)
        return scraped_articles

    def crawl_site(
        self, 
        url: str, 
        max_depth: int = 2, 
        depth: int = 0, 
        scraped_articles: Set[ScrapedArticle] = set()
    ) -> Set[ScrapedArticle]:
        netloc_source: str = urlparse(url).netloc
        scraped_articles: Set[ScrapedArticle] = self._recursive_crawl_site(url, netloc_source=netloc_source, max_depth=max_depth, depth=depth, scraped_articles=scraped_articles)
        return scraped_articles
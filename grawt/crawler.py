from hashlib import sha3_256
import os
from time import sleep
from typing import List, Set
from urllib.parse import urlparse
import json

import requests
from bs4 import BeautifulSoup

from grawt.models import ScrapedArticle
from grawt.scraper.base_scraper import BaseScraper
from grawt.scraper.general_scraper import GeneralScraper

#TODO create config
URL_RETRY_DELAY: float = 0.25
MAX_RETRIES: int = 5
URLS_FILE_PATH: str = './urls.json'


class MaxRetriesReached(Exception):
    pass


class Crawler():

    def __init__(self) -> None:
        self._general_scraper = GeneralScraper()
        self._scrapers: List[BaseScraper] = [
            # To be filled
        ]
        self._urls_file: str = URLS_FILE_PATH
        self._check_urls_file()
        self._urls: List[str] = self._load_urls_file()

    def _check_urls_file(self) -> None:
        """ Check if urls file exists and create one in case it is not.
        """
        if not os.path.exists(self._urls_file):
            with open(self._urls_file, 'w') as file:
                json.dump([], file)

    def _load_urls_file(self) -> List[str]:
        """ Load urls file using json.

        Returns:
            List[str]: List with hashed URLs.
        """
        with open(self._urls_file, 'r') as file:
            return json.load(file)

    def _write_urls_file(self) -> None:
        """Write urls to json file
        """
        with open(self._urls_file, 'w') as file:
            json.dump(self._urls, file)


    def _load_url(self, url: str, retry: int = 0) -> str:
        """Download the raw html text from an url.

        Args:
            url (str): URL to the source.
            retry (int, optional): Recursive retry state variable. Defaults to 0.

        Raises:
            MaxRetriesReached: Raised when the maximum amount of retries is reached.

        Returns:
            str: The raw html in form of a string.
        """
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
        """Based on the domain name choose a custom scraper or use the GeneralScraper.

        Args:
            netloc (str): Domain name.

        Returns:
            BaseScraper: Scraper that is used for the website.
        """
        for scraper in self._scrapers:
            if type(scraper).__name__.lower()[:-7] in netloc.lower():
                return scraper
        return self._general_scraper

    def _single_scrape(self, url: str) -> ScrapedArticle:
        """Load the url, choose the scraper and scrape the URL.

        Args:
            url (str): URL to scrape.

        Returns:
            ScrapedArticle: Scraped article.
        """
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
    ) -> Set[ScrapedArticle]:
        """Scrape the website and the sub urls.

        The scraper only takes URLs into account that have the
        same domain name.

        Args:
            url (str): Starting URL.
            netloc_source (str): Domain of the starting URL.
            max_depth (int, optional): Maximum recursive depth. Defaults to 2.
            depth (int, optional): Recursive depth state variable. Defaults to 0.
            scraped_articles (Set[ScrapedArticle], optional): Recursive state variable for the scraped articles. Defaults to set().

        Returns:
            Set[ScrapedArticle]: Set of scraped articles.
        """
        if depth > max_depth:
            return

        article: ScrapedArticle
        try:
            article: ScrapedArticle = self._single_scrape(url)
            if url in self._urls:
                print('Found an already scraped article: {}'.format(url))
            else:
                self._urls.append(url)
                scraped_articles.add(article)
                print('Scraped {}'.format(url))
        except Exception as e:
            print(str(e))
            return

        depth += 1
        link: str
        for link in article.netloc_links:
            if netloc_source not in link:
                continue
            self._recursive_crawl_site(
                link, 
                netloc_source=netloc_source, 
                max_depth=max_depth, 
                depth=depth, 
                scraped_articles=scraped_articles
            )
        return scraped_articles

    def crawl_site(
        self, 
        url: str, 
        max_depth: int = 2, 
        depth: int = 0, 
        scraped_articles: Set[ScrapedArticle] = set()
    ) -> Set[ScrapedArticle]:
        """Calls the recursive scraping function.

        Args:
            url (str): Starting URL.
            max_depth (int, optional): Maximum recursive depth. Defaults to 2. Defaults to 2.
            depth (int, optional): Recursive depth state variable. Defaults to 0.
            scraped_articles (Set[ScrapedArticle], optional): Recursive state variable for the scraped articles. Defaults to set().

        Returns:
            Set[ScrapedArticle]: Set of scraped articles.
        """
        netloc_source: str = urlparse(url).netloc
        scraped_articles: Set[ScrapedArticle] = self._recursive_crawl_site(
            url, 
            netloc_source=netloc_source, 
            max_depth=max_depth, 
            depth=depth, 
            scraped_articles=scraped_articles
        )
        self._write_urls_file()
        if scraped_articles is None:
            return []
        else:
            return scraped_articles

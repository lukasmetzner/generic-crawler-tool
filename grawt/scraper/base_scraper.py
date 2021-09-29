from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup
from grawt.models import ScrapedArticle


class BaseScraper(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def extract_headline(self, soup: BeautifulSoup) -> str:
        """Implement a method that extracts the headline.

        Args:
            soup (BeautifulSoup): Websites soup.

        Returns:
            str: Headline string.
        """
        pass

    @abstractmethod
    def extract_main_text(self, soup: BeautifulSoup, min_chars: int = 100) -> str:
        """Implement a method that extracts the main text.

        Args:
            soup (BeautifulSoup): Websites soup.
            min_chars (int): Minimum characters for a text or paragraph to be considered. Default to 100.

        Returns:
            str: Aggregated main text.
        """
        pass

    @abstractmethod
    def extract_date(self, soup: BeautifulSoup) -> datetime:
        """Implement a method that extracts for example the publish date.

        Args:
            soup (BeautifulSoup): Websites soup.

        Returns:
            datetime: Required date.
        """
        pass

    @abstractmethod
    def extract_all_hrefs(self, soup: BeautifulSoup) -> List[str]:
        """Implement a method that extracts all uris from the website.

        Args:
            soup (BeautifulSoup): Websites soup.

        Returns:
            List[str]: List of uris.
        """
        pass

    @abstractmethod
    def extract_netloc_links(self, soup: BeautifulSoup) -> List[str]:
        """Implement a method that extracts all links from the website.

        Supposed to be a link that points to another netloc.

        Args:
            soup (BeautifulSoup): Websites soup.

        Returns:
            List[str]: List of links.
        """
        pass

    def scrape_article(self, soup: BeautifulSoup, main_text_min_length: int) -> ScrapedArticle:
        """Scrape an article from a websites soup.

        Args:
            soup (BeautifulSoup): Websites soup.

        Returns:
            ScrapedArticle: Scraped article.
        """
        sa = ScrapedArticle()
        sa.headline = self.extract_headline(soup)
        sa.main_text = self.extract_main_text(soup, main_text_min_length)
        sa.datetime_ = self.extract_date(soup)
        sa.hrefs = self.extract_all_hrefs(soup)
        sa.netloc_links = self.extract_netloc_links(soup)
        return sa

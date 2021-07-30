from datetime import date, datetime
from typing import Any, List
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from dateutil import parser
from grawt.scraper.base_scraper import BaseScraper


class GeneralScraper(BaseScraper):

    def __init__(self) -> None:
        super().__init__()
        self._min_length: int = 150

    def extract_headline(self, soup: BeautifulSoup) -> str:
        """Extract the headline of the website.

        Iterate overall possible headlines h1 to h6 and take the first
        headline that is found. If there is no headline found take the 
        html title.

        Args:
            soup (BeautifulSoup): Websites soup.

        Returns:
            str: Headline string
        """
        headlines: List[Any] = []
        for i in range(1, 7):
            curr_hl: List[Any] = soup.find_all(f'h{i}')
            headlines.extend(curr_hl)
        if len(headlines) > 0:
            return headlines[0].get_text()
        else:
            return soup.find('title').get_text()

    def extract_main_text(self, soup: BeautifulSoup, min_chars: int) -> str:
        """Extract the main text of the website.

        Iterates over all paragraphs of a website and takes all into
        consideration that have at least the min_chars length.

        Args:
            soup (BeautifulSoup): Websites soup.
            min_chars (int): Min length for a paragraph.

        Returns:
            str: Main text of the website.
        """
        full_text: str = ''
        for p in soup.find_all('p'):
            text: str = p.get_text()
            if len(text) >= min_chars:
                full_text += text + '\n'
        return full_text

    def extract_date(self, soup: BeautifulSoup) -> datetime:
        """Extract the publish date of a website.

        Looks up every html time object and takes the oldest value.

        Args:
            soup (BeautifulSoup): Websites soup.

        Returns:
            datetime: Latest html time object.
        """
        datetimes: List[datetime] = []
        for time in soup.find_all('time'):
            date_str = time.get('datetime')
            dt: datetime 
            try:
                datetimes.append(parser.parse(date_str))
            except parser.ParserError as pe:
                print(pe)
        if len(datetimes) > 0:
            return min(datetimes)
        else:
            return datetime.now()

    def extract_all_hrefs(self, soup: BeautifulSoup) -> List[str]:
        """Extract all hrefs found on a website.

        Args:
            soup (BeautifulSoup): Websites soup.

        Returns:
            List[str]: List with hrefs.
        """
        links: List[str] = []
        for a in soup.find_all('a'):
            link = a.get('href', None)
            if link is not None:
                links.append(link)
        return links

    def extract_netloc_links(self, soup: BeautifulSoup) -> List[str]:
        """Tries to find all links other websites.

        Take all urls that have a netloc value from the urllib.parse.urlparse().

        Args:
            soup (BeautifulSoup): Websites soup.

        Returns:
            List[str]: List of links.
        """
        netloc_urls: List[str] = []
        for url in self.extract_all_hrefs(soup):
            parsed = urlparse(url)
            if parsed.netloc:
                netloc_urls.append(url)
        return netloc_urls

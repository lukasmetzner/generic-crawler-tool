from datetime import datetime
from typing import Any, List
from urllib.parse import urlparse

import bs4
import requests
from bs4 import BeautifulSoup
from dateutil import parser

url = 'https://www.msn.com/de-de/nachrichten/politik/wahlkampf-ich-will-ja-auch-kanzler-werden-und-nicht-zirkusdirektor/ar-AAMFO5N?li=BBqg6Q9'
url2 = 'https://www.dailymail.co.uk/news/article-9840903/The-Given-FINALLY-arrives-Rotterdam-unload-cargo-megaship-blocked-Suez-Canal.html'
url3 = 'https://stackoverflow.com/questions/22214492/python-beautifulsoup-cannot-find-the-data-in-the-page-source'
resp = requests.get(url2)
soup = BeautifulSoup(resp.text, 'html.parser')

def extract_headline(soup: BeautifulSoup) -> str:
    headlines: List[Any] = []
    for i in range(1, 7):
        curr_hl: List[Any] = soup.find_all(f'h{i}')
        headlines.extend(curr_hl)
    if len(headlines) > 0:
        return headlines[0].get_text()
    else:
        return soup.find('title').get_text()

def extract_text(soup: BeautifulSoup, min_chars: int) -> str:
    full_text: str = ''
    for p in soup.find_all('p'):
        text: str = p.get_text()
        if len(text) > min_chars:
            full_text += text + '\n'
    return full_text

def extract_date(soup: BeautifulSoup) -> datetime:
    datetimes: List[datetime] = []
    for time in soup.find_all('time'):
        date_str = time.get('datetime')
        dt: datetime = parser.parse(date_str)
        datetimes.append(dt)
    return min(datetimes)

def extract_all_urls(soup: BeautifulSoup) -> List[str]:
    links: List[str] = []
    for a in soup.find_all('a'):
        link = a.get('href', None)
        if link is not None:
            links.append(link)
    return links

def extract_netloc_urls(soup: BeautifulSoup) -> List[str]:
    netloc_urls: List[str] = []
    for url in extract_all_urls(soup):
        parsed = urlparse(url)
        if parsed.netloc:
            netloc_urls.append(url)

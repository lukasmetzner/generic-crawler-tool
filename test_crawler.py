from typing import List
from grawt.crawler import Crawler
from grawt.models import ScrapedArticle

url: str = 'https://www.dailymail.co.uk/home/index.html'
crawler = Crawler()
scraped_articles: List[ScrapedArticle] = crawler.crawl_site(url, max_depth=1)
article: ScrapedArticle
for article in scraped_articles:
    print(article.headline)

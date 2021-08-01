# GRAWT - Generic Crawler Tool
Easy to use recursive crawler and scraper for non Javascript heavy websites. Uses a 'urls.json' file to keep track of already scraped urls. This prevents duplicates even after restarting the crawler. This could be useful if you want to crawl news articles on a daily basis.
## Usage
``` bash
pip3 install requirements.txt
```

``` Python
from typing import List
from grawt.crawler import Crawler
from grawt.models import ScrapedArticle

url: str = 'https://www.dailymail.co.uk/home/index.html'
crawler = Crawler()
scraped_articles: List[ScrapedArticle] = crawler.crawl_site(url, max_depth=1)
article: ScrapedArticle
for article in scraped_articles:
    print(article.headline)
```
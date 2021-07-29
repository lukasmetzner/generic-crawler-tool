from datetime import datetime
from typing import List


class ScrapedArticle():
    headline: str
    main_text: str
    datetime_: datetime
    hrefs: List[str]
    netloc_links: List[str]

    def to_dict(self) -> dict:
        self.__dict__

    @staticmethod
    def from_dict(doc: dict):
        sa = ScrapedArticle()
        sa.headline = doc['headline']
        sa.main_text = doc['maintext']
        sa.datetime_ = doc['datetime_']
        sa.hrefs = doc['hrefs']
        sa.netloc_links = doc['netloc_links']
        return sa
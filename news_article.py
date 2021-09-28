import datetime 
from dataclasses import dataclass

@dataclass
class NewsArticle:
    url: str = ''
    title: str = ''
    content: str = ''
    source: str = ''
    published: datetime.datetime = datetime.datetime.now()
    jobid: str = ''

import datetime 
from dataclasses import dataclass

@dataclass
class NewsArticle:
    url: str = ''
    title: str = ''
    content: str = ''
    description: str = ''
    source: str = ''
    published: datetime.datetime = datetime.datetime.now()
    jobid: str = ''
    score: str = ''
    label: str = ''

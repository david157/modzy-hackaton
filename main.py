import requests
from news_article import NewsArticle

API_KEY = ''
KEYWORD = 'Apple'

url = ('https://newsapi.org/v2/everything?'
       'q=%s&'
       'from=2021-09-28&'
       'sortBy=popularity&'
       'apiKey=%s' % (KEYWORD, API_KEY))

response = requests.get(url)

articles = response.json()
news = []


for article in articles['articles']:
  n = NewsArticle()
  n.content = article['content']
  n.source = article['source']['name']
  n.title =  article['title']
  n.url = article['url']
  # n.published = None

  # optional - run summarization here
  # run sentiment analysis here
  n.sentiment = 'positive'
  print(n)
  news.append(n)

print(news)
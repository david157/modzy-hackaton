import requests
from flask import request, Flask
from news_article import NewsArticle
import dataclasses, json
from datetime import date, datetime

API_KEY = ''

app = Flask(__name__)

@app.route('/getnews', methods=['GET'])
def getNews():
  keyword = request.args.get("q")
  url = ('https://newsapi.org/v2/everything?'
        'q=%s&'
        'from=2021-09-28&'
        'sortBy=popularity&'
        'apiKey=%s' % (keyword, API_KEY))

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
    n.jobid = 'placeholder'
    # print(n)
    news.append(n)

  # print(news)

  response = app.response_class(
        response=json.dumps(news, cls=EnhancedJSONEncoder),
        status=200,
        mimetype='application/json'
    )

  return response


class EnhancedJSONEncoder(json.JSONEncoder):
      def default(self, o):
          if dataclasses.is_dataclass(o):
              return dataclasses.asdict(o)
          elif isinstance(o, (datetime, date)):
            return o.isoformat()
          return super().default(o)
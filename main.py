import requests
from flask import request, Flask
from news_article import NewsArticle
import dataclasses, json
from datetime import date, datetime
import dateutil.parser
from modzy import ApiClient, error

API_KEY = ''

app = Flask(__name__)
modzyclient = ApiClient(base_url='https://app.modzy.com/api', api_key='')

@app.route('/getnews', methods=['GET'])
def getNews():

  news_sources = [ 'bbc-news', 'breitbart-news', 'cnn', 'fox-news', 'msnbc'] 

  keyword = request.args.get("q")

  # url = ('https://newsapi.org/v2/everything?'
  #       'q=%s&'
  #       'from=2021-09-25&'
  #       'sortBy=popularity&'
  #       'apiKey=%s' % (keyword, API_KEY))
  # response = requests.get(url)
  # articles = response.json()

  articles = {}
  articles['articles'] = []
  for s in news_sources:
    url = ('https://newsapi.org/v2/everything?'
        'q=%s&'
        'sources=%s&'
        'apiKey=%s' % (keyword, s, API_KEY))
    response = requests.get(url)
    [ articles['articles'].append(x) for x in response.json()['articles'] ]
    # articles['articles'].append(response.json()['articles'])
    

  news = []

  sources = {}
  i = 0
  for article in articles['articles']:
    n = NewsArticle()
    n.content = article['content']
    n.description = article['description']
    n.source = article['source']['name']
    n.title =  article['title']
    n.url = article['url']
    n.published = dateutil.parser.parse(article['publishedAt'])

    # optional - run summarization here
    # run sentiment analysis here
    #n.jobid = 'placeholder'
    # print(n)
    news.append(n)
    sources[str(i)] = {"input.txt": n.title}
    i += 1

  job = modzyclient.jobs.submit_text('ed542963de', '1.0.1', sources)
  result = modzyclient.results.block_until_complete(job, timeout=600)

  for j in range(i):
    outputs = result.get_source_outputs(source_name=str(j))
    classpredict = outputs['results.json']['data']['result']['classPredictions']
    maxscore = classpredict[0]
    for l in range(3):
      if classpredict[l]['score'] > maxscore['score']:
        maxscore = classpredict[l]
    print(maxscore)
    news[j].score = maxscore['score']
    news[j].label = maxscore['class']


  # outputs = result.get_source_outputs(source_name="*")
  # print(outputs)
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
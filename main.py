import requests

API_KEY = ''
KEYWORD = 'Apple'

url = ('https://newsapi.org/v2/everything?'
       'q=%s&'
       'from=2021-09-28&'
       'sortBy=popularity&'
       'apiKey=%s' % (KEYWORD, API_KEY))

response = requests.get(url)

print(response.json())
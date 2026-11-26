import requests
import os
from dotenv import load_dotenv
from datetime import date, timedelta

load_dotenv()

print()

API_KEY = os.getenv("NEWS_API_KEY")

SEARCH_KEYWORD = "Trump"
YESTERDAY = date.today() - timedelta(days=1)
URL = "https://newsapi.org/v2/everything"

params = {
    "q" : SEARCH_KEYWORD,
    "apiKey" : API_KEY,
    "pageSize" : 10,
    "from" : YESTERDAY,
    "language" : "en",
    "sortBy" : "relevancy, popularity, publishedAt",
    "searchIn" : "title,description"
}

response = requests.get(URL, params=params, timeout=10)

if response.status_code == 200:

    data = response.json()

    print(F"\n----LAST 24 HRS NEWS ON {SEARCH_KEYWORD}----\n")

    for news in data['articles']:
        print(f"Headline    : {news['title']}")
        print(f"Description : {news['description']}")
        print(f"Source      : {news['url']}")
        print(f"Published   : {news['publishedAt'].split('T')[0]} @ {news['publishedAt'].split('T')[1].split('Z')[0]}")
        print(f"Author      : {news['author']}")
        print()
        
elif response.status_code == 401:
    print("API key is invalid or not yet active. Check your .env file.")

elif response.status_code == 404:
    print(f"Not found. Check the endpoint url or search term.")

elif response.status_code == 429:
    print("Too many requests. Wait before trying again.")

else:
    print(f"Unexpected error: {response.status_code}")
    print(response.text)
print(len(data['articles']))


print()

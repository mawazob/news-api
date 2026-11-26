import os
from datetime import datetime, timedelta, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
if not API_KEY:
    raise SystemExit("NEWS_API_KEY not found. Check your .env file.")

SEARCH_KEYWORD = "Trump"
HOURS_BACK = 72 
URL = "https://newsapi.org/v2/everything"

# Start of the time window, in UTC (the API works in UTC)
since = datetime.now(timezone.utc) - timedelta(hours=HOURS_BACK)

params = {
    "q": SEARCH_KEYWORD,
    "apiKey": API_KEY,
    "pageSize": 10,
    "from": since.strftime("%Y-%m-%dT%H:%M:%S"),
    "language": "en",
    "sortBy": "publishedAt",
    "searchIn": "title,description",
}

ERROR_MESSAGES = {
    400: "Bad request. Check your parameters.",
    401: "API key is invalid or not yet active. Check your .env file.",
    404: "Not found. Check the endpoint URL or search term.",
    429: "Too many requests. Wait before trying again.",
}

try:
    response = requests.get(URL, params=params, timeout=10)
except requests.exceptions.RequestException as e:
    raise SystemExit(f"Could not reach NewsAPI: {e}")

if response.status_code != 200:
    print(ERROR_MESSAGES.get(response.status_code, f"Unexpected error: {response.status_code}"))
    print(response.text)  # NewsAPI explains the problem in the body
    raise SystemExit(1)

data = response.json()
articles = data["articles"]

if not articles:
    raise SystemExit(f"No articles found for '{SEARCH_KEYWORD}' in the last {HOURS_BACK} hours.")

print(f"\n----LAST {HOURS_BACK} HRS NEWS ON {SEARCH_KEYWORD}----\n")

for article in articles:
    published = datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00"))
    published_local = published.astimezone()

    print(f"Headline    : {article['title']}")
    print(f"Description : {article['description'] or 'N/A'}")
    print(f"Source      : {article['source']['name']} - {article['url']}")
    print(f"Published   : {published_local:%Y-%m-%d @ %H:%M}")
    print(f"Author      : {article['author'] or 'N/A'}")
    print()

print(f"Showing {len(articles)} articles")
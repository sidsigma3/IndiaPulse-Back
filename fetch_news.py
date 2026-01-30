import requests
import uuid
import datetime
import json
import time

from config import (
    NEWS_API_KEY,
    NEWS_API_URL,
    COUNTRY,
    TTL_SECONDS
)
from redis_client import redis_client
from location_extractor import extract_locations
from geocoder import geocode_location


MAX_PAGES = 10          # safety limit
PAGE_SIZE = 10          # GNews free-tier safe
SLEEP_BETWEEN_CALLS = 1 # seconds (avoid rate-limit)


def fetch_news():
    print("Fetching today's news from GNews...")

    today = datetime.date.today().isoformat()
    page = 1
    total_saved = 0

    while page <= MAX_PAGES:
        print(f"Fetching page {page}...")

        params = {
            "apikey": NEWS_API_KEY,
            "country": COUNTRY,
            "lang": "en",
            "max": PAGE_SIZE,
            "page": page,
            "from": today,
            "to": today,
        }

        response = requests.get(NEWS_API_URL, params=params, timeout=10)

        if response.status_code != 200:
            print("GNews error:", response.status_code, response.text)
            break

        articles = response.json().get("articles", [])
        if not articles:
            print("No more articles.")
            break

        for article in articles:
            title = article.get("title", "")
            description = article.get("description", "")
            content = f"{title}. {description}"

            locations = extract_locations(content)
            if not locations:
                continue

            lat = lng = city = None

            for loc in locations:
                lat, lng = geocode_location(loc)
                if lat and lng:
                    city = loc
                    break

            if not lat or not lng:
                continue

            news_id = str(uuid.uuid4())

            news_data = {
                "id": news_id,
                "title": title,
                "summary": description,
                "city": city,
                "lat": lat,
                "lng": lng,
                "source": article.get("source", {}).get("name"),
                "url": article.get("url"),
                "publishedAt": article.get("publishedAt"),
                "category": "general",
            }

            # store news
            redis_client.set(
                f"news:{today}:{news_id}",
                json.dumps(news_data),
                ex=TTL_SECONDS
            )

            # link news to city
            marker_key = f"markers:{today}:{city.lower()}"
            redis_client.lpush(marker_key, news_id)
            redis_client.expire(marker_key, TTL_SECONDS)

            total_saved += 1

        page += 1
        time.sleep(SLEEP_BETWEEN_CALLS)

    print(f"✅ Done. Saved {total_saved} news items for {today}.")


if __name__ == "__main__":
    while True:
        fetch_news()
        time.sleep(1800) 

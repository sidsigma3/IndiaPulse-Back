import os
from dotenv import load_dotenv

load_dotenv()

# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# News API (use GNews or any you want)
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://gnews.io/api/v4/top-headlines"

# Mapbox (for geocoding)
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")

# App config
COUNTRY = "in"
TTL_SECONDS = 60 * 60 * 24  # 24 hours

import logging
import requests
import pandas as pd
from datetime import datetime, timedelta


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def extract_weather(lat=6.6271, lon=-1.6278, days=7):
    """Extract last N days historical weather from Open-Meteo API (Kumasi)"""
    end = datetime.now().date()
    start = end - timedelta(days=days - 1)
    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}&longitude={lon}"
        f"&start_date={start}&end_date={end}"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
        "&timezone=Africa/Accra"
    )
    
    try:
        logger.info(f"Fetching historical weather data from {start} to {end}...")
        r = requests.get(url, timeout=10).json()
        if "daily" not in r:
            raise ValueError("Invalid API response")
        logger.info(f"Extracted {len(r['daily']['time'])} days of weather data")
        return pd.DataFrame({
            "date": r["daily"]["time"],
            "temp_max": r["daily"]["temperature_2m_max"],
            "temp_min": r["daily"]["temperature_2m_min"],
            "precipitation": r["daily"]["precipitation_sum"]
        })
    except Exception as e:
        logger.error(f"Extract failed: {e}")
        raise
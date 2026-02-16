import logging
from datetime import datetime, timedelta

import pandas as pd
import requests


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def extract_weather(lat=6.6271, lon=-1.6278, days=7):
    """Extract last N days historical weather from Open-Meteo API (Kumasi)"""
    logger.debug(f"Starting extraction for lat={lat}, lon={lon}, days={days}")
    
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
        logger.debug(f"API URL: {url}")
        
        r = requests.get(url, timeout=10)
        logger.debug(f"API response status: {r.status_code}")
        
        r = r.json()
        if "daily" not in r:
            raise ValueError("Invalid API response: 'daily' key not found")
        
        num_days = len(r['daily']['time'])
        logger.info(f"[OK] Successfully extracted {num_days} days of weather data")
        logger.debug(f"Columns available: {list(r['daily'].keys())}")
        
        df = pd.DataFrame({
            "date": r["daily"]["time"],
            "temp_max": r["daily"]["temperature_2m_max"],
            "temp_min": r["daily"]["temperature_2m_min"],
            "precipitation": r["daily"]["precipitation_sum"]
        })
        
        logger.debug(f"DataFrame shape: {df.shape}, dtypes:\n{df.dtypes}")
        return df
        
    except requests.exceptions.Timeout:
        logger.error("Extract failed: API request timed out (10s)")
        raise
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Extract failed: Connection error - {e}")
        raise
    except ValueError as e:
        logger.error(f"Extract failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Extract failed with unexpected error: {type(e).__name__}: {e}")
        raise
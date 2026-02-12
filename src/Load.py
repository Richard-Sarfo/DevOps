from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import logging
import pandas as pd

logger = logging.getLogger(__name__)

engine = create_engine("sqlite:///weather.db", echo=False)

def load_to_sqlite(raw_data):
    if not raw_data or 'daily' not in raw_data:
        raise ValueError("No valid data to load")
    
    df = pd.DataFrame({
        'date': raw_data['daily']['time'],
        'temp_max': raw_data['daily']['temperature_2m_max'],
        'temp_min': raw_data['daily']['temperature_2m_min'],
        'precipitation': raw_data['daily']['precipitation_sum']
    })
    
    df.to_sql('raw_weather', engine, if_exists='append', index=False)
    logger.info(f"Loaded {len(df)} rows to raw_weather table")
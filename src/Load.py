import logging

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

engine = create_engine("sqlite:///weather.db", echo=False)

def load_to_sqlite(data):
    """Load a pandas DataFrame or the original API-style dict into sqlite `weather` table with detailed logging.

    Accepts either:
    - a pandas.DataFrame with columns including `date`, `temp_max`, `temp_min`, `precipitation`, `temp_avg`, `temp_category`
    - a dict similar to the Open-Meteo `daily` response (keeps backward compatibility)
    """
    logger.debug(f"Starting load operation with data type: {type(data).__name__}")
    
    if data is None:
        logger.error("Load failed: Received None instead of data")
        raise ValueError("No valid data to load")

    try:
        # If data is an API-style dict with 'daily' key, convert to DataFrame
        if isinstance(data, dict) and 'daily' in data:
            logger.debug("Converting API-style dict to DataFrame")
            df = pd.DataFrame({
                'date': data['daily']['time'],
                'temp_max': data['daily']['temperature_2m_max'],
                'temp_min': data['daily']['temperature_2m_min'],
                'precipitation': data['daily']['precipitation_sum']
            })
        elif isinstance(data, pd.DataFrame):
            logger.debug(f"Using provided DataFrame with shape {data.shape}")
            df = data.copy()
        else:
            logger.error(f"Load failed: Unsupported data type {type(data).__name__}")
            raise ValueError("Unsupported data format for load_to_sqlite")

        logger.debug(f"DataFrame before processing: shape={df.shape}, columns={list(df.columns)}")

        # Ensure types and defaults
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            logger.debug(f"Date range: {df['date'].min()} to {df['date'].max()}")
            
        if 'precipitation' in df.columns:
            initial_nulls = df['precipitation'].isna().sum()
            df['precipitation'] = df['precipitation'].fillna(0)
            if initial_nulls > 0:
                logger.debug(f"Filled {initial_nulls} null precipitation values")

        logger.debug(f"DataFrame ready for insert: shape={df.shape}, dtypes:\n{df.dtypes}")
        
        # Check if weather table exists
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='weather'"))
            table_exists = result.fetchone() is not None
            logger.debug(f"Weather table exists: {table_exists}")

        # Write to the `weather` table
        df.to_sql('weather', engine, if_exists='append', index=False)
        logger.info(f"[OK] Loaded {len(df)} rows to weather table")
        logger.debug(f"Total rows in weather table after load: {len(df)}")
        
    except Exception as e:
        logger.error(f"Load failed with error: {type(e).__name__}: {e}")
        raise
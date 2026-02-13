import pandas as pd
import logging

logger = logging.getLogger(__name__)

def transform(df):
    """Clean & enrich data with detailed logging"""
    logger.debug(f"Starting transformation on DataFrame with shape {df.shape}")
    logger.debug(f"Input columns: {list(df.columns)}")
    logger.debug(f"Input dtypes:\n{df.dtypes}")
    
    if df.empty:
        logger.warning("Input DataFrame is empty; returning as-is")
        return df
    
    df = df.copy()
    logger.debug("Created DataFrame copy")
    
    try:
        # Calculate average temperature
        df["temp_avg"] = (df["temp_max"] + df["temp_min"]) / 2
        logger.debug(f"Calculated temp_avg: min={df['temp_avg'].min():.2f}, max={df['temp_avg'].max():.2f}, mean={df['temp_avg'].mean():.2f}")
        
        # Categorize temperature
        df["temp_category"] = pd.cut(
            df["temp_avg"], bins=[-float("inf"), 5, 15, float("inf")],
            labels=["Cold", "Mild", "Hot"], include_lowest=True
        )
        logger.debug(f"Temperature distribution:\n{df['temp_category'].value_counts().to_dict()}")
        
        # Handle precipitation nulls
        initial_nulls = df["precipitation"].isna().sum()
        df["precipitation"] = df["precipitation"].fillna(0).astype(float)
        logger.debug(f"Filled {initial_nulls} null precipitation values with 0")
        
        # Convert dates
        df["date"] = pd.to_datetime(df["date"])
        logger.debug(f"Converted dates; range: {df['date'].min()} to {df['date'].max()}")
        
        logger.info(f"[OK] Transformation complete: {df.shape[0]} rows, {df.shape[1]} columns")
        logger.debug(f"Output columns: {list(df.columns)}")
        logger.debug(f"Output dtypes:\n{df.dtypes}")
        
        return df
        
    except KeyError as e:
        logger.error(f"Transform failed: Missing column {e}")
        raise
    except Exception as e:
        logger.error(f"Transform failed with unexpected error: {type(e).__name__}: {e}")
        raise
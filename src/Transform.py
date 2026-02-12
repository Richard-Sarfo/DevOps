import pandas as pd
import logging

logger = logging.getLogger(__name__)

def transform(df):
    """Clean & enrich data"""
    df = df.copy()
    df["temp_avg"] = (df["temp_max"] + df["temp_min"]) / 2
    df["temp_category"] = pd.cut(
        df["temp_avg"], bins=[-float("inf"), 5, 15, float("inf")],
        labels=["Cold", "Mild", "Hot"], include_lowest=True
    )
    df["precipitation"] = df["precipitation"].fillna(0)
    df["date"] = pd.to_datetime(df["date"])
    logger.info("Transformed data")
    return df
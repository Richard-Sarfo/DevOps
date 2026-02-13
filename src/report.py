import logging
import os
from datetime import datetime
from pathlib import Path
import pandas as pd

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s [%(name)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def generate_report(df, output_dir="data"):
    """
    Generate daily summary CSV report from weather data.
    
    Args:
        df (pd.DataFrame): Input dataframe with weather data.
        output_dir (str): Directory to save the report. Default: 'data'.
    
    Returns:
        str: Path to the generated report file.
    
    Raises:
        ValueError: If input dataframe is empty or required columns are missing.
        IOError: If report cannot be written to disk.
    """
    logger.debug("Starting report generation")
    
    try:
        # Input validation
        if df is None or df.empty:
            error_msg = "Input dataframe is empty or None"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        required_cols = {"date", "temp_avg", "precipitation", "temp_category"}
        missing_cols = required_cols - set(df.columns)
        if missing_cols:
            error_msg = f"Missing required columns: {missing_cols}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info(f"Input validation passed. Processing {len(df)} rows")
        
        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        logger.debug(f"Output directory ensured: {output_dir}")
        
        # Generate summary aggregation
        logger.debug("Aggregating data by date")
        summary = df.groupby("date").agg({
            "temp_avg": "mean",
            "precipitation": "sum",
            "temp_category": lambda x: x.mode()[0] if not x.empty else None
        }).reset_index()
        logger.info(f"Aggregated to {len(summary)} daily records")
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = f"report_{timestamp}.csv"
        path = os.path.join(output_dir, filename)
        logger.debug(f"Report filename: {filename}")
        
        # Write report to CSV
        summary.to_csv(path, index=False)
        logger.info(f"Report successfully saved: {path}")
        logger.debug(f"Report size: {os.path.getsize(path)} bytes")
        
        return path
    
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise
    except IOError as e:
        logger.error(f"IO error while writing report: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in generate_report: {type(e).__name__}: {e}")
        raise

    
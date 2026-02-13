from pathlib import Path
import sys
import logging
import traceback

# Ensure project root (DevOps/) is on sys.path so `src` imports work
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Configure logging with more detailed format
log_format = "%(asctime)s [%(name)s] [%(levelname)s] %(message)s"
logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(project_root / "logs" / "pipeline.log")
    ]
)
logger = logging.getLogger(__name__)

from src.Extract import extract_weather
from src.Transform import transform
from src.Load import load_to_sqlite, engine
from src.report import generate_report
import pandas as pd


def main():
    """Run the complete ETL pipeline with comprehensive logging and error handling"""
    logger.info("=" * 80)
    logger.info("Starting Pipeline Execution")
    logger.info("=" * 80)
    
    try:
        # Extract phase
        logger.info("--- EXTRACT PHASE ---")
        try:
            df = extract_weather(days=3)
            if df is None or df.empty:
                raise ValueError("Extraction returned empty DataFrame")
            logger.info(f"[OK] Extract successful: {len(df)} rows extracted")
        except Exception as e:
            logger.error(f"[FAILED] Extract phase failed: {e}")
            logger.debug(traceback.format_exc())
            raise

        # Transform phase
        logger.info("--- TRANSFORM PHASE ---")
        try:
            df_t = transform(df)
            if df_t is None or df_t.empty:
                raise ValueError("Transform returned empty DataFrame")
            logger.info(f"[OK] Transform successful: {len(df_t)} rows transformed")
        except Exception as e:
            logger.error(f"[FAILED] Transform phase failed: {e}")
            logger.debug(traceback.format_exc())
            raise

        # Load phase
        logger.info("--- LOAD PHASE ---")
        try:
            load_to_sqlite(df_t)
            logger.info("[OK] Load successful: data persisted to weather.db")
        except Exception as e:
            logger.error(f"[FAILED] Load phase failed: {e}")
            logger.debug(traceback.format_exc())
            raise

        # Report generation phase
        logger.info("--- REPORT GENERATION PHASE ---")
        try:
            report_path = generate_report(df_t, output_dir=project_root / "data")
            logger.info(f"[OK] Report generated successfully: {report_path}")
        except Exception as e:
            logger.error(f"[FAILED] Report generation phase failed: {e}")
            logger.debug(traceback.format_exc())
            raise

        # Verification phase
        logger.info("--- VERIFICATION PHASE ---")
        try:
            with engine.connect() as conn:
                # Check tables
                tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
                logger.info(f"Tables in database: {tables['name'].tolist()}")
                
                # Check row count
                if 'weather' in tables['name'].values:
                    count = pd.read_sql("SELECT COUNT(*) as count FROM weather", conn)
                    total_rows = count['count'].iloc[0]
                    logger.info(f"Total rows in weather table: {total_rows}")
                    
                    # Show sample
                    rows = pd.read_sql("SELECT * FROM weather ORDER BY date ASC LIMIT 5", conn)
                    logger.debug(f"Sample (first 5 rows):\n{rows}")
                    logger.info("[OK] Verification successful")
                else:
                    logger.warning("Weather table not found in database")
        except Exception as e:
            logger.error(f"[FAILED] Verification phase failed: {e}")
            logger.debug(traceback.format_exc())
            # Don't raise here; pipeline succeeded, verification just failed
        
        logger.info("=" * 80)
        logger.info("[OK] Pipeline Execution Completed Successfully")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error("=" * 80)
        logger.error(f"[FAILED] Pipeline Execution Failed: {e}")
        logger.error("=" * 80)
        sys.exit(1)


if __name__ == '__main__':
    main()

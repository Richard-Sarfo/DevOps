import logging
import os
import sys
import tempfile
from pathlib import Path

import pandas as pd
import pytest

# Ensure project root is on sys.path so `src` is importable when running this file directly
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.Extract import extract_weather  # noqa: E402
from src.Transform import transform  # noqa: E402
from src.Load import load_to_sqlite, engine  # noqa: E402
from src.report import generate_report  # noqa: E402

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_extract():
    logger.info("Running test_extract...")
    df = extract_weather(days=2)
    logger.debug(f"Extracted {len(df)} rows")
    assert isinstance(df, pd.DataFrame), "Extract should return a DataFrame"
    assert len(df) >= 1, "Extract should return at least 1 row"
    assert "temp_max" in df.columns, "DataFrame should contain temp_max column"
    logger.info("[OK] test_extract passed")


def test_transform():
    logger.info("Running test_transform...")
    sample = pd.DataFrame({
        "date": ["2026-02-01"],
        "temp_max": [3.0],
        "temp_min": [-2.0],
        "precipitation": pd.array([None], dtype="Float64")  # Use nullable Float64
    })
    logger.debug(f"Input sample: {sample.to_dict()}")
    result = transform(sample)
    logger.debug(f"Transform result: temp_avg={result['temp_avg'].iloc[0]}, category={result['temp_category'].iloc[0]}")
    assert result["temp_avg"].iloc[0] == 0.5, f"Expected temp_avg=0.5, got {result['temp_avg'].iloc[0]}"
    assert result["temp_category"].iloc[0] == "Cold", f"Expected Cold, got {result['temp_category'].iloc[0]}"
    assert result["precipitation"].iloc[0] == 0, "Null precipitation should be filled with 0"
    logger.info("[OK] test_transform passed")


def test_load_roundtrip():
    logger.info("Running test_load_roundtrip...")
    df = pd.DataFrame({
        "date": [pd.Timestamp("2026-02-10 00:00:00")],
        "temp_max": [10.0],
        "temp_min": [5.0],
        "precipitation": [0.0],
        "temp_avg": [7.5],
        "temp_category": ["Mild"]
    })
    logger.debug(f"Loading test data: {df.to_dict()}")
    load_to_sqlite(df)
    
    with engine.connect() as conn:
        result = pd.read_sql("SELECT * FROM weather WHERE date LIKE '2026-02-10%'", conn)
    
    logger.debug(f"Retrieved rows: {len(result)}")
    assert len(result) >= 1, "Should find at least one row with date 2026-02-10"
    assert result["temp_avg"].iloc[-1] == 7.5, f"Expected temp_avg=7.5, got {result['temp_avg'].iloc[-1]}"
    logger.info("[OK] test_load_roundtrip passed")


# Additional tests for edge cases and error handling

def test_transform_temperature_categories():
    """Test that temperature categorization works correctly for all ranges"""
    logger.info("Running test_transform_temperature_categories...")
    
    # bins [-inf, 5, 15, inf] so:
    # Cold: temp_avg <= 5, Mild: 5 < temp_avg <= 15, Hot: temp_avg > 15
    test_cases = [
        (0.0, "Cold"),
        (4.9, "Cold"),
        (5.0, "Cold"),      # At boundary (included in Cold due to include_lowest)
        (5.01, "Mild"),
        (10.0, "Mild"),
        (14.99, "Mild"),
        (15.0, "Mild"),     # At boundary (included in Mild)
        (15.01, "Hot"),
        (25.0, "Hot"),
    ]
    
    for temp_avg, expected_category in test_cases:
        sample = pd.DataFrame({
            "date": ["2026-02-01"],
            "temp_max": [temp_avg + 5],
            "temp_min": [temp_avg - 5],
            "precipitation": [0]
        })
        result = transform(sample)
        actual_category = result["temp_category"].iloc[0]
        logger.debug(f"temp_avg={temp_avg} -> category={actual_category} (expected: {expected_category})")
        assert actual_category == expected_category, f"Expected {expected_category} for avg {temp_avg}, got {actual_category}"
    
    logger.info("[OK] test_transform_temperature_categories passed")


def test_extract_returns_required_columns():
    """Test that extract returns all required columns"""
    logger.info("Running test_extract_returns_required_columns...")
    df = extract_weather(days=1)
    required_cols = {"date", "temp_max", "temp_min", "precipitation"}
    missing = required_cols - set(df.columns)
    logger.debug(f"Columns: {list(df.columns)}")
    assert not missing, f"Missing columns: {missing}"
    logger.info("[OK] test_extract_returns_required_columns passed")


def test_transform_handles_empty_dataframe():
    """Test that transform handles empty DataFrame gracefully"""
    logger.info("Running test_transform_handles_empty_dataframe...")
    empty_df = pd.DataFrame({
        "date": [],
        "temp_max": [],
        "temp_min": [],
        "precipitation": []
    })
    logger.debug("Testing with empty DataFrame")
    result = transform(empty_df)
    assert result.empty, "Transform should return empty DataFrame for empty input"
    logger.info("[OK] test_transform_handles_empty_dataframe passed")


def test_report_generation():
    """Test report generation functionality"""
    logger.info("Running test_report_generation...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        logger.debug(f"Using temporary directory: {tmpdir}")
        
        # Create test data
        test_df = pd.DataFrame({
            "date": pd.date_range("2026-02-10", periods=3),
            "temp_max": [32.0, 33.3, 34.4],
            "temp_min": [21.9, 22.4, 23.1],
            "precipitation": [6.3, 0.3, 0.3],
            "temp_avg": [26.95, 27.85, 28.75],
            "temp_category": ["Hot", "Hot", "Hot"]
        })
        
        # Generate report
        report_path = generate_report(test_df, output_dir=tmpdir)
        logger.debug(f"Report generated at: {report_path}")
        
        # Verify report exists and has content
        assert os.path.exists(report_path), f"Report file not created at {report_path}"
        
        # Verify report content
        report_df = pd.read_csv(report_path)
        logger.debug(f"Report shape: {report_df.shape}")
        logger.debug(f"Report columns: {list(report_df.columns)}")
        
        assert len(report_df) == 3, f"Expected 3 days in report, got {len(report_df)}"
        assert "temp_avg" in report_df.columns, "Report should contain temp_avg column"
        assert "precipitation" in report_df.columns, "Report should contain precipitation column"
        
    logger.info("[OK] test_report_generation passed")


def test_report_generation_missing_columns():
    """Test that report generation raises error for missing required columns"""
    logger.info("Running test_report_generation_missing_columns...")
    
    invalid_df = pd.DataFrame({
        "date": ["2026-02-01"],
        # Missing temp_avg, precipitation, temp_category
    })
    
    logger.debug("Testing report with missing columns")
    with pytest.raises(ValueError):
        generate_report(invalid_df)
    
    logger.info("[OK] test_report_generation_missing_columns passed")
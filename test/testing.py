import sys
from pathlib import Path
import pytest
import pandas as pd

# Ensure project root is on sys.path so `src` is importable when running this file directly
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.Extract import extract_weather
from src.Transform import transform
from src.Load import load_to_sqlite, engine

def test_extract():
    df = extract_weather(days=2)
    assert isinstance(df, pd.DataFrame)
    assert len(df) >= 1
    assert "temp_max" in df.columns


def test_transform():
    sample = pd.DataFrame({
        "date": ["2026-02-01"],
        "temp_max": [3.0],
        "temp_min": [-2.0],
        "precipitation": [None]
    })
    result = transform(sample)
    assert result["temp_avg"].iloc[0] == 0.5
    assert result["temp_category"].iloc[0] == "Cold"
    assert result["precipitation"].iloc[0] == 0


def test_load_roundtrip():
    df = pd.DataFrame({
        "date": [pd.Timestamp("2026-02-10")],
        "temp_max": [10.0],
        "temp_min": [5.0],
        "precipitation": [0.0],
        "temp_avg": [7.5],
        "temp_category": ["Mild"]
    })
    load_to_sqlite(df)
    with engine.connect() as conn:
        result = pd.read_sql("SELECT * FROM weather WHERE date = '2026-02-10'", conn)
    assert len(result) == 1
    assert result["temp_avg"].iloc[0] == 7.5
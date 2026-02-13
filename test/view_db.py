"""Utility script to view weather.db content"""
import sqlite3
import pandas as pd
from pathlib import Path

db_path = Path(__file__).parent.parent / "weather.db"

print("=" * 80)
print(f"Database: {db_path}")
print("=" * 80)

# Connect to database
conn = sqlite3.connect(db_path)

# List all tables
print("\n--- TABLES ---")
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)
print(tables)

# Show schema for each table
print("\n--- SCHEMA ---")
for table in tables['name']:
    print(f"\nTable: {table}")
    schema = pd.read_sql(f"PRAGMA table_info({table})", conn)
    print(schema)

# Show data from weather table
print("\n--- DATA (All rows) ---")
try:
    data = pd.read_sql("SELECT * FROM weather", conn)
    print(f"Total rows: {len(data)}")
    print(data.to_string())
    
    print("\n--- SUMMARY STATISTICS ---")
    print(data[['temp_max', 'temp_min', 'temp_avg', 'precipitation']].describe())
except Exception as e:
    print(f"Error reading weather table: {e}")

conn.close()
print("\n" + "=" * 80)

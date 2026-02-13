# Weather ETL Pipeline 

A reliable, automated data pipeline that fetches, transforms, and loads daily weather observations for analysis, demonstrating end-to-end data engineering practices with modern tooling and CI/CD.

## Project Overview

This project implements a complete ETL (Extract, Transform, Load) pipeline that:
- **Extracts** historical weather data from the Open-Meteo API
- **Transforms** raw weather observations into clean, enriched datasets
- **Loads** processed data into SQLite for persistent storage
- **Generates** daily summary reports for stakeholders
- **Monitors** pipeline health with comprehensive logging

**Target Location:** Kumasi, Ghana (6.6271°N, 1.6278°W)

## Architecture

```
┌─────────────────┐
│  Open-Meteo API │
└────────┬────────┘
         │
         ▼
    ┌─────────┐
    │ EXTRACT │  (Extract.py)
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │TRANSFORM│  (Transform.py)
    └────┬────┘
         │
         ▼
    ┌─────────┐
    │  LOAD   │  (Load.py)
    └────┬────┘
         │
         ▼
    ┌───────────────┐
    │  SQLite DB    │
    │ (weather.db)  │
    └───────────────┘
         │
         ▼
    ┌─────────┐
    │ REPORT  │  (report.py)
    └─────────┘
```

## Project Structure

```
DevOps/
├── src/
│   ├── Extract.py          # API data extraction
│   ├── Transform.py        # Data cleaning & enrichment
│   ├── Load.py             # Database operations
│   ├── report.py           # Report generation
│   └── __init__.py
├── test/
│   ├── testing.py          # Unit & integration tests
│   └── view_db.py          # Database inspection utility
├── data/
│   └── report_2026-02-13.csv  # Sample generated report
├── logs/
│   └── pipeline.log        # Pipeline execution logs
├── Scripts/
│   └── run_pipeline.py     # Main pipeline orchestrator
├── requirements.txt        # Python dependencies
├── Sprint 0.md            # Project planning & backlog
├── Sprint 1 Review.md     # Sprint retrospectives
├── Sprint 2 Review.md
├── Final Retrospective.md
└── README.md              # This file
```

##  Quick Start

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DevOps
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Pipeline

**Option 1: Run the complete pipeline**
```bash
python Scripts/run_pipeline.py
```

**Option 2: Run individual components**
```bash
# Extract only
python -c "from src.Extract import extract_weather; df = extract_weather(); print(df)"

# Transform data
python -c "from src.Transform import transform_weather; df = transform_weather()"

# Load to database
python -c "from src.Load import load_to_db; load_to_db()"

# Generate report
python -c "from src.report import generate_report; generate_report()"
```

##  Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | 2.2.3 | Data manipulation & analysis |
| requests | 2.32.3 | API calls (Open-Meteo) |
| sqlalchemy | 2.0.35 | Database ORM |
| pytest | 8.3.3 | Testing framework |
| ruff | 0.7.0 | Code linting & formatting |

##  Testing

Run the test suite:
```bash
pytest test/testing.py -v
```

View database contents:
```bash
python test/view_db.py
```

## Data Schema

### Weather Table
| Column | Type | Description |
|--------|------|-------------|
| date | DATE | Observation date |
| temp_max | FLOAT | Maximum temperature (°C) |
| temp_min | FLOAT | Minimum temperature (°C) |
| precipitation | FLOAT | Precipitation sum (mm) |
| temp_category | STRING | Category: cold/mild/hot |
| inserted_at | TIMESTAMP | Record insertion time |

## Features Implemented

-  **Extraction**: Fetches 7 days of historical weather data from Open-Meteo API
-  **Transformation**: Data cleaning, validation, and enrichment
-  **Loading**: Upsert logic to SQLite (avoids duplicate dates)
-  **Reporting**: Daily summary CSV reports with aggregated metrics
-  **Logging**: Comprehensive logging to console and file
-  **Error Handling**: Graceful API/database error handling
-  **Orchestration**: Single command to run end-to-end pipeline
-  **CI/CD**: GitHub Actions workflows for automated testing

## Sample Output

**Generated Report** (`data/report_2026-02-13.csv`):
```csv
date,avg_temp,max_temp,min_temp,total_precipitation,temp_category
2026-02-13,22.5,28.3,16.7,0.0,mild
2026-02-12,21.8,27.9,15.5,0.0,mild
...
```

##  Logging

Logs are saved to `logs/pipeline.log` and include:
- ✓ Extraction status and row counts
- ✓ Transformation operations applied
- ✓ Database operations (inserts/updates)
- ✓ Report generation confirmation
- ✗ Error messages with stack traces

Example log output:
```
2026-02-13 15:52:42,967 [INFO] [OK] Successfully extracted 7 days of weather data
2026-02-13 15:52:43,123 [INFO] [OK] Transformed 7 rows
2026-02-13 15:52:43,456 [INFO] [OK] Loaded 7 rows to database
2026-02-13 15:52:43,789 [INFO] [OK] Report generated: data/report_2026-02-13.csv
```

## Configuration

Edit `src/Extract.py` to change location or date range:
```python
def extract_weather(lat=6.6271, lon=-1.6278, days=7):
    # Modify lat/lon for different locations
    # Modify days for different time ranges
```

## Sprint Progress

- **Sprint 0**: Planning & backlog creation 
- **Sprint 1**: Core ETL implementation 
- **Sprint 2**: Testing & CI/CD enhancement 
- **Final**: Documentation & retrospective 

See [Sprint reviews](./Sprint%201%20Review.md) for detailed progress.

##  Development

### Code Quality
```bash
# Lint code
ruff check src/

# Format code
ruff format src/
```

### Running Locally
```bash
# Full pipeline
python Scripts/run_pipeline.py

# With verbose output
python Scripts/run_pipeline.py --verbose
```

##  Troubleshooting

| Issue | Solution |
|-------|----------|
| API timeout | Check internet connection; increase timeout in `Extract.py` |
| Database locked | Ensure no other processes are accessing `weather.db` |
| Missing dependencies | Run `pip install -r requirements.txt` |
| Import errors | Verify you're in the correct directory and virtual environment activated |

##  API Reference

### Extract Module
```python
from src.Extract import extract_weather
df = extract_weather(lat=6.6271, lon=-1.6278, days=7)
```

### Transform Module
```python
from src.Transform import transform_weather
df = transform_weather()
```

### Load Module
```python
from src.Load import load_to_db
load_to_db()
```

### Report Module
```python
from src.report import generate_report
generate_report()
```

##  Additional Resources

- [Open-Meteo API Documentation](https://open-meteo.com/en/docs)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

##  License

This project is open source and available under the MIT License.

## Contributors

- **Richard Anane Sarfo** - Lead Developer

##  Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the development team.

---

**Last Updated**: February 13, 2026

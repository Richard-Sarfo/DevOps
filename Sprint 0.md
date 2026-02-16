## Sprint 0: Planning

Product Vision
Weather ETL Pipeline is a reliable, automated data pipeline that fetches, cleans, and stores daily weather observations for analysis, demonstrating end-to-end data engineering practices with modern tooling and CI/CD.


## Product Backlog

| ID | User Story | Acceptance Criteria | Priority | Points |
|---|---|---|---|---|
| **US01** | As a data consumer, I want daily weather data extracted from Open-Meteo API so I have raw source data. | • Script fetches data for a fixed location for the last 7 days • JSON/CSV output saved • Handles API errors gracefully | Highest | 3 |
| **US02** | As a data engineer, I want extracted data loaded into SQLite so it's queryable and persistent. | • Creates table if not exists (date, temp_max, temp_min, precipitation, etc.) • Upsert/append logic (avoid duplicates by date) • Script succeeds → data visible via sqlite3 CLI | High | 3 |
| **US03** | As a data consumer, I want basic transformations applied so data is clean & enriched. | • Convert units if needed, fill missing values (e.g. mean or 0), add column "temp_category" (cold/mild/hot) • Transformed data saved to new table or updated | High | 3 |
| **US04** | As a data engineer, I want pipeline logging & basic monitoring so I can trace runs & errors. | • INFO/ERROR logs for each step • Simple health check script (returns success/failure + row count) • Logs written to file + console | Medium | 2 |
| **US05** | As a data consumer, I want daily summary CSV reports generated so I can easily share insights. | • After load, generate weather_summary_YYYY-MM-DD.csv (avg temp, total precip, etc.) • Saved to reports/ folder | Medium | 2 |
| **US06** | As a data engineer, I want the full pipeline runnable via one command so it's easy to execute/schedule. | • main.py or pipeline.sh that runs extract → transform → load → report • Configurable location via env var or arg | Medium | 2 |


## Definition of Done (DoD)
- Code committed via small PRs (or direct to main with good messages)
- All tests pass (unit + integration where feasible)
- CI pipeline (GitHub Actions) succeeds: lint (black/flake8/ruff), pytest
- Pipeline runs end-to-end locally without errors
- Logs produced, database updated, report file created
- README documents how to run + architecture diagram (simple text or draw.io screenshot)

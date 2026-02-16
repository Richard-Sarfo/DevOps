## Sprint 0: Planning

Product Vision
Weather ETL Pipeline is a reliable, automated data pipeline that fetches, cleans, and stores daily weather observations for analysis, demonstrating end-to-end data engineering practices with modern tooling and CI/CD.


## Product Backlog

| ID | User Story | Acceptance Criteria | Priority | Points |
|----|------------|---------------------|----------|--------|
| **US01** | As a data consumer, I want daily weather data extracted from Open-Meteo API so I have raw source data. | Fetch last 7 days; save JSON/CSV; handle API errors | Highest | 3 |
| **US02** | As a data engineer, I want extracted data loaded into SQLite so it's queryable and persistent. | Create table if not exists; upsert by date; visible via sqlite3 CLI | High | 3 |
| **US03** | As a data consumer, I want transformations applied so data is clean & enriched. | Convert units; fill missing values; add temp_category | High | 3 |
| **US04** | As a data engineer, I want logging & monitoring. | INFO/ERROR logs; health check; logs to file & console | Medium | 2 |
| **US05** | As a data consumer, I want daily summary CSV reports. | Generate summary CSV; save to reports folder | Medium | 2 |
| **US06** | As a data engineer, I want the pipeline runnable via one command. | main.py or pipeline.sh runs full pipeline; configurable location | Medium | 2 |


## Definition of Done (DoD)
- Code committed via small PRs (or direct to main with good messages)
- All tests pass (unit + integration where feasible)
- CI pipeline (GitHub Actions) succeeds: lint (black/flake8/ruff), pytest
- Pipeline runs end-to-end locally without errors
- Logs produced, database updated, report file created
- README documents how to run + architecture diagram (simple text or draw.io screenshot)

# Sprint 1 Retrospective – Weather ETL Pipeline

**What went well**  
- Simple Python ETL pipeline was straightforward to implement and test  
- Writing unit tests early (`test_extract`, `test_transform`, `test_load_roundtrip`) caught data structure and transformation issues  
- SQLite persistence made data inspection and validation easy  
- Incremental pipeline development (extract → transform → load → report) was manageable  
- Comprehensive logging at DEBUG, INFO, ERROR levels provided visibility into each pipeline phase  

**What didn't go well**  
- Initial import issues (`ModuleNotFoundError: No module named 'src'`) took time to diagnose  
- Unicode checkmark characters (✓) caused Windows console encoding errors — had to replace with [OK] tags  
- Hard-coded parameters (lat/lon, days=3) limit reusability  
- Database schema validation wasn't explicit until later in testing  
- Report generation was added after core ETL, not planned upfront

**Concrete improvements for Sprint 2**  
1. Add CLI arguments/env variables for configurable location, days, and output paths  
2. Implement database schema validation as a separate health-check function  
3. Add retry logic and timeout handling for API calls  
4. Include visualization (matplotlib) to complement CSV reports  
5. Add more edge-case tests (empty data, API failures, malformed responses)  
6. Containerize with Docker for consistent cross-platform execution  
7. Consider adding scheduling (cron/Airflow) for automated daily runs
# Sprint 1 Review – Weather ETL Pipeline

**Sprint Goal**  
Deliver a working basic ETL pipeline: extract weather data from Open-Meteo API and load it into SQLite.

**Completed Stories**  
- US01 – Extract daily weather data (7 days, Kumasi)  
- US02 – Load raw data into SQLite table `weather`

**Definition of Done met**  
- Code committed incrementally  
- Unit/integration tests passing  
- CI pipeline (GitHub Actions) green  
- Pipeline runs end-to-end locally without errors  
- Data visible in `weather.db`

**Evidence / Demo**

- **Pipeline run log**  
  ![Pipeline run log](logs/pipeline.log)

- **Extracted data sample (console / df.head())**  
  ![Extract sample](Screenshots\Screenshot 2026-02-13 090949.png)

- **SQLite table after load**  
  ![SQLite content](screenshots/sprint1-sqlite-select.png)

- **CI pipeline success**  
  ![GitHub Actions success](logs/pipeline.log)

- **Commit history showing incremental delivery**  
  ![Commit graph Sprint 1](Screenshots/Screenshot 2026-02-13 112314.png)

**Delivered increment**  
Basic extract → load pipeline working. Raw weather data is now persistently stored and queryable.
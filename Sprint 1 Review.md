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

- **API extraction output**  
  ![Extract sample](Screenshots/Screenshot%202026-02-13%20090949.png)

- **DataFrame structure verification**  
  ![DataFrame columns](Screenshots/Screenshot%202026-02-13%20090938.png)

- **SQLite database validation**  
  ![SQLite content](Screenshots/Screenshot%202026-02-12%20101612.png)

- **Commit history showing incremental delivery**  
  ![Commit graph Sprint 1](Screenshots/Screenshot%202026-02-13%20112314.png)

**Delivered increment**  
Basic extract → load pipeline working. Raw weather data is now persistently stored and queryable.
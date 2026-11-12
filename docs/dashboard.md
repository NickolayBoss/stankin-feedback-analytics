# Dashboard walkthrough

## Run
1. Copy `.env.example` to `.env` and set a local password.
2. Run `docker compose up --build -d`.
3. Open http://localhost:8501.
4. To reset demo data: `docker compose down -v` then restart. **Warning:** removes the local database volume.

## Sections
- Total feedback and resolved percentage: throughput and closure.
- Response SLA: answered requests meeting a 24-hour threshold (unanswered requests excluded).
- Median first-response time: robust central tendency.
- Weekly category volume: recurring issues and shifts in demand.
- Department performance: workload and CSAT.
- Backlog: open tickets and those older than 72 hours.

## Data policy
The seed dataset contains 500 generated records and no real student information. The dashboard has read-only SQL queries. Do not expose this demo publicly with a real database or credentials.

## Screenshot checklist
Capture the KPI row, weekly trends and department table after starting the demo; add images to `docs/screenshots/` only after verifying actual output. No fabricated screenshots are provided.

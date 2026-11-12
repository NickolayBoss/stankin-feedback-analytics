# Analytics portfolio roadmap / План развития аналитического портфолио

> Project status: educational MVP. Features must be marked as verified only after an actual successful run.

## Delivered in main
- Telegram-based feedback collection and moderation prototype.
- PostgreSQL data model and SQL reporting examples.
- Bilingual documentation and analyst-oriented SQL modules.

## Work in progress
- [ ] Review and merge the SQL-first demo pull request after checks pass.
- [ ] Verify KPI definitions against SQL queries and seed data.
- [ ] Validate Python tests and PostgreSQL integration in GitHub Actions.
- [ ] Run the Streamlit dashboard locally with Docker Compose.
- [ ] Capture genuine dashboard screenshots and add them to documentation.

## Analyst acceptance criteria
1. **Data quality:** foreign keys, status transitions, missing values and duplicates are explicitly checked.
2. **Metric contracts:** numerator, denominator, filters, time zone and null handling are documented.
3. **Reproducibility:** a reviewer can start the demo with documented commands and generated, non-personal data.
4. **Transparency:** screenshots show real application output; unverified functionality is not presented as completed.
5. **Security:** no Telegram tokens, credentials or personal student submissions are committed.

## Portfolio narrative
**Problem:** student feedback is difficult to evaluate without a consistent workflow and measurable indicators.

**Approach:** collect and moderate submissions, model them relationally, define metrics and report trends and operational bottlenecks.

**Demonstrated skills:** requirements analysis, PostgreSQL/SQL, data-quality controls, KPI design, technical documentation and reproducible testing.

## Next review
Check the open feature pull request, resolve CI failures, and merge only when checks are green. This document intentionally tracks intermediate progress rather than claiming production readiness.

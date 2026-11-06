# SQL Analytics / SQL-аналитика

**RU:** Это SQL-first проект: вычисления выполняет PostgreSQL 16, Python отвечает за Telegram-интерфейс. Файлы пронумерованы по сложности.  
**EN:** PostgreSQL 16 computes metrics; Python handles Telegram presentation.

| SQL file | RU / EN | Techniques |
|---|---|---|
| 01_schema.sql | Модель / Schema | DDL, FK, indexes |
| 02_quality.sql | Качество / Quality | LEFT JOIN, EXISTS, FILTER |
| 03_kpi.sql | Показатели / KPIs | CTE, GROUP BY, NULLIF |
| 04_funnel_sla.sql | Воронка / Funnel | LAG, FIRST_VALUE, PERCENTILE_CONT |
| 05_cohorts.sql | Когорты / Cohorts | JOIN, CTE, retention |
| 06_trends.sql | Динамика / Trends | GENERATE_SERIES, moving AVG, LAG |
| 07_demo.sql | Синтетика / Synthetic demo | INSERT SELECT, isolated schema |
| 08_views.sql | Витрины / Views | CREATE VIEW |

## Запуск / Run
После запуска Docker / After starting Docker:
```bash
docker compose exec -T db psql -U stankin -d stankin < sql/03_kpi.sql
```
**RU:** Замените путь на нужный SQL-файл. `07_demo.sql` создаёт отдельную схему `demo`, не изменяя реальные записи. Для выполнения аналитики по demo в одной psql-сессии задайте `SET search_path TO demo, public;`.

**EN:** Replace the path to run other modules. Demo records are isolated in `demo` schema.

**Definitions / Определения:** reviewed = not pending; accepted = approved or published; approval rate = accepted / reviewed; review latency = reviewed_at − created_at; returning author = more than one submission. Daily dates are in Moscow time.

**RU:** Предложения не равны просмотрам или охвату Telegram-канала. Метрики показывают активность предложки, не просмотры.  
**EN:** Submission counts do not measure channel reach or views.

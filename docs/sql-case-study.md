# SQL Case Study / Аналитический кейс

## Business problem / Бизнес-задача
**RU:** Определить, как меняется активность предложки, насколько быстро администратор обрабатывает сообщения и сколько авторов возвращаются.  
**EN:** Quantify incoming submissions, moderation efficiency, and contributor retention.

## Data model / Модель
`users (1) -> (N) submissions (1) -> (N) moderation_events`

## Metrics / Метрики
| RU / EN | Formula / Формула |
|---|---|
| Доля одобрений / Approval rate | (approved + published) / reviewed |
| Время проверки / Review time | reviewed_at - created_at |
| p90 обработки / Review p90 | PERCENTILE_CONT(0.9) |
| Повторные авторы / Returning authors | COUNT per author > 1 |
| Когортное удержание / Cohort retention | Active cohort members / initial cohort size |
| Недельное изменение / WoW change | (current - previous) / previous |

## SQL skills / Навыки
**RU:** CTE, JOIN, FILTER, GROUP BY, оконные функции LAG/FIRST_VALUE, перцентили, календарь GENERATE_SERIES, CREATE VIEW, частичные индексы и контроль качества данных.

**EN:** CTEs, joins, window functions, percentiles, date spines, reusable views, partial indexes and data quality checks.

## Interpretation / Интерпретация
**RU:** Доля одобрений может быть высокой при растущей очереди; анализируйте вместе с pending и p90. Когортный анализ показывает повторное участие в предложке, но не причинный эффект и не охват канала.

**EN:** Approval rate must be interpreted alongside backlog and p90 latency. Cohort activity is descriptive, not causal.

## Privacy / Конфиденциальность
**RU:** SQL-модули не содержат реальных Telegram ID, токенов и дампов БД. Демо-данные синтетические.  
**EN:** No real user identifiers, secrets, or production dumps are included.

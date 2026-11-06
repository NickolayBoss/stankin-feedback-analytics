# Системная аналитика / Systems Analysis

## Бизнес-цель / Business objective
**RU:** Измерять активность студенческого сообщества, скорость обработки предложений и эффективность публикаций.
**EN:** Measure community activity, submission review time, and publication effectiveness.

## Участники / Actors
- Студент / Subscriber: отправляет предложение / submits content
- Администратор / Administrator: проверяет, публикует, читает SQL-отчёты / moderates and reads reports
- Telegram-канал / Channel: получает опубликованный контент / receives published content

## Требования / Functional requirements
- FR-01: Принимать сообщения / Accept text, photo, video, GIF, documents.
- FR-02: Сохранять метаданные в PostgreSQL / Persist submission metadata.
- FR-03: Уведомлять администратора / Notify the admin privately.
- FR-04: Ограничивать права по ADMIN_ID / Authorize by Telegram admin ID.
- FR-05: Хранить историю решений / Audit moderation actions.
- FR-06: Формировать SQL-отчёты в Telegram / Deliver SQL reports in Telegram.
- FR-07: Публиковать одобренные предложения / Publish approved submissions.

## ER-модель / Entity relationships
\`users (1) -> (N) submissions (1) -> (N) moderation_events\`

## KPI / Показатели
| KPI | Расчёт / Definition |
|---|---|
| Received / Получено | COUNT(*) |
| Pending / В очереди | status='pending' |
| Approval rate / Доля одобрений | (approved + published) / reviewed |
| Average review time / Среднее время обработки | AVG(reviewed_at - created_at) |
| Unique authors / Уникальные авторы | COUNT(DISTINCT user_id) |
| Returning authors / Повторные авторы | Authors with more than one submission |

## Конфиденциальность / Privacy
**RU:** Публичный репозиторий содержит только код, тестовые шаблоны и документацию. Отчёты показывают агрегаты, а не персональные Telegram ID.
**EN:** Public repository stores only code, templates and docs; admin reports show aggregates, not user identifiers.

## Ограничения / Known limitations
**RU:** Один администратор; нет альбомов, ответов авторам, антиспама и гарантии exactly-once публикации. 
**EN:** Single admin; no albums, reply relay, rate limiting or exactly-once publication guarantee.

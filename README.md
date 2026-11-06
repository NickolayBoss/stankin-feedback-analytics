# STANKIN Feedback Analytics Platform
## Платформа аналитики предложений СТАНКИНа / STANKIN Feedback Analytics Platform

**RU:** Telegram-бот для сбора предложений студентов, модерации, хранения событий в PostgreSQL и получения SQL-отчётов прямо в Telegram администратора.

**EN:** Telegram bot for student submissions, moderation, PostgreSQL event storage and SQL-powered admin reports delivered in Telegram.

### Возможности / Features
- Приём сообщений / Submission intake: текст, фото, видео, GIF, файлы
- Модерация / Moderation: одобрить, отклонить, опубликовать
- Аналитика / Analytics: SQL-метрики, таблицы, ежедневная динамика
- Безопасность / Security: только администратор видит отчёты

### Команды / Commands
| Команда / Command | Назначение / Purpose |
|---|---|
| /help | Справка / Help |
| /my | Мои предложения (только автор) / My submissions |
| /stats | Общая статистика / Overview |
| /report | Полный отчёт (5 сообщений) / Full report |
| /daily | По дням (7 дней, МСК) / Daily |
| /formats | Типы контента / Content types |
| /moderation | Скорость обработки / Moderation performance |
| /authors | Уникальные и повторные авторы / Contributors |

### Запуск / Run
1. Установите Docker Desktop / Install Docker Desktop.
2. Скопируйте \`.env.example\` в \`.env\` / Copy the environment template.
3. Заполните \`BOT_TOKEN\`, \`ADMIN_ID\`, \`POSTGRES_PASSWORD\` и пароль в \`DATABASE_URL\` / Fill in credentials locally.
4. Откройте диалог с ботом и нажмите Start / Start the bot chat.
5. Выполните \`docker compose up --build -d\` / Run Docker Compose.
6. Проверьте отправку предложения с другого Telegram-аккаунта / Test a submission from another account.

**RU:** Чтобы включить публикацию, назначьте бота администратором канала с правом публикации и укажите \`CHANNEL_ID\`. Для круглосуточной работы нужен постоянно работающий сервер.

**EN:** To enable channel posting, grant the bot posting rights and configure \`CHANNEL_ID\`. Always-on hosting is required for 24/7 operation.

### Архитектура / Architecture
\`Telegram -> aiogram -> PostgreSQL -> SQL -> Telegram admin reports\`

Сущности / Entities: \`users\`, \`submissions\`, \`moderation_events\`.

SQL-примеры / SQL examples: [sql/analytics.sql](sql/analytics.sql).  
Требования и KPI / Requirements and KPIs: [docs/architecture.md](docs/architecture.md).

### Секреты / Secrets
**RU:** Никогда не загружайте \`.env\`, токены, пароли или дампы базы данных в публичный репозиторий. \`.env.example\` содержит только примеры. Если токен уже был опубликован, перевыпустите его через BotFather.

**EN:** Never commit secrets, credentials, or real database dumps. Rotate any previously exposed tokens.

### Ограничения / Limitations
**RU:** MVP поддерживает одного администратора и одиночные сообщения. Группировка альбомов, ответы авторам, антиспам, резервные копии и гарантия публикации ровно один раз пока не реализованы. SQL-отчёты показывают агрегаты, а не личные данные.

**EN:** MVP supports one admin and single-message submissions. Albums, reply relay, rate limiting, backups and exactly-once publishing are not implemented yet.

### Личный кабинет / My submissions
**RU:** Команда `/my` показывает пользователю только его последние 10 предложений и текущие статусы. После одобрения, отклонения или публикации бот пытается уведомить автора. Неудачная отправка уведомления не отменяет решение администратора.

**EN:** `/my` displays only the user's latest 10 submissions and their statuses. The bot attempts to notify the author when a submission is approved, rejected or published. Failed notifications do not roll back moderation.

### SQL-first portfolio / SQL как основа портфолио

**RU:** [8 отдельных SQL-модулей](sql/README.md) показывают реляционную модель, проверки качества, KPI, воронку модерации, p50/p90, когортный анализ, оконные функции, витрины и синтетический набор данных. [Аналитический кейс](docs/sql-case-study.md) объясняет бизнес-смысл расчётов.

**EN:** [8 SQL modules](sql/README.md) demonstrate data modeling, quality checks, KPIs, moderation funnel, latency percentiles, cohorts, window functions, views and synthetic data. Read the [SQL case study](docs/sql-case-study.md).

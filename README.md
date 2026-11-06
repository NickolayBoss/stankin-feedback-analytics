# STANKIN Feedback Analytics Platform

Telegram feedback moderation and SQL analytics for a university community.

## Features
- Receive text, photo, video, GIF, and document submissions
- Private admin notifications, approve/reject/publish controls
- PostgreSQL database, audit trail, SQL reports in Telegram
- Admin commands: `/stats`, `/report`
- Docker Compose deployment

## Quick start
1. Install Docker Desktop.
2. Copy `.env.example` to `.env`.
3. Set `BOT_TOKEN` from BotFather, numeric `ADMIN_ID`, and a strong database password.
4. Open your bot in Telegram and press Start.
5. Run `docker compose up --build -d`.
6. Send a submission from a different Telegram account.
7. Optional: grant the bot channel posting rights and set `CHANNEL_ID` to enable Publish.

The repository contains **no secrets**. Never commit `.env` or real user data. GitHub stores source code, not a running bot: 24/7 operation requires an always-on host.

## Architecture
Telegram -> aiogram -> PostgreSQL -> SQL analytics -> admin Telegram chat

Tables: users, submissions, moderation_events. SQL examples in `sql/analytics.sql`.
Requirements and known limitations in `docs/architecture.md`.

## Current scope
Initial MVP, one administrator, polling, single-message submissions. No web dashboard, anonymous reply relay, album grouping, rate limiting, automatic backups or exactly-once publishing yet.

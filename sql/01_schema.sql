-- Schema / Схема. Reference DDL / Справочная структура.
CREATE TABLE IF NOT EXISTS users(telegram_id BIGINT PRIMARY KEY,username TEXT,created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS submissions(id BIGSERIAL PRIMARY KEY,user_id BIGINT NOT NULL REFERENCES users(telegram_id),chat_id BIGINT NOT NULL,message_id BIGINT NOT NULL,content_type TEXT NOT NULL,status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','approved','rejected','published')),created_at TIMESTAMPTZ NOT NULL DEFAULT now(),reviewed_at TIMESTAMPTZ,published_at TIMESTAMPTZ,UNIQUE(chat_id,message_id));
CREATE TABLE IF NOT EXISTS moderation_events(id BIGSERIAL PRIMARY KEY,submission_id BIGINT NOT NULL REFERENCES submissions(id),admin_id BIGINT NOT NULL,action TEXT NOT NULL,created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE INDEX IF NOT EXISTS idx_submissions_created ON submissions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_submissions_author ON submissions(user_id,created_at DESC);
CREATE INDEX IF NOT EXISTS idx_submissions_pending ON submissions(created_at) WHERE status='pending';
CREATE INDEX IF NOT EXISTS idx_events_submission ON moderation_events(submission_id,created_at DESC);

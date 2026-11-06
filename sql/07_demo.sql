-- SYNTHETIC ONLY / ТОЛЬКО СИНТЕТИЧЕСКИЕ ДАННЫЕ
-- Separate demo schema / Отдельная схема demo; production data untouched.
CREATE SCHEMA IF NOT EXISTS demo;
DROP TABLE IF EXISTS demo.moderation_events;
DROP TABLE IF EXISTS demo.submissions;
DROP TABLE IF EXISTS demo.users;
CREATE TABLE demo.users(LIKE public.users INCLUDING ALL);
CREATE TABLE demo.submissions(LIKE public.submissions INCLUDING ALL);
CREATE TABLE demo.moderation_events(LIKE public.moderation_events INCLUDING ALL);
INSERT INTO demo.users(telegram_id,username,created_at)
SELECT 9000000000+n,'synthetic_'||n,now()-interval '90 days' FROM generate_series(1,100) n;
WITH g AS(
 SELECT n,9000000000+(n%100)+1 uid,
 now()-((n%85)||' days')::interval-((n%24)||' hours')::interval created,
 CASE WHEN n%10<2 THEN 'pending' WHEN n%10<4 THEN 'rejected'
 WHEN n%10<7 THEN 'approved' ELSE 'published' END status,
 (ARRAY['text','photo','video','document','animation'])[(n%5)+1] kind
 FROM generate_series(1,400) n
)
INSERT INTO demo.submissions(user_id,chat_id,message_id,content_type,status,created_at,reviewed_at,published_at)
SELECT uid,uid,n,kind,status,created,
CASE WHEN status<>'pending' THEN created+((n%240+1)||' minutes')::interval END,
CASE WHEN status='published' THEN created+((n%240+10)||' minutes')::interval END FROM g;
INSERT INTO demo.moderation_events(submission_id,admin_id,action,created_at)
SELECT id,9000000999,CASE WHEN status='rejected' THEN 'reject' ELSE 'approve' END,reviewed_at
FROM demo.submissions WHERE status<>'pending';
SELECT COUNT(*) synthetic_submissions FROM demo.submissions;
-- For demo analytics in same psql session / Для аналитики demo в той же сессии:
-- SET search_path TO demo, public;
-- \i sql/03_kpi.sql

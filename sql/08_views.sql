-- Reusable SQL data marts / Переиспользуемые витрины
CREATE OR REPLACE VIEW analytics_daily AS
SELECT (created_at AT TIME ZONE 'Europe/Moscow')::date day,
COUNT(*) received,COUNT(*) FILTER(WHERE status<>'pending') reviewed,
COUNT(*) FILTER(WHERE status IN('approved','published')) accepted
FROM submissions GROUP BY 1;
CREATE OR REPLACE VIEW analytics_formats AS
SELECT content_type,COUNT(*) received,
COUNT(*) FILTER(WHERE status='pending') pending,
COUNT(*) FILTER(WHERE status IN('approved','published')) accepted
FROM submissions GROUP BY content_type;
CREATE OR REPLACE VIEW analytics_latency AS
SELECT content_type,COUNT(*) reviewed,
ROUND(AVG(EXTRACT(EPOCH FROM reviewed_at-created_at)/60.0)::numeric,2) avg_min
FROM submissions WHERE reviewed_at IS NOT NULL AND reviewed_at>=created_at GROUP BY content_type;
SELECT * FROM analytics_daily ORDER BY day DESC LIMIT 14;

-- Daily submission volume and conversion
SELECT created_at::date AS day, count(*) AS received,
 count(*) FILTER(WHERE status IN ('approved','published')) AS accepted
FROM submissions GROUP BY 1 ORDER BY 1 DESC;

-- Average review time by content type
SELECT content_type, count(*) AS submissions,
 round(avg(extract(epoch FROM reviewed_at-created_at))
 FILTER(WHERE reviewed_at IS NOT NULL)/60.0,2) AS mean_review_minutes
FROM submissions GROUP BY 1 ORDER BY 2 DESC;

-- Window function: contributor activity (admin-only)
SELECT user_id,count(*) AS submissions,
 dense_rank() OVER(ORDER BY count(*) DESC) AS activity_rank
FROM submissions GROUP BY user_id;

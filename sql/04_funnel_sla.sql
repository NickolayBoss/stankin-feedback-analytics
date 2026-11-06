-- Moderation funnel / Воронка модерации
WITH stages AS (
 SELECT 1 n,'Received / Получено' stage,COUNT(*) amount FROM submissions
 UNION ALL SELECT 2,'Reviewed / Проверено',COUNT(*) FILTER(WHERE status<>'pending') FROM submissions
 UNION ALL SELECT 3,'Accepted / Одобрено',COUNT(*) FILTER(WHERE status IN('approved','published')) FROM submissions
 UNION ALL SELECT 4,'Published / Опубликовано',COUNT(*) FILTER(WHERE status='published') FROM submissions
), f AS (
 SELECT n,stage,amount,FIRST_VALUE(amount) OVER(ORDER BY n) first_amount,LAG(amount) OVER(ORDER BY n) previous_amount FROM stages
)
SELECT stage,amount,ROUND(100.0*amount/NULLIF(first_amount,0),2) total_conversion_pct,
ROUND(100.0*amount/NULLIF(previous_amount,0),2) step_conversion_pct FROM f ORDER BY n;
-- SLA p50 / p90 / Перцентили времени модерации
SELECT content_type,COUNT(*) reviewed,
ROUND(AVG(EXTRACT(EPOCH FROM reviewed_at-created_at)/60.0)::numeric,1) avg_min,
ROUND((PERCENTILE_CONT(.5) WITHIN GROUP(ORDER BY EXTRACT(EPOCH FROM reviewed_at-created_at)/60.0))::numeric,1) p50_min,
ROUND((PERCENTILE_CONT(.9) WITHIN GROUP(ORDER BY EXTRACT(EPOCH FROM reviewed_at-created_at)/60.0))::numeric,1) p90_min
FROM submissions WHERE reviewed_at IS NOT NULL AND reviewed_at>=created_at GROUP BY content_type ORDER BY reviewed DESC;
-- Pending backlog / Возраст очереди
SELECT CASE WHEN now()-created_at<interval '1 hour' THEN '0-1h'
 WHEN now()-created_at<interval '6 hours' THEN '1-6h'
 WHEN now()-created_at<interval '24 hours' THEN '6-24h'
 ELSE '24h+' END bucket,COUNT(*) pending
FROM submissions WHERE status='pending' GROUP BY 1 ORDER BY 1;

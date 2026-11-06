-- Executive KPIs / Ключевые показатели
WITH k AS (
 SELECT COUNT(*) received,COUNT(*) FILTER(WHERE status='pending') pending,
 COUNT(*) FILTER(WHERE status='approved') approved,
 COUNT(*) FILTER(WHERE status='rejected') rejected,
 COUNT(*) FILTER(WHERE status='published') published,
 COUNT(DISTINCT user_id) authors,
 COUNT(*) FILTER(WHERE status<>'pending') reviewed,
 COUNT(*) FILTER(WHERE status IN('approved','published')) accepted,
 AVG(EXTRACT(EPOCH FROM reviewed_at-created_at)/60.0) FILTER(WHERE reviewed_at IS NOT NULL) avg_review_min
 FROM submissions
)
SELECT received,pending,approved,rejected,published,authors,
ROUND(100.0*accepted/NULLIF(reviewed,0),2) approval_pct,
ROUND(avg_review_min::numeric,2) avg_review_min,
ROUND(100.0*published/NULLIF(accepted,0),2) publish_pct FROM k;
-- Segmentation / Сегментация
SELECT content_type,COUNT(*) total,
COUNT(*) FILTER(WHERE status IN('approved','published')) accepted,
ROUND(100.0*COUNT(*) FILTER(WHERE status IN('approved','published'))/NULLIF(COUNT(*) FILTER(WHERE status<>'pending'),0),2) approval_pct
FROM submissions GROUP BY content_type ORDER BY total DESC;

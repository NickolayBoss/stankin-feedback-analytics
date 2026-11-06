-- STANKIN SQL analytics / SQL-аналитика СТАНКИНа
-- 1. Daily trend / Динамика по дням (Moscow time / МСК)
SELECT (created_at AT TIME ZONE 'Europe/Moscow')::date AS day,
       COUNT(*) AS received,
       COUNT(*) FILTER (WHERE status IN ('approved','published')) AS accepted,
       COUNT(*) FILTER (WHERE status='rejected') AS rejected
FROM submissions
WHERE created_at >= now() - interval '7 days'
GROUP BY 1 ORDER BY 1 DESC;

-- 2. Conversion KPI / Конверсия модерации
SELECT COUNT(*) AS total,
       COUNT(*) FILTER (WHERE status='pending') AS pending,
       ROUND(100.0 * COUNT(*) FILTER (WHERE status IN ('approved','published'))
           / NULLIF(COUNT(*) FILTER (WHERE status<>'pending'),0),1) AS approval_rate
FROM submissions;

-- 3. Format breakdown / Разбивка по форматам
SELECT content_type, COUNT(*) AS total,
       COUNT(*) FILTER (WHERE status IN ('approved','published')) AS accepted
FROM submissions
GROUP BY content_type ORDER BY total DESC;

-- 4. Review SLA / Время обработки
SELECT content_type,
       COUNT(*) FILTER (WHERE reviewed_at IS NOT NULL) AS reviewed,
       ROUND(AVG(EXTRACT(EPOCH FROM reviewed_at-created_at))
         FILTER (WHERE reviewed_at IS NOT NULL)/60.0,1) AS avg_minutes
FROM submissions GROUP BY content_type;

-- 5. Returning contributors / Повторные авторы
WITH author_activity AS (
  SELECT user_id, COUNT(*) AS submissions_count
  FROM submissions GROUP BY user_id
)
SELECT COUNT(*) AS authors,
       COUNT(*) FILTER (WHERE submissions_count > 1) AS returning
FROM author_activity;

-- 6. Weekly activity with window function / Недельная динамика с оконной функцией
WITH weekly AS (
  SELECT date_trunc('week',created_at)::date AS week, COUNT(*) AS total
  FROM submissions GROUP BY 1
)
SELECT week,total,
       LAG(total) OVER (ORDER BY week) AS previous_week,
       total-LAG(total) OVER (ORDER BY week) AS delta
FROM weekly ORDER BY week DESC;

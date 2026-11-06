-- Returning contributors / Повторные авторы
WITH a AS(SELECT user_id,COUNT(*) n FROM submissions GROUP BY user_id)
SELECT COUNT(*) authors,COUNT(*) FILTER(WHERE n=1) one_time,
COUNT(*) FILTER(WHERE n>1) returning,
ROUND(100.0*COUNT(*) FILTER(WHERE n>1)/NULLIF(COUNT(*),0),2) returning_pct FROM a;
-- Cohort retention / Когортное удержание: month 0-3
WITH active AS(
 SELECT DISTINCT user_id,DATE_TRUNC('month',created_at AT TIME ZONE 'Europe/Moscow')::date month FROM submissions
), first_seen AS(
 SELECT user_id,MIN(month) cohort FROM active GROUP BY user_id
), grouped AS(
 SELECT f.cohort,
 (EXTRACT(YEAR FROM a.month)::int-EXTRACT(YEAR FROM f.cohort)::int)*12+
 EXTRACT(MONTH FROM a.month)::int-EXTRACT(MONTH FROM f.cohort)::int age_month,
 COUNT(DISTINCT a.user_id) active_authors
 FROM active a JOIN first_seen f USING(user_id) GROUP BY 1,2
), sizes AS(SELECT cohort,COUNT(*) cohort_size FROM first_seen GROUP BY cohort)
SELECT g.cohort,g.age_month,s.cohort_size,g.active_authors,
ROUND(100.0*g.active_authors/NULLIF(s.cohort_size,0),2) retention_pct
FROM grouped g JOIN sizes s USING(cohort)
WHERE g.age_month BETWEEN 0 AND 3 ORDER BY g.cohort,g.age_month;

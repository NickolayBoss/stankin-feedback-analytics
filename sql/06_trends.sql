-- 30-day calendar + moving average / Календарь и скользящее среднее
WITH calendar AS(
 SELECT GENERATE_SERIES((now() AT TIME ZONE 'Europe/Moscow')::date-29,
 (now() AT TIME ZONE 'Europe/Moscow')::date,interval '1 day')::date day
), daily AS(
 SELECT (created_at AT TIME ZONE 'Europe/Moscow')::date day,COUNT(*) n
 FROM submissions WHERE created_at>=now()-interval '31 days' GROUP BY 1
), filled AS(
 SELECT c.day,COALESCE(d.n,0) received FROM calendar c LEFT JOIN daily d USING(day)
)
SELECT day,received,ROUND(AVG(received) OVER(ORDER BY day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW),2) moving_avg_7d,
SUM(received) OVER(ORDER BY day) cumulative_30d FROM filled ORDER BY day;
-- Week-over-week / Изменение к прошлой неделе
WITH weeks AS(
 SELECT DATE_TRUNC('week',created_at AT TIME ZONE 'Europe/Moscow')::date week,COUNT(*) n FROM submissions GROUP BY 1
), changes AS(SELECT week,n,LAG(n) OVER(ORDER BY week) previous FROM weeks)
SELECT week,n,previous,n-previous delta,
ROUND(100.0*(n-previous)/NULLIF(previous,0),2) wow_pct FROM changes ORDER BY week DESC;

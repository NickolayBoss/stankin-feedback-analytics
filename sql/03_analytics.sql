-- Response SLA denominator: answered tickets only.
CREATE VIEW kpi_overview AS SELECT count(*) total,
count(*) FILTER(WHERE status='resolved') resolved,
round(100.0*count(*) FILTER(WHERE status='resolved')/nullif(count(*),0),2) resolution_pct,
round(100.0*count(*) FILTER(WHERE first_response_at-created_at<=interval '24 hours')/nullif(count(*) FILTER(WHERE first_response_at IS NOT NULL),0),2) answered_within_24h_pct,
round(avg(satisfaction)::numeric,2) csat,
round((percentile_cont(.5) WITHIN GROUP(ORDER BY extract(epoch FROM first_response_at-created_at)/3600) FILTER(WHERE first_response_at IS NOT NULL))::numeric,2) median_response_hours FROM feedback;
CREATE VIEW department_performance AS SELECT d.name,count(f.id) tickets,count(f.id) FILTER(WHERE f.status='resolved') resolved,round(avg(f.satisfaction)::numeric,2) csat FROM departments d LEFT JOIN feedback f ON f.department_id=d.id GROUP BY d.id,d.name;
SELECT * FROM kpi_overview;
SELECT * FROM department_performance ORDER BY tickets DESC;
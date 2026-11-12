-- Synthetic demonstration only. Run once on an empty database.
INSERT INTO departments(name) VALUES ('Engineering'),('IT'),('Student Services');
INSERT INTO feedback(department_id,category,created_at,first_response_at,resolved_at,status,satisfaction)
SELECT 1+g%3,(ARRAY['education','facilities','schedule','digital','other'])[1+g%5],
TIMESTAMPTZ '2026-09-01 09:00+03'+g*INTERVAL '5 hours',
CASE WHEN g%9=0 THEN NULL ELSE TIMESTAMPTZ '2026-09-01 09:00+03'+g*INTERVAL '5 hours'+(g%60+1)*INTERVAL '1 hour' END,
CASE WHEN g%5<3 THEN TIMESTAMPTZ '2026-09-01 09:00+03'+g*INTERVAL '5 hours'+(g%90+2)*INTERVAL '1 hour' END,
CASE WHEN g%5<3 THEN 'resolved' WHEN g%5=3 THEN 'in_progress' ELSE 'new' END,
CASE WHEN g%5<3 THEN 1+g%5 END FROM generate_series(0,499) g;
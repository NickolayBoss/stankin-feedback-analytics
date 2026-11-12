-- Expect zero failures for each check
SELECT 'invalid_response_time' check_name,count(*) failures FROM feedback WHERE first_response_at<created_at
UNION ALL SELECT 'resolved_without_date',count(*) FROM feedback WHERE status='resolved' AND resolved_at IS NULL
UNION ALL SELECT 'missing_department',count(*) FROM feedback f LEFT JOIN departments d ON f.department_id=d.id WHERE d.id IS NULL;
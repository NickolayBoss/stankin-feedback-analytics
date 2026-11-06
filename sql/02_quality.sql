-- Data quality / Качество данных: 0 = no issues / нет проблем
SELECT 'missing_author / Нет автора' check_name,COUNT(*) issues FROM submissions s LEFT JOIN users u ON u.telegram_id=s.user_id WHERE u.telegram_id IS NULL
UNION ALL SELECT 'reviewed_without_time / Нет даты проверки',COUNT(*) FROM submissions WHERE status<>'pending' AND reviewed_at IS NULL
UNION ALL SELECT 'pending_with_review_time / Очередь с датой проверки',COUNT(*) FROM submissions WHERE status='pending' AND reviewed_at IS NOT NULL
UNION ALL SELECT 'published_without_time / Нет даты публикации',COUNT(*) FROM submissions WHERE status='published' AND published_at IS NULL
UNION ALL SELECT 'negative_review_time / Отрицательное время',COUNT(*) FROM submissions WHERE reviewed_at<created_at;
-- Audit completeness / Полнота истории
SELECT s.status,COUNT(*) total,COUNT(*) FILTER(WHERE EXISTS(SELECT 1 FROM moderation_events e WHERE e.submission_id=s.id)) with_audit
FROM submissions s GROUP BY s.status ORDER BY s.status;

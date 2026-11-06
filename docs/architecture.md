# System analysis: requirements and architecture

## Business objective
Measure submission activity, content moderation efficiency, and engagement of the STANKIN Telegram community.

## Actors
- Subscriber: submits content
- Admin: reviews, approves, rejects, publishes, reads SQL reports
- Channel: receives approved posts

## Functional requirements
FR-01: Accept single-message text, photo, video, GIF and document submissions.
FR-02: Persist submission metadata and status in PostgreSQL.
FR-03: Deliver submission to authorized admin's private chat.
FR-04: Only configured ADMIN_ID may moderate and view reports.
FR-05: Record moderation actions for audit.
FR-06: Provide aggregate /stats and daily /report commands.
FR-07: Optionally publish approved messages to configured channel.

## Data model
users (1) -> (N) submissions (1) -> (N) moderation_events

## KPIs
Submission volume; unique contributors; approval conversion (approved + published / reviewed); average review duration; seven-day activity.

## Known limitations
MVP uses polling and one administrator. No album grouping, anonymous replies, spam protection, backup scheduling, dashboard or exactly-once publication. Network failure after posting but before recording publication may lead to duplicate posts on retry. No real user messages should be committed to GitHub.

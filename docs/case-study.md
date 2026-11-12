# Student feedback: SQL analytics case study

**Status:** synthetic portfolio prototype; not an official university service.

## Problem
Moderators need to measure resolution, first-response delays and recurring problems. Department leads need actionable comparisons.

## Stakeholders
Student (feedback submitter), moderator (triage), department lead (performance), analyst (metrics).

## KPI definitions
- Resolution rate = resolved / all feedback.
- Response SLA = answered within 24h / answered feedback. Unanswered tickets are excluded and must be tracked separately in a production SLA.
- CSAT = average rating of rated resolved tickets, 1–5.
- Weekly growth = (current weekly count - previous observed weekly count) / previous observed weekly count. Missing weeks are not filled with zeros.
- Overdue open = unresolved tickets older than 72h as of query time.

## Acceptance criteria
Schema loads in PostgreSQL 15+; 500 synthetic records are inserted; views return department and overall metrics; quality queries report zero violations.

## Limitations
Synthetic data is not representative. No personal information, real Telegram integration, deployed dashboard or automated PostgreSQL tests are included. Future work: moderation event history, consent/privacy, complete SLA cohorts, API and dashboard.
SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
 telegram_id BIGINT PRIMARY KEY,
 username TEXT,
 created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS submissions (
 id BIGSERIAL PRIMARY KEY,
 user_id BIGINT NOT NULL REFERENCES users(telegram_id),
 chat_id BIGINT NOT NULL,
 message_id BIGINT NOT NULL,
 content_type TEXT NOT NULL,
 status TEXT NOT NULL DEFAULT 'pending'
 CHECK(status IN ('pending','approved','rejected','published')),
 created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
 reviewed_at TIMESTAMPTZ,
 published_at TIMESTAMPTZ,
 UNIQUE(chat_id,message_id)
);
CREATE TABLE IF NOT EXISTS moderation_events (
 id BIGSERIAL PRIMARY KEY,
 submission_id BIGINT NOT NULL REFERENCES submissions(id),
 admin_id BIGINT NOT NULL,
 action TEXT NOT NULL,
 created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""

async def init(pool):
    async with pool.acquire() as conn:
        await conn.execute(SCHEMA)

async def insert(pool, user, message):
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                """INSERT INTO users(telegram_id,username) VALUES($1,$2)
                ON CONFLICT(telegram_id) DO UPDATE SET username=EXCLUDED.username""",
                user.id,user.username)
            return await conn.fetchval(
                """INSERT INTO submissions(user_id,chat_id,message_id,content_type)
                VALUES($1,$2,$3,$4)
                ON CONFLICT(chat_id,message_id) DO NOTHING RETURNING id""",
                user.id,message.chat.id,message.message_id,message.content_type)

async def review(pool, sid, admin, action):
    status = {'approve':'approved','reject':'rejected'}[action]
    async with pool.acquire() as conn:
        async with conn.transaction():
            row = await conn.fetchrow(
                """UPDATE submissions SET status=$2,reviewed_at=now()
                WHERE id=$1 AND status='pending' RETURNING *""",sid,status)
            if row:
                await conn.execute(
                    "INSERT INTO moderation_events(submission_id,admin_id,action) VALUES($1,$2,$3)",
                    sid,admin,action)
            return row

async def get(pool,sid):
    return await pool.fetchrow("SELECT * FROM submissions WHERE id=$1",sid)

async def published(pool,sid,admin):
    async with pool.acquire() as conn:
        async with conn.transaction():
            row=await conn.fetchrow(
                """UPDATE submissions SET status='published',published_at=now()
                WHERE id=$1 AND status='approved' RETURNING id""",sid)
            if row:
                await conn.execute(
                    "INSERT INTO moderation_events(submission_id,admin_id,action) VALUES($1,$2,'publish')",sid,admin)
            return row

async def stats(pool):
    return await pool.fetchrow("""
        SELECT count(*) total,
        count(*) FILTER(WHERE status='pending') pending,
        count(*) FILTER(WHERE status='approved') approved,
        count(*) FILTER(WHERE status='rejected') rejected,
        count(*) FILTER(WHERE status='published') published,
        count(DISTINCT user_id) authors,
        round(100.0*count(*) FILTER(WHERE status IN ('approved','published'))
          /nullif(count(*) FILTER(WHERE status<>'pending'),0),1) approval_rate,
        round(avg(extract(epoch FROM reviewed_at-created_at))
          FILTER(WHERE reviewed_at IS NOT NULL)/60.0,1) review_minutes
        FROM submissions
    """)

async def report(pool):
    return await pool.fetch("""
        SELECT created_at::date day,count(*) received,
        count(*) FILTER(WHERE status IN ('approved','published')) accepted
        FROM submissions WHERE created_at >= now()-interval '7 days'
        GROUP BY 1 ORDER BY 1 DESC
    """)

async def my_submissions(pool, user_id, limit=10):
    """Return only the requesting author's submissions / Только свои предложения."""
    return await pool.fetch(
        """SELECT id, status, content_type,
                  (created_at AT TIME ZONE 'Europe/Moscow') AS created_local
           FROM submissions
           WHERE user_id=$1
           ORDER BY created_at DESC, id DESC
           LIMIT $2""",
        user_id, limit)

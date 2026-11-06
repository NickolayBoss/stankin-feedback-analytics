"""SQL-powered administrator reports / SQL-отчёты администратора."""
from datetime import datetime, timezone
from html import escape

def table(headers, rows, widths):
    """Monospaced Telegram-safe table / Моноширинная таблица для Telegram."""
    def cell(value, width):
        value = str(value if value is not None else "—").replace("\n", " ")
        return value[:width].ljust(width)
    lines = [" ".join(cell(h, w) for h, w in zip(headers, widths)),
             " ".join("─" * w for w in widths)]
    lines.extend(" ".join(cell(v, w) for v, w in zip(row, widths)) for row in rows)
    return "<pre>" + escape("\n".join(lines)) + "</pre>"

async def overview(pool):
    s = await pool.fetchrow("""
        SELECT COUNT(*) AS total,
          COUNT(*) FILTER (WHERE status='pending') AS pending,
          COUNT(*) FILTER (WHERE status='approved') AS approved,
          COUNT(*) FILTER (WHERE status='rejected') AS rejected,
          COUNT(*) FILTER (WHERE status='published') AS published,
          COUNT(DISTINCT user_id) AS authors,
          ROUND(100.0*COUNT(*) FILTER (WHERE status IN ('approved','published'))
            /NULLIF(COUNT(*) FILTER (WHERE status<>'pending'),0),1) AS approval_rate,
          ROUND(AVG(EXTRACT(EPOCH FROM reviewed_at-created_at))
            FILTER (WHERE reviewed_at IS NOT NULL)/60.0,1) AS review_minutes
        FROM submissions
    """)
    return (
        "<b>Общая статистика / Overview</b>\n"
        + table(["Метрика / KPI", "Знач."], [
            ("Всего / Total", s["total"]),
            ("В очереди / Pending", s["pending"]),
            ("Одобрено / Approved", s["approved"]),
            ("Отклонено / Rejected", s["rejected"]),
            ("Опубликовано / Published", s["published"]),
            ("Авторов / Authors", s["authors"]),
            ("Одобрение / Approval %", f'{s["approval_rate"] or 0}%'),
            ("Проверка / Review min", s["review_minutes"] or 0),
        ], [25, 8])
        + "\n<i>Одобрение = (одобрено + опубликовано) / обработано.</i>"
    )

async def daily(pool):
    rows = await pool.fetch("""
        SELECT (created_at AT TIME ZONE 'Europe/Moscow')::date AS day,
          COUNT(*) AS received,
          COUNT(*) FILTER (WHERE status IN ('approved','published')) AS accepted,
          COUNT(*) FILTER (WHERE status='rejected') AS rejected
        FROM submissions
        WHERE created_at >= now() - interval '7 days'
        GROUP BY 1 ORDER BY 1 DESC
    """)
    return "<b>По дням / Daily (7 дней, МСК)</b>\n" + table(
        ["Дата", "Всего", "Одобр.", "Откл."],
        [(r["day"].strftime("%d.%m"),r["received"],r["accepted"],r["rejected"]) for r in rows],
        [7, 6, 7, 6]) if rows else "<b>По дням / Daily</b>\nПока нет данных за 7 дней."

async def formats(pool):
    rows = await pool.fetch("""
        SELECT content_type, COUNT(*) AS total,
          COUNT(*) FILTER (WHERE status IN ('approved','published')) AS accepted
        FROM submissions GROUP BY content_type ORDER BY total DESC, content_type
    """)
    names = {"text":"Текст","photo":"Фото","video":"Видео","document":"Файл","animation":"GIF"}
    return "<b>Форматы / Content types</b>\n" + table(
        ["Тип / Type","Всего","Одобр."],
        [(names.get(r["content_type"],r["content_type"]),r["total"],r["accepted"]) for r in rows],
        [14,6,7]) if rows else "<b>Форматы / Content types</b>\nПока нет данных."

async def moderation(pool):
    rows = await pool.fetch("""
        SELECT content_type,
          COUNT(*) FILTER (WHERE reviewed_at IS NOT NULL) AS reviewed,
          ROUND(AVG(EXTRACT(EPOCH FROM reviewed_at-created_at))
            FILTER (WHERE reviewed_at IS NOT NULL)/60.0,1) AS avg_minutes
        FROM submissions GROUP BY content_type ORDER BY reviewed DESC,content_type
    """)
    return "<b>Модерация / Moderation</b>\n" + table(
        ["Тип / Type","Провер.","Мин. ср."],
        [(r["content_type"],r["reviewed"],r["avg_minutes"] if r["avg_minutes"] is not None else "—") for r in rows],
        [13,7,8]) if rows else "<b>Модерация / Moderation</b>\nПока нет данных."

async def authors(pool):
    s = await pool.fetchrow("""
        SELECT COUNT(*) AS authors,
          COUNT(*) FILTER (WHERE submissions_count > 1) AS returning
        FROM (SELECT user_id,COUNT(*) AS submissions_count
              FROM submissions GROUP BY user_id) x
    """)
    return (
        "<b>Авторы / Contributors</b>\n"
        + table(["Метрика / KPI","Знач."], [
            ("Уникальных / Unique",s["authors"]),
            ("Повторных / Returning",s["returning"]),
        ], [23,8])
        + "\n<i>Повторный автор = отправил более одного предложения.</i>"
    )

async def full_report(pool):
    sections = [await overview(pool), await daily(pool), await formats(pool),
                await moderation(pool), await authors(pool)]
    return sections

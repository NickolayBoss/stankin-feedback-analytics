"""STANKIN Telegram bot / Telegram-бот для предложений и SQL-аналитики."""
import asyncio
import logging
import os

import asyncpg
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from dotenv import load_dotenv

from app import db, reports
from html import escape

load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])
DATABASE_URL = os.environ["DATABASE_URL"]
CHANNEL_ID = os.getenv("CHANNEL_ID", "").strip()
dp = Dispatcher()
pool = None

HELP = (
    "<b>Панель администратора / Admin panel</b>\n"
    "/stats — общая статистика / Overview\n"
    "/report — полный отчёт / Full report\n"
    "/daily — по дням / Daily\n"
    "/formats — форматы / Content types\n"
    "/moderation — модерация / Moderation\n"
    "/authors — авторы / Contributors\n"
    "/help — справка / Help"
)

STATUS = {
    "pending": "На проверке / Pending",
    "approved": "Одобрено / Approved",
    "rejected": "Отклонено / Rejected",
    "published": "Опубликовано / Published",
}

async def notify_author(bot, row, sid, status):
    """Best-effort status notification / Уведомление без влияния на модерацию."""
    try:
        await bot.send_message(
            row["user_id"],
            f"Статус предложения #{sid} изменён / Submission status updated:\\n"
            f"{STATUS[status]}".replace("\\\\n", "\\n"))
    except Exception:
        logging.exception("Unable to notify author for submission %s", sid)

def keyboard(sid, approved=False):
    if approved:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Опубликовать / Publish", callback_data=f"publish:{sid}")]
        ])
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Одобрить / Approve", callback_data=f"approve:{sid}"),
        InlineKeyboardButton(text="Отклонить / Reject", callback_data=f"reject:{sid}")
    ]])

def is_admin(m):
    return m.chat.type == "private" and m.from_user and m.from_user.id == ADMIN_ID

async def send_report(m, text):
    await m.answer(text, parse_mode=ParseMode.HTML)

@dp.message(CommandStart())
async def start(m: Message):
    if m.chat.type != "private":
        return
    if is_admin(m):
        await send_report(m, HELP)
    else:
        await m.answer("Предложка «Опорники СТАНКА».\n"
                       "Отправьте текст, фото, видео, GIF или документ.\n"
                       "Submit a text, photo, video, GIF or document.\n"\n                       "/my — мои предложения / My submissions.")

@dp.message(Command("help"))
async def help_command(m: Message):
    if is_admin(m):
        await send_report(m, HELP)

@dp.message(Command("my"))
async def my_command(m: Message):
    if m.chat.type != "private" or not m.from_user:
        return
    rows = await db.my_submissions(pool, m.from_user.id)
    if not rows:
        await m.answer("У вас пока нет предложений. / No submissions yet.")
        return
    lines = ["<b>Мои предложения / My submissions</b>",
             "<i>Последние 10 / Latest 10</i>"]
    for r in rows:
        date = r["created_local"].strftime("%d.%m.%Y %H:%M")
        lines.append(f"#{r['id']} · {escape(r['content_type'])} · {date} МСК\\n"
                     f"{STATUS.get(r['status'], escape(r['status']))}")
    await send_report(m, "\\n\\n".join(lines).replace("\\\\n", "\\n"))

@dp.message(Command("stats"))
async def stats_command(m: Message):
    if is_admin(m):
        await send_report(m, await reports.overview(pool))

@dp.message(Command("daily"))
async def daily_command(m: Message):
    if is_admin(m):
        await send_report(m, await reports.daily(pool))

@dp.message(Command("formats"))
async def formats_command(m: Message):
    if is_admin(m):
        await send_report(m, await reports.formats(pool))

@dp.message(Command("moderation"))
async def moderation_command(m: Message):
    if is_admin(m):
        await send_report(m, await reports.moderation(pool))

@dp.message(Command("authors"))
async def authors_command(m: Message):
    if is_admin(m):
        await send_report(m, await reports.authors(pool))

@dp.message(Command("report"))
async def report_command(m: Message):
    if is_admin(m):
        for section in await reports.full_report(pool):
            await send_report(m, section)

@dp.callback_query(F.data.regexp(r"^(approve|reject|publish):[0-9]+$"))
async def moderate(c: CallbackQuery, bot: Bot):
    if c.from_user.id != ADMIN_ID or not c.message:
        await c.answer("Нет доступа / Unauthorized", show_alert=True)
        return
    action, value = c.data.split(":")
    sid = int(value)
    if action == "publish":
        if not CHANNEL_ID:
            await c.answer("CHANNEL_ID не настроен / Not configured", show_alert=True)
            return
        item = await db.get(pool, sid)
        if not item or item["status"] != "approved":
            await c.answer("Сначала одобрите / Approve first", show_alert=True)
            return
        try:
            await bot.copy_message(CHANNEL_ID, item["chat_id"], item["message_id"])
        except Exception:
            logging.exception("Publishing failed")
            await c.answer("Ошибка публикации / Publishing error", show_alert=True)
            return
        await db.published(pool, sid, ADMIN_ID)
        await c.message.edit_reply_markup(reply_markup=None)
        await notify_author(bot, item, sid, "published")
        await c.answer("Опубликовано / Published")
        return
    row = await db.review(pool, sid, ADMIN_ID, action)
    if not row:
        await c.answer("Уже обработано / Already reviewed", show_alert=True)
        return
    await c.message.edit_reply_markup(
        reply_markup=keyboard(sid, True) if action == "approve" else None)
    await notify_author(bot, row, sid, row["status"])
    await c.answer("Готово / Done")

@dp.message(F.chat.type == "private")
async def incoming(m: Message, bot: Bot):
    if is_admin(m):
        await send_report(m, HELP)
        return
    if not m.from_user:
        return
    if m.content_type not in ("text", "photo", "video", "document", "animation"):
        await m.answer("Поддерживаются текст, фото, видео, GIF и файлы. / Unsupported format.")
        return
    sid = await db.insert(pool, m.from_user, m)
    if sid is None:
        return
    try:
        await bot.send_message(ADMIN_ID, f"Новое предложение / New submission #{sid} · {m.content_type}")
        await bot.copy_message(ADMIN_ID, m.chat.id, m.message_id, reply_markup=keyboard(sid))
    except Exception:
        logging.exception("Admin notification failed")
        await m.answer("Сообщение сохранено, уведомление временно недоступно. / Saved; notification unavailable.")
        return
    await m.answer(f"Предложение #{sid} получено! / Submission received!\\n"
                   "Проверить статус: /my".replace("\\\\n", "\\n"))

async def main():
    global pool
    logging.basicConfig(level=logging.INFO)
    pool = await asyncpg.create_pool(DATABASE_URL)
    await db.init(pool)
    bot = Bot(BOT_TOKEN)
    try:
        await dp.start_polling(bot)
    finally:
        await pool.close()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())

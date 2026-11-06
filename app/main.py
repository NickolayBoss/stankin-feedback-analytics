import asyncio
import logging
import os

import asyncpg
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from app import db

load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]
ADMIN_ID = int(os.environ["ADMIN_ID"])
DATABASE_URL = os.environ["DATABASE_URL"]
CHANNEL_ID = os.getenv("CHANNEL_ID", "").strip()
dp = Dispatcher()
pool = None

def keyboard(sid, approved=False):
    if approved:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Опубликовать",callback_data=f"publish:{sid}")]
        ])
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Одобрить",callback_data=f"approve:{sid}"),
         InlineKeyboardButton(text="Отклонить",callback_data=f"reject:{sid}")]
    ])

@dp.message(CommandStart())
async def start(m: Message):
    if m.chat.type != "private": return
    if m.from_user.id == ADMIN_ID:
        await m.answer("Панель администратора. Команды: /stats, /report")
    else:
        await m.answer("Предложка «Опорники СТАНКА». Пришлите текст, фото, видео или файл.")

@dp.message(Command("stats"))
async def stats(m: Message):
    if m.chat.type != "private" or m.from_user.id != ADMIN_ID: return
    s = await db.stats(pool)
    await m.answer(
        f"SQL-отчёт\nВсего: {s['total']}\nОжидают: {s['pending']}\n"
        f"Одобрено: {s['approved']}\nОтклонено: {s['rejected']}\n"
        f"Опубликовано: {s['published']}\nАвторов: {s['authors']}\n"
        f"Доля одобрений: {s['approval_rate'] or 0}%\n"
        f"Среднее время проверки: {s['review_minutes'] or 0} мин")

@dp.message(Command("report"))
async def report(m: Message):
    if m.chat.type != "private" or m.from_user.id != ADMIN_ID: return
    rows = await db.report(pool)
    await m.answer("\n".join(["Последние 7 дней: получено / принято"] +
        [f"{r['day']}: {r['received']} / {r['accepted']}" for r in rows]))

@dp.callback_query(F.data.regexp(r"^(approve|reject|publish):[0-9]+$"))
async def moderate(c: CallbackQuery, bot: Bot):
    if c.from_user.id != ADMIN_ID:
        await c.answer("Нет доступа",show_alert=True)
        return
    action, value = c.data.split(":")
    sid = int(value)
    if action == "publish":
        if not CHANNEL_ID:
            await c.answer("CHANNEL_ID не настроен",show_alert=True)
            return
        item = await db.get(pool,sid)
        if not item or item["status"] != "approved":
            await c.answer("Сначала одобрите или запись уже обработана",show_alert=True)
            return
        try:
            await bot.copy_message(CHANNEL_ID,item["chat_id"],item["message_id"])
        except Exception:
            logging.exception("Publish failed")
            await c.answer("Ошибка публикации",show_alert=True)
            return
        await db.published(pool,sid,ADMIN_ID)
        await c.message.edit_reply_markup(reply_markup=None)
        await c.answer("Опубликовано")
        return
    row = await db.review(pool,sid,ADMIN_ID,action)
    if not row:
        await c.answer("Уже обработано",show_alert=True)
        return
    await c.message.edit_reply_markup(reply_markup=keyboard(sid,True) if action=="approve" else None)
    await c.answer("Готово")

@dp.message(F.chat.type == "private")
async def incoming(m: Message, bot: Bot):
    if m.from_user.id == ADMIN_ID:
        await m.answer("Команды администратора: /stats, /report")
        return
    if m.content_type not in ("text","photo","video","document","animation"):
        await m.answer("Отправьте текст, фото, видео, GIF или документ.")
        return
    sid = await db.insert(pool,m.from_user,m)
    if sid is None: return
    try:
        await bot.send_message(ADMIN_ID,f"Новое предложение #{sid} · {m.content_type}")
        await bot.copy_message(ADMIN_ID,m.chat.id,m.message_id,reply_markup=keyboard(sid))
    except Exception:
        logging.exception("Admin notification failed")
        await m.answer("Сообщение сохранено, но уведомление пока недоступно.")
        return
    await m.answer("Предложение получено!")

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

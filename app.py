import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import feedparser
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Ganti dengan token bot Telegram kamu (dari BotFather)
TOKEN = 'YOUR_BOT_TOKEN_HERE'
# Ganti dengan chat ID grup/channel (bisa pakai @getidsbot untuk cek)
CHAT_ID = 'YOUR_CHAT_ID_HERE'
# RSS feed contoh dari ANN
RSS_URL = 'https://www.animenewsnetwork.com/news/rss.xml'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Bot RSS aktif! Cek update ANN.')

async def check_rss(context: ContextTypes.DEFAULT_TYPE):
    feed = feedparser.parse(RSS_URL)
    # Ambil entry terbaru (contoh: post judul dan link)
    if feed.entries:
        entry = feed.entries[0]  # Entry pertama (terbaru)
        message = f"Update Baru: {entry.title}\n{entry.link}"
        await context.bot.send_message(chat_id=CHAT_ID, text=message)
    else:
        logger.info("No new entries.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_rss, trigger=IntervalTrigger(hours=1), args=[app])
    scheduler.start()

    app.run_polling()  # Pakai polling dulu buat testing; nanti ganti webhook untuk Render

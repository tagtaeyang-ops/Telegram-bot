import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime, timedelta

TOKEN = os.getenv("TOKEN")

# 👉 테스트용 데이터
schedule = {
    "2026-04-03": "수영장: 박준수(A), 정상진(S)\n안내: 박수정(E)",
    "2026-04-04": "수영장: 탁태양(C)\n안내: 박선영(A)"
}

# /오늘
async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today_date = datetime.now().strftime("%Y-%m-%d")
    text = schedule.get(today_date, "오늘 스케줄 없음")
    await update.message.reply_text(f"📅 오늘\n{text}")

# /내일
async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    text = schedule.get(tomorrow_date, "내일 스케줄 없음")
    await update.message.reply_text(f"📅 내일\n{text}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("today", today))
app.add_handler(CommandHandler("tomorrow", tomorrow))

print("봇 실행 중...")

app.run_polling()
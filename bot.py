import requests
import schedule
import time
from datetime import datetime, timedelta
import os
import threading
import pytz

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =========================
# 🔐 환경변수
# =========================
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# 🇰🇷 한국 시간 설정
# =========================
KST = pytz.timezone("Asia/Seoul")

# =========================
# 📅 스케줄 데이터
# =========================
schedule_data = {
    3: {
        1:"A", 2:"A", 3:"/", 4:"S", 5:"A", 6:"A", 7:"B",
        8:"A", 9:"/", 10:"/", 11:"A", 12:"A", 13:"A", 14:"A",
        15:"/", 16:"S", 17:"C", 18:"A", 19:"#", 20:"#", 21:"D",
        22:"D", 23:"S", 24:"A", 25:"/", 26:"/", 27:"S", 28:"S",
        29:"B", 30:"/", 31:"/"
    },
    4: {
    1:"C", 2:"A", 3:"#", 4:"S", 5:"D", 6:"C", 7:"C",
    8:"/", 9:"/", 10:"S", 11:"D", 12:"B", 13:"A", 14:"/",
    15:"/", 16:"S", 17:"D", 18:"A", 19:"#", 20:"/",
    21:"S", 22:"/", 23:"S", 24:"B", 25:"B", 26:"A",
    27:"A", 28:"/", 29:"/", 30:"A"
}
}

# =========================
# 📩 메시지 전송
# =========================
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

# =========================
# 📊 근무 조회
# =========================
def get_work(month, day):
    return schedule_data.get(month, {}).get(day, "정보없음")

# =========================
# 📝 메시지 포맷
# =========================
def make_msg(month, day, work, title):
    if work == "/":
        return f"📅 {title}({month}/{day})\n👉 휴무 😎"
    elif work == "#":
        return f"📅 {title}({month}/{day})\n👉 특수 일정(#)"
    else:
        return f"📅 {title}({month}/{day})\n👉 근무: {work}"

# =========================
# 🔔 자동 알림 (한국 기준)
# =========================
def send_tomorrow_schedule():
    now = datetime.now(KST)
    tomorrow = now + timedelta(days=1)

    work = get_work(tomorrow.month, tomorrow.day)
    msg = make_msg(tomorrow.month, tomorrow.day, work, "내일")

    send_message(msg)

# =========================
# 🤖 텔레그램 명령어
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 근무 봇\n\n"
        "/today - 오늘 근무\n"
        "/tomorrow - 내일 근무"
    )

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(KST)

    work = get_work(now.month, now.day)
    msg = make_msg(now.month, now.day, work, "오늘")

    await update.message.reply_text(msg)

async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tomorrow = datetime.now(KST) + timedelta(days=1)

    work = get_work(tomorrow.month, tomorrow.day)
    msg = make_msg(tomorrow.month, tomorrow.day, work, "내일")

    await update.message.reply_text(msg)

# =========================
# ⏰ 스케줄러 (한국 21시 정확히)
# =========================
def run_scheduler():
    send_message("✅ 봇 정상 작동 확인!")

    while True:
        now = datetime.now(KST)

        # 👉 한국시간 21:00에 실행
        if now.hour == 21 and now.minute == 0:
            send_tomorrow_schedule()
            time.sleep(60)  # 중복 방지

        time.sleep(1)

# 스케줄러 실행 (백그라운드)
threading.Thread(target=run_scheduler, daemon=True).start()

# =========================
# 🚀 봇 실행
# =========================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("today", today))
app.add_handler(CommandHandler("tomorrow", tomorrow))

print("봇 실행 중...")

app.run_polling()
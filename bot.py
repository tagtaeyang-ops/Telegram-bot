import requests
import schedule
import time
from datetime import datetime, timedelta
import os
import threading

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 환경변수
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("TOKEN:", TOKEN)
print("CHAT_ID:", CHAT_ID)

# 👉 스케줄 데이터
schedule_data = {
    3: {
        1:"A", 2:"A", 3:"/", 4:"S", 5:"A", 6:"A", 7:"B",
        8:"A", 9:"/", 10:"/", 11:"A", 12:"A", 13:"A", 14:"A",
        15:"/", 16:"S", 17:"C", 18:"A", 19:"#", 20:"#", 21:"D",
        22:"D", 23:"S", 24:"A", 25:"/", 26:"/", 27:"S", 28:"S",
        29:"B", 30:"/", 31:"/"
    },
    4: {
        1:"C", 2:"A", 3:"#", 4:"S", 5:"D", 6:"C", 7:"A",
        8:"/", 9:"/", 10:"D", 11:"D", 12:"B", 13:"A", 14:"A",
        15:"/", 16:"S", 17:"S", 18:"B", 19:"#", 20:"S", 21:"S",
        22:"/", 23:"/", 24:"D", 25:"B", 26:"A", 27:"/",
        28:"S", 29:"/", 30:"/"
    }
}

# 📤 메시지 보내기
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

# 📅 근무 가져오기
def get_work(month, day):
    return schedule_data.get(month, {}).get(day, "정보없음")

# 📆 메시지 만들기
def make_msg(month, day, work, title):
    if work == "/":
        return f"📅 {title}({month}/{day})\n👉 휴무 😎"
    elif work == "#":
        return f"📅 {title}({month}/{day})\n👉 특수 일정(#)"
    else:
        return f"📅 {title}({month}/{day})\n👉 근무: {work}"

# 🔔 내일 자동 알림
def send_tomorrow_schedule():
    tomorrow = datetime.now() + timedelta(days=1)
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
    now = datetime.now()
    work = get_work(now.month, now.day)
    msg = make_msg(now.month, now.day, work, "오늘")
    await update.message.reply_text(msg)

async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tomorrow = datetime.now() + timedelta(days=1)
    work = get_work(tomorrow.month, tomorrow.day)
    msg = make_msg(tomorrow.month, tomorrow.day, work, "내일")
    await update.message.reply_text(msg)

# =========================
# ⏰ 스케줄러 (백그라운드)
# =========================

def run_scheduler():
    send_message("✅ 봇 정상 작동 확인!")

    # 테스트용 (1분마다)
    schedule.every(1).minutes.do(send_tomorrow_schedule)

    while True:
        schedule.run_pending()
        time.sleep(1)

# 👉 스케줄러 먼저 실행 (백그라운드)
threading.Thread(target=run_scheduler, daemon=True).start()

# =========================
# 🚀 봇 실행 (메인)
# =========================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("today", today))
app.add_handler(CommandHandler("tomorrow", tomorrow))

print("봇 실행 중...")

app.run_polling() 
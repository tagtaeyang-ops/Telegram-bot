import requests
import schedule
import time
from datetime import datetime, timedelta
import os

# 환경변수
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("TOKEN:", TOKEN)
print("CHAT_ID:", CHAT_ID)

# 스케줄 데이터 (3월 + 4월)
schedule_data = {
    3: {
        1:"A", 2:"A", 3:"/", 4:"S", 5:"A", 6:"A", 7:"B",
        8:"A", 9:"/", 10:"/", 11:"A", 12:"A", 13:"A", 14:"A",
        15:"/", 16:"S", 17:"C", 18:"A", 19:"#", 20:"#", 21:"D",
        22:"S", 23:"A", 24:"/", 25:"/", 26:"S", 27:"S", 28:"B",
        29:"/", 30:"/", 31:"/"
    },

    4: {
        1:"C", 2:"A", 3:"#", 4:"S", 5:"D", 6:"C", 7:"A",
        8:"/", 9:"/", 10:"D", 11:"D", 12:"B", 13:"A", 14:"A",
        15:"/", 16:"S", 17:"S", 18:"B", 19:"#", 20:"S", 21:"S",
        22:"/", 23:"/", 24:"D", 25:"B", 26:"A", 27:"/",
        28:"S", 29:"/", 30:"/"
    }
}

# 메시지 보내기 함수
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

# 내일 스케줄 보내기
def send_tomorrow_schedule():
    tomorrow = datetime.now() + timedelta(days=1)

    month = tomorrow.month
    day = tomorrow.day

    work = schedule_data.get(month, {}).get(day, "정보없음")

    if work == "/":
        msg = f"📅 내일({month}/{day})은 휴무입니다 😎"
    elif work == "#":
        msg = f"📅 내일({month}/{day})은 특수 일정(#)입니다"
    else:
        msg = f"📅 내일({month}/{day}) 근무: {work}"

    send_message(msg)

# 테스트 메시지 (서버 켜질 때 1번)
send_message("✅ 봇 정상 작동 확인!")

# 매일 밤 9시 실행
schedule.every().day.at("21:00").do(send_tomorrow_schedule)

# 계속 실행
while True:
    schedule.run_pending()
    time.sleep(1)
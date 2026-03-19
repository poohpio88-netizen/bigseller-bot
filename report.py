import requests
import os
from datetime import datetime

BIGSELLER_COOKIES = os.environ.get('BIGSELLER_COOKIES', '')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')

def get_order_count():
    url = "https://www.bigseller.com/api/v1/order/getOrderStatusCount.json"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Referer": "https://www.bigseller.com/web/order/index.htm?status=new",
        "Cookie": BIGSELLER_COOKIES
    }
    try:
        response = requests.post(url, headers=headers, json={}, timeout=30)
        data = response.json()
        if data.get('code') == 0:
            status_map = data['data']['statusCountMap']
            return {
                'new': status_map.get('new', 0),
                'pickup': status_map.get('pickup', 0),
                'shipped': status_map.get('shipped', 0),
                'unpaid': status_map.get('unpaid', 0),
                'processing': status_map.get('processing', 0),
            }
    except Exception as e:
        print(f"Error: {e}")
    return None

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload, timeout=10)
    print(f"Telegram: {response.status_code}")

def main():
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    counts = get_order_count()

    if counts:
        msg = (
            f"<b>BAO CAO DON HANG BIGSELLER</b>\n"
            f"Ngay {now}\n\n"
            f"<b>CHO XU LY:</b> {counts['new']} don\n"
            f"<b>CHO LAY HANG:</b> {counts['pickup']} don\n"
            f"<b>DANG GIAO HANG:</b> {counts['shipped']} don\n"
            f"<b>CHUA THANH TOAN:</b> {counts['unpaid']} don\n"
            f"<b>DANG XU LY:</b> {counts['processing']} don"
        )
    else:
        msg = f"Khong lay duoc du lieu BigSeller luc {now}. Vui long cap nhat cookie."

    send_telegram(msg)
    print(msg)

if __name__ == "__main__":
    main()

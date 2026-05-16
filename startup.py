import requests
import socket
import subprocess
import time
import random
import pigpio
from datetime import datetime
import pytz

TOKEN = "TELEGRAM_BOT_TOKEN"
CHAT_ID = "CHAT_ID"
PIN = 18
pi = pigpio.pi()
VOLUME = 15000

def play_gameboy():
    print("STARTUP -gameboy-")
    if not pi.connected:
        return

    notes = [
        (523, 0.08),
        (659, 0.08),
        (784, 0.08),
        (1046, 0.15)
    ]

    for freq, dur in notes:
        pi.hardware_PWM(PIN, freq, VOLUME)
        time.sleep(dur)

    pi.hardware_PWM(PIN, 0, 0)

def get_local_ip():
    print("Getting local IP...")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 1))
        ip = s.getsockname()[0]
        s.close()
        return ip

    except Exception:
        return "Unable to get local IP."


def get_public_ip():
    print("Getting public IP...")
    for _ in range(3):
        try:
            return requests.get(
                "https://api.ipify.org",
                timeout=10
            ).text

        except Exception:
            time.sleep(5)

    return "Unable to get public IP. (Timeout)"


def get_wifi_ssid():
    print("Getting WiFi SSID...")
    try:
        ssid = subprocess.check_output(
            ["iwgetid", "-r"]
        ).decode("utf-8").strip()

        return ssid if ssid else "Ethernet"

    except Exception:
        return "Unknown."


def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        requests.post(
            url,
            data=payload,
            timeout=10
        )

    except Exception as e:
        print(f"Error while sending startup to Telegram: {e}")

def check_internet():
    print("Checking internet connection...")
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

try:
    retries = 0
    connected = False
    print("Waiting for connection...")
    
    while retries < 30:
        if check_internet():
            connected = True
            print("Connected!")
            break
        retries += 1
        time.sleep(1)

    tz_ar = pytz.timezone("America/Argentina/Buenos_Aires")
    now = datetime.now(tz_ar)
    exact_time = now.strftime("%H:%M:%S")

    message = (
        f"```\n"
        f"  ______      _            \n"
        f" /_  __/___ _(_)___  __  __\n"
        f"  / / / __ `/ / __ \\/ / / /\n"
        f" / / / /_/ / / / / / /_/ / \n"
        f"/_/  \\__,_/_/_/ /_/\\__, /  \n"
        f"                  /____/   \n"
        f"\n"
        f"Welcome to Tainy! - \"Small but Dangerous.\"\n"
        f"```\n\n"
        f"🚀 *Raspberry Pi / Tainy Started!*\n\n"
        f"📍 *Local IP:* `{get_local_ip()}`\n"
        f"🌐 *Public IP:* `{get_public_ip()}`\n"
        f"📶 *WiFi:* `{get_wifi_ssid()}`\n"
        f"⏰ *Started at:* {exact_time}"
    )

    send_telegram_msg(message)
    if pi.connected:
        play_gameboy()

except KeyboardInterrupt:
    pass

finally:
    pi.stop()
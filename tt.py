import subprocess
import time
import random
import os
import requests
import socket
def get_ipv4_address():
    try:
        # Kết nối tới một địa chỉ ngoài (Google DNS) để lấy IP cục bộ
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return f"Lỗi: {e}"
# Webhook URLs

webhook_luot = "https://discord.com/api/webhooks/1368179478823571466/w3OImK7m5ue6pq4MppLetGgH7H35d9CDb8Xf0_JH1aO3wkHQasaHY8GNQbN8RhISr4Sn"
webhook_like = "https://discord.com/api/webhooks/1368179852603035658/9vPe8sbE1S0GQJpTPluaKKP9CXvJTBnQ_BwZkkKQlfVNON_iuxCHcyk0syyW8v--OLEw"
webhook_follow = "https://discord.com/api/webhooks/1368179736156835870/gS1nTqZluXiAHS2a88lLCAl3eAeboBJQ1GuqDtUtzUk-ccVan77JbYfUqqa2BHRxu-wx"

# Biến đếm
demvideo = 0
demtym = 0
demfolow = 0
def send_webhook(webhook_url, message):
    """Gửi thông báo lên Discord qua webhook"""
    data = {
        "content": message
    }
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code != 204:
            print(f"❌ Gửi webhook thất bại: {response.status_code}")
    except Exception as e:
        print(f"❌ Lỗi gửi webhook: {e}")
def run(cmd, device=None):
    """Chạy lệnh adb"""
    if device:
        cmd = f'adb -s {device} {cmd}'
    subprocess.run(cmd, shell=True)
def get_connected_devices():
    """Lấy danh sách thiết bị đã kết nối"""
    result = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
    devices = []
    for line in result.stdout.splitlines():
        if "\tdevice" in line:
            devices.append(line.split("\t")[0])
    return devices
def open_tiktok(device):
    """Mở TikTok"""
    run("shell monkey -p com.ss.android.ugc.trill -c android.intent.category.LAUNCHER 1", device)
    time.sleep(5)
def swipe_up(device):
    """Vuốt lên để lướt video"""
    global demvideo
    run("shell input swipe 365 1320 365 500 bb3300", device)
    demvideo += 1
    msg = f"[{device}] 📹 Đã lướt video thứ: {demvideo}"
    print(msg)
    send_webhook(webhook_luot, msg)
    time.sleep(random.randint(4, 7))
def tap_like(device):
    """Thả tym"""
    global demtym
    run("shell input tap 675 1030", device)
    demtym += 1
    msg = f"[{device}] ❤️ Đã tym: {demtym}"
    print(msg)
    send_webhook(webhook_like, msg)
def tap_follow(device):
    """Follow user"""
    global demfolow
    run("shell input tap 675 950", device)
    demfolow += 1
    msg = f"[{device}] 👤 Đã follow: {demfolow}"
    print(msg)
    send_webhook(webhook_follow, msg)
def auto_tiktok(devices):
    """Chạy auto TikTok"""
    print("🚀 Bắt đầu thao tác TikTok trên các thiết bị...")
    time_start = time.time()
    for device in devices:
        open_tiktok(device)
    while True:
        time.sleep(20)
        for device in devices:
            for i in range(1, 6):

                if random.randint(1, 2) == 1:
                    swipe_up(device)
                    break
            if random.randint(1, 8) == 7:
                tap_like(device)
            if random.randint(1, 13) == 9:
                tap_follow(device)
        if (time.time() - time_start) % 300 == 0:
            for device in devices:
                open_tiktok(device)
def auto_adb(ipv4):
    try:
        os.system("adb tcpip 5555")
        st="adb connect " + str(ipv4)+":5555"
        os.system(st)
    except:
        print("ERROR IN AUTO CONNECT ADB")
        return
def main():
    os.system("clear")
    auto_adb(get_ipv4_address())
    print("🔧 Tool Auto TikTok\n")
    devices = get_connected_devices()
    if not devices:
        print("❌ Không có thiết bị nào kết nối qua ADB!")
        return
    print(f"🔌 Thiết bị đã kết nối: {devices}")
    auto_tiktok(devices)
if __name__ == "__main__":
    main()

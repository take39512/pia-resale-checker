import requests
import hashlib
import os

# =====================
# 設定ここだけ触ればOK
# =====================

URL = "https://t.pia.jp/pia/artist/artists.do?artistsCd=2610456"
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# =====================
# ページ取得
# =====================

def get_page_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.text

# =====================
# ハッシュで変化検知
# =====================

def get_hash(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()

# =====================
# Discord通知
# =====================

def send_discord(message):
    data = {
        "content": message
    }
    requests.post(DISCORD_WEBHOOK_URL, json=data)

# =====================
# メイン処理
# =====================

def main():
    html = get_page_content(URL)
    current_hash = get_hash(html)

    # 前回の状態を保存（GitHub上のファイル）
    try:
        with open("last_hash.txt", "r") as f:
            old_hash = f.read().strip()
    except FileNotFoundError:
        old_hash = ""

    # 初回は保存だけして終わり
    if old_hash == "":
        with open("last_hash.txt", "w") as f:
            f.write(current_hash)
        send_discord("監視開始したよ👀（初回状態保存）")
        return

    # 変化あり
    if current_hash != old_hash:
        send_discord("🔥チケットページに変化あり！リセール出てる可能性ある！")
        with open("last_hash.txt", "w") as f:
            f.write(current_hash)
    else:
        print("変化なし")

if __name__ == "__main__":
    main()

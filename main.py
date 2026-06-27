import requests
import os

# =====================
# 設定
# =====================

URL = "https://cloak.pia.jp/resale/item/list?eventCd=2610456"
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

    # エラーページ除外 + リセール出現チェック
    if "アクセス集中" in html:
        print("アクセス集中ページだったのでスキップ")
        return

    if "ありません" not in html:
        send_discord("🔥リセール or 表示変化あり！要確認")
    else:
        print("リセールなし")

if __name__ == "__main__":
    main()

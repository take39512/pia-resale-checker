import os
import requests

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
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    return response.text


# =====================
# Discord通知
# =====================

def send_discord(message):
    data = {
        "content": message
    }

    requests.post(DISCORD_WEBHOOK_URL, json=data, timeout=20)


# =====================
# メイン処理
# =====================

def main():
    try:
        html = get_page_content(URL)

        # アクセス制限ページなら何もしない
        if "アクセス集中" in html:
            print("アクセス集中のためスキップ")
            return

        # リセールなし
        if "出品されたリセールチケットはありません" in html:
            print("リセールなし")
            return

        # 上の文字が無ければ通知
        send_discord("🚨 リセールが出品された可能性があります！\nhttps://cloak.pia.jp/resale/item/list?eventCd=2610456")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()

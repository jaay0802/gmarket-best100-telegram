# PC에서 1회 실행해 Telegram Chat ID 확인 (Python 기본 기능만 사용)
import json
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

token = input("새 Telegram 봇 토큰을 입력하세요 (이 대화에 붙여넣지 마세요): ").strip()
if not token:
    raise SystemExit("토큰이 없습니다.")

try:
    with urlopen(f"https://api.telegram.org/bot{token}/getUpdates", timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))
except (HTTPError, URLError) as exc:
    raise SystemExit(f"Telegram API 접속 오류: {exc}")

if not data.get("ok"):
    raise SystemExit("Telegram API 오류. 토큰을 확인하세요.")

chats = {}
for update in data.get("result", []):
    msg = update.get("message") or update.get("edited_message")
    if msg and msg.get("chat", {}).get("type") == "private":
        chats[msg["chat"]["id"]] = msg["chat"].get("first_name", "private chat")

if not chats:
    print("Chat ID를 찾지 못했습니다. 텔레그램에서 봇에게 /start를 보낸 뒤 다시 실행하세요.")
else:
    print("발견된 개인 Chat ID:")
    for chat_id, first_name in chats.items():
        print(f"{first_name}: {chat_id}")
    print("이 숫자를 GitHub Secret TELEGRAM_CHAT_ID에 저장하세요.")

import requests


async def notify(client, message: str, bot_token: str, dest_chat_id: int) -> None:
    if bot_token and dest_chat_id:
        try:
            resp = requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={
                    "chat_id": dest_chat_id,
                    "text": message,
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                },
                timeout=10,
            )
            if resp.ok:
                return
            print("Bot API send error:", resp.status_code, resp.text)
        except Exception as exc:
            print("Bot API send exception:", exc)

    await client.send_message("me", message, parse_mode="html")


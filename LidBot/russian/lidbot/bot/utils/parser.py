import html
from typing import Optional, Tuple


def extract_text(event) -> str:
    if getattr(event, "raw_text", None):
        return event.raw_text
    if getattr(event, "message", None) and getattr(event.message, "message", None):
        return event.message.message
    return ""


async def resolve_chat_meta(event) -> Tuple[str, Optional[str]]:
    chat = await event.get_chat()
    username = getattr(chat, "username", None)
    message_id = getattr(event.message, "id", None) or getattr(event, "id", None)

    if not message_id:
        link = None
    elif username:
        link = f"https://t.me/{username}/{message_id}"
    else:
        cid = getattr(chat, "id", None)
        if cid is None:
            link = None
        else:
            raw = str(cid)
            if raw.startswith("-100"):
                chat_part = raw[4:]
            else:
                chat_part = raw.lstrip("-")
            link = f"https://t.me/c/{chat_part}/{message_id}"

    title = getattr(chat, "title", getattr(chat, "first_name", "chat"))
    return str(title), link


def build_notification(title: str, text: str, link: Optional[str]) -> str:
    excerpt = html.escape(text[:900])
    escaped_title = html.escape(title)
    if link:
        return (
            f"🔎 <b>Найдено сообщение</b> в <b>{escaped_title}</b>:\n\n"
            f"{excerpt}\n\n"
            f"👉 <a href=\"{link}\">Открыть сообщение</a>"
        )
    return f"🔎 <b>Найдено сообщение</b> в <b>{escaped_title}</b>:\n\n{excerpt}"


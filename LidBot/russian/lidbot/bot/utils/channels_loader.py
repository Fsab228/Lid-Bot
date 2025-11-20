import json
from pathlib import Path
from typing import List, Tuple

from telethon.errors import UsernameNotOccupiedError

from .filters import extract_username


async def load_target_chats(
    client,
    groups_file: Path,
    groups_ids_file: Path,
    cleaned_usernames_file: Path,
    auto_write_cleaned: bool,
    max_skip_log: int,
) -> Tuple[List, List[str]]:
    """
    Возвращает список чатов (валидные сущности) и лог для печати.
    """
    logs: List[str] = []
    valid_chats: List = []
    valid_usernames: List[str] = []

    ids_loaded = False
    if groups_ids_file.exists():
        try:
            ids = _read_id_cache(groups_ids_file)
            if ids:
                valid_chats.extend(ids)
                ids_loaded = True
                logs.append(f"📗 Загружено ID каналов: {len(ids)} из {groups_ids_file}")
        except Exception as exc:
            logs.append(f"⚠️ Не удалось прочитать {groups_ids_file}: {exc}")

    if ids_loaded:
        return valid_chats, logs

    if not groups_file.exists():
        logs.append(f"❌ Файл {groups_file} отсутствует, кэш пуст.")
        return [], logs

    usernames = [
        extract_username(line)
        for line in groups_file.read_text(encoding="utf-8").splitlines()
    ]
    usernames = [u for u in usernames if u]
    if not usernames:
        logs.append("❌ Нет username в all_channels.txt и нет ID.")
        return [], logs

    logs.append(f"📊 В списке каналов: {len(usernames)}")
    skipped = skipped_logged = 0

    for username in usernames:
        try:
            entity = await client.get_input_entity(username)
            valid_chats.append(entity)
            valid_usernames.append(username)
        except UsernameNotOccupiedError:
            skipped += 1
            skipped_logged = _log_skip(
                logs, skipped_logged, max_skip_log, f"@{username} свободен или не существует"
            )
        except ValueError:
            skipped += 1
            skipped_logged = _log_skip(
                logs, skipped_logged, max_skip_log, f"не удалось разрешить @{username}"
            )
        except Exception as exc:
            skipped += 1
            skipped_logged = _log_skip(
                logs, skipped_logged, max_skip_log, f"ошибка @{username}: {exc}"
            )

    if not valid_chats:
        logs.append("❌ Нет валидных каналов/чатов для прослушивания.")
        return [], logs

    logs.append(f"✅ Буду слушать {len(valid_chats)} чатов. Пропущено: {skipped}")
    if skipped > skipped_logged:
        logs.append(f"ℹ️ Ещё пропусков без логов: {skipped - skipped_logged}")

    if auto_write_cleaned and valid_usernames:
        try:
            cleaned_usernames_file.write_text(
                "\n".join(f"@{name}" for name in valid_usernames),
                encoding="utf-8",
            )
            logs.append(f"💾 Сохранил валидные username в {cleaned_usernames_file}")
        except Exception as exc:
            logs.append(f"⚠️ Не удалось записать {cleaned_usernames_file}: {exc}")

    return valid_chats, logs


def _read_id_cache(path: Path) -> List[int]:
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return []

    try:
        parsed = json.loads(content)
    except Exception:
        parsed = None

    ids: List[int] = []
    if isinstance(parsed, dict) and "channels" in parsed:
        for item in parsed.get("channels", {}).values():
            cid = item.get("id") if isinstance(item, dict) else item
            _append_int(ids, cid)
    elif isinstance(parsed, list):
        for item in parsed:
            _append_int(ids, item)
    else:
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith("@"):
                _append_int(ids, line)
    return ids


def _append_int(target: List[int], value) -> None:
    try:
        target.append(int(value))
    except Exception:
        pass


def _log_skip(logs: List[str], logged: int, max_logged: int, text: str) -> int:
    if logged < max_logged:
        logs.append(f"⚠️ Пропускаю: {text}")
        return logged + 1
    return logged


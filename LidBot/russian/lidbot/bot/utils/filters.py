import re
from functools import lru_cache
from typing import List, Optional

import pymorphy3

morph = pymorphy3.MorphAnalyzer()

TOKEN_RE = re.compile(r"[A-Za-zА-Яа-яёЁ0-9]+")
PHONE_RE = re.compile(r"(?:\+?\d[\d\-\s\(\)]{6,}\d)")
URL_RE = re.compile(r"https?://\S+")

BANNED_SUBSTRINGS = [
    "наркот", "мета", "амфет", "героин", "кокаин", "спайс", "травк",
    "weed", "cocaine", "heroin", "mdma",
    "мошенн", "скам", "лохотрон", "пирамид", "обман", "фейк", "подделк", "fake passport", "скаммер",
    "казино", "ставк", "беттинг", "порно", "эротик", "18+", "xxx",
    "крипто-", "бинарн", "форекс сигнал", "продвижение канала", "раскрутка",
]

REAL_ESTATE_KEYWORDS = [
    "студи", "квартир", "комнат", "апартамент", "недвижимост",
    "жилье", "жилья", "мастеррум", "bedroom", "apartment", "studio",
    "flat", "property", "real estate",
]

SPAM_KEYWORDS = [
    "ознакомься с правилами", "подобные форумы", "туры, отели, прокат машин",
    "всё о рекламе в телеграм", "репетиторы онлайн", "пробное занятие",
]

TAXI_KILLERS = [
    "из джумейры на пальму", "от аэропорта до", "из дубая в абу",
    "могу забрать попутчиков", "еду из", "выезжаю из",
    "from sharjah to dubai", "from dubai to", "pick up passengers",
    "такси", "transfer", "трансфер", "поездка", "еду", "подвезти", "довезти",
]

JOB_KILLERS = [
    "ваканси", "работа", "зарплат", "требуют", "ищем сотруд", "мойщик",
    "cleaner", "hiring",
]

RAW_CAR_LEMMAS = {
    "машина", "автомобиль", "авто", "тачка", "машинка", "транспорт", "легковушка",
    "седан", "джип", "хэтчбек", "кроссовер", "внедорожник", "универсал", "фургон",
    "минивэн", "car", "cars", "auto", "vehicle", "vehicles", "suv", "jeep", "sedan",
    "hatchback", "crossover", "truck", "van", "minivan",
}

RAW_INTENT_LEMMAS = {
    "искать", "нужный", "нуждаться", "хотеть", "снять", "взять", "арендовать",
    "требоваться", "ищется", "надо", "нужно", "нужна", "нужен", "нужны",
    "хочу", "возьму", "понадобиться", "ищу", "помогите", "подходит", "подойдет", "ищем",
    "need", "needed", "require", "required", "looking", "want", "wanted", "wanna",
    "seek", "seeking", "search", "searching", "rent", "renting", "hire", "hiring",
    "book", "booking", "get", "getacar", "geta", "get",
}

RAW_OFFER_LEMMAS = {
    "продать", "продавать", "продажа", "продам", "сдать", "сдавать", "сдам", "сдаю", "сдается",
    "предлагать", "предложение", "предлагаем", "предлагаю",
    "услуга", "услуги", "сервис", "компания", "фирма", "магазин", "склад", "оптом",
    "цена", "стоимость", "тариф", "скидка", "акция", "звоните", "контакт", "whatsapp", "viber",
    "offer", "offers", "offering", "provide", "provides", "providing",
    "give", "gives", "giving", "sell", "sells", "selling", "sale", "sales",
    "company", "agency", "service", "services", "business",
    "rentacar", "rent-a-car",
    "price", "prices", "pricing", "cost", "costs", "discount", "discounts", "promo", "promotion",
    "available", "availability", "contact", "call", "whatsapp", "viber",
}

RAW_RENTAL_KEYWORDS = {
    "аренда", "арендовать", "арендую", "прокат", "снять", "взять", "напрокат",
    "rental", "rent", "renting", "hire", "hiring", "lease", "leasing",
}

CLIENT_PHRASES = [
    "нужна машина", "нужен автомобиль", "нужно авто", "нужна машина в аренду",
    "нужен автомобиль в аренду", "нужна машина напрокат", "нужно авто в аренду",
    "ищу машину", "ищу авто", "ищу автомобиль", "ищу машину в аренду",
    "ищу авто в аренду", "ищу машину напрокат", "ищу автомобиль в аренду",
    "ищу автопрокат", "ищу прокат", "ищу где арендовать",
    "хочу арендовать", "хочу взять", "хочу взять в аренду", "хочу снять",
    "хочу машину", "хочу авто", "хочу арендовать машину", "хочу арендовать авто",
    "где можно", "где взять", "где арендовать", "где снять", "где найти",
    "кто знает", "кто может", "кто сдает", "кто арендует",
    "подскажите", "помогите", "помогите найти", "помогите снять",
    "ищем машину", "ищем авто", "нужна на", "на день", "на неделю", "на месяц",
    "need a car", "need car", "need a car for rent", "need car rental",
    "looking for", "looking for a car", "looking for car rental",
    "want to rent", "want to rent a car", "want a car",
    "where to rent", "where can i rent", "who rents", "who can rent",
    "help me find", "can someone help", "anyone know", "anyone can help",
]

QUICK_SUBSTR = [
    "машин", "авто", "тачк", "аренд", "снять", "нуж", "ищ", "хоч", "взять",
    "need", "rent", "car", "vehicle",
]

CAR_LEMMAS = set()
INTENT_LEMMAS = set()
OFFER_LEMMAS = set()
RENTAL_KEYWORDS = set()


def _populate_sets():
    global CAR_LEMMAS, INTENT_LEMMAS, OFFER_LEMMAS, RENTAL_KEYWORDS
    CAR_LEMMAS = {safe_lemma(w) for w in RAW_CAR_LEMMAS}
    INTENT_LEMMAS = {safe_lemma(w) for w in RAW_INTENT_LEMMAS}
    OFFER_LEMMAS = {safe_lemma(w) for w in RAW_OFFER_LEMMAS}
    RENTAL_KEYWORDS = {safe_lemma(w) for w in RAW_RENTAL_KEYWORDS}


@lru_cache(maxsize=20000)
def safe_lemma(word: str) -> str:
    cleaned = (word or "").strip()
    if not cleaned:
        return cleaned
    try:
        if re.search('[а-яА-ЯёЁ]', cleaned):
            return morph.parse(cleaned)[0].normal_form
    except Exception:
        pass
    return cleaned.lower()


def extract_username(line: str) -> Optional[str]:
    if not line:
        return None
    value = line.strip()
    if not value:
        return None
    match = re.search(r"(?:https?://)?t\.me/([^/\s]+)", value)
    if match:
        value = match.group(1)
    value = value.strip().lstrip("@")
    if not value or "joinchat" in value.lower():
        return None
    return value


def tokenize(text_lower: str) -> List[str]:
    return TOKEN_RE.findall(text_lower)


def has_proximity(lemmas: List[str], left_set: set, right_set: set, window: int) -> bool:
    left_idx = [i for i, token in enumerate(lemmas) if token in left_set]
    if not left_idx:
        return False
    right_idx = [i for i, token in enumerate(lemmas) if token in right_set]
    if not right_idx:
        return False
    j = 0
    for i in left_idx:
        while j < len(right_idx) and right_idx[j] < i - window:
            j += 1
        if j < len(right_idx) and abs(right_idx[j] - i) <= window:
            return True
    return False


def has_contact_info(text: str) -> bool:
    return bool(PHONE_RE.search(text) or URL_RE.search(text))


def passes_filters(text: str, proximity_window: int) -> bool:
    if not text:
        return False

    text_lower = text.lower()
    if any(bad in text_lower for bad in BANNED_SUBSTRINGS):
        return False

    if not any(sub in text_lower for sub in QUICK_SUBSTR):
        return False

    tokens = tokenize(text_lower)
    if not tokens:
        return False

    lemmas = [safe_lemma(token) for token in tokens]

    if any(keyword in text_lower for keyword in REAL_ESTATE_KEYWORDS):
        return False
    if any(keyword in text_lower for keyword in SPAM_KEYWORDS):
        return False
    if any(keyword in text_lower for keyword in TAXI_KILLERS):
        return False
    if any(keyword in text_lower for keyword in JOB_KILLERS):
        return False
    if "детск" in text_lower and ("игруш" in text_lower or "toy" in text_lower):
        return False

    seller_word_count = sum(1 for lemma in lemmas if lemma in OFFER_LEMMAS)
    if seller_word_count >= 1:
        return False

    if has_contact_info(text):
        return False

    is_client_seeking = any(phrase in text_lower for phrase in CLIENT_PHRASES)
    has_intent_near_car = has_proximity(lemmas, CAR_LEMMAS, INTENT_LEMMAS, proximity_window) or has_proximity(
        lemmas, INTENT_LEMMAS, CAR_LEMMAS, proximity_window
    )
    has_rental_word = any(word in text_lower for word in RAW_RENTAL_KEYWORDS)

    return (is_client_seeking or has_intent_near_car) and has_rental_word


_populate_sets()


from decimal import Decimal

def parse_eur_price(text: str) -> Decimal | None:
    if not text:
        return None
    s = text.strip()
    # убрать евро и пробелы-разделители тысяч, заменить запятую на точку
    s = s.replace("€", "").replace("\xa0", " ").strip()
    s = s.replace(" ", "").replace(",", ".")
    try:
        return Decimal(s)
    except Exception:
        return None
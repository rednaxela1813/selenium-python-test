import csv
from pathlib import Path
from decimal import Decimal


def _to_csv_value(v):
    if v is None:
        return ""
    if isinstance(v, Decimal):
        return str(v)
    return v


def save_to_csv(rows, path: str = "output/products.csv"):
    Path(path).parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        # создадим пустой файл с заголовком минимально
        with open(path, "w", newline="", encoding="utf-8") as f:
            f.write("url,name,price\n")
        return

    # Собираем все ключи, которые встретились (стабильно по порядку)
    fieldnames = []
    seen = set()
    for row in rows:
        for k in row.keys():
            if k not in seen:
                seen.add(k)
                fieldnames.append(k)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()

        for row in rows:
            writer.writerow({k: _to_csv_value(row.get(k)) for k in fieldnames})
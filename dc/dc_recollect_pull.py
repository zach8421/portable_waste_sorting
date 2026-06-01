import json
import re
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

import requests


SOURCE_URL = "https://api.recollect.net/api/areas/WashingtonDC/services/220/pages"

PAGE_SIZE = 100
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR / "data"

BASE_PARAMS = {
    "suggest": "",
    "type": "material",
    "set": "default",
    "include_links": "true",
    "locale": "en-US",
    "accept_list": "true",
    "limit": PAGE_SIZE,
}


def fetch_all_pages():
    all_items = []
    offset = 0
    last_url = None
    while True:
        params = {**BASE_PARAMS, "offset": offset}
        response = requests.get(SOURCE_URL, params=params, timeout=30)
        response.raise_for_status()
        batch = response.json()
        last_url = response.url
        if not batch:
            break
        all_items.extend(batch)
        print(f"  offset={offset}: +{len(batch)} (total={len(all_items)})")
        if len(batch) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
    return all_items, last_url


def strip_html(value):
    if not value:
        return ""
    text = re.sub(r"<[^>]+>", " ", value)
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def get_variable(item, name, locale="en-US"):
    variables = item.get("opts", {}).get("variables", [])
    for var in variables:
        if var.get("name") == name:
            value = var.get("value", "")
            if isinstance(value, dict):
                return value.get(locale) or value.get("en") or ""
            return value or ""
    return ""


def extract_options(item):
    options = []

    for section in item.get("sections", []):
        title = section.get("title")
        included_from = section.get("included_from")

        rows = section.get("rows", [])
        row_text = []

        for row in rows:
            if row.get("type") == "html":
                html = row.get("html") or row.get("value") or ""
                cleaned = strip_html(html)
                if cleaned:
                    row_text.append(cleaned)

        if title or included_from or row_text:
            options.append({
                "section_title": title,
                "included_from": included_from,
                "text": " ".join(row_text)
            })

    return options


def normalize_item(item):
    title = get_variable(item, "title") or item.get("caption", "")
    synonyms_raw = get_variable(item, "synonyms")

    synonyms = [
        s.strip()
        for s in synonyms_raw.split(",")
        if s.strip()
    ]

    return {
        "item_id": str(item.get("id")),
        "item_name": title,
        "page_name": item.get("page_name"),
        "synonyms": synonyms,
        "dropoff_instructions": strip_html(get_variable(item, "dropoff_instructions")),
        "special_instructions": strip_html(get_variable(item, "special_instructions")),
        "options": extract_options(item),
        "source_reference": f"https://api.recollect.net/api/areas/WashingtonDC/services/220/pages/en-US/{item.get('id')}.json",
        "city_jurisdiction": "Washington, DC",
    }


def main():
    print("Fetching pages with offset-based pagination:")
    raw_items, last_url = fetch_all_pages()
    print(f"Fetched {len(raw_items)} raw material records")

    DATA_DIR.mkdir(exist_ok=True)

    raw_path = DATA_DIR / "dc_recollect_raw_pages.json"
    with raw_path.open("w", encoding="utf-8") as f:
        json.dump(raw_items, f, indent=2, ensure_ascii=False)

    items = [
        normalize_item(item)
        for item in raw_items
        if item.get("page_type") == "material"
    ]

    snapshot = {
        "metadata": {
            "source": "ReCollect API for Zero Waste DC What Goes Where",
            "source_url": last_url,
            "schema_version": "0.1",
            "item_count": len(items),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "items": items,
    }

    items_path = DATA_DIR / "dc_items.json"
    with items_path.open("w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(items)} normalized records to {items_path}")
    print("First item:", items[0]["item_name"])
    print("Last item:", items[-1]["item_name"])


if __name__ == "__main__":
    main()

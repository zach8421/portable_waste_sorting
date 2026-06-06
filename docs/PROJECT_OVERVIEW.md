# 🗑️ Portable Waste Sorting Information for Seattle

*Final-project overview, following the course's About / Methodology / Access / Structure / Example format. For the per-criterion artifact map, see [RUBRIC_MAP.md](RUBRIC_MAP.md).*

## 🗑️ About
This project restructures Seattle Public Utilities' [Where Does It Go?](https://www.seattle.gov/utilities/your-services/collection-and-disposal/where-does-it-go) guidance into a portable, item-based JSON dataset that can be reused across lookup tools, mobile apps, kiosks, bin-side signage, and classroom exercises. The audience is Seattle residents who need quick disposal answers, plus the developers, educators, and civic-tech contributors who build tools on that guidance. The dataset is openly accessible: a snapshot generated from two public SPU taxonomy endpoints and saved as a single `data/items.json`, alongside a Jupyter notebook and a small Flask API. Every record links back to the authoritative SPU page, and the schema follows FAIR principles (stable IDs, open format, shared schema, per-item provenance) so the data moves between systems without proprietary lock-in.

## 🗑️ Methodology
- Two public JSON endpoints on `seattle.gov` (`taxonomy/3087/tree` for the category hierarchy, `taxonomy/3086/pages` for the items) were discovered by inspecting the *Where Does It Go?* page's network traffic.
- [`portable_waste_sorting.ipynb`](../portable_waste_sorting.ipynb) fetches both live with `requests`, then transforms each raw page into the uniform schema from the G3 submission. Full transformation detail: [03_transformations.md](03_transformations.md).
- Each item is normalized to: stable `item_id`, name, synonyms, the `disposal_streams` it belongs to, per-stream `disposal_conditions`, a plain-language `explanation`, a breadcrumb `category_path`, a `source_reference`, and `city_jurisdiction`.
- Multi-stream items (e.g. "Acoustic Ceiling Tile" → `[garbage, hazardous, dropoff]`) preserve **all** streams plus per-stream conditions rather than forcing one answer.
- The notebook writes a versioned snapshot to `data/items.json` (metadata header + category tree + ~310 items) and renders a Plotly sunburst and a per-stream bar chart as visual validation.
- A Washington, DC variant ([`dc/`](../dc/), 468 items) demonstrates interoperability by mapping a structurally different source (ReCollect templates) into the same schema.
- SPU remains the authoritative source; the dataset is decision support, and the `source_reference` is the recommended tie-breaker when guidance changes between refreshes.

## 🗑️ Access
Three documented ways to use the data:

- **Notebook (Colab or local)** — open [`portable_waste_sorting.ipynb`](../portable_waste_sorting.ipynb) and *Run all*; it fetches, transforms, visualizes, and writes `data/items.json`. Local: `pip install pandas plotly requests jupyter`.
- **Direct snapshot** — load `data/items.json` in any language with a JSON parser and iterate `data["items"]`. No key, account, or rate limit.
- **REST API** — the Flask app in [`i8/which_bin_api.py`](../i8/which_bin_api.py) loads the snapshot as a NoSQL-style document store and exposes **nine** endpoints:

  ```
  GET /                      API info + data source
  GET /items                 all items (summary)
  GET /items/<item_id>       full record (404 if missing)
  GET /search?q=&stream=&category=   AND-combined filters (400 on empty/invalid)
  GET /streams               item counts per stream
  GET /streams/<stream>      items in one stream
  GET /categories            categories with counts
  GET /categories/<name>     items in one category
  GET /stats                 totals, multi-stream count, top categories
  ```

  Run it:
  ```bash
  pip install -r i8/requirements.txt
  python3 -m flask --app i8/which_bin_api.py run --port 5055
  ```

## 🗑️ Structure
See [04_new_structure.md](04_new_structure.md) for the full field table. Each record is a JSON object keyed by a stable `item_id`, with `disposal_streams` (array) and `disposal_conditions` (per-stream object) capturing the multi-valued disposal logic, plus `source_reference` and `city_jurisdiction` provenance. A top-level `metadata` block carries `schema_version`, `item_count`, and `generated_at`.

## 🗑️ Example

**Request (REST API):**
```
GET http://127.0.0.1:5055/search?q=aerosol
```
**Response (abridged):**
```json
{
  "query": {"q": "aerosol", "stream": null, "category": null},
  "count": 1,
  "items": [{
    "item_id": "x130610",
    "item_name": "Aerosol Cans",
    "disposal_streams": ["recycling", "garbage", "hazardous"],
    "category_path": ["Hazardous Items"]
  }]
}
```

**Request (direct snapshot in Python):**
```python
import json
data = json.load(open("data/items.json"))
for item in data["items"]:
    if "battery" in item["item_name"].lower():
        print(item["item_name"], "→", item["disposal_streams"])
```
**Output:**
```
Batteries → ['hazardous', 'dropoff']
Batteries - Lithium → ['hazardous', 'dropoff']
Batteries - Rechargeable → ['hazardous', 'dropoff']
```

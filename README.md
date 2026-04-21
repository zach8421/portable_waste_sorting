# Portable Waste-Sorting Information for Seattle Residents

> IMT 542 — I3 Assignment · Spring 2026

A lightweight Jupyter notebook that reframes Seattle Public Utilities' [Where Does It Go?](https://www.seattle.gov/utilities/your-services/collection-and-disposal/where-does-it-go) guidance as a portable JSON structure, then visualizes it as a tree and exposes it through a simple lookup function.

## Why this project is useful

Seattle residents regularly encounter uncertainty when sorting waste. SPU publishes disposal guidance, but it's distributed across rules, lists, and exception cases that are awkward to consult during everyday decision-making. This project takes that same guidance and expresses it as one uniform JSON record per item — an item name, its synonyms, the disposal category, preparation steps, an explanation, and a link back to the authoritative source. Because every item follows the same shape, the data can drive a website, an app, an API, a voice assistant, or a classroom exercise without further transformation.

The notebook demonstrates three uses of the structure:

1. **Tree visualization** — a Plotly sunburst chart showing the category to sub-category to item hierarchy, coloured by disposal stream.
2. **Distribution analysis** — a bar chart of items per disposal category (recycle, compost, garbage, hazardous waste, etc.).
3. **Item lookup** — a small Python function that answers "where does this go?" using item names or synonyms.

The JSON schema is the output from my G3 submission ("Portable Waste-Sorting Information for Seattle Residents"); this notebook is the I3 implementation that applies that schema to real data.

## What's in the repo

```
portable_waste_sorting/
├── portable_waste_sorting.ipynb   # main notebook
├── data/
│   └── items.json                 # seed dataset (categories + items in the G3 schema)
└── README.md
```

## How to download and run

### Option A — Google Colab (easiest)

1. Click the **Open In Colab** badge at the top of `portable_waste_sorting.ipynb` on GitHub.
2. Run each cell top to bottom (`Runtime to Run all`).

No setup required beyond Colab's default environment. The notebook pulls `items.json` straight from this repo's raw URL.

### Option B — Local

```bash
git clone https://github.com/YOUR_USERNAME/portable_waste_sorting.git
cd portable_waste_sorting
pip install pandas plotly requests jupyter
jupyter notebook portable_waste_sorting.ipynb
```

The notebook falls back to `data/items.json` on disk when the GitHub raw URL is unreachable, so it runs offline as well.

## How to use the data directly

If you want the JSON without running the notebook:

```python
import json
with open("data/items.json") as f:
    data = json.load(f)

# Every item follows the same shape
for item in data["items"]:
    if "battery" in item["item_name"]:
        print(item["disposal_category"], "to", item["disposal_conditions"])
```

Each item has these fields (the G3 schema):

| Field | Description |
|---|---|
| `item_id` | Stable slug for the item |
| `item_name` | Display name |
| `synonyms` | Alternate names users might search for |
| `material` | Primary material (plastic, glass, metal, organic, etc.) |
| `disposal_category` | Where it goes: `recycle`, `compost`, `garbage`, `hazardous_waste`, `transfer_station`, `special_pickup`, `donate` |
| `disposal_conditions` | Plain-language instructions, including drop-off options |
| `preparation_required` | What to do before disposing |
| `explanation` | Why it's classified this way |
| `source_reference` | URL to the SPU page for the item |
| `confidence_level` | `high` when transcribed verbatim from SPU, `medium` when derived from common guidance |
| `category_path` | Breadcrumb through the category tree |

## Expanding the dataset

The seed file covers the Electronics to Batteries sub-tree verbatim from the SPU page plus representative items from the other top-level categories. The last cell of the notebook is an optional Playwright-based scraper that renders the SPU SPA and fetches every item on the live site. (Plain `requests` does not work — the page is a JavaScript single-page app with `#/item/...` hash routes, and the server returns 403 to non-browser clients.) To run it, set `RUN_SCRAPER = True` in the last code cell while in Colab; the scraped text is saved to `data/items_raw_scrape.json` for further parsing into the full schema.

## License / data source

Disposal guidance is derived from [Seattle Public Utilities' Where Does It Go? tool](https://www.seattle.gov/utilities/your-services/collection-and-disposal/where-does-it-go). SPU is the authoritative source for all disposal decisions; always check the linked `source_reference` URL for the current rule. Code is MIT-licensed.

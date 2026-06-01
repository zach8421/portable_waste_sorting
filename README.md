# Portable Waste-Sorting Information

> IMT 542 — I3 Assignment · Spring 2026

A lightweight set of Jupyter notebooks that transform local waste-sorting guidance into portable JSON structures, then visualize the data and expose it through simple lookup functions. The original notebook uses Seattle Public Utilities' [Where Does It Go?](https://www.seattle.gov/utilities/your-services/collection-and-disposal/where-does-it-go) guidance; the `dc/` folder adds a Washington, DC version based on Zero Waste DC's ReCollect-powered "What Goes Where" data.

## Why this project is useful

Seattle residents regularly encounter uncertainty when sorting waste. SPU publishes item-level disposal guidance, but the data sits behind a JavaScript single-page app — it isn't easy to reuse in other interfaces or to query programmatically. This project pulls the same guidance directly from the two JSON endpoints powering that page and expresses every item as one uniform record: an item name, its synonyms, the disposal streams it belongs to, preparation instructions, an explanation, and a link back to the authoritative source.

Because every item follows the same shape, the data can drive a website, an app, an API, a voice assistant, or a classroom exercise without further transformation.

The notebook demonstrates three uses of the structure:

1. **Tree visualization** — a Plotly sunburst chart showing the category → sub-category → item hierarchy, coloured by the item's primary disposal stream.
2. **Distribution analysis** — a bar chart of items per disposal stream (recycling, compost, garbage, hazardous waste, drop-off, special pickup, donate/reuse).
3. **Item lookup** — a Python function that answers "where does this go?" using item names or synonyms.

### A note on the sunburst colouring

Roughly two-thirds of the 310 items have **more than one** valid disposal stream — a greasy pizza box can be compost *or* garbage; a cell phone can be hazardous *or* drop-off. The underlying JSON records every valid stream for each item, but the sunburst paints each slice with a **single colour** based on a resident-priority ordering (`hazardous` → `recycling` → `compost` → `garbage` → `dropoff` → `special` → `donate`). An earlier revision tried diagonal stripes to encode multi-stream items visually; the result was noisy and hard to read at small slice sizes, so the visualization stays one-colour-per-slice. The full list of valid streams and the per-stream instructions are always available in the hover tooltip and in `data/items.json` itself.

The JSON schema comes from my G3 submission ("Portable Waste-Sorting Information for Seattle Residents"); this notebook is the I3 implementation that applies that schema to real data.

## Data source

Two JSON endpoints on `seattle.gov`, discovered by inspecting the network traffic on the Where Does It Go? page:

| URL | Contents |
|---|---|
| `https://seattle.gov/api/content/taxonomy/3087/tree` | Category hierarchy (14 top-level categories, ~56 nodes total) |
| `https://seattle.gov/api/content/taxonomy/3086/pages` | Every item (name, synonyms, disposal instructions per stream) |

The notebook fetches both live, transforms each page record into the G3 schema, and writes a snapshot to `data/items.json`.

Washington, DC data lives in [`dc/`](dc/). It is pulled from ReCollect's
WashingtonDC material endpoint and saved as `dc/data/dc_items_portable.json`.
Because DC's source records use reusable option templates rather than explicit
Seattle-style stream fields, the DC notebook infers streams from templates such
as `wizard_recycling`, `wizard_trash`, and `wizard_drop-off_*`.

> **Sidenote:** Because the notebook renders SPU's taxonomy verbatim, the occasional upstream quirk carries through — for example, the item **Boat** is tagged with SPU's "Bedroom" taxonomy ID and appears under that category in the sunburst. These are preserved rather than hand-corrected, since SPU is the authoritative source and the data should reflect whatever they publish today.

## What's in the repo

```
portable_waste_sorting/
├── portable_waste_sorting.ipynb   # main notebook (I3)
├── data/
│   └── items.json                 # generated on first notebook run
├── dc/                            # Washington, DC notebook and data
│   ├── dc_waste_sorting.ipynb
│   ├── dc_recollect_pull.py
│   ├── README.md
│   └── data/
│       └── dc_items_portable.json
├── i8/                            # I8 assignment — Flask API over data/items.json
│   ├── which_bin_api.py
│   ├── requirements.txt
│   ├── I8_demo.mp4
│   └── README.md
├── I7_api_access_demo.mp4         # I7 assignment demo video
└── README.md
```

> The **I8 — Advanced DBs** assignment lives in [`i8/`](i8/). It puts a
> Flask API (nine endpoints, JSON-only, with 400/404 error handling) in
> front of `data/items.json`, used as a NoSQL-style document store loaded
> at server startup. See [`i8/README.md`](i8/README.md) for run instructions
> and example calls, and [`i8/I8_demo.mp4`](i8/I8_demo.mp4) for the demo
> walkthrough.

## How to download and run

### Option A — Google Colab (easiest)

1. Click the **Open In Colab** badge at the top of `portable_waste_sorting.ipynb` on GitHub.
2. Run each cell top to bottom (`Runtime → Run all`).

No local setup needed. The notebook fetches from the SPU API, transforms every item, draws the sunburst and bar chart, and writes `data/items.json` into the Colab session.

### Option B — Local

```bash
git clone https://github.com/zach8421/portable_waste_sorting.git
cd portable_waste_sorting
pip install pandas plotly requests jupyter
jupyter notebook portable_waste_sorting.ipynb
```

To run the Washington, DC notebook:

```bash
cd dc
jupyter notebook dc_waste_sorting.ipynb
```

## The G3 schema

Each item record has these fields:

| Field | Description |
|---|---|
| `item_id` | SPU's stable ID for the item (e.g. `x130614`) |
| `item_name` | Display name (e.g. "Acetylene Tanks") |
| `synonyms` | Alternate names users might search for |
| `disposal_streams` | List of valid streams: `recycling`, `compost`, `garbage`, `hazardous`, `dropoff`, `special`, `donate`. Items commonly have multiple (e.g. "Napkins" → `[compost, garbage, donate]` depending on whether they're soiled or reusable). The sunburst paints each slice with the item's primary stream only — see the "A note on the sunburst colouring" section above for why. |
| `disposal_conditions` | Dict keyed by stream → plain-text instructions for that stream |
| `explanation` | SPU's short plain-language summary (the `VoiceInstructions` field) |
| `category_path` | Breadcrumb through the category tree (e.g. `["Construction & Demolition", "Floors & Ceiling"]`) |
| `source_reference` | URL to the SPU item page |
| `city_jurisdiction` | Source jurisdiction, such as `"Seattle, WA"` or `"Washington, DC"` |

## Using the data directly

After running the notebook once, `data/items.json` contains the full snapshot:

```python
import json
with open("data/items.json") as f:
    data = json.load(f)

for item in data["items"]:
    if "battery" in item["item_name"].lower():
        print(item["item_name"], "→", item["disposal_streams"])
```

## License / data source

Disposal guidance is derived from [Seattle Public Utilities' Where Does It Go? tool](https://www.seattle.gov/utilities/your-services/collection-and-disposal/where-does-it-go). SPU is the authoritative source for all disposal decisions; always check the linked `source_reference` URL for the current rule. Code is MIT-licensed.

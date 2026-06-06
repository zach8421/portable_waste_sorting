# Portable Waste-Sorting Information

> IMT 542 — **Final Project** · Spring 2026 · *You act as the Information Architect*

This project restructures local waste-sorting guidance into a portable JSON structure, then visualizes the data and exposes it through a notebook, a static snapshot, and a REST API. The core product uses Seattle Public Utilities' [Where Does It Go?](https://www.seattle.gov/utilities/your-services/collection-and-disposal/where-does-it-go) guidance; the `dc/` folder adds a Washington, DC interoperability demonstration based on Zero Waste DC's ReCollect-powered "What Goes Where" data.

## Final project — deliverables & rubric map

This repository is the cumulative final project. Graders should start with **[`docs/RUBRIC_MAP.md`](docs/RUBRIC_MAP.md)**, which maps each of the 10 rubric criteria to the artifact that satisfies it.

| Deliverable | Location |
|---|---|
| Project README (this file) | `README.md` |
| Presentation | [`Portable_Waste_Sorting.pptx`](Portable_Waste_Sorting.pptx) |
| Information story & requirements (areas 1) | [`docs/01_information_story.md`](docs/01_information_story.md) |
| Existing structure + **FAIR assessment** (area 2) | [`docs/02_existing_structure_and_FAIR_assessment.md`](docs/02_existing_structure_and_FAIR_assessment.md) |
| Transformations incl. DC adaptations (area 2) | [`docs/03_transformations.md`](docs/03_transformations.md) |
| The new portable structure (area 3) | [`docs/04_new_structure.md`](docs/04_new_structure.md) |
| Quality & performance, measured (area 5) | [`docs/05_quality_and_performance.md`](docs/05_quality_and_performance.md) · [`TESTPLAN.md`](TESTPLAN.md) |
| Ethics, limitations & societal impact | [`docs/06_ethics_and_limitations.md`](docs/06_ethics_and_limitations.md) |
| Full project overview | [`docs/PROJECT_OVERVIEW.md`](docs/PROJECT_OVERVIEW.md) |
| Functional system (areas 4) | [`i8/which_bin_api.py`](i8/which_bin_api.py) · demo videos |

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

```text
portable_waste_sorting/
├── README.md                      # this file
├── Portable_Waste_Sorting.pptx    # final presentation deck
├── TESTPLAN.md                    # functional/performance/quality test plan
├── portable_waste_sorting.ipynb   # main notebook (fetch → transform → visualize → snapshot)
├── data/
│   └── items.json                 # generated snapshot (310 Seattle items)
├── docs/                          # supporting artifacts for all five graded areas
│   ├── RUBRIC_MAP.md              # criterion → artifact map (start here)
│   ├── PROJECT_OVERVIEW.md
│   ├── 01_information_story.md
│   ├── 02_existing_structure_and_FAIR_assessment.md
│   ├── 03_transformations.md
│   ├── 04_new_structure.md
│   ├── 05_quality_and_performance.md
│   ├── 06_ethics_and_limitations.md
│   ├── build_pptx.py              # regenerates the .pptx
│   └── exhibits/                  # before/after structure samples
├── dc/                            # Washington, DC interoperability demonstration
│   ├── dc_waste_sorting.ipynb
│   ├── dc_recollect_pull.py
│   ├── README.md
│   └── data/
│       └── dc_items_portable.json # 468 DC items in the same schema
├── i8/                            # Flask REST API over data/items.json
│   ├── which_bin_api.py
│   ├── requirements.txt
│   ├── I8_demo.mp4
│   └── README.md
└── I7_api_access_demo.mp4         # API access demo video
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

### Option C — REST API

The Flask app in [`i8/which_bin_api.py`](i8/which_bin_api.py) serves `data/items.json` as a NoSQL-style document store over nine JSON endpoints (`/items`, `/items/<item_id>`, `/search`, `/streams`, `/categories`, `/stats`, …). See [`i8/README.md`](i8/README.md) for the full list.

```bash
pip install -r i8/requirements.txt
python3 -m flask --app i8/which_bin_api.py run --port 5055
# then, in another shell:
curl http://127.0.0.1:5055/items/x130614
curl 'http://127.0.0.1:5055/search?q=cardboard'
curl http://127.0.0.1:5055/stats
```

Measured locally: single-item lookups respond in ~1 ms and the server starts in ~0.3 s — see [`docs/05_quality_and_performance.md`](docs/05_quality_and_performance.md).

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

# 03 — Transformations

*Graded area 2 · Rubric criterion #4 (transformations clear, well-defined, fully covered by requirements)*
*Directly addresses instructor feedback: "I would want some documentation about the specific transformations needed… Did you have to change any formatting…? What were the adaptations needed for the other data source?"*

The transformation turns the **category-nested, free-text SPU payload** ([02](02_existing_structure_and_FAIR_assessment.md)) into the **flat, uniform, item-keyed JSON** ([04](04_new_structure.md)). All of it is implemented in [`portable_waste_sorting.ipynb`](../portable_waste_sorting.ipynb) (Seattle) and [`dc/dc_waste_sorting.ipynb`](../dc/dc_waste_sorting.ipynb) (DC).

## Seattle transformations (existing → portable)

| # | Transformation | Why (requirement) | How |
|---|---|---|---|
| T1 | **Fetch** both taxonomy endpoints live | A1, A1.1 | `requests.get` on `taxonomy/3087/tree` and `taxonomy/3086/pages` |
| T2 | **Flatten** category-nested pages into one item array | F4, I1 | iterate `pages`, emit one record per item; the hierarchy moves into a `category_path` field instead of being the container |
| T3 | **Assign a stable `item_id`** to every record | F1, F3 | carry SPU's stable page ID (e.g. `x130614`) as the primary key |
| T4 | **Normalize disposal streams** to a controlled vocabulary | I1, I3 | map SPU's labels onto `{recycling, compost, garbage, hazardous, dropoff, special, donate}`; preserve **all** valid streams as an array (74% of items are multi-stream) rather than collapsing to one |
| T5 | **Restructure disposal text** from paragraphs to per-stream fields | I3, R1 | split SPU's guidance into `disposal_conditions` keyed by stream; keep SPU's `VoiceInstructions` summary as `explanation` |
| T6 | **Strip HTML / clean text** | quality | remove markup and normalize whitespace from instruction text |
| T7 | **Build `category_path`** breadcrumb | F2 | traverse the category tree (T1) to attach each item's path, e.g. `["Construction & Demolition", "Floors & Ceiling"]` |
| T8 | **Attach provenance** | F3, R1.2 | add `source_reference` (the item's SPU page URL) and `city_jurisdiction` to every record |
| T9 | **Add a metadata header + version** | A2, R1 | wrap items with `source`, `source_urls`, `schema_version`, `item_count`, `generated_at` |
| T10 | **Write a portable snapshot** | F4, A1.1 | serialize to `data/items.json` (310 items) usable offline by any JSON parser |

### Formatting changes required to make the visualizations run

The instructor asked specifically whether formatting had to change for the charts. Yes:

- **A `primary_stream` was derived** for coloring. Because most items have several valid streams, the Plotly **sunburst** needs a single color per slice, so the notebook computes a primary stream by a resident-priority ordering (`hazardous → recycling → compost → garbage → dropoff → special → donate`). The full multi-stream list is retained in the data and shown on hover; only the *visual* collapses to one stream.
- **`pandas.json_normalize`** flattens the nested records into a DataFrame so Plotly can consume them; list-valued fields (`disposal_streams`, `synonyms`) are handled explicitly rather than left as nested objects.
- An earlier revision tried diagonal stripes to encode multi-stream items; it was noisy at small slice sizes and was dropped in favor of one-color-per-slice + hover detail.

## DC adaptations (the second data source)

DC's open data comes from **ReCollect's "What Goes Where" API** (`api.recollect.net/.../WashingtonDC/...`), pulled by [`dc/dc_recollect_pull.py`](../dc/dc_recollect_pull.py). The **target schema is identical** to Seattle — the whole point is interoperability — but the *source* is shaped differently, so three extra adaptations were needed:

| Adaptation | Seattle | Washington, DC |
|---|---|---|
| **Stream signal** | Explicit per-stream guidance fields | **No explicit stream field.** DC exposes reusable *option templates* (`wizard_recycling`, `wizard_trash`, `wizard_drop-off_*`). Streams are **inferred** from template names and text patterns. |
| **Pagination** | Two endpoints, fetched whole | Offset/limit pagination (100-item pages) walked until exhausted |
| **Resilience** | Live fetch | Live fetch with **fallback to a cached raw snapshot** if the API is unreachable |

After those adaptations DC normalizes into the *same* `item_id / item_name / synonyms / disposal_streams / disposal_conditions / explanation / category_path / source_reference / city_jurisdiction` shape, written to [`dc/data/dc_items_portable.json`](../dc/data/dc_items_portable.json) (468 items). Six DC items could not have a stream inferred and are flagged rather than guessed — see [05 — Quality & Performance](05_quality_and_performance.md).

**Why this matters:** the same portable schema absorbed a structurally different second city with only stream-inference + pagination changes. That is the concrete evidence of interoperability the instructor appreciated, and it validates that the structure — not a single scraper — is the reusable asset.

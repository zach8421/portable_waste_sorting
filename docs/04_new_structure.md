# 04 — The New Portable Structure

*Graded area 3 · Rubric criteria #5 (differs substantially, ≥2 dimensions) and #6 (meets requirements, no scope creep)*

## The schema

Every item is one JSON object with the same shape (full sample in [`exhibits/improved_waste_sorting_structure.json`](exhibits/improved_waste_sorting_structure.json)):

| Field | Type | Description | Requirement |
|---|---|---|---|
| `item_id` | string | Stable SPU ID (e.g. `x130614`) — unique key for joins, updates, dedup | F1 |
| `item_name` | string | Display name (e.g. "Acetylene Tanks") | F2 |
| `synonyms` | array&lt;string&gt; | Alternate names / search terms | F2 |
| `disposal_streams` | array&lt;string&gt; | Valid streams from `{recycling, compost, garbage, hazardous, dropoff, special, donate}`; commonly multi-valued | I1, I3 |
| `disposal_conditions` | object&lt;string,string&gt; | Per-stream preparation instructions, keyed by stream | I3 |
| `explanation` | string | SPU's short plain-language summary | F2 |
| `category_path` | array&lt;string&gt; | Breadcrumb through the category tree | F2 |
| `source_reference` | string (URL) | Link to the authoritative SPU page | F3, R1.2 |
| `city_jurisdiction` | string | `"Seattle, WA"` (or `"Washington, DC"`) | R1.2 |

A top-level `metadata` block (`source`, `source_urls`, `schema_version`, `item_count`, `generated_at`) plus the SPU `category_tree` wrap the `items` array (A2, R1). Live snapshot: **310 Seattle items**, schema v1.0.

One full record:

```json
{
  "item_id": "x130615",
  "item_name": "Acoustic Ceiling Tile",
  "synonyms": ["Ceiling Materials", "Ceiling Panels", "Soundproofing"],
  "disposal_streams": ["garbage", "hazardous", "dropoff"],
  "disposal_conditions": {
    "garbage": "Ceiling tiles that don't contain asbestos can go in the garbage…",
    "hazardous": "If you believe the tile contains asbestos, contact the Puget Sound Clean Air Agency…",
    "dropoff": "Bring tiles without asbestos to city transfer stations. Fees apply."
  },
  "explanation": "ACOUSTIC CEILING TILE without asbestos can go in the garbage or be dropped off…",
  "category_path": ["Construction & Demolition", "Floors & Ceiling"],
  "source_reference": "https://www.seattle.gov/…/item/acoustic-ceiling-tile",
  "city_jurisdiction": "Seattle, WA"
}
```

## How it differs from the existing structure (criterion #5 — needs ≥2; this changes all 4)

| Dimension | Existing | New |
|---|---|---|
| **Information** | Category pages with free-text paragraphs | One normalized record per item, with explicit multi-stream logic and synonyms |
| **Structure** | Items nested inside category containers; hierarchy *is* the structure | Flat `items` array keyed by stable `item_id`; hierarchy demoted to a `category_path` field |
| **Format** | HTML/JS single-page app payload | Portable, versioned JSON snapshot (open, parseable in any language) |
| **Access** | Human navigation through a SPA (or undocumented endpoints) | Three documented paths: notebook, static `items.json`, and a 9-endpoint REST API |

## How it meets the requirements (criterion #6 — and nothing extra)

- **F1–F4** → stable `item_id`, structured metadata, per-item provenance, single searchable `items.json`. ✔
- **A1 / A1.1 / A2** → retrievable by ID via `GET /items/<id>`; plain HTTP/JSON, savable offline; versioned snapshot. ✔
- **I1 / I3** → one schema for all items; multi-stream relationships made explicit with per-stream conditions. ✔
- **R1 / R1.1–R1.3** → enough detail to drive a tool; MIT-licensed code with documented SPU source terms; provenance on every record; SPU preserved as the authoritative standard. ✔

**No scope creep:** the structure carries only fields the requirements call for. SPU quirks are *preserved, not "improved"* (e.g. the item "Boat" inherits SPU's "Bedroom" taxonomy ID) because SPU is the authoritative source and the dataset must reflect what they publish — silently hand-correcting would violate R1.3 and the non-consequential-ethics commitment in [06](06_ethics_and_limitations.md). The decision itself is left to the user; "depends/uncertain" outcomes are preserved rather than forced.

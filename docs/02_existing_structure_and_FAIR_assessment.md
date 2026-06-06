# 02 — Existing Structure & FAIR Assessment

*Graded area 2 · Rubric criterion #3 (assess existing structure, access, quality, performance)*
*Directly addresses instructor feedback: "Missing FAIR assessment of existing vs. the visualizations… to understand the strengths and weaknesses of the dataset that needed to be reframed."*

## What the existing structure is

SPU's *Where Does It Go?* guidance is published as **website content organized by category navigation** inside a JavaScript single-page app. A resident drills down: *Where Does It Go? → Hazardous Items → Aerosol Cans → read a paragraph.* The data that powers the page is not exposed as a documented dataset — it is delivered to the browser by two undocumented taxonomy endpoints discovered by inspecting network traffic:

| Endpoint | Contents |
|---|---|
| `https://seattle.gov/api/content/taxonomy/3087/tree` | Category hierarchy (15 top-level categories, ~56 nodes) |
| `https://seattle.gov/api/content/taxonomy/3086/pages` | Every item: title, related terms, per-stream disposal text |

A representative existing record (full sample in [`exhibits/existing_waste_sorting_structure.json`](exhibits/existing_waste_sorting_structure.json)):

```json
{
  "category_name": "Hazardous Items",
  "navigation_path": ["Where Does It Go?", "Hazardous Items"],
  "items_embedded_in_page": [{
    "title": "Aerosol Cans",
    "page_text": "AEROSOL CANS may go in the garbage but only if they are empty…",
    "related_terms": ["mace", "pepper spray", "Spray Cans", …],
    "disposal_guidance": { "recycling": "…", "garbage": "…", "hazardous": "…" },
    "possible_destinations": ["recycling", "garbage", "hazardous"],
    "source_page": "https://www.seattle.gov/…/item/aerosol-cans"
  }]
}
```

## How it is accessed (and why that limits portability)

- **Access path:** human navigation through a SPA, or undocumented JSON endpoints with no contract, no schema, and no stability guarantee.
- **Shape:** items are **nested inside category pages**, mixing the navigation hierarchy with the item data. The same item conceptually belongs to several streams, but that's encoded as free-text paragraphs plus a loosely-related `possible_destinations` list.
- **Identity:** the page is keyed by a slug in the URL fragment; there is no stable, documented item ID surfaced for reuse.

## Quality & performance of the existing information (analyzed in part)

| Dimension | Finding on the existing structure |
|---|---|
| **Consistency** | Free-form, inconsistent formatting; disposal logic lives in long paragraphs (`page_text`) rather than discrete fields. |
| **Validatability** | No schema → automated checks for missing fields, empty values, or invalid types are impractical. |
| **Reuse** | Strongly coupled to the website; cannot drive an app, sign, or API without scraping and hand-cleaning. |
| **Findability** | A resident must know the category to navigate to an item; no portable index for search/filter. |
| **Performance** | Adequate for one-off human lookups, but every consumer pays the full cost of fetching + parsing the SPA payload on each use; no cacheable, queryable artifact. |

*(Existing-structure analysis adapted from `wk7/G7_Improve_Information_Structure_Report.md`.)*

## FAIR assessment — existing structure vs. the reframed structure

Scored **L**ow / **M**edium / **H**igh against each FAIR facet. This is the strengths/weaknesses comparison the instructor asked for.

| FAIR facet | Existing SPU structure | Reframed portable structure | What changed |
|---|---|---|---|
| **F1** — globally unique, persistent IDs | **L** — slug in a URL fragment, undocumented | **H** — stable `item_id` (e.g. `x130614`) on every record | IDs promoted to first-class keys |
| **F2** — rich metadata | **M** — terms + text exist but unstructured | **H** — name, synonyms, streams, conditions, category path, provenance as discrete fields | metadata structured & typed |
| **F3** — metadata reference the data | **L** — implicit, page-embedded | **H** — each record carries its own `source_reference` URL | explicit per-item provenance |
| **F4** — indexed/searchable | **L** — behind a SPA, no index | **H** — single `items.json` + REST search endpoints | portable, queryable index |
| **A1** — retrievable by ID over open protocol | **M** — endpoints exist but undocumented | **H** — `GET /items/<item_id>`, plus offline snapshot | documented access contract |
| **A1.1** — open/free protocol | **M** — HTTP but no contract | **H** — plain HTTP/JSON, no key, savable locally | reuse without a handshake |
| **A2** — metadata persist | **L** — tied to live site | **M** — versioned snapshot with `generated_at`, `schema_version` | data survives independent of the site |
| **I1** — formal, shared representation | **L** — bespoke page payload | **H** — one consistent JSON schema for all items | uniform interoperable shape |
| **I3** — qualified references | **M** — `possible_destinations` list | **H** — `disposal_streams` + per-stream `disposal_conditions` | relationships made explicit |
| **R1.1** — clear license/usage | **L** — not stated for reuse | **M** — MIT code + documented SPU-source terms | reuse terms documented |
| **R1.2** — provenance | **M** — source page implied | **H** — `source_reference` + `city_jurisdiction` per item | provenance on every record |
| **R1.3** — domain standards | **H** — SPU *is* the standard | **H** — preserves SPU as authoritative source | standard retained, not replaced |

**Takeaway:** the existing structure is strong on *authority* (R1.3) but weak on *Findability, Interoperability, and machine-Reusability*. Those weak facets are exactly what the transformation targets — see [03 — Transformations](03_transformations.md).

# 01 — Information Story & Requirements

*Graded area 1 · Rubric criteria #1 (purpose/user/goal) and #2 (requirements/scope)*

## The user and the problem

**Who:** Seattle residents standing at the bin with an item in hand, asking one question — *"Which bin does this go in?"* — plus the developers, educators, and civic-tech contributors who build lookup tools, apps, kiosks, and bin-side signage on top of that guidance.

**The problem:** Seattle Public Utilities (SPU) publishes authoritative item-level disposal guidance through its [*Where Does It Go?*](https://www.seattle.gov/utilities/your-services/collection-and-disposal/where-does-it-go) tool, but that guidance is locked inside a JavaScript single-page app. The rules are hard to use in the moment, and the underlying data cannot be reused programmatically without reverse-engineering the page. Residents guess and make mistakes; a business that wants to put a simple sorting visual above its bins has to re-derive the rules by hand.

**Why it matters:** Wrong-bin items contaminate recycling and compost streams, raise processing cost, and undercut the city's waste-reduction goals. Making the *same* official guidance portable lets one dataset drive many trustworthy experiences — a search box, an app, a printed sign, a voice assistant, a classroom exercise — without anyone re-keying the rules.

## The insight area

This project is an **Analyze + Visualize + Automate** play on a single portable structure: it restructures existing public information so it can be *queried, charted, and embedded* anywhere, rather than navigated one click at a time on a website.

## Information experience (two concrete uses)

- **Individual use** — search an item by name or synonym and get its bin(s), per-stream preparation steps, a plain-language explanation, and a link back to the SPU source.
- **Business use** — map a menu or product list to disposal categories and generate clear visuals above bins so customers sort correctly without confusion.

The same dataset supports both. *(Source slides: `wk4/G4/Slides.md`.)*

## Requirements (what's in scope vs. out of scope)

Requirements are expressed against FAIR principles (full detail in [02 — Existing Structure & FAIR Assessment](02_existing_structure_and_FAIR_assessment.md); originals in `wk5/G5_portable_waste_sorting.txt`).

**In scope — the portable structure MUST:**

| ID | Requirement |
|----|-------------|
| F1 | Every item carries a **stable SPU `item_id`** (unique key for joins, updates, dedup). |
| F2 | Every item includes useful metadata: name, synonyms, category path, disposal guidance. |
| F3 | Metadata clearly points back to the item it describes. |
| F4 | Items are stored in a **searchable JSON** lookup structure. |
| A1 / A1.1 | Items are retrievable by `item_id`, fetched over standard web protocols and saved locally for offline reuse. |
| I1 | A **single consistent JSON schema** is used for all items. |
| I3 | Each item references its source data / source link. |
| R1 / R1.1–R1.3 | Each item holds enough detail to power a sorting tool, documents its license/usage terms, records provenance, and follows SPU guidance as the domain standard. |

**Explicitly out of scope:**

- Jurisdictions other than Seattle (the [`dc/`](../dc/) folder is a *separate interoperability demonstration*, not part of the core Seattle product).
- Making the disposal decision *for* the user — the structure preserves "depends/uncertain" outcomes rather than forcing a single answer.
- Unusual commercial, hazardous, and construction waste beyond what SPU publishes (redirected to SPU).
- Non-English content and any feature requiring user accounts or personal data.

## Portability features captured in the requirements

Open JSON format (no proprietary lock-in), stable identifiers, a shared schema, per-item provenance, multi-valued disposal streams with per-stream conditions, and three independent access paths (notebook, static snapshot file, REST API). Together these let the data move between systems unchanged — the definition of portability for this product.

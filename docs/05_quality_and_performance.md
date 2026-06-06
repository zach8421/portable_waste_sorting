# 05 — Quality & Performance (Desired vs. Measured)

*Graded area 5 · Rubric criteria #9 (quality) and #10 (performance)*
*Directly addresses instructor feedback: "The expectations of quality should be documented, so an end user knows what to expect in case something changes" and "some documentation here, and expectations about how quickly the data should be processed might be helpful."*

Targets come from [`../TESTPLAN.md`](../TESTPLAN.md). The measured columns below were produced by validating the committed snapshot and load-testing the running Flask API on **2026-06-05** (commands at the bottom).

---

## What an end user should expect (the short version)

- **310 Seattle items** (468 for the DC demo), every one with a stable unique ID, valid disposal stream(s), and a link back to the authoritative SPU page.
- Answers are **as current as the snapshot's `generated_at`** field (currently `2026-04-21`). SPU is always the tie-breaker; re-running the notebook refreshes the data.
- A small number of items are **enrichment-incomplete** (no extra synonyms, or SPU published no one-line summary). Disposal guidance is still present for these — see the gap table.
- The API answers in **single-digit milliseconds** locally; this is a small, static, in-memory dataset, not a high-load service.

---

## Quality — desired vs. measured

| Metric | Target (TESTPLAN) | Measured (Seattle, 310) | Measured (DC, 468) | Result |
|---|---|---|---|---|
| JSON validity | Always parses | Parses | Parses | ✅ |
| `item_id` present & unique | 0 duplicates | 310/310 unique, 0 dup | 468/468 unique, 0 dup | ✅ |
| `item_name` present | 100% | 100% | 100% | ✅ |
| Valid disposal streams | 0 unknown | 0 unknown | 0 unknown | ✅ |
| Stream ↔ conditions consistency | every stream has a condition | 0 mismatches | 0 mismatches | ✅ |
| File size | < 2 MB | 0.39 MB | 1.24 MB | ✅ |
| Multi-stream preserved | n/a (feature) | 230 items (74%) | 311 items (66%) | ✅ |

### Known quality gaps and remediation (the honest part)

| Gap | Seattle | DC | Cause | Remediation plan |
|---|---|---|---|---|
| Items with **no disposal stream** | 1 | 6 | Source record had no mappable stream / no inferable template | Flag in validation (already counted); review against source and either add a mapping rule or mark `needs_review`. Not silently guessed. |
| Empty `explanation` | 73 | 6 | SPU's `VoiceInstructions` summary field is blank for some items | Non-blocking: `disposal_conditions` still carries the actionable text. Fallback plan: derive a one-line summary from the primary stream's condition when `explanation` is empty. |
| Empty `synonyms` | 12 | 121 | Source had no alternate terms (more common in DC's ReCollect data) | Enrichment-only; does not affect lookup by name. Optional future step: seed synonyms from item-name tokenization. |

These are **differences between desired and final quality**, documented with a remediation path as the rubric requires. None blocks the core lookup: `item_id`, `item_name`, and at least one valid `disposal_stream` are present for ≥99.7% of Seattle items.

---

## Performance — desired vs. measured

Measured with `curl -w '%{time_total}'`, median of 10 runs, Flask API loaded with the 310-item snapshot, local loopback.

| Test | Target | Measured (median) | Result |
|---|---|---|---|
| API startup → first 200 | starts cleanly (< ~2.5s) | **0.26 s** | ✅ |
| Single item lookup `/items/<id>` | < 50 ms | **1.1 ms** | ✅ |
| Full item list `/items` | < 200 ms | **1.5 ms** | ✅ |
| Search `/search?q=cardboard` | < 250 ms | **1.4 ms** | ✅ |
| Stats `/stats` | < 250 ms | **1.2 ms** | ✅ |
| Basic load (50 requests across endpoints) | no 500s / drops | **50/50 → 200, zero 500s** | ✅ |
| Notebook full run | < 60 s | n/a this run (snapshot validated directly) | ➖ |

**Why so fast:** the store is loaded once at startup into an in-memory dict keyed by `item_id` (O(1) lookups); the dataset is small (0.39 MB). The measured margins are large, so there is no performance gap to remediate at this scale. *If hosted publicly*, the documented remediation is the TESTPLAN monitoring plan (UptimeRobot, Flask logs, GitHub Actions JSON/endpoint checks) — added only if/when deployed, to avoid over-engineering a static dataset.

### Correctness spot check (criterion #8 corroboration)

`GET /stats` returns `total_items=310`, `items_with_multiple_streams=230`, and stream counts (`garbage 231, recycling 105, dropoff 100, donate 87, compost 62, special 51, hazardous 48`) that match an independent recomputation over `data/items.json`. Error paths return JSON, not HTML stack traces: `404 {"error":"item not found"}`, `400 {"error":"invalid stream", …}`, `404 {"error":"route not found"}`.

---

## How to reproduce

```bash
# Quality audit of the snapshot(s)
python3 - <<'PY'
import json
from collections import Counter
d=json.load(open("data/items.json")); items=d["items"]
ids=[i["item_id"] for i in items]
print("items",len(items),"unique",len(set(ids)),"dupes",len(ids)-len(set(ids)))
PY

# Performance: start API and time endpoints
python3 -m flask --app i8/which_bin_api.py run --port 5055 &
curl -s -o /dev/null -w '%{time_total}\n' http://127.0.0.1:5055/items/x130614
curl -s -o /dev/null -w '%{http_code} %{time_total}\n' http://127.0.0.1:5055/search?q=cardboard
```

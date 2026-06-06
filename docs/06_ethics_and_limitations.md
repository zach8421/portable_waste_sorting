# 06 — Availability, Limitations, Ethics & Societal Impact

*Supporting artifact (originally the G6 statement) — informs scope (area 1), provenance (area 2), and quality/remediation (area 5).*

## Availability

- Restructures SPU waste-sorting guidance into a portable, item-based **JSON** dataset; the same records can be exported to CSV for non-developer reuse.
- Each item carries an ID, name, synonyms, disposal streams, per-stream conditions, explanation, source link, and jurisdiction.
- Follows **FAIR** principles via stable IDs, open formats, a shared schema, and per-item provenance (see [02](02_existing_structure_and_FAIR_assessment.md)).
- Supports **OECD 2021 data portability** by avoiding proprietary lock-in — the dataset moves freely between lookup tools, apps, kiosks, and bin-side signage.

## Limitations

- **Seattle-only** core; not validated for other jurisdictions. (The `dc/` folder is an interoperability demonstration, not a validated DC product.)
- Rules change; the dataset needs ongoing refresh and may lag SPU between snapshots (`generated_at` makes staleness visible).
- Many items are **conditional** (clean vs. soiled, size, material, contamination); the user still judges condition.
- Coverage is finite; unusual commercial, hazardous, and construction waste is redirected to SPU.
- Text-based and **English-only** at launch.
- **Decision support, not a replacement** for official guidance.

## Ethics

**Virtue** — prioritizes clarity, honesty, and equal access to civic information; no accounts, paywalls, or proprietary formats; cites the SPU source on every record so users can verify answers themselves.

**Consequential** — intended benefit is fewer wrong-bin items and more consistent guidance across tools that reuse the data; main risks are outdated guidance or reuse outside Seattle, mitigated by source links, `generated_at` dates, scope notes, and preserved "depends/uncertain" outcomes instead of forced answers.

**Non-consequential** — treats SPU as authoritative; attributes every item, preserves conditions and warnings, avoids silent rewriting, follows source-reuse terms, and requires no personal accounts or user data; the disposal decision stays with the user.

## Societal impact

- Helps residents sort more confidently and supports Seattle's recycling, composting, and waste-reduction goals.
- Lowers the cost for schools, restaurants, and event venues to produce clear, consistent sorting guidance instead of re-deriving rules independently.
- **Equity caveat:** English-only coverage under-serves some residents and workers; multilingual support is a documented future improvement.

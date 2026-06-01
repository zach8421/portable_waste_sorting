# Washington, DC Waste-Sorting Data

This folder adapts the portable waste-sorting workflow to Washington, DC using
the ReCollect API behind Zero Waste DC's "What Goes Where" tool.

## Files

- `dc_waste_sorting.ipynb` - notebook version of the DC workflow. It fetches
  DC material records, normalizes them into a portable item schema, visualizes
  stream distribution, provides `lookup()` / `explain()`, saves JSON, and runs
  validation checks.
- `dc_recollect_pull.py` - standalone pull script for the raw ReCollect records
  and a lightly normalized DC snapshot.
- `data/dc_items_portable.json` - generated portable DC dataset with the same
  core fields used by the Seattle data: item name, synonyms, disposal streams,
  instructions, explanation, source URL, and jurisdiction.

## Run

From this folder:

```bash
pip install pandas plotly requests jupyter
jupyter notebook dc_waste_sorting.ipynb
```

Or run the standalone pull script:

```bash
python dc_recollect_pull.py
```

The script writes into this folder's `data/` directory even if it is launched
from the repository root.

## Notes

Seattle's source API exposes explicit stream fields such as `Garbage`,
`Recycling`, and `Hazardous`. DC's ReCollect records expose reusable option
templates instead, so the notebook infers comparable streams from templates
such as `wizard_recycling`, `wizard_trash`, `wizard_bulk_trash_collection`, and
`wizard_drop-off_*`.

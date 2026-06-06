# Rubric Map — where each criterion is satisfied

This repository is the IMT 542 final project, **Portable Waste Sorting**. The table maps each of the 10 graded criteria (5 pts each, 50 total) to the artifact that satisfies it, so grading is direct.

| # | Criterion | Primary artifact(s) | Instructor's prior mark |
|---|-----------|---------------------|--------------------------|
| 1 | Information story — purpose, user, goal clear | [docs/01_information_story.md](01_information_story.md) · [docs/PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) | Yes |
| 2 | Requirements define scope & portability features | [docs/01_information_story.md](01_information_story.md) (requirements table) | Yes |
| 3 | Existing structure analyzed (structure, access, quality, performance) + **FAIR** | [docs/02_existing_structure_and_FAIR_assessment.md](02_existing_structure_and_FAIR_assessment.md) · [exhibits/existing_waste_sorting_structure.json](exhibits/existing_waste_sorting_structure.json) | Yes *(FAIR of existing was the flagged gap — now added)* |
| 4 | Transformations clear & fully defined (incl. DC adaptations) | [docs/03_transformations.md](03_transformations.md) · [../portable_waste_sorting.ipynb](../portable_waste_sorting.ipynb) · [../dc/](../dc/) | Yes *(explicit write-up was requested — now added)* |
| 5 | New structure differs substantially (≥2 of info/structure/format/access) | [docs/04_new_structure.md](04_new_structure.md) · [exhibits/improved_waste_sorting_structure.json](exhibits/improved_waste_sorting_structure.json) | Yes |
| 6 | New structure meets requirements, no scope creep | [docs/04_new_structure.md](04_new_structure.md) (requirements mapping) | Yes |
| 7 | Information accessible as documented | [../README.md](../README.md) · [../i8/which_bin_api.py](../i8/which_bin_api.py) · demo videos | **Was "No?" → fixed:** public repo + 3 documented access paths |
| 8 | Information correct & complete | [docs/05_quality_and_performance.md](05_quality_and_performance.md) (correctness spot check) · [../data/items.json](../data/items.json) | Yes |
| 9 | Quality desired vs. final + remediation | [docs/05_quality_and_performance.md](05_quality_and_performance.md) · [../TESTPLAN.md](../TESTPLAN.md) | **Was "Somewhat" → fixed:** measured results + gap/remediation table |
| 10 | Performance desired vs. final + remediation | [docs/05_quality_and_performance.md](05_quality_and_performance.md) · [../TESTPLAN.md](../TESTPLAN.md) | **Was "Maybe" → fixed:** measured timings vs. targets |

## Deliverables checklist (from the assignment)

- [x] **README.md** describing the project, the download/convert code, and how the data is exposed as an API — [../README.md](../README.md)
- [x] **Presentation `.pptx`** in the repo — [../Portable_Waste_Sorting.pptx](../Portable_Waste_Sorting.pptx)
- [x] **Supporting artifacts** for all five graded areas with clear names — this `docs/` folder
- [x] Public GitHub repository — `https://github.com/zach8421/portable_waste_sorting`

## Supporting / context artifacts

- [docs/06_ethics_and_limitations.md](06_ethics_and_limitations.md) — availability, limitations, ethics, societal impact
- [../TESTPLAN.md](../TESTPLAN.md) — full functional/performance/quality test plan with alarms & actions
- [../dc/README.md](../dc/README.md) — the Washington, DC interoperability demonstration

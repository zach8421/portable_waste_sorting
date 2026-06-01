# Portable Waste-Sorting - Test Plan

## Purpose

This document outlines the testing strategy for the **Portable Waste-Sorting
Information for Seattle Residents** system. The goal is to make sure the data,
notebook, and API remain accurate, usable, and reliable for people who want to
look up how to dispose of common items in Seattle.

The plan is intended to be a living reference during implementation and future
maintenance.

---

## System Overview

- **Data source**: Seattle Public Utilities "Where Does It Go?" JSON endpoints
- **Data file**: `data/items.json`
- **Notebook**: `portable_waste_sorting.ipynb`
- **API**: Flask app in `i8/which_bin_api.py`
- **Main API endpoints**:
  - `GET /`
  - `GET /items`
  - `GET /items/<item_id>`
  - `GET /search?q=&stream=&category=`
  - `GET /streams`
  - `GET /streams/<stream>`
  - `GET /categories`
  - `GET /categories/<name>`
  - `GET /stats`

Valid disposal streams are `garbage`, `recycling`, `compost`, `donate`,
`dropoff`, `hazardous`, and `special`.

---

## Test Objectives

- Ensure the JSON data follows the G3 waste-sorting schema
- Confirm API endpoints return the expected JSON responses
- Catch missing, duplicate, or invalid item records
- Verify search, stream, category, and stats features work correctly
- Confirm the API is fast enough for a local demo or small hosted deployment
- Define simple alarms and actions for data or API failures

---

## Functional Testing

| Test Case | Description | Method | Expected Result |
|-----------|-------------|--------|-----------------|
| SPU Source Access | Fetch the SPU pages and tree endpoints | Run notebook fetch cells | Both endpoints return valid JSON |
| JSON File Validity | Check `data/items.json` can be parsed | `python3 -m json.tool data/items.json` | File parses without error |
| Required Fields | Check each item has the G3 fields | Script or notebook assertions | No item is missing required fields |
| Unique Item IDs | Check all `item_id` values | Compare list length to unique set length | No duplicate IDs |
| Valid Streams | Check each disposal stream value | Compare against approved stream list | No unknown streams |
| Item Count Check | Count generated items | Notebook assertion | Count stays in a reasonable range, currently about 310 |
| API Info | Call `GET /` | Browser, curl, or pytest | 200 response with endpoint list |
| List Items | Call `GET /items` | Browser, curl, or pytest | 200 response with item count and item summaries |
| Valid Item Lookup | Call `GET /items/x130614` | Browser, curl, or pytest | 200 response with the full item record |
| Missing Item Lookup | Call `GET /items/does-not-exist` | Browser, curl, or pytest | 404 JSON error |
| Keyword Search | Call `GET /search?q=cardboard` | Browser, curl, or pytest | Matching items are returned |
| Stream Search | Call `GET /search?stream=compost` | Browser, curl, or pytest | All returned items include `compost` |
| Category Search | Call `GET /search?category=Plastic` | Browser, curl, or pytest | Returned items match the category |
| Empty Search | Call `GET /search` | Browser, curl, or pytest | 400 JSON error |
| Invalid Stream | Call `GET /search?stream=notreal` | Browser, curl, or pytest | 400 JSON error with valid streams listed |
| Stream Rollup | Call `GET /streams` | Browser, curl, or pytest | Counts are returned by stream |
| Category Rollup | Call `GET /categories` | Browser, curl, or pytest | Category names and counts are returned |
| Stats Endpoint | Call `GET /stats` | Browser, curl, or pytest | Total items, stream counts, and top categories are returned |
| Unknown Route | Call `GET /not-a-route` | Browser, curl, or pytest | 404 JSON error |

---

## Performance Testing

| Test Case | Description | Tool | Target |
|-----------|-------------|------|--------|
| API Startup | Start the Flask app and call `/` | Terminal + browser/curl | Server starts without traceback |
| Single Item Lookup | Call `/items/x130614` repeatedly | `curl -w` | Median response under 50 ms locally |
| Full Item List | Call `/items` | `curl -w` | Median response under 200 ms locally |
| Search Request | Call `/search?q=cardboard` | `curl -w` | Median response under 250 ms locally |
| Stats Request | Call `/stats` | `curl -w` | Median response under 250 ms locally |
| Basic Load | Send 50 requests across endpoints | Bash loop, `hey`, or similar | No 500 errors or dropped requests |
| Notebook Run | Run all notebook cells | Jupyter or Colab | Completes in under 60 seconds |
| Data File Size | Check `data/items.json` size | `du -h data/items.json` | Remains under 2 MB |

Example timing command:

```bash
curl -s -o /dev/null -w '%{http_code} %{time_total}\n' \
  http://127.0.0.1:5000/search?q=cardboard
```

---

## Quality Metrics

| Metric | Goal |
|--------|------|
| JSON validity | `data/items.json` always parses successfully |
| Schema completeness | 100% of items have required G3 fields |
| Stream validity | 0 unknown disposal streams |
| ID uniqueness | 0 duplicate `item_id` values |
| API correctness | All functional endpoint tests pass |
| Error handling | All errors return JSON, not HTML stack traces |
| Response time | Most API responses complete under 250 ms locally |
| Data freshness | Data is reviewed or regenerated at least once per quarter |

---

## Alarms & Actions

| Alarm | Trigger | Action |
|-------|---------|--------|
| SPU Fetch Failure | Notebook cannot reach the SPU endpoints | Stop the refresh and keep the previous `data/items.json` |
| Invalid JSON | `data/items.json` fails to parse | Fix the data generation step before committing |
| Missing Required Field | Any item is missing a G3 field | Identify the item and fix the transform logic |
| Duplicate Item ID | Two records have the same `item_id` | Review the source data and prevent overwrite in the API lookup map |
| Unknown Stream | A stream outside the approved list appears | Update the mapping intentionally or correct the transform |
| Large Item Count Change | Item count changes by more than about 20% | Review the SPU response before accepting the new snapshot |
| API Startup Failure | Flask app exits or logs a traceback | Check that `data/items.json` exists and is valid |
| API 500 Error | Any smoke test returns a 500 response | Capture the failing endpoint and fix before demo/release |
| Slow Response | Local response time is consistently above target | Check data size and endpoint logic |
| Stale Data | Snapshot has not been reviewed for a quarter | Rerun the notebook and review the diff |

Planned monitoring tools if the API is hosted:

- UptimeRobot or BetterStack for uptime checks
- Flask logs for API errors
- GitHub Actions for automated JSON and endpoint checks

---

## Continuous Testing & Maintenance

- Run the notebook from top to bottom when refreshing the data
- Validate `data/items.json` before committing changes
- Manually smoke-test the Flask API before demos
- Add pytest tests later for the main API endpoints
- Review the data quarterly or when SPU changes its source pages
- Record any known data issues or source changes in the repository

---

## Status Summary

| Area | Status |
|------|--------|
| Notebook data generation | Implemented |
| JSON data file | Implemented with about 310 items |
| Flask API endpoints | Implemented |
| Error handling | Implemented for common 400 and 404 cases |
| Functional tests | Currently manual; pytest planned |
| Performance tests | Currently manual timing checks |
| Monitoring | Planned if hosted |

---

## Future Additions

- Pytest suite for the Flask API
- JSON schema validation for `data/items.json`
- GitHub Actions workflow for automatic checks
- Scheduled data-refresh review
- Hosted uptime monitoring if the API is deployed publicly

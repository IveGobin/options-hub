# Options Hub — project instructions

## Options P&L rules
Before any change that touches option P&L, stock P&L from assignments or P&L aggregation (monthly chart,
Closed P&L matrix / quarters, KPIs) in `IBKR Unified Analyzer.html`, read @OPTIONS_PNL_RULES.md, follow it,
check its invariants, and update it (including the changelog) in the same change.

## Always bump the version
Every change to an app file must bump its visible version label, so the user can tell after opening the app that it refreshed.

- Bump the minor number on each change: `v2.6` → `v2.7` → … (`v2.9` → `v2.10`).
- Version labels:
  - `IBKR Unified Analyzer.html`: `v2.6` in the `<h1>` of the top bar
  - `IBKR Tax Calculator.html`: `v1.0` in the `<h1>`
  - `Compound Growth Simulator.html`: `v1.1` in `.gs-section-title`
  - `Put Coach.html`: `v1.0` in `.title` (span `.ver`)
  - `Loan Calculator.html`: `v1.0` in `.gs-section-title` (span `.ver`)
  - `Loan vs Invest.html`: `v1.0` in `.hdr-title` (span `.ver`)
  - `index.html` (hub): `v1.0` in the welcome `<h1>` (span `.ver`)
  - A new tool page gets a `v1.0` label in its main title from the start.
- The hub (`index.html`) opens tools with a `?v=<timestamp>` cache-buster, so a new deploy shows up immediately.
- Mobile preview (`IBKR Unified Analyzer (mobile preview).html`): never edit it by hand. Change `make_mobile_preview.py`, bump `PREVIEW_VERSION` there, then run `python make_mobile_preview.py`. The label shows as e.g. `v2.6 · m5` (original version · preview iteration). When the original's version changes, regenerate the preview so it picks that up.
- Mention the new version in the commit message.

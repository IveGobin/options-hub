# Options Hub — project instructions

## Always bump the version
Every change to an app file must bump its visible version label, so the user can tell after opening the app that it refreshed.

- Bump the minor number on each change: `v2.6` → `v2.7` → … (`v2.9` → `v2.10`).
- Version labels:
  - `IBKR Unified Analyzer.html`: `v2.6` in the `<h1>` of the top bar
  - `IBKR Tax Calculator.html`: `v1.0` in the `<h1>`
  - `Compound Growth Simulator.html`: `v1.1` in `.gs-section-title`
  - Other tool pages: if one has no version label yet, ask before adding one.
- Mobile preview (`IBKR Unified Analyzer (mobile preview).html`): never edit it by hand. Change `make_mobile_preview.py`, bump `PREVIEW_VERSION` there, then run `python make_mobile_preview.py`. The label shows as e.g. `v2.6 · m5` (original version · preview iteration). When the original's version changes, regenerate the preview so it picks that up.
- Mention the new version in the commit message.

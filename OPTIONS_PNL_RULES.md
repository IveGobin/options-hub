# Options P&L rules — IBKR Unified Analyzer

Reference for every change to how `IBKR Unified Analyzer.html` calculates option P&L, stock P&L from
assignments, or any P&L aggregation (monthly chart, Closed P&L matrix / quarters, KPIs, stat badges).
**Read this before such a change, keep the code consistent with it, check the invariants below, and
update this file (incl. the changelog) in the same change.**

## 1. Data sources (IBKR Activity Statement CSV)

| Section | Used for |
|---|---|
| `Trades` – `Order` rows (Equity and Index Options) | proceeds, commission, dates, codes `O` / `C` / `A` (assignment) / `Ex` (exercise) / `Ep` (expired); `Basis` column of `A`/`Ex` rows = option premium |
| `Trades` – `SubTotal` rows | IBKR realized P/L and net quantity per option symbol (one row per loaded file → summed) |
| `Realized & Unrealized Performance Summary` | list of option symbols, open vs. closed (`unrTotal`) |
| `Open Positions` | open options: quantity, cost basis (premium), value, unrealized P/L |
| `Financial Instrument Information` | option symbol aliases after corporate actions (see §4) |
| `Trades` – `Order` rows (Stocks) | FIFO stock lots |

## 2. Assignment / exercise rule (the core rule)

**The option premium is realized OPTION P&L. Shares from an assignment are booked at the STRIKE price.**

- IBKR does the opposite: it reports realized P/L = 0 on the assignment row and rolls the premium into
  the share cost basis (`strike − premium/sh` for puts, `strike + premium/sh` for calls). This app does not.
- Formula, per option symbol:
  `realPL = Σ SubTotal Realized P/L + Σ Basis of the symbol's A / Ex rows` (Basis is signed:
  + credit kept on a short option, − debit paid on a long option that is exercised).
- Month of realization = date of the assignment (last closing trade, see §3).
- Examples (2026 statement):
  - `EOSE 16OCT26 3.5 P`: sold for $122 − $5.39 commission, assigned 2026-10-12 → realized **+$116.61** in Oct '26; 500 EOSE shares at **$3.50**.
  - `NFLX 17JUL26 75 P`: SubTotal −1,167.63 + assigned premium 88.30 → **−$1,079.34**.
  - `TEM 21AUG26 60 C` (short call assigned): premium +$24.96 is option P&L; the 100 TEM shares are sold at **$60**.
- In code: `optTradeMap[sym].realPL` / `optRealPL(sym)` is the **single source of truth**. It feeds
  `closedPL` (Closed P&L matrix, quarters, stat badges, win rate, “Options income”), `optByMonth`
  (monthly chart), `o.tradePL` (put/call split) and `assignedPositions[].realAtAssign`.
  Never compute realized option P/L from `proceeds + comm` or from the raw SubTotal value elsewhere.
- Stocks: the FIFO book (`STOCKS TABLE`) books assigned shares at the strike (`perShare = 0`); no premium adjustment.
- Assigned table: “Stock cost / share” = strike; break-even (strike ∓ premium) is shown for information only.
- Closed options detail table includes assigned contracts (status `Assigned`, buyback 0).
- Win rate: an assigned short option with positive premium counts as a win.

## 3. Month attribution

- Closed option: month of `lastCloseDate` = last trade with code `C`, `Ep`, `A`, `Ex` or non-zero realized P/L
  (not simply the last trade — a symbol can be reopened after being closed).
- Open option: its premium goes into the **expiry month** as open premium (hatched bar).
- Partially closed open option: realized part (`realPL`) in the month it was realized; the open part in the expiry month.

## 4. Open vs. closed, symbol aliases

- An option is open when its (canonical) symbol is in `Open Positions`.
- Corporate actions can rename an option: e.g. `MOD 20NOV26 135 P` (Trades, R&U) → `MOD1 20NOV26 135 P`
  (Open Positions). `Financial Instrument Information` lists both OCC codes in one row with the new name as
  Description. `optAlias` maps old → new and every option symbol in Trades / SubTotal / R&U is canonicalised,
  otherwise the open position is treated as closed and its premium lands in the wrong month.

## 5. Stocks

- FIFO across all loaded files: buy cost = |proceeds| + |commission|; sell = proceeds − |commission|.
- Assigned shares at the strike (§2).
- Known limitation: fallbacks to IBKR’s own basis (quantity mismatch → `Open Positions` cost basis;
  shares sold that are not in the loaded history → `Basis` of the sell row; symbols with no trades → R&U)
  **include** assignment premium. Loading the full history avoids these fallbacks.
- The “IBKR statement” note under the stock table shows IBKR’s figures, which differ by the assigned premium.

## 6. Invariants — check after every change

Run the app with both statements loaded (2025 + 2026) and check:

1. For every month: closed part of the monthly options chart = same month in the Closed P&L matrix.
2. Sum of the quarters = sum of the months; a quarter with only one month so far equals that month
   (2026 statement: Oct '26 = Q4 '26 = **+$1,403.63**).
3. Moving premium between options and stocks must not change the total: options realized + stocks P&L in
   USD is the same before and after (2026: options +753.47 ⇔ USD stocks −753.47), and the NAV
   reconciliation difference is unchanged.
4. `MOD1 20NOV26 135 P` premium (+448.95) is in Nov '26 open premium, not in Sep '26.
5. Assigned shares show the strike as cost (EOSE lot 2026-10-12: $3.50/sh).

## 7. Known pitfalls

- IBKR SubTotal realized P/L excludes the premium of assigned contracts; IBKR stock cost basis includes it.
- Renamed symbols after corporate actions (§4).
- Multi-leg positions (spreads, synthetics): use the signed premium (`premiumCollected`, long = debit = negative).
- Several loaded statements: SubTotal rows per file must be **summed**, not overwritten.
- After changing the main HTML, regenerate the mobile preview (`python make_mobile_preview.py`), see CLAUDE.md.

## Changelog

- 2026-10-31 (v2.9): introduced the assignment rule (premium = option P&L, shares at strike) as a single
  source of truth (`optRealPL`); fixed monthly chart ≠ quarter matrix; added option alias mapping
  (MOD → MOD1); SubTotal rows summed across files; assigned contracts shown in the closed detail table.

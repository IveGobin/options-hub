// Trading Hub — shared i18n + theme helper
// Include this in each tool file: <script src="hub_shared.js"></script>

const HUB_I18N = {
    en: {
      nav_portfolio: 'Portfolio', nav_cost: 'Cost & Premium', nav_coach: 'Put Coach', nav_put_an: 'Put Analyzer', nav_call_an: 'Call Analyzer',
      nav_put_cal: 'Put Expiry Calendar', nav_call_cal: 'Call Expiry Calendar', nav_growth_sim: 'Growth Simulator', theme_dark: 'Dark', theme_light: 'Light', theme_toggle: 'Toggle theme',
      lang_en: 'English', lang_hr: 'Croatian', lang_switch: 'Language',
      cal_put_title: 'Put Expiry Calendar', cal_call_title: 'Call Expiry Calendar',
      cal_hint_put: 'Load your IBKR put export CSV (e.g. IBKR - PUT.csv) to see expirations.',
      cal_hint_call: 'Load your IBKR call export CSV (e.g. IBKR - CALL.csv) to see expirations.',
      cal_load_csv: 'Load CSV', cal_no_file: 'No file loaded', cal_past: 'past', cal_pos_badge: '{n} pos', cal_empty: 'empty',
      cal_total: 'Total', cal_no_exp: 'No expirations this week', cal_premium: 'premium', cal_exp: 'exp',
      cal_hdr_ticker: 'Ticker', cal_hdr_strike: 'Strike / Exp', cal_hdr_qty: 'Qty', cal_hdr_exposure: 'Exposure', cal_hdr_premium: 'Premium',
      rpt_title: 'Cost & premium (per ticker)', rpt_sub: 'Combine your portfolio export with IBKR put and call CSVs. Adjusted average cost per share includes option cash flows by ticker. Use the same file shapes as in Portfolio and the Put/Call analyzers.',
      rpt_up1: '1 · Portfolio CSV', rpt_up2: '2 · Puts CSV', rpt_up3: '3 · Calls CSV', rpt_no_file: 'No file',
      rpt_slider_prefix: 'Include open (non-expired) option premium: ', rpt_slider_suffix: '%',
      rpt_hint: '0% (default): only realized option P&L — Closed and Expired rows. 100%: add the full Total Premium from Open positions (premium in play). Values between 0–100% blend open premium linearly.',
      rpt_empty: 'Load at least one CSV (portfolio and/or put and/or call export) to build the report.',
      rpt_th_ticker: 'Ticker', rpt_th_shares: 'Shares', rpt_th_stock_basis: 'Stock basis', rpt_th_puts: 'Puts (opt. $)', rpt_th_calls: 'Calls (opt. $)',
      rpt_th_opt: 'Options total', rpt_th_net: 'Net basis', rpt_th_avg: 'Adj. avg $/sh', rpt_legend_h: 'How this works',
      rpt_legend_1: 'Stock basis uses Quantity × Average price from the portfolio CSV when possible; otherwise Current value − P/L.',
      rpt_legend_2: 'Option $ = realized P&L on Closed / Expired rows (Premium Exp, else Total Premium) + (slider %) × Total Premium on Open rows.',
      rpt_legend_3: 'Net basis = stock basis − options total (cash received on shorts lowers effective cost). Adj. avg = net basis ÷ shares.',
      po_page_title: 'Portfolio Optimizer', po_logo_sub: 'Portfolio Optimizer', po_upload_strong: 'Choose CSV file', po_upload_or: 'or drag & drop',
      po_no_file: 'No file loaded', po_total_value: 'Total Value', po_positions: '{n} positions', po_cash: 'Cash',
      po_unrealised: 'Unrealised P&L', po_total_ret: '{n}% total return', po_pl_pct: '{sign}{n}% total return', po_stocks: 'Stocks Value', po_allocation: 'Allocation', po_portfolio: 'Portfolio',
      po_pct_of_pf: '{pct}% of portfolio',
      po_holdings: 'Holdings & Limits', po_th_ticker: 'Ticker', po_th_price: 'Price', po_th_qty: 'Qty', po_th_value: 'Value', po_th_alloc: 'Allocation',
      po_th_limits: 'Limits', po_th_status: 'Status', po_th_pl: 'P&L', po_th_action: 'Action', po_empty_pf: 'Load a CSV file to see your portfolio',
      po_theme_toggle: 'Toggle theme', po_chart_assets: '{n} assets',
      an_csv_empty: 'CSV is empty or has no data.', an_kpi_real: 'Realized P&L', an_kpi_prem: 'Premium in play', an_kpi_exp: 'Open exposure',
      an_kpi_open_n: 'Open positions', an_kpi_closed_n: 'Closed positions', an_sec_open: 'Open positions — premium in play',
      an_sec_prem_ticker: 'Premium in play — share by ticker', an_sec_monthly: 'Premium in play — next 4 months', an_sec_pl: 'P&L distribution by ticker',
      an_pie_open_t: 'Open positions — premium by ticker', an_pie_pos: 'Positive profits — share by ticker', an_pie_neg: 'Losses — share by ticker',
      an_empty_data: 'No data', an_empty_open: 'No open positions', an_empty_closed: 'No closed positions', an_trade: 'trade', an_trades: 'trades',
      an_profit: '▲ Profit', an_loss: '▼ Loss', an_reset: 'New file', an_days_left: 'Days left',
      an_open_hdr_date: 'Open date', an_open_hdr_exp: 'Exp. date', an_open_hdr_strike: 'Strike', an_open_hdr_prem: 'Premium in play',
      an_drop_label: 'Interactive Tracker', an_put_h1: 'IBKR <span>PUT</span><br>Options Analyzer', an_put_drag_strong: 'Drag CSV here or click',
      an_put_drop_line: 'Load IBKR PUT export (.csv)', an_put_pick: 'Choose file', an_dash_h1: 'PUT Options <span>Dashboard</span>', an_reset_btn: 'New file',
      an_th_ticker: 'Ticker', an_th_open_date: 'Open date', an_th_exp: 'Exp. date', an_th_strike: 'Strike', an_th_qty: 'Qty',
      an_th_prem_open: 'Premium in play', an_th_exposure: 'Exposure', an_th_days: 'Days left', an_sec_closed: 'Closed positions — P&L by ticker',
      an_pie_neg_title: 'Losses — share by ticker',
      an_call_drop: 'Load IBKR CALL export (.csv)', an_call_h1: 'IBKR <span>CALL</span><br>Options Analyzer', an_call_drag_strong: 'Drag CSV here or click',
      an_call_drop_line: 'Load IBKR CALL export (.csv)', an_call_pick: 'Choose file', an_dash_h1_call: 'CALL Options <span>Dashboard</span>', an_reset_btn_call: 'New file',
      an_chart_center_call: 'CALL allocation', an_chart_center_put: 'PUT allocation', ca_page_title: 'IBKR CALL Options Tracker',
      pu_page_title: 'IBKR PUT Options Tracker', an_pie_empty: 'No data',
      doc_open_label: 'Docs', doc_close_aria: 'Close documentation',
      doc_modal_title: 'Trading Hub — documentation',
      doc_modal_intro: '<p class="hub-doc-intro">Each tab is documented below. Use <strong>EN / HR</strong> in the top bar to switch the whole interface (including embedded tools where supported).</p>',
      doc_sec_portfolio_h: 'Portfolio', doc_sec_portfolio_p: '<p>Upload your broker portfolio CSV (drag-and-drop or file picker) to see total value, cash, allocation per ticker, limits, and P&amp;L. The chart summarizes weights; the table lists every holding with status and suggested actions.</p><ul><li>Theme (dark/light) follows the main hub toggle.</li><li>Data stays in your browser — nothing is uploaded to a server.</li></ul>',
      doc_sec_cost_h: 'Cost &amp; Premium', doc_sec_cost_p: '<p>Combine three IBKR-style exports: portfolio CSV, put export, and call export. The report shows stock basis, option cash flows by ticker, net basis, and <strong>adjusted average cost per share</strong>.</p><ul><li>The slider blends in open (non-expired) option premium from 0–100%.</li><li>0% uses realized P&amp;L on closed/expired rows; 100% adds full premium still in play on open positions.</li></ul>',
      doc_sec_coach_h: 'Put Coach', doc_sec_coach_p: '<p>Enter VIX, net liquidation value, excess liquidity, and put margin %. The calculator computes your ratio vs a VIX-scaled target, <strong>safe buying power</strong>, and <strong>max put notional</strong>. Trading modes (Conservative / Moderate / Aggressive) change the survival floor and VIX targets.</p><p>The stress test simulates a configurable 10–30% market drop (5% step) with optional sold put notional and an OTM position slider (loss factor).</p>',
      doc_sec_putan_h: 'Put Analyzer', doc_sec_putan_p: '<p>Load an IBKR PUT export CSV. Dashboard shows open vs closed positions, premium in play, exposure, days to expiry, and P&amp;L distribution and pie charts.</p>',
      doc_sec_callan_h: 'Call Analyzer', doc_sec_callan_p: '<p>Same workflow for IBKR CALL exports: allocation, monthly premium view, and P&amp;L breakdowns.</p>',
      doc_sec_putcal_h: 'Put Expiry Calendar', doc_sec_putcal_p: '<p>Upload your put CSV to group expirations by month and week. Expand a week to see tickers, strikes, quantities, exposure, and premium.</p>',
      doc_sec_callcal_h: 'Call Expiry Calendar', doc_sec_callcal_p: '<p>Identical layout for call positions and expirations.</p>',
      coach_page_title: 'Put Strategy Coach',
      coach_eyebrow: 'Risk manager', coach_h2_l1: 'Put Strategy', coach_h2_l2: 'Coach',
      coach_btn_rules: 'Rules', coach_btn_theme: 'Theme', coach_tab_calc: 'Calculator', coach_tab_docs: 'Documentation',
      coach_trading_mode: 'Trading mode',
      coach_mode_cons_l1: 'Conservative', coach_mode_cons_l2: 'Hard stop 40%', coach_mode_mod_l1: 'Moderate', coach_mode_mod_l2: 'Hard stop 30%', coach_mode_agg_l1: 'Aggressive', coach_mode_agg_l2: 'Hard stop 20%',
      coach_vix_apply: 'Apply', coach_lbl_vix: 'VIX index', coach_lbl_nlv: 'Net liq', coach_ph_nlv: 'e.g. 100000',
      coach_lbl_excess: 'Excess liquidity', coach_ph_excess: 'Free margin', coach_lbl_margin: 'Put margin %', coach_ph_margin: 'e.g. 20',
      coach_section_assessment: 'Assessment', coach_status_enter: 'Enter values above', coach_ml_safe_bp: 'Safe buying power', coach_ml_max_put: 'Max put notional',
      coach_ml_margin_sub: 'at {n}% margin req.', coach_target_prefix: 'VIX-adjusted target:', coach_chip_fmt: '{label} · floor {stop}%',
      coach_stress_15: 'Stress test · −{n}% market drop', coach_lbl_drop: 'Market drop scenario', coach_drop_selected: 'Selected drop:', coach_lbl_notional: 'Total sold put notional', coach_ph_notional: 'e.g. 53000 (optional)',
      coach_lbl_otm_pos: 'Put position (OTM)', coach_otm_deep: 'Deep OTM', coach_otm_deep_sub: 'delta ~0.10', coach_otm_mid: 'OTM', coach_otm_mid_sub: 'delta ~0.20',
      coach_otm_atm: 'ATM', coach_otm_atm_sub: 'delta ~0.35+', coach_otm_factor: 'Loss factor on margin value: ', coach_stress_badge: 'SCENARIO', coach_stress_short_delta: 'Short delta amplification model',
      coach_st_putloss: 'Loss on short puts', coach_st_nlv: 'Post-drop NLV', coach_st_excess: 'Post-drop excess liq.', coach_st_ratio: 'Resulting ratio', coach_st_dd: 'Drawdown (NLV)', coach_st_verdict_lbl: 'Verdict',
      coach_stress_enter_notional: 'Enter notional for a precise stress estimate',
      coach_modal_rules: '📜 Linear risk scaling', coach_modal_close: 'Close',
      coach_rule_r1t: 'Hard stop: {n}%', coach_rule_r1b: 'If excess / NLV falls below this floor, reduce exposure immediately. This is the survival minimum.',
      coach_rule_r2t: 'VIX-scaled target', coach_rule_r2b: 'Required minimum ratio rises with VIX. Each mode has its own base, slope, and cap (see the Rules tab in the coach).',
      coach_rule_r3t: 'Stress test', coach_rule_r3b: 'A selected 10–30% drop hits NLV and excess proportionally; short puts add an extra loss when notional is provided (margin × OTM loss factor).',
      coach_rule_r4t: 'Max put notional', coach_rule_r4b: 'Safe buying power divided by (put margin %) gives the maximum notional you can sell while staying above the target.',
      coach_err_excess: 'Excess liquidity cannot exceed NLV', coach_err_check: 'Check your inputs',
      coach_zone_crit: 'Critical — trim positions immediately', coach_zone_caution: 'Caution — hold, do not add', coach_zone_clear: 'Clear — room to add exposure',
      coach_ratio_floor: 'Ratio: {r}% (Floor: {n}%)', coach_ratio_target: 'Ratio: {r}% (Target: {t}%)',
      coach_bp_avail: 'available to deploy', coach_bp_needed: 'needed to reach target', coach_bp_survive: 'needed to reach survival floor ({n}%)',
      coach_vix_sug_up_t: 'VIX {v} — consider {mode}', coach_vix_sug_up_b: 'VIX is above {thr}. A more conservative mode fits elevated volatility.',
      coach_vix_sug_up_btn: 'Switch to {emoji}', coach_vix_sug_dn_t: 'VIX {v} — consider {mode}', coach_vix_sug_dn_b: 'VIX is below {thr}. The market is calm — you may use a less conservative mode.',
      coach_stress_sub_otm: '{label} · factor {pct}% · drop −{drop}%',
      coach_verdict_mc: '⚠ Margin call risk', coach_verdict_warn: '⚡ Caution zone', coach_verdict_ok: '✓ Survives',
      coach_mode_cons_lbl: 'Conservative', coach_mode_mod_lbl: 'Moderate', coach_mode_agg_lbl: 'Aggressive'
    },
    hr: {
      nav_portfolio: 'Portfolio', nav_cost: 'Trošak i premija', nav_coach: 'Put Coach', nav_put_an: 'Put analiza', nav_call_an: 'Call analiza',
      nav_put_cal: 'Put kalendar isteka', nav_call_cal: 'Call kalendar isteka', nav_growth_sim: 'Simulator rasta', theme_dark: 'Tamno', theme_light: 'Svijetlo', theme_toggle: 'Promijeni temu',
      lang_en: 'Engleski', lang_hr: 'Hrvatski', lang_switch: 'Jezik',
      cal_put_title: 'Kalendar isteka put opcija', cal_call_title: 'Kalendar isteka call opcija',
      cal_hint_put: 'Učitaj IBKR put export CSV (npr. IBKR - PUT.csv) za prikaz isteka.',
      cal_hint_call: 'Učitaj IBKR call export CSV (npr. IBKR - CALL.csv) za prikaz isteka.',
      cal_load_csv: 'Učitaj CSV', cal_no_file: 'Nema datoteke', cal_past: 'prošlo', cal_pos_badge: '{n} poz', cal_empty: 'prazno',
      cal_total: 'Ukupno', cal_no_exp: 'Nema isteka ovaj tjedan', cal_premium: 'premija', cal_exp: 'exp',
      cal_hdr_ticker: 'Ticker', cal_hdr_strike: 'Strike / istek', cal_hdr_qty: 'Kol', cal_hdr_exposure: 'Exposure', cal_hdr_premium: 'Premija',
      rpt_title: 'Trošak i premija (po tickeru)', rpt_sub: 'Spoji portfolio export s IBKR put i call CSV-ovima. Prilagođeni prosječni trošak po dionici uključuje novčane tokove opcija po tickeru. Isti format datoteka kao u Portfolio i Put/Call analizama.',
      rpt_up1: '1 · Portfolio CSV', rpt_up2: '2 · Put CSV', rpt_up3: '3 · Call CSV', rpt_no_file: 'Nema datoteke',
      rpt_slider_prefix: 'Uključi otvorenu (neisteklu) premiju opcije: ', rpt_slider_suffix: '%',
      rpt_hint: '0% (zadano): samo realizirani P&L — redovi Closed i Expired. 100%: dodaj puni Total Premium s Open pozicija (premija u igri). Vrijednosti 0–100% linearno miješaju otvorenu premiju.',
      rpt_empty: 'Učitaj barem jedan CSV (portfolio i/ili put i/ili call export) za izvještaj.',
      rpt_th_ticker: 'Ticker', rpt_th_shares: 'Dionice', rpt_th_stock_basis: 'Osnova dionice', rpt_th_puts: 'Put (opt. $)', rpt_th_calls: 'Call (opt. $)',
      rpt_th_opt: 'Opcije ukupno', rpt_th_net: 'Neto osnova', rpt_th_avg: 'Prilag. prosj. $/dion.', rpt_legend_h: 'Kako ovo radi',
      rpt_legend_1: 'Osnova dionice koristi Quantity × Average price iz portfolio CSV-a kad je moguće; inače Current value − P/L.',
      rpt_legend_2: 'Opcijski $ = realizirani P&L na Closed / Expired redovima (Premium Exp, inače Total Premium) + (slider %) × Total Premium na Open redovima.',
      rpt_legend_3: 'Neto osnova = osnova dionice − ukupno opcija (gotovina s shortova snižava učinkoviti trošak). Prilag. prosjek = neto osnova ÷ dionice.',
      po_page_title: 'Optimizator portfelja', po_logo_sub: 'Optimizator portfelja', po_upload_strong: 'Odaberi CSV datoteku', po_upload_or: 'ili povuci ovdje',
      po_no_file: 'Nema učitane datoteke', po_total_value: 'Ukupna vrijednost', po_positions: '{n} pozicija', po_cash: 'Gotovina', po_pct_of_pf: '{pct}% portfelja',
      po_unrealised: 'Nerealizirani P&L', po_total_ret: '{n}% ukupni povrat', po_pl_pct: '{sign}{n}% ukupni povrat', po_stocks: 'Vrijednost dionica', po_allocation: 'Alokacija', po_portfolio: 'Portfolio',
      po_holdings: 'Pozicije i limiti', po_th_ticker: 'Ticker', po_th_price: 'Cijena', po_th_qty: 'Kol', po_th_value: 'Vrijednost', po_th_alloc: 'Udio',
      po_th_limits: 'Limiti', po_th_status: 'Status', po_th_pl: 'P&L', po_th_action: 'Akcija', po_empty_pf: 'Učitaj CSV za prikaz portfelja',
      po_theme_toggle: 'Promijeni temu', po_chart_assets: '{n} imovina',
      an_csv_empty: 'CSV je prazan ili nema podataka.', an_kpi_real: 'Realizirani P&L', an_kpi_prem: 'Premija u igri', an_kpi_exp: 'Otvoreni exposure',
      an_kpi_open_n: 'Otvorenih pozicija', an_kpi_closed_n: 'Zatvorenih pozicija', an_sec_open: 'Otvorene pozicije — premija u igri',
      an_sec_prem_ticker: 'Premija u igri — udio po tickeru', an_sec_monthly: 'Premija u igri — sljedeća 4 mjeseca', an_sec_pl: 'P&L raspodjela po tickerima',
      an_pie_open_t: 'Otvorene pozicije — premija po tickeru', an_pie_pos: 'Pozitivni profiti — udio po tickeru', an_pie_neg: 'Gubitci — udio po tickeru',
      an_empty_data: 'Nema podataka', an_empty_open: 'Nema otvorenih pozicija', an_empty_closed: 'Nema zatvorenih pozicija', an_trade: 'trade', an_trades: 'trades',
      an_profit: '▲ Profit', an_loss: '▼ Gubitak', an_reset: 'Novi file', an_days_left: 'Days left',
      an_open_hdr_date: 'Datum otvaranja', an_open_hdr_exp: 'Exp. datum', an_open_hdr_strike: 'Strike', an_open_hdr_prem: 'Premija u igri',
      an_drop_label: 'Interaktivni tracker', an_put_h1: 'IBKR <span>PUT</span><br>Options Analyzer', an_put_drag_strong: 'Povuci CSV ovdje ili klikni',
      an_put_drop_line: 'Učitaj IBKR PUT export (.csv)', an_put_pick: 'Odaberi datoteku', an_dash_h1: 'PUT opcije <span>Dashboard</span>', an_reset_btn: 'Novi file',
      an_th_ticker: 'Ticker', an_th_open_date: 'Datum otvaranja', an_th_exp: 'Exp. datum', an_th_strike: 'Strike', an_th_qty: 'Qty',
      an_th_prem_open: 'Premija u igri', an_th_exposure: 'Exposure', an_th_days: 'Days left', an_sec_closed: 'Zatvorene pozicije — P&L po tickeru',
      an_pie_neg_title: 'Negativni profiti — udio po tickeru',
      an_call_drop: 'Učitaj IBKR CALL export (.csv)', an_call_h1: 'IBKR <span>CALL</span><br>Options Analyzer', an_call_drag_strong: 'Povuci CSV ovdje ili klikni',
      an_call_drop_line: 'Učitaj IBKR CALL export (.csv)', an_call_pick: 'Odaberi datoteku', an_dash_h1_call: 'CALL opcije <span>Dashboard</span>', an_reset_btn_call: 'Novi file',
      an_chart_center_call: 'CALL alokacija', an_chart_center_put: 'PUT alokacija', ca_page_title: 'IBKR CALL Options Tracker',
      pu_page_title: 'IBKR PUT Options Tracker', an_pie_empty: 'Nema podataka',
      doc_open_label: 'Dokumentacija', doc_close_aria: 'Zatvori dokumentaciju',
      doc_modal_title: 'Trading Hub — dokumentacija',
      doc_modal_intro: '<p class="hub-doc-intro">Svaki tab je opisan u nastavku. Prebacivanje <strong>EN / HR</strong> u gornjoj traci mijenja cijelo sučelje (uključujući ugrađene alate gdje je podržano).</p>',
      doc_sec_portfolio_h: 'Portfolio', doc_sec_portfolio_p: '<p>Učitaj CSV portfelja (povuci ili odaberi datoteku) za ukupnu vrijednost, gotovinu, alokaciju po tickeru, limite i P&amp;L. Graf prikazuje udjele; tablica prikazuje sve pozicije sa statusom i prijedlozima.</p><ul><li>Tema (tamno/svijetlo) slijedi glavni hub.</li><li>Podaci ostaju u pregledniku — ništa se ne šalje na server.</li></ul>',
      doc_sec_cost_h: 'Trošak i premija', doc_sec_cost_p: '<p>Spoji tri IBKR izvoza: portfolio CSV, put export i call export. Izvještaj pokazuje osnovu dionice, novčane tokove opcija po tickeru, neto osnovu i <strong>prilagođeni prosječni trošak po dionici</strong>.</p><ul><li>Klizač uključuje otvorenu (neisteklu) premiju opcije 0–100%.</li><li>0% = realizirani P&amp;L na zatvorenim/isteklim redovima; 100% = puna premija u igri na otvorenim pozicijama.</li></ul>',
      doc_sec_coach_h: 'Put Coach', doc_sec_coach_p: '<p>Unesi VIX, neto likvidacijsku vrijednost, excess likvidnost i postotak margine za put. Kalkulator računa omjer prema VIX-skaliranom cilju, <strong>sigurnu kupovnu moć</strong> i <strong>maks. nominalnu vrijednost putova</strong>. Trading modovi (konzervativno / umjereno / agresivno) mijenjaju pod za preživljavanje i VIX ciljeve.</p><p>Stress test simulira podesivi pad tržišta 10–30% (korak 5%) s opcionalnom nominalnom vrijednošću prodanih putova i kliznikom OTM pozicije (faktor gubitka).</p>',
      doc_sec_putan_h: 'Put analiza', doc_sec_putan_p: '<p>Učitaj IBKR PUT export CSV. Dashboard prikazuje otvorene i zatvorene pozicije, premiju u igri, exposure, dane do isteka i P&amp;L grafove.</p>',
      doc_sec_callan_h: 'Call analiza', doc_sec_callan_p: '<p>Isti tijek za IBKR CALL export: alokacija, premija po mjesecima i P&amp;L raspodjele.</p>',
      doc_sec_putcal_h: 'Put kalendar isteka', doc_sec_putcal_p: '<p>Učitaj put CSV za grupiranje isteka po mjesecu i tjednu. Proširi tjedan za tickere, strikeove, količine, exposure i premiju.</p>',
      doc_sec_callcal_h: 'Call kalendar isteka', doc_sec_callcal_p: '<p>Isti raspored za call pozicije i isteke.</p>',
      coach_page_title: 'Put Strategy Coach',
      coach_eyebrow: 'Upravljanje rizikom', coach_h2_l1: 'Put Strategy', coach_h2_l2: 'Coach',
      coach_btn_rules: 'Pravila', coach_btn_theme: 'Tema', coach_tab_calc: 'Kalkulator', coach_tab_docs: 'Dokumentacija',
      coach_trading_mode: 'Trading mode',
      coach_mode_cons_l1: 'Konzervativno', coach_mode_cons_l2: 'Hard stop 40%', coach_mode_mod_l1: 'Umjereno', coach_mode_mod_l2: 'Hard stop 30%', coach_mode_agg_l1: 'Agresivno', coach_mode_agg_l2: 'Hard stop 20%',
      coach_vix_apply: 'Primijeni', coach_lbl_vix: 'VIX indeks', coach_lbl_nlv: 'Neto likvidnost', coach_ph_nlv: 'npr. 100000',
      coach_lbl_excess: 'Excess likvidnost', coach_ph_excess: 'Slobodni margin', coach_lbl_margin: 'Put margin %', coach_ph_margin: 'npr. 20',
      coach_section_assessment: 'Procjena', coach_status_enter: 'Unesi vrijednosti gore', coach_ml_safe_bp: 'Sigurna kupovna moć', coach_ml_max_put: 'Maks. nominalna put',
      coach_ml_margin_sub: 'uz {n}% zahtjeva margine', coach_target_prefix: 'VIX-prilagođeni cilj:', coach_chip_fmt: '{label} · pod {stop}%',
      coach_stress_15: 'Stress test · pad tržišta −{n}%', coach_lbl_drop: 'Scenarij pada tržišta', coach_drop_selected: 'Odabrani pad:', coach_lbl_notional: 'Ukupna nominalna vrijednost prodanih putova', coach_ph_notional: 'npr. 53000 (opcionalno)',
      coach_lbl_otm_pos: 'Pozicija putova (OTM)', coach_otm_deep: 'Deep OTM', coach_otm_deep_sub: 'delta ~0.10', coach_otm_mid: 'OTM', coach_otm_mid_sub: 'delta ~0.20',
      coach_otm_atm: 'ATM', coach_otm_atm_sub: 'delta ~0.35+', coach_otm_factor: 'Faktor gubitka na margin vrijednosti: ', coach_stress_badge: 'SCENARIO', coach_stress_short_delta: 'Model pojačanja short delte',
      coach_st_putloss: 'Gubitak na put pozicijama', coach_st_nlv: 'NLV nakon pada', coach_st_excess: 'Excess nakon pada', coach_st_ratio: 'Rezultirajući omjer', coach_st_dd: 'Drawdown (NLV)', coach_st_verdict_lbl: 'Verdikt',
      coach_stress_enter_notional: 'Unesi nominalnu vrijednost za precizniji izračun',
      coach_modal_rules: '📜 Linearno skaliranje rizika', coach_modal_close: 'Zatvori',
      coach_rule_r1t: 'Hard stop: {n}%', coach_rule_r1b: 'Ako excess / NLV padne ispod ovog poda, odmah smanji exposure. Apsolutni minimum za preživljavanje.',
      coach_rule_r2t: 'VIX-skalirani cilj', coach_rule_r2b: 'Minimalni potrebni omjer raste s VIX-om. Svaki mod ima svoju bazu, nagib i cap (vidi Coach u kartici Pravila).',
      coach_rule_r3t: 'Stress test', coach_rule_r3b: 'Odabrani pad od 10–30% proporcionalno smanjuje NLV i excess; short putovi dodaju dodatni gubitak kad je unesena nominalna vrijednost (margin × OTM faktor).',
      coach_rule_r4t: 'Maks. nominalna put', coach_rule_r4b: 'Sigurna kupovna moć podijeljena s (put margin %) daje maksimalnu nominalnu vrijednost koju možeš prodati uz zadržavanje iznad cilja.',
      coach_err_excess: 'Excess likvidnost ne može biti veća od NLV', coach_err_check: 'Provjeri unose',
      coach_zone_crit: 'Kritično — odmah smanji pozicije', coach_zone_caution: 'Oprez — drži, ne dodavaj', coach_zone_clear: 'OK — prostor za nove pozicije',
      coach_ratio_floor: 'Omjer: {r}% (Pod: {n}%)', coach_ratio_target: 'Omjer: {r}% (Cilj: {t}%)',
      coach_bp_avail: 'dostupno za nove pozicije', coach_bp_needed: 'potrebno do cilja', coach_bp_survive: 'potrebno do poda preživljavanja ({n}%)',
      coach_vix_sug_up_t: 'VIX {v} — preporučujemo {mode}', coach_vix_sug_up_b: 'VIX je iznad {thr}. Konzervativniji mode bolje štiti pri povišenoj volatilnosti.',
      coach_vix_sug_up_btn: 'Prebaci na {emoji}', coach_vix_sug_dn_t: 'VIX {v} — možeš koristiti {mode}', coach_vix_sug_dn_b: 'VIX je ispod {thr}. Tržište je mirno — možeš slobodnije upravljati pozicijama.',
      coach_stress_sub_otm: '{label} · faktor {pct}% · pad −{drop}%',
      coach_verdict_mc: '⚠ Rizik margin calla', coach_verdict_warn: '⚡ Oprezna zona', coach_verdict_ok: '✓ Preživljava',
      coach_mode_cons_lbl: 'Konzervativno', coach_mode_mod_lbl: 'Umjereno', coach_mode_agg_lbl: 'Agresivno'
    }
  }

function hubT(key, vars) {
  var lang = window._hubLang || 'en';
  var raw = (HUB_I18N[lang] && HUB_I18N[lang][key]) || (HUB_I18N.en && HUB_I18N.en[key]) || key;
  if (vars && typeof raw === 'string') {
    Object.keys(vars).forEach(function(k) {
      raw = raw.split('{' + k + '}').join(String(vars[k]));
    });
  }
  return raw;
}
window.hubT = hubT;

// Apply {{key}} placeholders in the document
function applyI18nPlaceholders() {
  document.querySelectorAll('[data-i18n]').forEach(function(el) {
    el.innerHTML = hubT(el.dataset.i18n);
  });
  document.querySelectorAll('[data-i18n-ph]').forEach(function(el) {
    el.placeholder = hubT(el.dataset.i18nPh);
  });
}

// Listen for postMessage from hub shell (lang + theme)
window.addEventListener('message', function(ev) {
  if (!ev.data) return;
  if (ev.data.type === 'hub-lang') {
    window._hubLang = ev.data.lang;
    if (window._onHubLang) window._onHubLang(ev.data.lang);
  }
  if (ev.data.type === 'hub-theme') {
    var theme = ev.data.theme;
    document.documentElement.setAttribute('data-theme', theme);
    document.body && document.body.setAttribute('data-theme', theme);
    if (window._onHubTheme) window._onHubTheme(theme);
  }
});

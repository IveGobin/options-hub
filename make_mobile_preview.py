"""Kopira 'IBKR Unified Analyzer.html' u 'IBKR Unified Analyzer (mobile preview).html' i na kopiji
dodaje mobilni prikaz Stocks taba s karticama (ispod 700px širine). Original se ne mijenja.

Pokretanje:  python make_mobile_preview.py
Pregled na desktopu: suzi prozor ispod 700px ili u DevTools uključi prikaz za mobitel (npr. 390px),
ili na kraj URL-a dodaj #cards da se kartice prikažu na bilo kojoj širini.
"""
import re
from pathlib import Path

# Preview iteration, shown after the original's version (e.g. "v2.6 · m5"). Bump on every change to this script.
PREVIEW_VERSION = 8

HERE = Path(__file__).resolve().parent
SRC = HERE / 'IBKR Unified Analyzer.html'
DST = HERE / 'IBKR Unified Analyzer (mobile preview).html'

s = SRC.read_text(encoding='utf-8')


def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, f'Očekivano točno 1 pojavljivanje, nađeno {n}: {old[:80]!r}'
    s = s.replace(old, new)


# ── Version label in the top bar: original version + preview iteration ──
s, n = re.subn(r'(margin-left:8px;">)(v\d+\.\d+)(</span></h1>)', rf'\g<1>\g<2> · m{PREVIEW_VERSION}\g<3>', s, count=1)
assert n == 1, 'Version label in the top bar not found'

# ── HTML: kontejner za kartice ispod tablice ──
rep("""          <tbody id="stock-tbody"></tbody>
        </table>
      </div>""", """          <tbody id="stock-tbody"></tbody>
        </table>
      </div>
      <div class="stock-cards" id="stock-cards"></div>""")

# ── CSS ──
rep("</style>", """  /* ── Mobile preview: Stocks as cards (below 700px, or anywhere with #cards in the URL) ── */
  .stock-cards { display:none; }
  @media(max-width:700px) {
    #tab-stocks .table-wrapper { display:none; }
    .stock-cards { display:flex; }
  }
  body.force-cards #tab-stocks .table-wrapper { display:none; }
  body.force-cards .stock-cards { display:flex; max-width:480px; }
  .stock-cards { flex-direction:column; gap:8px; }
  .stock-cards .pos { color:var(--green); }
  .stock-cards .neg { color:var(--red); }
  .stock-cards .neu { color:var(--muted); }
  .sc-group { font-family:'Space Mono',monospace; font-size:10px; letter-spacing:0.12em; text-transform:uppercase; color:var(--muted); font-weight:700; padding:14px 2px 2px; }
  .sc-card { background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:12px 14px; }
  .sc-card.sold .sc-sym, .sc-card.sold .sc-desc { opacity:0.7; }
  .sc-head { display:flex; justify-content:space-between; align-items:baseline; gap:10px; }
  .sc-sym { font-family:'Space Mono',monospace; font-weight:700; font-size:14px; white-space:nowrap; }
  .sc-total { font-family:'Space Mono',monospace; font-weight:700; font-size:15px; white-space:nowrap; }
  .sc-desc { font-size:11px; color:var(--muted); margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .sc-split { display:flex; flex-wrap:wrap; gap:4px 16px; margin-top:8px; font-family:'Space Mono',monospace; font-size:11px; color:var(--muted); }
  .sc-split b { font-weight:400; }
  .sc-more > summary { cursor:pointer; list-style:none; margin-top:10px; font-size:11px; color:var(--blue); font-family:'Space Mono',monospace; }
  .sc-more > summary::-webkit-details-marker { display:none; }
  .sc-more > summary::before { content:'▶ '; font-size:9px; }
  .sc-more[open] > summary::before { content:'▼ '; }
  .sc-grid { display:grid; grid-template-columns:auto 1fr; gap:5px 12px; margin-top:10px; font-family:'Space Mono',monospace; font-size:11px; }
  .sc-grid > span:nth-child(odd) { color:var(--muted); }
  .sc-grid > span:nth-child(even) { text-align:right; }
  .sc-tx { overflow-x:auto; margin:12px -14px -12px; background:var(--surface2); border-radius:0 0 10px 10px; }
  .sc-tx .stock-tx-inner { padding:8px 14px 12px; border-top:1px solid var(--border); }
  .sc-tx table.tx-table td { white-space:nowrap; }
  .sc-total-card { background:var(--surface2); border-color:rgba(0,180,216,0.4); }
  .sc-note { font-size:11px; color:var(--muted); margin-top:8px; line-height:1.5; }
</style>""")

# ── JS: kartice se grade u istoj petlji kao redovi tablice (isti stockEurFigures, isti zbrojevi) ──
rep("""  tbody.innerHTML = '';
  const _stRows = data.stocksTable || data.stocks;""", """  tbody.innerHTML = '';
  const cards = [];   // mobile card view, built from the same figures as the table rows
  const _stRows = data.stocksTable || data.stocks;""")

rep("""      tbody.appendChild(hdr);
    }""", """      tbody.appendChild(hdr);
      cards.push(`<div class="sc-group">${escHtml(hdr.textContent)}</div>`);
    }""")

rep("""    tbody.appendChild(tr);
    tbody.appendChild(txRow);
  });""", """    tbody.appendChild(tr);
    tbody.appendChild(txRow);

    const txInner = hasTrades ? txRow.querySelector('.stock-tx-inner') : null;
    cards.push(`<div class="sc-card${s.held ? '' : ' sold'}">
      <div class="sc-head">
        <span class="sc-sym">${escHtml(s.sym)}${s.held ? '' : '<span class="stock-sold-badge">SOLD</span>'}</span>
        <span class="sc-total ${pnlCls(eurRow.total)}">${fmtPnl(eurRow.total, dispSym())}</span>
      </div>
      <div class="sc-desc">${escHtml(data.instrMap[s.sym] || '')}${data.instrMap[s.sym] ? ' · ' : ''}${ccy}${s.held ? ' · ' + mktV : ''}</div>
      <div class="sc-split">
        <span>Realized <b class="${pnlCls(eurRow.real)}">${fmtPnl(eurRow.real, dispSym())}</b></span>
        <span>Unrealized <b class="${pnlCls(eurRow.unr)}">${fmtPnl(eurRow.unr, dispSym())}</b></span>
      </div>
      <details class="sc-more"><summary>Details${hasTrades ? ' · ' + trades.length + ' trade' + (trades.length !== 1 ? 's' : '') : ''}</summary>
        <div class="sc-grid">
          <span>Qty</span><span>${qty}</span>
          <span>Avg cost</span><span>${costP}</span>
          <span>Last price</span><span>${lastP}</span>
          <span>Market value</span><span>${mktV}</span>
          <span>Realized (${ccy})</span><span class="${rCls}">${fmtPnl(s.realTotal, sym)}</span>
          <span>Unrealized (${ccy})</span><span class="${uCls}">${fmtPnl(s.unrTotal, sym)}</span>
          <span>Total (${ccy})</span><span class="${tCls}">${fmtPnl(s.total, sym)}</span>
        </div>
        ${txInner ? `<div class="sc-tx">${txInner.outerHTML}</div>` : ''}
      </details>
    </div>`);
  });""")

rep("""    tbody.appendChild(stmtRow);
  }
}
""", """    tbody.appendChild(stmtRow);
  }

  cards.push(`<div class="sc-card sc-total-card">
    <div class="sc-head"><span class="sc-sym">TOTAL (${DISP})</span><span class="sc-total ${pnlCls(eurFig.total)}">${fmtPnl(eurFig.total, dispSym())}</span></div>
    <div class="sc-split">
      <span>Realized <b class="${pnlCls(eurFig.real)}">${fmtPnl(eurFig.real, dispSym())}</b></span>
      <span>Unrealized <b class="${pnlCls(eurFig.unr)}">${fmtPnl(eurFig.unr, dispSym())}</b></span>
    </div>
    <div class="sc-note">${DISP === 'EUR'
      ? `of which currency effect: <strong style="color:${pnlColor(eurFig.fx)}">${fmtPnl(eurFig.fx, dispSym())}</strong>
      <span class="info-tip" tabindex="0" title="${escHtml(STOCK_ECON_TIP)}">ⓘ</span>`
      : 'USD view: native P&amp;L (EUR stocks at the statement rate). Switch to EUR to see the currency effect.'}
      ${stmt && Number.isFinite(stmt.real) && Number.isFinite(stmt.unr) ? `<br>IBKR statement (excl. FX): realized ${dPnl(stmt.real, 'EUR')} / unrealized ${dPnl(stmt.unr, 'EUR')}` : ''}</div>
  </div>`);
  const cardBox = document.getElementById('stock-cards');
  if (cardBox) cardBox.innerHTML = cards.join('');
  if (location.hash === '#cards') document.body.classList.add('force-cards');
}
""")

# ════════════════════════════════════════════════════════════════════
# Open Options as cards: progress bar toward the 80% target, action badges, grouping by expiry
# ════════════════════════════════════════════════════════════════════
rep("""      <div class="table-wrapper">
        <table class="open-table">
          <thead><tr>
            <th>#</th><th>Ticker</th>""", """      <div class="table-wrapper" id="open-table-wrap">
        <table class="open-table">
          <thead><tr>
            <th>#</th><th>Ticker</th>""")
rep("""          <tbody id="open-tbody"></tbody>
        </table>
      </div>""", """          <tbody id="open-tbody"></tbody>
        </table>
      </div>
      <div class="opt-cards" id="opt-cards"></div>""")

rep("</style>", """  /* ── Mobile preview: Open Options as cards ── */
  .opt-cards { display:none; flex-direction:column; gap:8px; }
  @media(max-width:700px) {
    #open-table-wrap { display:none; }
    .opt-cards { display:flex; }
  }
  body.force-cards #open-table-wrap { display:none; }
  body.force-cards .opt-cards { display:flex; max-width:480px; }
  .oc-group { display:flex; justify-content:space-between; align-items:baseline; gap:8px; flex-wrap:wrap; font-family:'Space Mono',monospace; font-size:10px; letter-spacing:0.12em; text-transform:uppercase; color:var(--muted); font-weight:700; padding:14px 2px 2px; }
  .oc-group-sum { letter-spacing:0.04em; text-transform:none; font-weight:400; }
  .oc-card { background:var(--surface); border:1px solid var(--border); border-left:3px solid var(--border); border-radius:10px; padding:12px 14px; }
  .oc-card.quiet { opacity:0.8; }
  .oc-card.act-close { border-left-color:var(--green); }
  .oc-card.act-soon  { border-left-color:var(--yellow); }
  .oc-card.act-loss  { border-left-color:var(--red); }
  .oc-head { display:flex; justify-content:space-between; align-items:center; gap:10px; }
  .oc-title { display:flex; align-items:center; gap:8px; font-family:'Space Mono',monospace; font-size:14px; white-space:nowrap; }
  .oc-strike { color:var(--muted); font-size:13px; }
  .oc-sub { font-family:'Space Mono',monospace; font-size:11px; color:var(--muted); margin-top:4px; }
  .oc-bar { position:relative; height:8px; background:var(--surface2); border-radius:4px; margin-top:10px; overflow:visible; }
  .oc-fill { height:100%; border-radius:4px; }
  .oc-fill.high { background:var(--green); } .oc-fill.mid { background:var(--yellow); } .oc-fill.low { background:#ff8c00; } .oc-fill.neg { background:var(--red); }
  .oc-target { position:absolute; top:-3px; bottom:-3px; width:2px; background:var(--text); opacity:0.6; border-radius:1px; }
  .oc-barlbl { display:flex; justify-content:space-between; font-family:'Space Mono',monospace; font-size:10.5px; color:var(--muted); margin-top:5px; }
  .oc-badges { display:flex; flex-wrap:wrap; gap:6px; margin-top:9px; }
  .oc-badge { font-family:'Space Mono',monospace; font-size:10.5px; border-radius:5px; padding:3px 8px; }
  .oc-badge.close { background:rgba(0,200,83,0.12); color:var(--green); }
  .oc-badge.soon  { background:rgba(255,211,42,0.12); color:var(--yellow); }
  .oc-badge.loss  { background:rgba(255,71,87,0.14); color:var(--red); }
  .oc-meta { display:flex; flex-wrap:wrap; gap:4px 14px; margin-top:9px; font-family:'Space Mono',monospace; font-size:11px; color:var(--muted); }
  .oc-meta b { font-weight:400; color:var(--text); }
  .oc-card .sc-more > summary { margin-top:8px; }
  .oc-acc { padding:0; border-left-width:1px; opacity:1; }
  .oc-acc > summary { list-style:none; cursor:pointer; padding:12px 14px; }
  .oc-acc > summary::-webkit-details-marker { display:none; }
  .oc-acc .oc-title strong { font-size:15px; }
  .oc-right { display:flex; align-items:center; gap:10px; white-space:nowrap; }
  .oc-chev { width:7px; height:7px; border-right:1.5px solid var(--muted); border-bottom:1.5px solid var(--muted); transform:rotate(45deg); margin:-3px 2px 0 0; transition:transform 0.15s; }
  .oc-acc[open] .oc-chev { transform:rotate(-135deg); margin-top:3px; }
  .oc-kept-inline { display:none; font-size:11px; opacity:0.85; }
  .oc-acc[open] .oc-kept-inline { display:inline; }
  .oc-acc .oc-minibar { height:4px; margin-top:9px; }
  .oc-acc .oc-minibar .oc-target { top:-2px; bottom:-2px; }
  .oc-acc[open] .oc-minibar { display:none; }
  .oc-body { padding:0 14px 12px; border-top:1px solid var(--border); padding-top:2px; }
  .oc-line2 { display:flex; justify-content:space-between; gap:8px; white-space:nowrap; }
  .oc-line2 b { font-weight:400; color:var(--text); }
  .oc-acc > summary .oc-chev { flex:0 0 auto; }
  .oc-flag { margin-left:8px; font-size:11px; }
  .oc-flag.soon { color:var(--yellow); } .oc-flag.neg { color:var(--red); } .oc-flag.pos { color:var(--green); }
  .oc-total { background:var(--surface2); border-color:rgba(0,180,216,0.4); border-left-color:rgba(0,180,216,0.4); }
</style>""")

rep("""  renderOpenTable(data.openPositions);
""", """  renderOpenTable(data.openPositions);
  renderOpenCards(data.openPositions);
""")

rep("""function renderAssignedTable(assignedPositions) {""", """// Mobile card view of the open options table: same figures, plus the 80% target, action badges and expiry groups.
function renderOpenCards(openPositions) {
  const box = document.getElementById('opt-cards');
  if (!box) return;
  if (!openPositions.length) { box.innerHTML = '<div class="empty-state">No open option positions found.</div>'; return; }
  const today = new Date(); today.setHours(0,0,0,0);
  const sunday = new Date(today); sunday.setDate(today.getDate() + ((7 - today.getDay()) % 7));   // end of this week
  const nextSunday = new Date(sunday); nextSunday.setDate(sunday.getDate() + 7);
  const groupOf = exp => {
    const e = new Date(exp); e.setHours(0,0,0,0);
    if (e < today) return 'Expired';
    if (e <= sunday) return 'This week';
    if (e <= nextSunday) return 'Next week';
    if (e.getFullYear() === today.getFullYear() && e.getMonth() === today.getMonth()) return 'This month';
    return e.toLocaleString('en-US', { month:'long', year:'numeric' });   // later expiries grouped by month
  };
  const pct = (v, d) => (v < 0 ? '−' : '') + Math.abs(v).toFixed(d) + '%';
  const keptOf = p => p.premiumCollected > 0 ? ((p.premiumCollected - p.currentValue) / p.premiumCollected) * 100 : null;
  const keptCls = k => k >= 75 ? 'high' : k >= 40 ? 'mid' : k >= 0 ? 'low' : 'neg';
  const sorted = [...openPositions].sort((a,b) => a.expiry - b.expiry);
  const groups = [];
  for (const p of sorted) {
    const g = groupOf(p.expiry);
    if (!groups.length || groups[groups.length-1].name !== g) groups.push({ name:g, items:[] });
    groups[groups.length-1].items.push(p);
  }
  let html = '';
  for (const g of groups) {
    const gPrem = g.items.reduce((s,p)=>s+p.premiumCollected,0);
    const gCtC  = g.items.reduce((s,p)=>s+p.currentValue,0);
    const gKept = gPrem > 0 ? ((gPrem - gCtC) / gPrem) * 100 : null;
    html += `<div class="oc-group"><span>${g.name} (${g.items.length})</span><span class="oc-group-sum">premium ${fmtPrem(gPrem)}${gKept !== null ? ' · ' + pct(gKept, 0) + ' kept' : ''}</span></div>`;
    for (const p of g.items) {
      const dl = daysLeft(new Date(p.expiry));
      const kept = keptOf(p);
      const perShare = p.premiumCollected / (Math.abs(p.qty) * 100);
      const target = perShare * 0.2;   // buy back at or below this per-share price to keep 80%
      const badges = [];
      let act = '';
      if (kept !== null && kept >= 80) { badges.push(`<span class="oc-badge close">✓ 80% reached · buy back ≤ ${fmtNative(target, '$')}/sh</span>`); act = 'act-close'; }
      if (dl < 0) { badges.push('<span class="oc-badge loss">Expired</span>'); act = act || 'act-loss'; }
      else if (dl <= 7) { badges.push(`<span class="oc-badge soon">⏳ ${dl === 0 ? 'Expires today' : 'Expires in ' + dl + 'd'}</span>`); act = act || 'act-soon'; }
      if (kept !== null && kept < 0) { badges.push('<span class="oc-badge loss">▼ Loss · option worth more than premium</span>'); act = 'act-loss'; }
      const flag = act === 'act-close' ? '<span class="oc-flag pos" title="80% reached">✓</span>'
                 : act === 'act-loss'  ? '<span class="oc-flag neg" title="Loss / expired">▼</span>'
                 : act === 'act-soon'  ? '<span class="oc-flag soon" title="Expires within 7 days">⏳</span>' : '';
      const fill = kept === null ? '' : `<div class="oc-fill ${keptCls(kept)}" style="width:${Math.max(0, Math.min(100, kept)).toFixed(1)}%"></div><div class="oc-target" style="left:80%"></div>`;
      // Accordion: the summary is the compact line, the body holds kept %, badges and details.
      html += `<details class="oc-card oc-acc">
        <summary>
          <div class="oc-head">
            <span class="oc-title"><span class="type-badge ${p.type}">${p.type}</span><strong>${escHtml(p.ticker)}</strong><span class="oc-strike">${fmtNative(p.strike, '$', p.strike%1===0?0:2)} ×${p.qty}</span></span>
            <span class="oc-right"><span class="${p.unrPL>0?'unr-pos':p.unrPL<0?'unr-neg':'unr-neu'}">${dPnl(p.unrPL, 'USD')}${kept !== null ? `<span class="oc-kept-inline"> (${pct(kept, 1)})</span>` : ''}</span><span class="oc-chev"></span></span>
          </div>
          <div class="oc-sub oc-line2"><span>${fmtDate(p.expiry)} · ${dl < 0 ? Math.abs(dl) + 'd ago' : dl === 0 ? 'today' : dl + 'd left'}${flag}</span><span>close <b>${dMoney(p.currentValue, 'USD')}</b></span></div>
        </summary>
        <div class="oc-body">
          ${kept === null
            ? `<div class="oc-barlbl"><span>Bought option (debit) · no premium to keep</span></div>`
            : `<div class="oc-bar">${fill}</div><div class="oc-barlbl"><span>${pct(kept, 1)} kept</span><span>target 80%</span></div>`}
          ${badges.length ? `<div class="oc-badges">${badges.join('')}</div>` : ''}
          <div class="oc-meta"><span>Premium <b>${fmtPrem(p.premiumCollected)}</b></span><span>To close <b>${dMoney(p.currentValue, 'USD')}</b></span></div>
          <div class="sc-grid">
            <span>Qty</span><span>${p.qty}</span>
            <span>Premium / share</span><span>${fmtPnl(perShare, '$')}</span>
            <span>80% buyback price</span><span>${kept === null ? '—' : fmtNative(target, '$') + '/sh'}</span>
            <span>Cost to close</span><span>${dMoney(p.currentValue, 'USD')}</span>
            <span>Unrealized P&amp;L</span><span class="${pnlCls(p.unrPL)}">${dPnl(p.unrPL, 'USD')}</span>
            <span>Exposure</span><span>${p.exposure !== null ? fmtK(p.exposure) : '—'}</span>
          </div>
        </div>
      </details>`;
    }
  }
  // TOTAL card: same sums as the table's TOTAL row
  const totPrem  = openPositions.reduce((s,p)=>s+p.premiumCollected,0);
  const totUnrPL = openPositions.reduce((s,p)=>s+p.unrPL,0);
  const totExp   = openPositions.filter(p=>p.type==='P').reduce((s,p)=>s+(p.exposure||0),0);
  const totCtC   = openPositions.reduce((s,p)=>s+p.currentValue,0);
  const totKept  = totPrem > 0 ? ((totPrem - totCtC) / totPrem) * 100 : null;
  html += `<div class="oc-card oc-total">
    <div class="oc-head"><span class="oc-title"><strong>TOTAL · ${openPositions.length}</strong></span><span class="${totUnrPL>0?'unr-pos':totUnrPL<0?'unr-neg':'unr-neu'}">${dPnl(totUnrPL, 'USD')}</span></div>
    ${totKept !== null ? `<div class="oc-bar"><div class="oc-fill ${keptCls(totKept)}" style="width:${Math.max(0, Math.min(100, totKept)).toFixed(1)}%"></div><div class="oc-target" style="left:80%"></div></div>
    <div class="oc-barlbl"><span>${pct(totKept, 1)} kept</span><span>target 80%</span></div>` : ''}
    <div class="oc-meta"><span>Premium <b>${fmtPrem(totPrem)}</b></span><span>To close <b>${dMoney(totCtC, 'USD')}</b></span><span>Put exposure <b>${fmtK(totExp)}</b></span></div>
  </div>`;
  box.innerHTML = html;
}

function renderAssignedTable(assignedPositions) {""")

# ════════════════════════════════════════════════════════════════════
# Closed P&L: stat grid, ticker list instead of the quarter matrix, trade cards grouped by month
# ════════════════════════════════════════════════════════════════════
rep("""        <div class="matrix-scroll">
          <table class="pnl-matrix">
            <thead id="closed-matrix-head"></thead>
            <tbody id="closed-matrix-body"></tbody>
          </table>
        </div>""", """        <div class="matrix-scroll">
          <table class="pnl-matrix">
            <thead id="closed-matrix-head"></thead>
            <tbody id="closed-matrix-body"></tbody>
          </table>
        </div>
        <div class="cl-cards" id="matrix-cards"></div>""")
rep("""        <div class="table-wrapper">
          <table class="detail-table">""", """        <div class="cl-cards" id="detail-cards"></div>
        <div class="table-wrapper" id="detail-table-wrap">
          <table class="detail-table">""")

rep("</style>", """  /* ── Mobile preview: Closed P&L ── */
  .cl-cards { display:none; flex-direction:column; gap:8px; }
  @media(max-width:700px) {
    #closed-stat-row { display:grid; grid-template-columns:1fr 1fr; gap:8px; }
    #closed-stat-row .stat-badge { min-width:0; padding:10px 12px; }
    #closed-stat-row .stat-badge-value { font-size:17px; white-space:nowrap; }
    #tab-closed .matrix-scroll, #detail-table-wrap { display:none; }
    .cl-cards { display:flex; }
  }
  body.force-cards #tab-closed .matrix-scroll, body.force-cards #detail-table-wrap { display:none; }
  body.force-cards .cl-cards { display:flex; max-width:480px; }
  .mx-card { background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:10px 14px; }
  .mx-head { display:flex; justify-content:space-between; align-items:baseline; gap:10px; font-family:'Space Mono',monospace; }
  .mx-head strong { font-size:13px; }
  .mx-head .mx-total { font-weight:700; font-size:14px; white-space:nowrap; }
  .mx-bar { height:4px; background:var(--surface2); border-radius:2px; margin-top:7px; }
  .mx-bar > div { height:100%; border-radius:2px; }
  .mx-qs { display:flex; flex-wrap:wrap; gap:3px 12px; margin-top:6px; font-family:'Space Mono',monospace; font-size:10.5px; color:var(--muted); }
  .cl-cards .pos { color:var(--green); } .cl-cards .neg { color:var(--red); } .cl-cards .neu { color:var(--muted); }
  .mx-acc { padding:0; }
  .mx-acc > summary { list-style:none; cursor:pointer; padding:10px 14px; }
  .mx-acc > summary::-webkit-details-marker { display:none; }
  .mx-acc[open] .oc-chev { transform:rotate(-135deg); margin-top:3px; }
  .mx-body { padding:2px 14px 12px; border-top:1px solid var(--border); }
  .mx-qhead { font-family:'Space Mono',monospace; font-size:10px; letter-spacing:0.12em; text-transform:uppercase; color:var(--muted); margin-top:10px; }
  .mx-body .sc-grid { margin-top:6px; }
  .mx-partial { font-size:9px; color:var(--muted); border:1px solid var(--muted); border-radius:3px; padding:0 4px; margin-left:6px; vertical-align:middle; font-weight:400; }
  .cl-sort { display:flex; align-items:center; gap:8px; font-size:12px; color:var(--muted); margin:6px 0 2px; }
  .cl-sort select { background:var(--surface2); border:1px solid var(--border); border-radius:6px; color:var(--text); font-family:'Space Mono',monospace; font-size:11px; padding:4px 8px; }
  .tc-card { padding:10px 14px; }
  .tc-card .oc-sub { display:flex; justify-content:space-between; gap:8px; align-items:center; flex-wrap:wrap; }
</style>""")

# ticker list from the same quarter aggregation as the matrix
rep("""  totRow.innerHTML=totCells; body.appendChild(totRow);
}""", """  totRow.innerHTML=totCells; body.appendChild(totRow);
  renderMatrixCards(sortedTickers, sortedQ, qLabels);
}

// Mobile list of the quarter matrix: ticker total, size bar and only the quarters with a result.
function renderMatrixCards(sortedTickers, sortedQ, qLabels) {
  const box = document.getElementById('matrix-cards');
  if (!box) return;
  const maxAbs = Math.max(...sortedTickers.map(([,d]) => Math.abs(d.total)), 0.01);
  // Quarter breakdown for the expanded card: one row per quarter with a result.
  const qGrid = d => `<div class="sc-grid">${sortedQ.filter(qk => d[qk]).map(qk => `<span>${escHtml(qLabels[qk])}</span><span class="${pnlCls(d[qk])}">${fmtPnl(toDisp(d[qk], 'USD'), dispSym())}</span>`).join('')}</div>`;
  const nQ = d => sortedQ.filter(qk => d[qk]).length;
  const card = (title, total, qData, extraCls, bar) => `<details class="mx-card mx-acc ${extraCls}">
      <summary>
        <div class="mx-head"><strong>${title}</strong>
          <span class="oc-right"><span class="mx-total ${pnlCls(total)}">${fmtPnl(toDisp(total, 'USD'), dispSym())}</span><span class="oc-chev"></span></span></div>
        ${bar}
      </summary>
      <div class="mx-body"><div class="mx-qhead">By quarter · ${nQ(qData)}</div>${qGrid(qData)}</div>
    </details>`;
  let html = sortedTickers.map(([ticker, d]) => card(
      escHtml(ticker) + (d.hasPartial ? '<span class="mx-partial" title="Partially closed — position still open">partial</span>' : ''),
      d.total, d.qData, '',
      `<div class="mx-bar"><div style="width:${(Math.abs(d.total) / maxAbs * 100).toFixed(1)}%;background:${pnlColor(d.total)}"></div></div>`)).join('');
  const colSums = {}; let grand = 0;
  sortedQ.forEach(qk => { colSums[qk] = sortedTickers.reduce((s,[,d]) => s + (d.qData[qk] || 0), 0); grand += colSums[qk]; });
  if (sortedTickers.length) html += card(`Total · ${sortedTickers.length} tickers`, grand, colSums, 'oc-total', '');
  box.innerHTML = html;
}""")

# trade cards from the same filtered/sorted rows as the detail table
rep("""    tbody.innerHTML = `<tr><td colspan="13" style="text-align:center;color:var(--muted);padding:20px;">No closed option trades found.</td></tr>`;
    return;""", """    tbody.innerHTML = `<tr><td colspan="13" style="text-align:center;color:var(--muted);padding:20px;">No closed option trades found.</td></tr>`;
    renderDetailCards(rows);
    return;""")
rep("""  ], 'border-top:1px solid var(--border);font-weight:700;background:var(--surface2);');
  tbody.appendChild(tfoot);
}""", """  ], 'border-top:1px solid var(--border);font-weight:700;background:var(--surface2);');
  tbody.appendChild(tfoot);
  renderDetailCards(rows);
}

// Mobile cards of the closed-trade detail table. Grouped by month when sorted by a date.
const DETAIL_CARD_SORTS = [['closeDate',-1,'Newest closed'],['closeDate',1,'Oldest closed'],['openDate',1,'Open date'],['profit',-1,'Best profit'],['profit',1,'Worst profit']];
function setDetailCardSort(v) {
  const [k, d] = v.split(':');
  window._detailSortKey = k; window._detailSortDir = +d;
  renderDetailTable();
}
function renderDetailCards(rows) {
  const box = document.getElementById('detail-cards');
  if (!box) return;
  const key = window._detailSortKey, dir = window._detailSortDir;
  const cur = key + ':' + dir;
  const opts = DETAIL_CARD_SORTS.map(([k,d,l]) => `<option value="${k}:${d}"${cur === k+':'+d ? ' selected' : ''}>${l}</option>`).join('')
    + (DETAIL_CARD_SORTS.some(([k,d]) => cur === k+':'+d) ? '' : `<option value="${cur}" selected>${escHtml(key)} ${dir > 0 ? '↑' : '↓'}</option>`);
  let html = `<div class="cl-sort"><label>Sort</label><select onchange="setDetailCardSort(this.value)">${opts}</select></div>`;
  if (!rows.length) { box.innerHTML = html + '<div class="empty-state">No closed option trades found.</div>'; return; }
  const fmtD = d => d instanceof Date ? d.toLocaleDateString('en-US', { month:'short', day:'numeric' }) : '—';
  const fmtY = d => d instanceof Date ? " '" + String(d.getFullYear()).slice(2) : '';
  const pct = v => v === null || v === undefined ? '—' : (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(v).toFixed(1) + '%';
  const groupKey = (key === 'closeDate' || key === 'openDate') ? key : null;
  const monthOf = r => r[groupKey] instanceof Date ? r[groupKey].toLocaleString('en-US', { month:'long', year:'numeric' }) : '—';
  let lastG = null;
  rows.forEach((r, i) => {
    if (groupKey) {
      const g = monthOf(r);
      if (g !== lastG) {
        lastG = g;
        const gRows = []; for (let j = i; j < rows.length && monthOf(rows[j]) === g; j++) gRows.push(rows[j]);
        const gProfit = gRows.reduce((s,x) => s + x.profit, 0);
        html += `<div class="oc-group"><span>${g} (${gRows.length})</span><span class="oc-group-sum ${pnlCls(gProfit)}">${dPnl(gProfit, 'USD')}</span></div>`;
      }
    }
    const held = r.openDate instanceof Date && r.closeDate instanceof Date ? Math.round((r.closeDate - r.openDate) / 86400000) : null;
    html += `<div class="oc-card tc-card">
      <div class="oc-head">
        <span class="oc-title"><span class="type-badge ${r.type}">${r.type}</span><strong>${escHtml(r.ticker)}</strong><span class="oc-strike">${fmtNative(r.strike, '$', r.strike%1===0?0:2)} ×${r.qty}</span></span>
        <span class="${pnlCls(r.profit)}" style="font-family:'Space Mono',monospace;font-weight:700;white-space:nowrap;">${dPnl(r.profit, 'USD')}</span>
      </div>
      <div class="oc-sub"><span>${fmtD(r.openDate)} → ${fmtD(r.closeDate)}${fmtY(r.closeDate)}${held !== null ? ' · ' + held + 'd' : ''}</span>
        <span><span class="status-pill ${r.status.toLowerCase()}">${r.status}</span> <span class="${pnlCls(r.profit)}">${pct(r.profitPct)}</span></span></div>
      <details class="sc-more"><summary>Details</summary>
        <div class="sc-grid">
          <span>Contract</span><span>${escHtml(r.sym)}</span>
          <span>Premium collected</span><span class="pos">${dPnl(r.premium, 'USD')}</span>
          <span>Paid to close</span><span class="${r.buyback>0?'neg':''}">${r.buyback>0 ? dPnl(-Math.abs(r.buyback), 'USD') : '—'}</span>
          <span>Open fee</span><span class="neg">${r.openFee!==0 ? dPnl(-Math.abs(r.openFee), 'USD') : '—'}</span>
          <span>Close fee</span><span class="neg">${r.closeFee!==0 ? dPnl(-Math.abs(r.closeFee), 'USD') : '—'}</span>
        </div>
      </details>
    </div>`;
  });
  const totalProfit  = rows.reduce((s,r)=>s+r.profit,0);
  const totalPremium = rows.reduce((s,r)=>s+r.premium,0);
  const fees = rows.reduce((s,r)=>s+r.openFee+r.closeFee,0);
  html += `<div class="oc-card oc-total">
    <div class="oc-head"><span class="oc-title"><strong>TOTAL · ${rows.length} trades</strong></span><span class="${pnlCls(totalProfit)}" style="font-family:'Space Mono',monospace;font-weight:700;">${dPnl(totalProfit, 'USD')}</span></div>
    <div class="oc-meta"><span>Premium <b>${dPnl(totalPremium, 'USD')}</b></span><span>Fees <b>${dPnl(-Math.abs(fees), 'USD')}</b></span><span>Avg <b>${pct(totalPremium > 0 ? totalProfit / totalPremium * 100 : null)}</b></span></div>
  </div>`;
  box.innerHTML = html;
}""")

with open(DST, 'w', encoding='utf-8', newline='') as f:
    f.write(s)
print(f'Napravljeno: {DST.name}')

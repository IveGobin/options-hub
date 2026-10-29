"""Kopira 'IBKR Unified Analyzer.html' u 'IBKR Unified Analyzer (mobile preview).html' i na kopiji
dodaje mobilni prikaz Stocks taba s karticama (ispod 700px širine). Original se ne mijenja.

Pokretanje:  python make_mobile_preview.py
Pregled na desktopu: suzi prozor ispod 700px ili u DevTools uključi prikaz za mobitel (npr. 390px),
ili na kraj URL-a dodaj #cards da se kartice prikažu na bilo kojoj širini.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / 'IBKR Unified Analyzer.html'
DST = HERE / 'IBKR Unified Analyzer (mobile preview).html'

s = SRC.read_text(encoding='utf-8')


def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, f'Očekivano točno 1 pojavljivanje, nađeno {n}: {old[:80]!r}'
    s = s.replace(old, new)


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
    <div class="sc-note">of which currency effect: <strong style="color:${pnlColor(eurFig.fx)}">${fmtPnl(eurFig.fx, dispSym())}</strong>
      <span class="info-tip" tabindex="0" title="${escHtml(STOCK_ECON_TIP)}">ⓘ</span>
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
      const bar = kept === null
        ? `<div class="oc-barlbl"><span>Bought option (debit) · no premium to keep</span></div>`
        : `<div class="oc-bar"><div class="oc-fill ${keptCls(kept)}" style="width:${Math.max(0, Math.min(100, kept)).toFixed(1)}%"></div><div class="oc-target" style="left:80%"></div></div>
           <div class="oc-barlbl"><span>${pct(kept, 1)} kept</span><span>target 80%</span></div>`;
      html += `<div class="oc-card ${act || 'quiet'}">
        <div class="oc-head">
          <span class="oc-title"><span class="type-badge ${p.type}">${p.type}</span><strong>${escHtml(p.ticker)}</strong><span class="oc-strike">${fmtNative(p.strike, '$', p.strike%1===0?0:2)}</span></span>
          <span class="${p.unrPL>0?'unr-pos':p.unrPL<0?'unr-neg':'unr-neu'}">${dPnl(p.unrPL, 'USD')}</span>
        </div>
        <div class="oc-sub">${fmtDate(p.expiry)} · ${dl < 0 ? Math.abs(dl) + 'd ago' : dl === 0 ? 'today' : dl + 'd left'} · ×${p.qty}</div>
        ${bar}
        ${badges.length ? `<div class="oc-badges">${badges.join('')}</div>` : ''}
        <div class="oc-meta"><span>Premium <b>${fmtPrem(p.premiumCollected)}</b></span><span>To close <b>${dMoney(p.currentValue, 'USD')}</b></span>${p.exposure !== null ? `<span>Exposure <b>${fmtK(p.exposure)}</b></span>` : ''}</div>
        <details class="sc-more"><summary>Details</summary>
          <div class="sc-grid">
            <span>Qty</span><span>${p.qty}</span>
            <span>Premium / share</span><span>${fmtPnl(perShare, '$')}</span>
            <span>80% buyback price</span><span>${kept === null ? '—' : fmtNative(target, '$') + '/sh'}</span>
            <span>Cost to close</span><span>${dMoney(p.currentValue, 'USD')}</span>
            <span>Unrealized P&amp;L</span><span class="${pnlCls(p.unrPL)}">${dPnl(p.unrPL, 'USD')}</span>
            <span>Exposure</span><span>${p.exposure !== null ? fmtK(p.exposure) : '—'}</span>
          </div>
        </details>
      </div>`;
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

with open(DST, 'w', encoding='utf-8', newline='') as f:
    f.write(s)
print(f'Napravljeno: {DST.name}')

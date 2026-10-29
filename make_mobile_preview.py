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

with open(DST, 'w', encoding='utf-8', newline='') as f:
    f.write(s)
print(f'Napravljeno: {DST.name}')

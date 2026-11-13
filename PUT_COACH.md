# Put Coach — dokumentacija (v1.8)

Put Coach je alat za upravljanje rizikom kod prodaje short putova na IBKR računu s marginom.
Odgovara na tri pitanja:

1. **Jesam li sada siguran?** (likvidnost, izloženost, margin cushion, kvaliteta i raspršenost knjige)
2. **Koliko još putova smijem prodati?** (slobodni prostor, "room")
3. **Što bi napravila jedna konkretna nova pozicija?** (what-if)

Svi izračuni rade se u pregledniku. Ništa se ne šalje na server.

---

## 1. Brzi početak

1. Otvori **Put Coach** iz huba.
2. Klikni **Import IBKR** i učitaj Activity Statement CSV (može više datoteka; koristi se najnoviji).
   Import popuni NLV, vrijednost dionica, nominal putova i podatke o pozicijama.
3. Iz **TWS / Client Portala** (prozor *Account*) prepiši **Excess Liquidity** u polje *Excess liquidity (TWS)*.
   Toga podatka nema u Activity Statementu, pa ga import nikad ne mijenja.
4. Provjeri **VIX** (učitava se iz `vix_povijest.json`, može se ručno pomaknuti) i **EUR/USD** tečaj
   (učitava se iz `tecajna_lista_usd.json`, zadano 1.17).
5. Odaberi **mod** (Conservative / Moderate / Aggressive) i po potrebi promijeni **Max assignment loan**.
6. Pročitaj **status** (zelena / žuta / crvena poruka), **radar** i karticu **What can I sell today?**
7. Prije nove pozicije upiši je u **What-if** (broj ugovora, strike u $, po želji ticker i datum isteka).

### Ručni unos (bez importa)

Upiši NLV, excess, nominal putova (slider) i vrijednost dionica. Radar, status i what-if rade normalno.
Koncentracija po tickeru/datumu i Put Quality trebaju import (bez njega su neutralni).

---

## 2. Ulazni podaci

| Polje | Valuta | Izvor | Napomena |
|---|---|---|---|
| Net liquidation value (NLV) | EUR/USD | import (*Net Asset Value → Total*) ili ručno | Bez NLV-a ništa se ne prikazuje |
| Excess liquidity (TWS) | EUR/USD | **samo ručno**, iz TWS-a | Već ima odbijenu trenutnu maintenance marginu |
| Put notional sold | EUR/USD (slider) | import: Σ \|qty\| × multiplier × strike svih short putova | U USD |
| Stock holdings | EUR/USD | import (*Net Asset Value → Stock*) ili ručno | Tržišna vrijednost dionica |
| Max assignment loan | % NLV | mod (0 / 20 / 50 %) ili ručno | Koliki margin kredit prihvaćaš ako se SVI putovi assignaju |
| VIX | — | `vix_povijest.json` ili slider 5–60 | Utječe na cilj likvidnosti |
| EUR/USD | — | `tecajna_lista_usd.json` ili ručno | Sve se interno računa u EUR |

**Valute.** Svako polje ima EUR/USD prekidač. Kod prebacivanja vrijednost se pretvara tečajem
(npr. 26 000 EUR ↔ 30 420 USD kod 1.17). Interno je sve u EUR: `EUR = USD / fx`.

**Upozorenje:** ako je excess veći od NLV-a, ispod polja se pojavi crveno upozorenje (vjerojatno tipfeler,
TWS excess nikad ne može biti veći od NLV-a).

---

## 3. Modovi

| Mod | Hard stop (excess % NLV) | VIX base | VIX slope | VIX cap | Zadani loan |
|---|---|---|---|---|---|
| 🛡️ Conservative | 40 % | 50 % | 0.50 | 70 % | 0 % |
| ⚖️ Moderate | 30 % | 40 % | 0.75 | 60 % | 20 % |
| 🔥 Aggressive | 20 % | 30 % | 0.50 | 45 % | 50 % |

Promjena moda postavlja *Max assignment loan* na zadanu vrijednost moda. Nakon toga se može ručno mijenjati.

---

## 4. Osnovne veličine

Sve u EUR. `wi` = what-if nominal (vidi §8); bez what-ifa je 0.

```
NLV            = net liquidation value
excessIn       = excess iz TWS-a (danas)
excess         = excessIn − wi × MARGIN               MARGIN = 0.20
notional       = put notional + wi
stocks         = vrijednost dionica
totalExp       = stocks + notional                    (izloženost ako se SVI putovi assignaju)
leverage       = totalExp / NLV
loan           = max(0, totalExp − NLV)

maxTotal       = NLV × (1 + loan% / 100)              zelena granica izloženosti
warnTotal      = NLV × (1 + (loan% + 25) / 100)       iznad toga je crveno

target%        = min(VIXcap, VIXbase + max(0, VIX − 15) × VIXslope)
targetExcess   = target% × NLV                        zeleni pod likvidnosti
stopExcess     = hardStop% × NLV                      hard stop

cushion        = max(0, excess) / totalExp            pad tržišta koji pojede excess
```

**Margin cushion** je ravnomjerni pad svih underlyinga (uz najgori slučaj, delta 1) koji bi potrošio
današnji excess, što znači margin call. Excess iz TWS-a već ima odbijenu marginu, pa se ona ne oduzima ponovno.
Ako bi ni potpuni gubitak ne potrošio excess, prikazuje se **100%+**.

**Primjer:** excess 26 000 EUR, dionice 59 500 EUR, putovi 138 000 EUR, pa je totalExp = 197 500 EUR i
cushion = 26 000 / 197 500 ≈ **13 %**. Knjiga preživi pad od 13 %; veći pad znači margin call.

---

## 5. Zone (semafor)

| Mjera | 🟢 Zeleno | 🟡 Upozorenje | 🔴 Opasno |
|---|---|---|---|
| Likvidnost | excess ≥ targetExcess | stopExcess ≤ excess < targetExcess | excess < stopExcess |
| Izloženost | totalExp ≤ maxTotal | ≤ warnTotal | > warnTotal |
| Margin cushion | ≥ 20 % | 10–20 % | < 10 % |

**Ukupna zona** = najgora od te tri. Bez ijedne pozicije (totalExp = 0) nizak excess je problem tek
ispod hard stopa.

Put Quality i koncentracija prikazuju se na radaru, ali **ne mijenjaju ukupnu zonu ni status poruku**.

---

## 6. Status poruka

Prikazuje se najteži problem, ovim redoslijedom:

| # | Uvjet | Poruka | Savjet |
|---|---|---|---|
| 1 | excess < stopExcess | 🔴 Reduce positions | treba još `stopExcess − excess` EUR excessa |
| 2 | izloženost crvena | 🔴 Overexposed | smanji izloženost za `totalExp − warnTotal` |
| 3 | cushion < 10 % | 🔴 Margin call risk | smanji izloženost za `cut(10 %)` |
| 4 | likvidnost žuta | ⚠️ Hold — liquidity low | treba još `targetExcess − excess` |
| 5 | izloženost žuta | ⚠️ Caution — above loan target | smanji za `totalExp − maxTotal` |
| 6 | cushion 10–20 % | ⚠️ Caution — thin margin cushion | smanji za `cut(20 %)` |
| 7 | room > 100 EUR | ✅ Free to sell | može se dodati ~room EUR nominala |
| 8 | inače | ✅ Green — at the limit | malo prostora |

Koliko izloženosti treba zatvoriti da cushion dođe na c. Zatvaranje puta oslobađa i ~20 % njegove margine:

```
cut(c) = max(0, (c × totalExp − excess) / (MARGIN + c))
```

---

## 7. Room — koliko još smijem prodati

Koliko NOVOG put nominala (EUR) stane prije nego ijedna granica prestane biti zelena.
Nova pozicija Δ troši `MARGIN × Δ` excessa. Sve tri granice linearne su u Δ:

```
exposure  = maxTotal − totalExp                                  (totalExp + Δ ≤ maxTotal)
liquidity = (excess − targetExcess) / MARGIN                     (excess − 0.2Δ ≥ targetExcess)
margin    = (excess − 0.20 × totalExp) / (MARGIN + 0.20)         ((excess − 0.2Δ)/(totalExp + Δ) ≥ 20 %)

room      = min(exposure, liquidity, margin)   (negativno = 0)
binding   = granica koja daje minimum
```

Isti izračun koriste status poruka, kartica *What can I sell today?* i what-if ("fits / too big").

---

## 8. What-if (nova short put pozicija)

Polja su u **USD** (US opcije): *Contracts*, *Strike $*, opcionalno *Ticker* i *Expiry*.

```
wiUSD = contracts × 100 × strike
wi    = wiUSD / fx                (EUR)
```

What-if se dodaje u nominal i troši 20 % svog nominala iz excessa (§4). Sve kartice (leverage, radar,
status, room) pokazuju stanje **nakon** te pozicije.

| Upisano | Prikaz |
|---|---|
| ništa / bez strikea | uputa |
| samo strike | "Up to N contracts fit at $K" |
| strike + broj ugovora | ✅ Fits / ⚠️ Too big (+ koja granica puca, max broj ugovora) i tablica prije → poslije |

**Max broj ugovora** (računa se iz roomBefore, tj. prije what-ifa):

```
fit = floor(roomBefore × fx / (100 × strike))
```

**Tablica prije → poslije:** notional, margin used (~20 %), leverage, excess (% NLV), survives drop,
udio tickera (ili "New ticker"), udio datuma isteka (ili "New expiry").
Bez tickera what-if se računa kao novi ticker, a bez datuma kao novi datum isteka.

**Clear** briše sva četiri polja.

---

## 9. Radar (6 osi)

Svaka os ima score 0–1 (na radaru 0–100 %). **≥ 0.70 zeleno, 0.40–0.70 žuto, < 0.40 crveno.**
Isprekidani zeleni poligon (cilj) je na 0.70 na svim osima. Vrijednosti i zone svake osi vide se u
**Axis breakdown** (zatvoren po defaultu, otvara se klikom).

### 9.1 Liquidity

```
excess ≥ targetExcess:  0.70 + (excess − targetExcess) / targetExcess × 0.30      (max 1.0)
excess ≥ stopExcess:    0.40 + (excess − stopExcess) / (targetExcess − stopExcess) × 0.30
inače:                  excess / stopExcess × 0.40
```

### 9.2 Put Quality

Koliko su prodani putovi "u redu", tj. koliko ih je OTM, a koliko ITM. Izvod **nema cijene dionica**, pa se
moneyness procjenjuje iz cijene opcije:

```
r = trenutna cijena opcije / prikupljena premija      (Close Price / Cost Price iz Open Positions)
d = max(0, (cijena opcije − premija) / strike)        gubitak po dionici kao % strikea
```

Kvaliteta svakog puta q:

| Stanje | Uvjet | q |
|---|---|---|
| Deep OTM | r ≤ 0.35 | 1 − 0.2·r → 0.93–1.00 |
| OTM | 0.35 < r ≤ 1 | 1 − 0.2·r → 0.80 (svježe prodan put) |
| Near strike | 1 < r ≤ 2 | 0.80 − 0.35·(r − 1) → 0.45 |
| Likely ITM | r > 2, d < 10 % | 0.45 · (1 − d / 0.10) |
| Deep ITM | r > 2, d ≥ 10 % | 0 |
| Nema podatka | r nepoznat | 0.70 |

Score knjige je prosjek q ponderiran nominalom. **ITM i deep ITM putovi broje dvostruko**:

```
w_i   = notional_i × (r_i > 2 ? 2 : 1)
score = Σ w_i × q_i / Σ w_i
```

What-if put ulazi kao svježe prodan (q = 0.80, ponder 1). Bez putova score je neutralnih 0.70.

| Knjiga | Score |
|---|---|
| sve svježe prodano | 0.80 🟢 |
| 50 % deep OTM + 50 % near strike (r = 1.5) | 0.81 🟢 |
| 70 % deep OTM + 30 % ITM (d = 5 %) | 0.64 🟡 |
| polovica deep ITM | < 0.40 🔴 |

**Vrijednost u Axis breakdown:** `score % · udio ITM` (likely + deep ITM, po nominalu).

**Ograničenje:** klasifikacija ide po r, a dubina ITM-a po d. Put s visokom početnom premijom može imati
r < 2 ("near strike") iako je d već oko 10 %.

### 9.3 Exposure

```
totalExp ≤ maxTotal:    0.70 + (1 − totalExp / maxTotal) × 0.30
totalExp ≤ warnTotal:   0.40 + (warnTotal − totalExp) / (warnTotal − maxTotal) × 0.30
inače:                  max(0, 0.40 − (totalExp − warnTotal) / warnTotal × 0.40)
```

### 9.4 Margin Safety

```
cushion ≥ 20 %:   0.70 + (cushion − 0.20) / 0.20 × 0.30     (max 1.0)
cushion ≥ 10 %:   0.40 + (cushion − 0.10) / 0.10 × 0.30
inače:            cushion / 0.10 × 0.40
```

### 9.5 Ticker Concentration (dionice + putovi)

```
udio tickera = (vrijednost dionica tickera + put nominal tickera) / (sve dionice + svi putovi)
tc           = najveći udio
```

- **ETF-ovi** (prema *Financial Instrument Information → Type ETF*) ulaze u ukupni zbroj, ali se nikad ne
  broje kao jedan ticker, jer su već raspršeni.
- Dionice u EUR pretvaraju se tečajem; dionice u ostalim valutama se preskaču.

```
raw = tc ≤ 40 %:  0.70 + (1 − tc / 0.40) × 0.30
      inače:      max(0, 0.70 − (tc − 0.40) / 0.20 × 0.30)        (60 % → 0.40)

weight = min(1, totalExp / maxTotal)
score  = raw + (1 − raw) × (1 − weight)
```

Mala knjiga u odnosu na limit nosi malo stvarnog rizika, pa se score povlači prema 1.0.

### 9.6 Date Concentration (samo putovi)

```
dc = najveći udio nominala na jednom datumu isteka

raw = dc ≤ 35 %:  0.70 + (1 − dc / 0.35) × 0.30
      dc ≤ 70 %:  0.40 + (0.70 − dc) / 0.35 × 0.30
      inače:      max(0, 0.40 − (dc − 0.70) / 0.30 × 0.40)

putRoom = maxTotal − stocks
weight  = min(1, notional / putRoom)
score   = raw + (1 − raw) × (1 − weight)
```

---

## 10. Kartica Leverage

- **Leverage if all puts assigned:** totalExp / NLV.
- **Loan:** `max(0, totalExp − NLV)` u % NLV-a, uz cilj (loan %).
- **Traka:** pozicija trenutne izloženosti uz oznake NLV, cilja (loan %) i crvene granice (loan % + 25).
  What-if je prikazan kao nastavak trake.
- **Tablica:** dionice, short putovi (EUR i USD), ukupna izloženost, loan, max uz cilj, preostali prostor
  ili prekoračenje.
- **Risk-weighted (info):** prikazuje se samo ako se razlikuje od sirovog leveragea (§11).
- **Excess liquidity today** (i *after the what-if*), uz cilj (VIX) i hard stop u % NLV-a.

---

## 11. Kartica Put book quality

Prikazuje se nakon importa. Svaki short put dobije status po r (i d, vidi §9.2):
**Deep OTM · OTM · Near strike · Likely ITM · Deep ITM · n/a**.

- **Traka i legenda:** udio nominala po statusu.
- **Risk-weighted nominal (samo informativno):** svaki put dobije ponder w (0.1–1.0):

  ```
  m  = 0.15 + 0.85 × min(1, r / 2.5)                moneyness
  t0 = 0.6 + 0.4 × min(1, DTE / 45)                 vremenski popust
  k  = clamp((r − 0.2) / 0.3, 0, 1)                 0 = jasno deep OTM, 1 = bez popusta
  t  = t0 + (1 − t0) × k
  w  = m × t                                         (nepoznat r: w = 0.6)

  riskFactor = 0.6 + 0.4 × (Σ w × notional / Σ notional)
  ```

  Loan cilj i margina **uvijek** koriste sirovi nominal; risk-weighted je samo informacija.
- **Needs attention:** putovi near strike, likely ITM ili deep ITM, te OTM / n/a putovi s DTE ≤ 7.
  Sortirani po `w × notional`, prikazuje se do 8 redaka.
- DTE se računa od datuma izvoda (cijene opcija su s tog dana).

---

## 12. What can I sell today?

Sklopiva kartica (klik na naslov).

- **Headline:** `+room EUR notional` ili *No room to add*, uz binding granicu.
- **Mjerači:**
  - Liquidity (`excess % NLV / ≥ cilj`)
  - Exposure (`leverage / ≤ 1 + loan%`)
  - Margin (`cushion % / ≥ 20 %`)
- **Avoid these tickers:** tickeri s udjelom ≥ 25 % (dionice + putovi, uključujući what-if).
- **Avoid these expiry dates:** datumi s ≥ 30 % put nominala.
- **Prefer these expiry months:** prva 3 od sljedećih 6 mjeseci koji nemaju koncentrirani datum isteka
  (npr. koncentrirani 18DEC26 blokira samo prosinac 2026).
- **Ideal next trade:** novi ticker, prvi predloženi mjesec, nominal ≤ min(room, 15 % NLV).
  Ako je room ≤ 100 EUR, prikazuje se *None*.

---

## 13. Import (IBKR Activity Statement CSV)

| Sekcija | Što se čita |
|---|---|
| `Statement → Period` | datum izvoda (kraj perioda) |
| `Net Asset Value` | *Total* → NLV, *Stock* → vrijednost dionica (bazna valuta, EUR) |
| `Open Positions` (opcije) | short putovi (qty < 0, simbol `TICKER DDMMMYY STRIKE P`): nominal = \|qty\| × multiplier × strike; *Cost Price* (premija), *Close Price* (cijena) |
| `Open Positions` (dionice, Summary) | ticker, valuta, tržišna vrijednost (za koncentraciju) |
| `Financial Instrument Information` | dionice tipa ETF (simbol može biti "COPA, COPAl") |

- Stupci se traže po nazivu u headeru, pa import radi i kad IBKR doda ili premjesti stupce.
- Kod više datoteka koristi se **samo najnoviji izvod**, jer je *Open Positions* snapshot.
  Zbrajanje bi dvaput brojalo iste putove.
- **Excess liquidity se nikad ne importira** (nije u izvodu).
- Banner nakon importa pokazuje NLV, dionice, nominal, top ticker, top datum i risk-weighted %.
  ✕ briše import.

---

## 14. Ograničenja i pretpostavke

- **MARGIN = 20 %** je gruba procjena margine za novi short put. Stvarna IBKR margina ovisi o
  underlyingu i volatilnosti.
- **Cushion** pretpostavlja ravnomjeran pad svih pozicija s deltom 1 (najgori slučaj). U stvarnosti
  OTM putovi gube sporije, ali korelacija u krahu je visoka.
- **Moneyness** (Put Quality, Put book quality) je procjena iz cijene opcije, ne iz cijene dionice.
- Excess i VIX su ručni ili dnevni podaci. Provjeri ih prije odluke.
- Podaci izvoda su s datuma izvoda, ne od danas.

---

## 15. Konstante (za izmjene)

| Konstanta | Vrijednost | Značenje |
|---|---|---|
| `MARGIN` | 0.20 | margina novog puta po EUR nominala |
| `CUSHION_GREEN` / `CUSHION_WARN` | 0.20 / 0.10 | granice margin cushiona |
| `LOAN_WARN_BAND` | 25 | p.p. iznad loan cilja do crvene zone |
| `LOAN_DEFAULT` | 0 / 20 / 50 | zadani loan po modu |
| `DEEP_ITM` | 0.10 | d iznad kojeg je put deep ITM |
| `FX_DEFAULT` | 1.17 | EUR/USD ako tečajna lista nije dostupna |
| Zone score | 0.70 / 0.40 | zeleno / crveno |

## Changelog

- 2026-11-13 (v1.8): prva verzija dokumentacije. Put Quality os umjesto VIX Buffer; Axis breakdown sklopiv.

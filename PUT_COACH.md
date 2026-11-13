# Put Coach — dokumentacija (v1.10)

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
   Ako je izvod stariji od 3 dana, banner upozorava: putovi prodani nakon izvoda već su u excessu, ali
   nisu u nominalu. Dodaj ih ručno na slider *Put notional sold*, inače su cushion i room precijenjeni.
3. Iz **TWS / Client Portala** (prozor *Account*) prepiši **Excess Liquidity** u polje *Excess liquidity (TWS)*.
   Toga podatka nema u Activity Statementu, pa ga import nikad ne mijenja.
4. Provjeri **VIX** (učitava se iz `vix_povijest.json`, može se ručno pomaknuti) i **EUR/USD** tečaj
   (učitava se iz `tecajna_lista_usd.json`, zadano 1.17).
5. Odaberi **mod** (Conservative / Moderate / Aggressive) i po potrebi odaberi drugi **Max assignment loan** (30 / 60 / 90 %).
6. Pročitaj **status** (zelena / žuta / crvena poruka), **radar** i karticu **What can I sell today?**
7. Prije nove pozicije upiši je u **What-if** (broj ugovora, strike u $, po želji ticker i datum isteka).

### Ručni unos (bez importa)

Upiši NLV, excess, nominal putova (slider) i vrijednost dionica. Radar, status i what-if rade normalno.
Koncentracija po tickeru/datumu i Put Quality trebaju import (bez njega su neutralni).
Nominal iznad importiranog (ručno podignut slider) ulazi u izloženost, ali ne u koncentraciju ni u Put Quality.

---

## 2. Ulazni podaci

| Polje | Valuta | Izvor | Napomena |
|---|---|---|---|
| Net liquidation value (NLV) | EUR/USD | import (*Net Asset Value → Total*) ili ručno | Bez NLV-a ništa se ne prikazuje |
| Excess liquidity (TWS) | EUR/USD | **samo ručno**, iz TWS-a | Već ima odbijenu trenutnu maintenance marginu |
| Put notional sold | EUR/USD (slider) | import: Σ \|qty\| × multiplier × strike svih short putova | U USD |
| Stock holdings | EUR/USD | import (*Net Asset Value → Stock*) ili ručno | Tržišna vrijednost dionica |
| Max assignment loan | % NLV | tri gumba: 30 / 60 / 90 % (zadano 60 %) | Koliki margin kredit prihvaćaš ako se SVI putovi assignaju |
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
| 🛡️ Conservative | 40 % | 50 % | 0.50 | 70 % | 30 % |
| ⚖️ Moderate | 30 % | 40 % | 0.75 | 60 % | 60 % |
| 🔥 Aggressive | 20 % | 30 % | 0.50 | 45 % | 90 % |

Promjena moda postavlja *Max assignment loan* na zadanu vrijednost moda. Nakon toga se gumbima može
odabrati druga vrijednost (npr. Moderate uz 90 %). Zadano pri otvaranju: Moderate, loan 60 %.

**Što loan znači.** To je najveći margin kredit koji prihvaćaš ako se SVI putovi assignaju odjednom:

| Loan | Poluga nakon assignmenta | Pad do margin calla nakon assignmenta (maintenance 25 % / 50 %) |
|---|---|---|
| 30 % | 1.3x | oko 69 % / 54 % |
| 60 % | 1.6x | oko 50 % / 25 % |
| 90 % | 1.9x | oko 37 % / 5 % |

Pad do margin calla je gruba procjena: `1 − loan / ((1 − maintenance) × (1 + loan))`. Volatilne dionice
često imaju maintenance marginu 50 % ili više.

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

**Primjer** (Moderate, VIX 18, loan 60 %): NLV 60 000, excess 26 000, dionice 59 500, putovi 138 000 EUR.

```
target%      = 40 + (18 − 15) × 0.75 = 42.25 %   →  targetExcess = 25 350    (excess 26 000: zeleno)
stopExcess   = 30 % × 60 000 = 18 000
totalExp     = 59 500 + 138 000 = 197 500        →  leverage 3.29x
maxTotal     = 96 000,  warnTotal = 111 000      (izloženost: crveno)
cushion      = 26 000 / 197 500 ≈ 13 %           (žuto)
```

Status: 🔴 Overexposed, smanji izloženost za 197 500 − 111 000 = 86 500 EUR; *Also: thin margin cushion*.
Uz samo dionice (59 500) prostor za putove je 96 000 − 59 500 = 36 500 EUR.

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

**Kada je margin cushion stvarna granica.** Čim su likvidnost i izloženost zelene, cushion je automatski
≥ target% / (1 + loan %), a target% je najmanje VIXbase:

| Mod \ Loan | 30 % | 60 % | 90 % |
|---|---|---|---|
| Conservative (VIXbase 50 %) | 38 % | 31 % | 26 % |
| Moderate (40 %) | 31 % | 25 % | 21 % |
| Aggressive (30 %) | 23 % | 19 % | 16 % |

Cushion (zeleno ≥ 20 %) zato može biti binding samo u modu Aggressive uz loan 60 % ili 90 % i nizak VIX.
U ostalim kombinacijama ga likvidnost i izloženost već pokrivaju, pa se poruke #3 i #6 pojavljuju samo
kao "Also" uz neki drugi problem.

---

## 6. Status poruka

Skupe se svi aktivni problemi ovim redoslijedom. Prvi je naslov i savjet, a ostali se navode iza
"Also: …".

| # | Uvjet | Poruka | Savjet |
|---|---|---|---|
| 1 | excess < stopExcess | 🔴 Reduce positions | excessu fali `stopExcess − excess`; zatvori ~`(stopExcess − excess) / MARGIN` nominala ili dodaj gotovinu |
| 2 | izloženost crvena | 🔴 Overexposed | smanji izloženost za `totalExp − warnTotal` |
| 3 | cushion < 10 % | 🔴 Margin call risk | smanji izloženost za `cut(10 %)` |
| 4 | likvidnost žuta | ⚠️ Hold — liquidity low | excessu fali `targetExcess − excess`; zatvori ~`(targetExcess − excess) / MARGIN` nominala ili dodaj gotovinu |
| 5 | izloženost žuta | ⚠️ Caution — above loan target | smanji za `totalExp − maxTotal` |
| 6 | cushion 10–20 % | ⚠️ Caution — thin margin cushion | smanji za `cut(20 %)` |
| 7 | nema problema, room > 100 EUR | ✅ Free to sell | može se dodati ~room EUR nominala |
| 8 | inače | ✅ Green — at the limit | malo prostora |

Koliko izloženosti treba zatvoriti da cushion dođe na c. Zatvaranje puta oslobađa i ~20 % njegove margine:

```
cut(c) = max(0, (c × totalExp − excess) / (MARGIN + c))
```

**Skori assignment.** Ako ima putova sa statusom Likely ITM ili Deep ITM koji istječu unutar 7 dana
(računato od danas), status na kraju dodaje: `⏰ N ITM puts expire within 7 days (~$X assignment)`.
To je kredit koji stvarno dolazi, a ne hipotetski "svi assignani".

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
status, room) pokazuju stanje **nakon** te pozicije. Iznimka je os Put Quality: what-if u nju ne ulazi,
jer prodaja novih putova ne smije popraviti ocjenu postojeće knjige.

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
excess ≥ targetExcess:  0.70 + (excess − targetExcess) / (NLV − targetExcess) × 0.30
excess ≥ stopExcess:    0.40 + (excess − stopExcess) / (targetExcess − stopExcess) × 0.30
inače:                  excess / stopExcess × 0.40
```

Score je 1.0 kad je excess jednak NLV-u (ništa nije na margini), u svakom modu i uz svaki VIX.

### 9.2 Put Quality

Koliko prodani putovi trenutno gube. Izvod **nema cijene dionica**, pa se os gradi od dvije veličine koje
se mogu točno izračunati iz *Open Positions*:

```
r = cijena opcije / prikupljena premija          je li put jeftiniji ili skuplji nego kad je prodan
L = max(0, (cijena opcije − premija) / strike)   nerealizirani gubitak kao udio nominala
```

L nikad nije veći od `cijena opcije / strike`, a to je gornja granica dubine ITM-a (cijena puta je uvijek
≥ intrinzične vrijednosti). Zato jeftin put kojem se cijena samo udvostručila ili utrostručila (skok
volatilnosti) ostaje "near strike".

Kvaliteta svakog puta q, bez skokova:

| Stanje | Uvjet | q |
|---|---|---|
| Deep OTM | r ≤ 0.35 | 1 − 0.2·r → 0.93–1.00 |
| OTM | 0.35 < r ≤ 1 | 1 − 0.2·r → 0.80 (svježe prodan put) |
| Near strike | r > 1, L < 5 % | 0.80 · (1 − L / 0.10) → 0.80–0.40 |
| Likely ITM | r > 1, 5 % ≤ L < 10 % | 0.80 · (1 − L / 0.10) → 0.40–0 |
| Deep ITM | r > 1, L ≥ 10 % | 0 |
| Nema podatka | r nepoznat | 0.70 |

Score knjige je prosjek q ponderiran nominalom. Putovi u gubitku teže više, do dvostruko:

```
w_i   = notional_i × (1 + min(1, L_i / 0.10))      (za r ≤ 1 ponder je 1)
score = Σ w_i × q_i / Σ w_i
```

What-if put **ne ulazi** u score. Bez importiranih putova score je neutralnih 0.70.

| Knjiga | Score |
|---|---|
| sve svježe prodano | 0.80 🟢 |
| 50 % deep OTM + 50 % s gubitkom L = 2 % | 0.80 🟢 |
| 70 % deep OTM + 30 % s L = 5 % | 0.77 🟢 |
| 50 % deep OTM + 50 % s L = 5 % | 0.64 🟡 |
| polovica deep ITM | 0.33 🔴 |

**Vrijednost u Axis breakdown:** `score % · udio ITM` (likely + deep ITM, po nominalu).

**Ograničenje:** L je gubitak, a ne stvarna dubina ITM-a. Dugoročni put s velikom vremenskom vrijednošću
može imati visok L, a još biti OTM. Nazivi "Likely ITM" i "Deep ITM" su zato procjena.

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
weight  = min(1, notional / putRoom)        (notional = 0 → 0;  putRoom ≤ 0 → 1)
score   = raw + (1 − raw) × (1 − weight)
```

Datumi se broje pojedinačno: 18DEC26 i 24DEC26 su dva različita datuma.

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

Prikazuje se nakon importa. Svaki short put dobije status po r i L (vidi §9.2):
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
  riskFactor je uvijek ≤ 1, pa ovaj broj može sliku samo uljepšati. Ne koristi ga kao granicu.
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
- Ovi pragovi (25 % / 30 %) su namjerno niži od zelene granice radara (40 % / 35 %): lista pokazuje što
  je **blizu** granice, da ga nova pozicija ne gurne preko nje. Ticker može biti zelen na radaru i na listi.
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
- **Excess je od danas, a pozicije s datuma izvoda.** Putovi prodani nakon izvoda su u excessu, ali ne u
  nominalu, pa su cushion i room precijenjeni. Koristi svjež izvod ili ručno podigni nominal (§1).
- **Čitaju se samo short putovi.** Long putovi (put spreadovi) se ne odbijaju, pa je nominal spreadova
  precijenjen. Short callovi se ne čitaju, pa goli callovi nisu u izloženosti.
- **ETF iznimka je gruba:** svaki ETF se smatra raspršenim, i sektorski, jednodržavni ili leveraged.
- **Dionice izvan EUR i USD** ulaze u izloženost (preko NLV izvoda), ali ne u koncentraciju po tickeru.
- **Margin cushion** je binding samo u modu Aggressive uz loan 60 % ili 90 % (§5).

---

## 15. Konstante (za izmjene)

| Konstanta | Vrijednost | Značenje |
|---|---|---|
| `MARGIN` | 0.20 | margina novog puta po EUR nominala |
| `CUSHION_GREEN` / `CUSHION_WARN` | 0.20 / 0.10 | granice margin cushiona |
| `LOAN_WARN_BAND` | 25 | p.p. iznad loan cilja do crvene zone |
| `LOAN_OPTIONS` | 30 / 60 / 90 | ponuđeni loan (gumbi) |
| `LOAN_DEFAULT` | 30 / 60 / 90 | zadani loan po modu |
| `NEAR_LOSS` / `DEEP_ITM` | 0.05 / 0.10 | gubitak L do kojeg je put near strike / od kojeg je deep ITM |
| r pragovi | 0.35 / 1 | deep OTM / OTM |
| Ticker koncentracija | 40 % / 60 % | zeleno / crveno na radaru; lista "Avoid" od 25 % |
| Date koncentracija | 35 % / 70 % | zeleno / crveno na radaru; lista "Avoid" od 30 % |
| Min. room | 100 EUR | ispod toga "at the limit" / "No room" |
| Ideal next trade | 15 % NLV | najveći predloženi nominal |
| Starost izvoda | 3 dana | iznad toga upozorenje u banneru |
| Skori assignment | 7 dana | ITM putovi koji istječu, u statusu |
| `FX_DEFAULT` | 1.17 | EUR/USD ako tečajna lista nije dostupna |
| Zone score | 0.70 / 0.40 | zeleno / crveno |

## Changelog

- 2026-11-13 (v1.10): Max assignment loan su tri gumba 30 / 60 / 90 % umjesto polja za unos; zadano 60 %.
  Zadani loan po modu 30 / 60 / 90 % (prije 0 / 20 / 50 %).

- 2026-11-13 (v1.9): nakon pregleda formula.
  - Liquidity score skalira se prema NLV-u (1.0 kad je excess = NLV).
  - Put Quality bez skoka na r = 2: za r > 1 q i ponder ovise o gubitku L. Statusi near / likely ITM /
    deep ITM idu po L (5 % / 10 %). What-if više ne ulazi u Put Quality.
  - Status: navodi i ostale aktivne probleme ("Also"), savjet za likvidnost u nominalu, skori assignment.
  - Upozorenje u banneru kad je izvod stariji od 3 dana.
  - Dokumentirano: cushion kao osigurač za ručni loan, pragovi liste "Avoid", opseg importa.

- 2026-11-13 (v1.8): prva verzija dokumentacije. Put Quality os umjesto VIX Buffer; Axis breakdown sklopiv.

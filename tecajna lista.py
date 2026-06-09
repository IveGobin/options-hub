import requests
import json
from datetime import date, timedelta
import yfinance as yf

URL      = "https://api.hnb.hr/tecajn-eur/v3"
VALUTA   = "USD"
JSON_FILE = "tecajna_lista_usd.json"
VIX_FILE  = "vix_povijest.json"

# ── 1. TEČAJEVI USD ───────────────────────────────────────────
with open(JSON_FILE, "r") as f:
    tecajevi = json.load(f)

if tecajevi:
    zadnji = date.fromisoformat(max(tecajevi.keys()))
else:
    zadnji = date(2025, 1, 1) - timedelta(days=1)

danas = date.today()

if zadnji >= danas:
    print(f"Tečajevi su već ažurni (zadnji: {zadnji}). Nema novih podataka za dohvat.")
else:
    od = zadnji + timedelta(days=1)
    print(f"Dohvaćam tečajeve od {od} do {danas}...")

    novi = 0
    dan = od
    while dan <= danas:
        r = requests.get(URL, params={"valuta": VALUTA, "datum-primjene": str(dan)})
        if r.status_code == 200:
            podaci = r.json()
            if podaci:
                zapis = podaci[0]
                key = zapis["datum_primjene"]
                if key not in tecajevi:
                    tecajevi[key] = zapis["srednji_tecaj"]
                    novi += 1
        dan += timedelta(days=1)

    tecajevi = dict(sorted(tecajevi.items()))
    with open(JSON_FILE, "w") as f:
        json.dump(tecajevi, f, indent=2)

    print(f"Dodano {novi} novih tečajeva.")
    print(f"Ukupno tečajeva u datoteci: {len(tecajevi)}")
    print(f"Raspon: {min(tecajevi.keys())} → {max(tecajevi.keys())}")


# ── 2. VIX ────────────────────────────────────────────────────
try:
    with open(VIX_FILE, "r") as f:
        vix_povijest = json.load(f)
except FileNotFoundError:
    vix_povijest = {}

danas_str = str(danas)

if danas_str in vix_povijest:
    print(f"VIX već upisan za danas ({danas_str}): {vix_povijest[danas_str]}")
else:
    vix = yf.Ticker("^VIX")
    data = vix.history(period="5d")  # 5d kao buffer za vikende/praznike

    if not data.empty:
        zadnja_cijena = round(float(data["Close"].iloc[-1]), 2)
        zadnji_datum  = str(data.index[-1].date())

        if zadnji_datum not in vix_povijest:
            vix_povijest[zadnji_datum] = zadnja_cijena
            print(f"VIX upisan: {zadnji_datum} = {zadnja_cijena}")
        else:
            print(f"VIX za {zadnji_datum} već postoji: {vix_povijest[zadnji_datum]}")
    else:
        print("VIX: nema podataka od yfinance.")

    vix_povijest = dict(sorted(vix_povijest.items()))
    with open(VIX_FILE, "w") as f:
        json.dump(vix_povijest, f, indent=2)

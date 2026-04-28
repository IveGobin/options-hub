import requests
import json
from datetime import date, timedelta

URL      = "https://api.hnb.hr/tecajn-eur/v3"
VALUTA   = "USD"
JSON_FILE = "tecajna_lista_usd.json"

# ── Učitaj postojeće tečajeve ─────────────────────────────────
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

    # Sortiraj po datumu i spremi
    tecajevi = dict(sorted(tecajevi.items()))
    with open(JSON_FILE, "w") as f:
        json.dump(tecajevi, f, indent=2)

    print(f"Dodano {novi} novih tečajeva.")
    print(f"Ukupno tečajeva u datoteci: {len(tecajevi)}")
    print(f"Raspon: {min(tecajevi.keys())} → {max(tecajevi.keys())}")




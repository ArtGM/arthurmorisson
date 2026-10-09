"""Rend tools/og-card.html en static/images/og.jpg, 1200x630.

Usage : python3 tools/og-render.py

Nécessite Playwright. L'image est l'aperçu affiché quand un lien du site est
partagé, et elle sert aussi de champ image au JSON-LD. Après régénération,
vérifier qu'elle reste sous 300 Ko : au-delà, certains réseaux ne la chargent
pas.
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

RACINE = pathlib.Path(__file__).resolve().parent.parent
SOURCE = RACINE / "tools" / "og-card.html"
SORTIE = RACINE / "static" / "images" / "og.jpg"

with sync_playwright() as p:
    navigateur = p.chromium.launch()
    page = navigateur.new_page(viewport={"width": 1200, "height": 630})
    page.goto(SOURCE.as_uri())
    page.wait_for_timeout(900)  # laisse la police se charger
    # JPEG et non PNG : la carte est faite d'aplats et de degrades, que le
    # PNG encode trois fois plus lourd pour aucun gain visible.
    page.screenshot(path=str(SORTIE), type="jpeg", quality=88)
    navigateur.close()

poids = SORTIE.stat().st_size
print(f"{SORTIE.relative_to(RACINE)} : {poids // 1024} Ko")
if poids > 300 * 1024:
    print("ATTENTION : au-dessus de 300 Ko", file=sys.stderr)

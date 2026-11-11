"""L'horloge de PuckProb (demande de Mitch, 10 nov. 2026 : la nuit et le midi sautaient, GitHub retarde ou saute ses
horaires automatiques). Roule dans la boucle du job Live de puckprob (aux 5 min, 24 h sur 24) et part elle-même le
calcul de Tirs-nhl à ses heures, par l'API de GitHub (secret TIRS_DISPATCH de puckprob : un jeton limité à
« Actions » sur Tirs-nhl). Envoyé dans live_code/ par le calcul, comme live.py et poster.py.

Une fenêtre de 75 min après chaque heure : si la boucle redémarre ou rate un tour, elle part quand même le calcul.
Un calcul déjà fait dans sa plage s'arrête tout seul en 15 s (src/garde.py, input « horloge »), donc partir deux
fois ne fait jamais deux calculs.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

# (plage, heure, minute) en heure de l'Est : les mêmes plages que src/garde.py
CRENEAUX = [("nuit", 0, 37), ("matin", 9, 7), ("midi", 11, 37), ("fil", 13, 7), ("soir", 16, 47)]
FENETRE = timedelta(minutes=75)
DEPOT, FLUX = "MitchBurns72/Tirs-nhl", "quotidien.yml"
ETAT = Path(os.environ.get("RUNNER_TEMP") or "/tmp") / "horloge.json"


def a_partir(maintenant, faits):
    """Les plages dont l'heure est passée depuis moins de 75 min et pas encore parties."""
    out = []
    for nom, h, m in CRENEAUX:
        t = maintenant.replace(hour=h, minute=m, second=0, microsecond=0)
        cle = f"{t.date().isoformat()}-{nom}"
        if t <= maintenant < t + FENETRE and cle not in faits:
            out.append((nom, cle))
    return out


def partir(nom, jeton):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{DEPOT}/actions/workflows/{FLUX}/dispatches",
        data=json.dumps({"ref": "main", "inputs": {"horloge": nom}}).encode(),
        headers={"Authorization": f"Bearer {jeton}", "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "puckprob-horloge"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status


def main():
    jeton = os.environ.get("TIRS_DISPATCH", "").strip()
    if "--test" in sys.argv:                 # Run workflow de Live, case « tester l'horloge » : part un calcul tout de suite
        if not jeton:
            print("horloge (test) : pas de secret TIRS_DISPATCH")
            return 1
        try:
            print(f"horloge (test) : calcul de Tirs-nhl parti ({partir('test', jeton)}) : regarde ses Actions")
            return 0
        except Exception as ex:  # noqa: BLE001
            print(f"horloge (test) : RATÉ, {str(ex)[:200]} (jeton expiré, mauvais dépôt ou permission Actions manquante ?)")
            return 1
    maintenant = datetime.now(ZoneInfo("America/Toronto"))
    try:
        faits = set(json.loads(ETAT.read_text()))
    except (OSError, ValueError):
        faits = set()
    for nom, cle in a_partir(maintenant, faits):
        if not jeton:
            print(f"horloge : {nom} dû, mais pas de secret TIRS_DISPATCH")
            continue
        try:
            print(f"horloge : calcul {nom} parti ({partir(nom, jeton)})")
            faits.add(cle)
        except Exception as ex:  # noqa: BLE001  (on réessaie au prochain tour, dans la fenêtre)
            print(f"horloge : {nom} raté ({str(ex)[:120]})")
    hier = (maintenant - timedelta(days=2)).date().isoformat()
    ETAT.write_text(json.dumps(sorted(c for c in faits if c[:10] > hier)))


if __name__ == "__main__":
    sys.exit(main())

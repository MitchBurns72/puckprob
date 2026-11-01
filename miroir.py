"""Miroir du site public PuckProb.

Le site est calculé dans le dépôt Tirs-nhl (docs/public/) à chaque calcul. Ce script le copie
ici, fichier par fichier, pour qu'il soit servi directement sur puckprob.ca : pas d'iframe,
Google voit tout le texte, et aucune page ne pointe vers Tirs-nhl.

Fonctionnement :
  1. lit manifeste.json (la liste de tous les fichiers + leur empreinte sha256);
  2. télécharge seulement ceux qui ont changé, et vérifie l'empreinte de chacun;
  3. efface les fichiers qui ne sont plus dans la liste (sauf ceux de ce dépôt : PROTEGES).
Si quoi que ce soit cloche (réseau, empreinte, liste trop courte), il arrête AVANT d'effacer :
le site en ligne reste celui d'avant, jamais à moitié copié.
"""
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

SOURCE = "https://mitchburns72.github.io/Tirs-nhl/public/"
LIVE = "https://mitchburns72.github.io/Tirs-nhl/live.json"   # scores en direct (copié à chaque passage)
ICI = Path(__file__).resolve().parent
# Ce qui appartient au dépôt lui-même : jamais écrasé ni effacé par le miroir
PROTEGES = {"miroir.py", "README.md", "CNAME", "live.json", ".nojekyll"}
DOSSIERS_PROTEGES = {".git", ".github"}
MIN_FICHIERS = 30   # une liste plus courte que ça = calcul brisé, on ne touche à rien


def lire(url, essais=3):
    for i in range(essais):
        try:
            req = urllib.request.Request(f"{url}?v={int(time.time())}", headers={"User-Agent": "puckprob-miroir"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception as ex:  # noqa: BLE001
            if i == essais - 1:
                raise
            print(f"  essai {i + 1} raté ({ex}), on réessaie")
            time.sleep(5 * (i + 1))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def chemin_sur(rel):
    """Refuse tout chemin qui sortirait du dépôt (../, absolu) ou toucherait un fichier protégé."""
    p = Path(rel)
    if p.is_absolute() or ".." in p.parts or not p.parts:
        return None
    # Fichiers cachés (.nojekyll, etc.) : GitHub Pages ne les sert pas chez Tirs-nhl, on les gère ici
    if any(x.startswith(".") for x in p.parts):
        return None
    if p.parts[0] in DOSSIERS_PROTEGES or rel in PROTEGES:
        return None
    return ICI / p


def main():
    man = json.loads(lire(SOURCE + "manifeste.json"))
    fichiers = man.get("fichiers") or {}
    if len(fichiers) < MIN_FICHIERS or "index.html" not in fichiers:
        sys.exit(f"Manifeste suspect ({len(fichiers)} fichiers) : rien n'est modifié.")
    # 1. Télécharger ce qui a changé (en mémoire d'abord : rien n'est écrit tant que tout n'est pas vérifié)
    nouveaux = {}
    for rel, empreinte in fichiers.items():
        dest = chemin_sur(rel)
        if dest is None:
            continue
        if dest.exists() and sha(dest.read_bytes()) == empreinte:
            continue
        try:
            b = lire(SOURCE + rel)
        except Exception as ex:  # noqa: BLE001
            sys.exit(f"Impossible de lire {rel} ({ex}) : rien n'est modifié.")
        if sha(b) != empreinte:
            sys.exit(f"Empreinte fausse pour {rel} (calcul en cours de publication?) : rien n'est modifié, on réessaiera.")
        nouveaux[dest] = b
    # 2. Écrire
    for dest, b in nouveaux.items():
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(b)
    (ICI / ".nojekyll").write_text("")   # sert les fichiers tels quels, sans passer par Jekyll
    (ICI / "manifeste.json").write_bytes(json.dumps(man, ensure_ascii=False, indent=0).encode())
    # 3. Effacer ce qui n'existe plus à la source
    gardes = {Path(r).as_posix() for r in fichiers} | {"manifeste.json"} | PROTEGES
    effaces = 0
    for p in sorted(ICI.rglob("*"), reverse=True):
        rel = p.relative_to(ICI).as_posix()
        if p.relative_to(ICI).parts[0] in DOSSIERS_PROTEGES or p.name.startswith("."):
            continue
        if p.is_file() and rel not in gardes:
            p.unlink()
            effaces += 1
        elif p.is_dir() and not any(p.iterdir()):
            p.rmdir()
    # 4. Scores en direct (facultatif : si absent, la page interroge la LNH directement)
    try:
        (ICI / "live.json").write_bytes(lire(LIVE, essais=1))
    except Exception:  # noqa: BLE001
        pass
    print(f"Miroir : {len(nouveaux)} fichiers mis à jour, {effaces} effacés, calcul du {man.get('date')} ({man.get('genere')}).")


if __name__ == "__main__":
    main()

"""
Infos du soir : blessures (ESPN), gardiens partants et trios / unités d'avantage
numérique (DailyFaceoff), plus les SONDES qui sauvent le JSON brut une fois par jour.

POURQUOI des sondes d'abord : DailyFaceoff est un site Next.js. Ses données sont dans un
bloc JSON (__NEXT_DATA__) dont on ne connaît pas encore les noms de champs. Plutôt que de
deviner (et de lire n'importe quoi en silence), on sauve le JSON brut une fois par jour
dans data/sondes/. Le lecteur sera écrit sur la VRAIE structure à l'étape suivante.

Tout ici est optionnel : si un site plante ou change, le calcul continue sans ces infos.
"""

import json
import re
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

from cotes import norm

ESPN_BLESSURES = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/injuries"
DFO_GARDIENS = "https://www.dailyfaceoff.com/starting-goalies"
DFO_TRIOS = "https://www.dailyfaceoff.com/teams/{slug}/line-combinations"
# Statuts ESPN qui veulent dire « ne jouera pas ce soir »
ABSENTS = {"out", "injured reserve", "ir", "suspension", "suspended", "long term injured reserve", "ltir"}


def _texte(url, timeout=25):
    # Navigateur ordinaire : certains sites refusent les robots sans User-Agent
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Linux; Android 13) tirs-nhl/1.0",
                                               "Accept": "text/html,application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def blessures():
    """{nom normalisé: {"statut", "detail", "retour", "equipe"}} d'après ESPN. {} si ça plante."""
    try:
        data = json.loads(_texte(ESPN_BLESSURES))
    except Exception as ex:  # noqa: BLE001
        print(f"  blessures ESPN indisponibles : {str(ex)[:100]}")
        return {}
    out = {}
    for groupe in data.get("injuries", []) or []:
        for b in groupe.get("injuries", []) or []:
            ath = b.get("athlete") or {}
            nom = norm(ath.get("displayName"))
            if not nom:
                continue
            det = b.get("details") or {}
            out[nom] = {"statut": b.get("status") or (b.get("type") or {}).get("description") or "?",
                        "detail": " ".join(x for x in (det.get("type"), det.get("detail")) if x) or b.get("shortComment", "")[:80],
                        "retour": det.get("returnDate"),
                        "equipe": ((ath.get("team") or {}).get("abbreviation") or groupe.get("displayName"))}
    return out


def absent(info):
    return bool(info) and str(info.get("statut", "")).lower() in ABSENTS


def annoter(entries, bless):
    """Ajoute "blesse" aux joueurs listés par ESPN. On ne les retire pas : si ESPN se
    trompe, on ne perd rien, et un joueur qui ne joue pas est annulé au grading."""
    n = 0
    for e in entries:
        info = bless.get(norm(e["name"]))
        if info:
            e["blesse"] = {k: info[k] for k in ("statut", "detail", "retour")}
            n += 1
    return n


# Abréviation NHL -> adresse de l'équipe chez DailyFaceoff (eux écrivent MON, NAS, VEG...)
SLUG = {"ANA": "anaheim-ducks", "BOS": "boston-bruins", "BUF": "buffalo-sabres", "CGY": "calgary-flames",
        "CAR": "carolina-hurricanes", "CHI": "chicago-blackhawks", "COL": "colorado-avalanche",
        "CBJ": "columbus-blue-jackets", "DAL": "dallas-stars", "DET": "detroit-red-wings", "EDM": "edmonton-oilers",
        "FLA": "florida-panthers", "LAK": "los-angeles-kings", "MIN": "minnesota-wild", "MTL": "montreal-canadiens",
        "NSH": "nashville-predators", "NJD": "new-jersey-devils", "NYI": "new-york-islanders",
        "NYR": "new-york-rangers", "OTT": "ottawa-senators", "PHI": "philadelphia-flyers",
        "PIT": "pittsburgh-penguins", "SJS": "san-jose-sharks", "SEA": "seattle-kraken", "STL": "st-louis-blues",
        "TBL": "tampa-bay-lightning", "TOR": "toronto-maple-leafs", "UTA": "utah-mammoth",
        "VAN": "vancouver-canucks", "VGK": "vegas-golden-knights", "WSH": "washington-capitals",
        "WPG": "winnipeg-jets"}
ABBR_DE_SLUG = {v: k for k, v in SLUG.items()}
# Ordre d'affichage des groupes (structure réelle vue dans la sonde du 24 octobre)
GROUPES = ["f1", "f2", "f3", "f4", "d1", "d2", "d3", "g", "pp1", "pp2", "pk1", "pk2", "ir"]


def lire_trios(combinations):
    """pageProps.combinations de DailyFaceoff -> alignement compact.
    joueurs : {nom: {no, pos, face, inj, gtd}} ; groupes : {"f1": [noms], "pp1": [...], ...}."""
    joueurs, groupes = {}, {}
    for p in combinations.get("players", []) or []:
        nom = p.get("name")
        if not nom:
            continue
        joueurs.setdefault(nom, {"no": p.get("jerseyNumber"), "pos": p.get("positionIdentifier"),
                                 "face": p.get("fantasydataFaceUrl"), "inj": p.get("injuryStatus"),
                                 "gtd": bool(p.get("gameTimeDecision"))})
        groupes.setdefault(p.get("groupIdentifier") or "?", []).append(nom)
    return {"maj": combinations.get("updatedAt"), "source": combinations.get("sourceName"),
            "joueurs": joueurs, "groupes": {g: groupes[g] for g in GROUPES if g in groupes}}


def lire_gardiens(page_props):
    """pageProps de la page des gardiens partants -> {abbr NHL: {nom, statut, sv, gaa, face, maj}}."""
    out = {}
    for m in page_props.get("data", []) or []:
        for cote in ("home", "away"):
            abbr = ABBR_DE_SLUG.get(m.get(f"{cote}TeamSlug"))
            nom = m.get(f"{cote}GoalieName")
            if abbr and nom:
                out[abbr] = {"nom": nom, "statut": m.get(f"{cote}NewsStrengthName"),
                             "sv": m.get(f"{cote}GoalieSavePercentage"), "gaa": m.get(f"{cote}GoalieGoalsAgainstAvg"),
                             "fiche": f'{m.get(f"{cote}GoalieWins", 0)}-{m.get(f"{cote}GoalieLosses", 0)}-{m.get(f"{cote}GoalieOvertimeLosses", 0)}',
                             "face": m.get(f"{cote}GoalieFantasydataFaceUrl") or m.get(f"{cote}GoalieHeadshotUrl"),
                             "maj": m.get(f"{cote}NewsCreatedAt") or m.get(f"{cote}NewsUpdatedAt")}
    return out


def _cle_nom(n):
    return norm(n or "")


def noms_lnh(roster):
    """Roster de la LNH (api-web /roster/X/current) -> [(nom complet, nom de famille, numéro)]."""
    out = []
    for grp in ("forwards", "defensemen", "goalies"):
        for p in (roster or {}).get(grp, []) or []:
            pre = (p.get("firstName") or {}).get("default", "")
            fam = (p.get("lastName") or {}).get("default", "")
            if fam:
                out.append((f"{pre} {fam}".strip(), fam, p.get("sweaterNumber")))
    return out


def nom_lnh(nom, no, lnh):
    """Le nom DailyFaceoff -> le nom de la LNH (celui de nos données), sinon le même nom. Bug vu par Mitch : « Zack
    Bolduc » (DFO) vs « Zachary Bolduc » (LNH) -> classé « pas dans l'alignement » alors qu'il jouait. Ordre :
    nom exact ; même nom de famille (si deux, celui au même numéro) ; même numéro + même initiale du nom de famille."""
    k = _cle_nom(nom)
    if not k or not lnh:
        return nom
    for n, _f, _no in lnh:
        if _cle_nom(n) == k:
            return n
    fam = k.split(" ")[-1]
    pareils = [x for x in lnh if _cle_nom(x[1]).split(" ")[-1] == fam or _cle_nom(x[1]) == " ".join(k.split(" ")[1:])]
    if len(pareils) == 1:
        return pareils[0][0]
    if len(pareils) > 1 and no is not None:
        meme = [x for x in pareils if str(x[2]) == str(no)]
        if len(meme) == 1:
            return meme[0][0]
    if no is not None:
        meme = [x for x in lnh if str(x[2]) == str(no) and _cle_nom(x[1])[:1] == fam[:1]]
        if len(meme) == 1:
            return meme[0][0]
    return nom


def canoniser(eq, lnh):
    """Renomme les joueurs d'un alignement d'équipe (joueurs + groupes) avec les noms de la LNH."""
    if not lnh:
        return eq
    ren = {n: nom_lnh(n, (j or {}).get("no"), lnh) for n, j in eq.get("joueurs", {}).items()}
    eq["joueurs"] = {ren[n]: j for n, j in eq["joueurs"].items()}
    # Le numéro manquant chez DailyFaceoff (un rappelé des mineures...) : celui de la LNH, pour la plaque du site
    nos = {n: no for n, _f, no in lnh}
    for n, j in eq["joueurs"].items():
        if isinstance(j, dict) and j.get("no") in (None, "") and nos.get(n) is not None:
            j["no"] = nos[n]
    eq["groupes"] = {g: [ren.get(n, n) for n in l] for g, l in eq.get("groupes", {}).items()}
    return eq


def alignements_soir(equipes):
    """Trios + gardiens pour les équipes de ce soir. Une équipe qui plante n'empêche pas les autres."""
    out = {"maj": datetime.now(timezone.utc).isoformat(timespec="minutes"), "equipes": {}, "gardiens": {}}
    lnh = {}
    for abbr in sorted(set(equipes)):
        slug = SLUG.get(abbr)
        if not slug:
            continue
        try:
            nd = _next_data(_texte(DFO_TRIOS.format(slug=slug)))
            comb = ((nd or {}).get("props", {}).get("pageProps", {}) or {}).get("combinations")
            if comb:
                out["equipes"][abbr] = lire_trios(comb)
        except Exception as ex:  # noqa: BLE001
            print(f"  trios {abbr} : {str(ex)[:100]}")
        # Les noms de DailyFaceoff ramenés aux noms de la LNH (Zack -> Zachary Bolduc...)
        try:
            import nhl_api
            lnh[abbr] = noms_lnh(nhl_api.roster(abbr))
            if abbr in out["equipes"]:
                canoniser(out["equipes"][abbr], lnh[abbr])
        except Exception as ex:  # noqa: BLE001
            print(f"  roster {abbr} : {str(ex)[:100]}")
    try:
        nd = _next_data(_texte(DFO_GARDIENS))
        out["gardiens"] = lire_gardiens((nd or {}).get("props", {}).get("pageProps", {}) or {})
    except Exception as ex:  # noqa: BLE001
        print(f"  gardiens : {str(ex)[:100]}")
    # Gardiens : nom de la LNH et numéro (pour la plaque)
    for abbr, g in out["gardiens"].items():
        L = lnh.get(abbr) or []
        g["nom"] = nom_lnh(g.get("nom"), None, L)
        g["no"] = next((no for n, _f, no in L if n == g["nom"]), None)
    return out


def _next_data(html):
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    return json.loads(m.group(1)) if m else None


def sonder(dossier, jour):
    """Une fois par jour : sauve le JSON brut de DailyFaceoff (gardiens + trios d'une
    équipe) et d'ESPN, pour écrire les lecteurs sur la vraie structure."""
    dossier = Path(dossier)
    dossier.mkdir(parents=True, exist_ok=True)
    marque = dossier / "date.txt"
    if marque.exists() and marque.read_text().strip() == jour:
        return
    rapport = {"jour": jour}
    for nom, url in (("dfo_gardiens", DFO_GARDIENS),
                     ("dfo_trios_mtl", DFO_TRIOS.format(slug="montreal-canadiens"))):
        try:
            html = _texte(url)
            nd = _next_data(html)
            if nd is not None:
                (dossier / f"{nom}.json").write_text(json.dumps(nd, ensure_ascii=False)[:3_000_000], encoding="utf-8")
                rapport[nom] = "ok (__NEXT_DATA__)"
            else:
                (dossier / f"{nom}.html").write_text(html[:1_500_000], encoding="utf-8")
                rapport[nom] = "ok (html, pas de __NEXT_DATA__)"
        except Exception as ex:  # noqa: BLE001
            rapport[nom] = f"erreur : {str(ex)[:150]}"
    try:
        (dossier / "espn_blessures.json").write_text(_texte(ESPN_BLESSURES)[:2_000_000], encoding="utf-8")
        rapport["espn"] = "ok"
    except Exception as ex:  # noqa: BLE001
        rapport["espn"] = f"erreur : {str(ex)[:150]}"
    (dossier / "rapport.json").write_text(json.dumps(rapport, ensure_ascii=False, indent=1), encoding="utf-8")
    marque.write_text(jour)
    print("  sondes :", rapport)


if __name__ == "__main__":
    sonder(Path(__file__).resolve().parent.parent / "data" / "sondes", date.today().isoformat())

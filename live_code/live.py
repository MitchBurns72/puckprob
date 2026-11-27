"""
Mise à jour LIVE pendant les matchs (roule aux 5 minutes via la GitHub Action).

Écrit docs/live.json : pour chaque match commencé ce soir, l'état (période,
temps), le score et les stats de chaque joueur (tirs, buts, passes). La page
s'en sert pour colorer les joueurs :
  vert  = objectif atteint (même si le match continue, c'est acquis)
  jaune = match en cours, pas encore atteint
  rouge = match fini, raté

POURQUOI un fichier séparé de data.json : il change aux 5 minutes et ne doit
jamais toucher aux prédictions (gelées à la mise au jeu). Petit et jetable.

POURQUOI on n'écrit que si quelque chose a changé : chaque écriture = un commit
= une republication de la page. Pas de changement, pas de bruit.
"""

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import alignements
import nhl_api as api

# LIVE_SORTIE : quand le live roule dans le dépôt puckprob (live_code/), il écrit live.json à la racine du site
SORTIE = Path(os.environ.get("LIVE_SORTIE") or Path(__file__).resolve().parent.parent / "docs" / "live.json")
AVANT = {"FUT", "PRE"}


def jour_soiree():
    """Date de la soirée en cours. Avant 6 h du matin, on est encore dans la
    soirée d'hier (un match de 22 h à Vegas finit après minuit chez nous)."""
    maintenant = datetime.now(ZoneInfo("America/Toronto"))
    if maintenant.hour < 6:
        maintenant -= timedelta(days=1)
    return maintenant.date().isoformat()


def _sec(t):
    """« 18:42 » -> 1122 secondes (0 si illisible)."""
    try:
        m, s_ = str(t).split(":")
        return int(m) * 60 + int(s_)
    except (ValueError, AttributeError):
        return 0


def _toi(t):
    """« 18:42 » -> « 18:42 » ; rien -> « » (le temps de glace tel que la LNH l'écrit)."""
    return str(t or "")


def detail_box(box):
    """Le box score du match (Mitch, 26 nov. 2026 : « box score des matchs en direct ») : les totaux de chaque équipe,
    chaque patineur et chaque gardien, tirés de la même feuille de match (boxscore) que l'état. Compact (des listes,
    pas des objets) : live.json est relu aux 30 s par la page.
      eq : {"a"|"h": [équipe, tirs, mises en échec, tirs bloqués, minutes de pénalité, buts en avantage numérique]}
      j  : {"a"|"h": [[id, nom, pos, B, A, +/-, tirs, MÉ, TB, PUN, temps de glace], ...]}  (par points, puis temps)
      g  : {"a"|"h": [[id, nom, "arrêts/tirs", % arrêts, buts accordés, temps de glace], ...]}"""
    pb = box.get("playerByGameStats", {}) or {}
    eq, J, G = {}, {}, {}
    for k_, cote in (("a", "awayTeam"), ("h", "homeTeam")):
        t = (box.get(cote) or {}).get("abbrev") or ""
        L, tot = [], [t, 0, 0, 0, 0, 0]
        for grp in ("forwards", "defense"):
            for j in pb.get(cote, {}).get(grp, []) or []:
                r = [j.get("playerId"), (j.get("name") or {}).get("default") or "", j.get("position") or "",
                     j.get("goals", 0), j.get("assists", 0), j.get("plusMinus", 0), j.get("sog", 0), j.get("hits", 0),
                     j.get("blockedShots", 0), j.get("pim", 0), _toi(j.get("toi"))]
                L.append(r)
                for i_, v in ((1, r[6]), (2, r[7]), (3, r[8]), (4, r[9]), (5, j.get("powerPlayGoals", 0))):
                    tot[i_] += v or 0
        # Le tir officiel de l'équipe quand la feuille l'a (les tirs des joueurs peuvent traîner d'une minute)
        tot[1] = (box.get(cote) or {}).get("sog", tot[1]) or tot[1]
        L.sort(key=lambda r: (-((r[3] or 0) + (r[4] or 0)), -(r[3] or 0), -_sec(r[10])))
        J[k_], eq[k_] = L, tot
        G[k_] = [[g.get("playerId"), (g.get("name") or {}).get("default") or "", g.get("saveShotsAgainst") or "",
                  g.get("savePctg"), g.get("goalsAgainst", 0), _toi(g.get("toi"))]
                 for g in pb.get(cote, {}).get("goalies", []) or [] if g.get("toi") not in (None, "00:00")]
    return {"eq": eq, "j": J, "g": G}


def buts_match(pbp, box):
    """Le sommaire des buts, tiré du jeu-par-jeu (/gamecenter/<id>/play-by-play, les événements « goal ») :
    [[période, temps, équipe, buteur, [passeurs], force, pointage visiteur, pointage local], ...]. Les noms viennent
    de la feuille de match (mêmes « C. Caufield » que le box). force : "AN" (avantage numérique), "DN" (désavantage),
    "FD" (filet désert) ou "". Un champ qui manque : le but est gardé avec ce qu'on a (jamais de plantage)."""
    pb = box.get("playerByGameStats", {}) or {}
    noms = {}
    for cote in ("awayTeam", "homeTeam"):
        for grp in ("forwards", "defense", "goalies"):
            for j in pb.get(cote, {}).get(grp, []) or []:
                noms[j.get("playerId")] = (j.get("name") or {}).get("default") or ""
    ids = {(box.get(c) or {}).get("id"): (box.get(c) or {}).get("abbrev") for c in ("awayTeam", "homeTeam")}
    a_id = (box.get("awayTeam") or {}).get("id")
    out = []
    for jeu in (pbp or {}).get("plays") or []:
        if jeu.get("typeDescKey") != "goal":
            continue
        d = jeu.get("details") or {}
        t = ids.get(d.get("eventOwnerTeamId")) or ""
        force, sc = "", str(jeu.get("situationCode") or "")
        if len(sc) == 4 and sc.isdigit():
            # situationCode : gardien visiteur, patineurs visiteurs, patineurs locaux, gardien local
            g_a, p_a, p_h, g_h = (int(c) for c in sc)
            vis = d.get("eventOwnerTeamId") == a_id
            moi, eux, g_eux = (p_a, p_h, g_h) if vis else (p_h, p_a, g_a)
            force = "FD" if g_eux == 0 else "AN" if moi > eux else "DN" if moi < eux else ""
        passes = [noms.get(d.get(k)) or "" for k in ("assist1PlayerId", "assist2PlayerId") if d.get(k)]
        out.append([(jeu.get("periodDescriptor") or {}).get("number"), jeu.get("timeInPeriod") or "", t,
                    noms.get(d.get("scoringPlayerId")) or "", passes, force, d.get("awayScore"), d.get("homeScore")])
    return out


def etat_match(box):
    pd = box.get("periodDescriptor", {}) or {}
    clock = box.get("clock", {}) or {}
    pb = box.get("playerByGameStats", {})
    joueurs, buts = {}, {"awayTeam": 0, "homeTeam": 0}
    for cote in ("awayTeam", "homeTeam"):
        for grp in ("forwards", "defense"):
            for j in pb.get(cote, {}).get(grp, []):
                joueurs[str(j["playerId"])] = [j.get("sog", 0), j.get("goals", 0), j.get("assists", 0)]
                buts[cote] += j.get("goals", 0)
    return {
        "state": box.get("gameState"),
        "period": pd.get("number"), "periodType": pd.get("periodType"),
        "clock": clock.get("timeRemaining"), "intermission": clock.get("inIntermission", False),
        # Score officiel si présent; sinon somme des buts des joueurs (fallback)
        "hs": box.get("homeTeam", {}).get("score", buts["homeTeam"]),
        "as": box.get("awayTeam", {}).get("score", buts["awayTeam"]),
        "joueurs": joueurs,
    }


ALIGN_MINUTES = 30   # les trios et gardiens changent rarement : 30 min suffit (et ménage DailyFaceoff)


def main():
    jour = jour_soiree()
    sched = api.schedule(jour) or {}
    jeux = next((d["games"] for d in sched.get("gameWeek", []) if d["date"] == jour), [])
    commences = [g for g in jeux if g.get("gameState") not in AVANT]

    ancien = {}
    try:
        ancien = json.loads(SORTIE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    if ancien.get("date") != jour:
        ancien = {}

    # Alignements DailyFaceoff : rafraîchis aux 30 min tant qu'il reste un match à venir
    align = ancien.get("alignements")
    vieux = True
    if align and align.get("maj"):
        age = datetime.now(timezone.utc) - datetime.fromisoformat(align["maj"])
        vieux = age > timedelta(minutes=ALIGN_MINUTES)
    a_venir = [g for g in jeux if g.get("gameState") in AVANT]
    nouvel_align = False
    if jeux and a_venir and vieux:
        try:
            align = alignements.alignements_soir([g[c]["abbrev"] for g in jeux for c in ("homeTeam", "awayTeam")])
            nouvel_align = True
        except Exception as ex:  # noqa: BLE001
            print(f"  alignements : {str(ex)[:120]}")

    games = {}
    for g in commences:
        box = api.boxscore(g["id"])
        if box:
            e_ = etat_match(box)
            # Le box score (détail) + le sommaire des buts. Le jeu-par-jeu est gros : on le redemande seulement quand
            # le pointage a bougé (sinon on garde les buts d'avant).
            try:
                e_["box"] = detail_box(box)
                av = (ancien.get("games") or {}).get(str(g["id"])) or {}
                if av.get("buts") is not None and (av.get("hs"), av.get("as")) == (e_["hs"], e_["as"]):
                    e_["buts"] = av["buts"]
                else:
                    e_["buts"] = buts_match(api.get_json(f"/gamecenter/{g['id']}/play-by-play") or {}, box)
            except Exception as ex:  # noqa: BLE001  (un ajout : le pointage passe quand même)
                print(f"  box {g['id']} : {str(ex)[:120]}")
            games[str(g["id"])] = e_

    if not games and not nouvel_align:
        print(f"{jour}: aucun match commencé, alignements à jour")
        return
    if ancien.get("games") == games and not nouvel_align:
        print(f"{jour}: rien de neuf")
        return
    SORTIE.write_text(json.dumps({
        "maj": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "date": jour, "games": games, "alignements": align,
    }, ensure_ascii=False), encoding="utf-8")
    print(f"{jour}: {len(games)} matchs mis à jour" + (", alignements rafraîchis" if nouvel_align else ""))


if __name__ == "__main__":
    main()

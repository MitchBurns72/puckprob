"""Le fil du soir de PuckProb (demande de Mitch, 7 nov. 2026) : publie sur Facebook et Instagram les posts préparés
par le calcul de Tirs-nhl, chacun à son heure, au lieu de tout d'un coup.

Roule dans le dépôt PUBLIC puckprob, dans le job live (aux 5 minutes, minutes de calcul illimitées) :
  - lit social/fil/<jour>.json (la file : heure, image, légendes, commentaires ; copiée là par le calcul) ;
  - publie ce qui est dû et pas encore sorti (au plus 2 par passage : un retard se rattrape doucement) ;
    un match déjà commencé est sauté (le post n'a plus de sens) ;
  - note ce qui est sorti dans social_poste.json (racine de puckprob ; le calcul le relit pour ne rien refaire
    et pour la page puckprob.ca/liens).
Secrets du dépôt puckprob (Settings → Secrets → Actions) : META_PAGE_TOKEN, META_PAGE_ID, META_IG_ID.
Sans META_PAGE_TOKEN : ne fait rien. Code copié ici par le calcul (live_code/) : le modifier dans Tirs-nhl.
"""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

RACINE = Path(__file__).resolve().parent.parent
POSTE = RACINE / "social_poste.json"
TZ = ZoneInfo("America/Toronto")
API = os.environ.get("META_API", "v25.0")
MAX_PAR_PASSAGE = 2
GARDER = 400              # posts gardés dans social_poste.json


def _lire(f, defaut):
    try:
        return json.loads(Path(f).read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        return defaut


def _graph(chemin, champs=None, fichier=None, methode="POST", mime="image/jpeg", nom_fichier="puckprob.jpg", hote="graph"):
    """hote="graph-video" : l'adresse de Meta pour téléverser une vidéo (les vidéos du mod)."""
    url = f"https://{hote}.facebook.com/{API}/{chemin.lstrip('/')}"
    champs = dict(champs or {})
    champs["access_token"] = os.environ["META_PAGE_TOKEN"]
    if methode == "GET":
        req = urllib.request.Request(url + "?" + urllib.parse.urlencode(champs))
    elif fichier:
        sep = uuid.uuid4().hex
        corps = b""
        for k, val in champs.items():
            corps += f'--{sep}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{val}\r\n'.encode()
        corps += (f'--{sep}\r\nContent-Disposition: form-data; name="source"; filename="{nom_fichier}"\r\n'
                  f"Content-Type: {mime}\r\n\r\n").encode() + fichier + f"\r\n--{sep}--\r\n".encode()
        req = urllib.request.Request(url, data=corps, headers={"Content-Type": f"multipart/form-data; boundary={sep}"})
    else:
        req = urllib.request.Request(url, data=urllib.parse.urlencode(champs).encode())
    try:
        with urllib.request.urlopen(req, timeout=300 if mime.startswith("video") else 90) as rep:
            return json.loads(rep.read().decode("utf-8"))
    except urllib.error.HTTPError as ex:
        raise RuntimeError(f"Meta {ex.code} : {ex.read().decode('utf-8', 'replace')[:300]}") from None


# ---------------------------------------------------------------------------------
# La garde d'Instagram (11 nov. 2026 : Instagram a bloqué nos posts pour « spam soupçonné », erreur 4 / 2207051,
# après une grosse journée : 16 posts, 2 commentaires automatiques sous chacun, des posts collés une minute
# l'un après l'autre). Les règles, pour avoir l'air de ce qu'on est (un humain qui poste, pas un robot) :
#   - pas de commentaire automatique sous les posts Instagram (Facebook les garde) ;
#   - au plus IG_MAX_JOUR posts Instagram par jour et IG_ECART_MIN minutes entre deux ; les autres sortent sur
#     Facebook seulement (le post n'est pas perdu) ;
#   - Instagram bloque (2207051, ou « request limit ») : on arrête d'essayer IG_PAUSE_H heures ; réessayer pendant
#     un blocage l'allonge.
# Chaque côté a son fichier : le calcul de Tirs-nhl (data/social/ig_garde.json, ses posts du matin et de la nuit)
# et le job live de puckprob (social/ig_garde.json, la file du soir et les stories).
# ---------------------------------------------------------------------------------
IG_MAX_JOUR, IG_ECART_MIN, IG_PAUSE_H = 8, 30, 72
# Après un blocage (13 nov. 2026 : bloqué le 11, puis encore le 12 à 14 h en réessayant après 24 h, puis le calcul de la
# nuit l'a réveillé à 0 h 55 parce qu'il ne savait pas que le job live était en pause) :
#   - la pause dure 72 h (réessayer trop tôt prolonge le blocage chez Meta) ;
#   - puis 72 h de RODAGE : au plus 3 posts et 2 stories Instagram par jour, pour remonter doucement ;
#   - les deux côtés (le calcul de Tirs-nhl et le job live de puckprob) respectent la pause de l'AUTRE : PAUSE_EXTERNE.
IG_RODAGE_H, IG_RODAGE_MAX, IG_RODAGE_STORIES = 72, 3, 2
PAUSE_EXTERNE = None       # la pause vue par l'autre côté (ISO), mise par main() (le fil) ou par social.py (le job live)
IG_COMMENTAIRE = False
# L'état est gardé sous la clé « _ig » du fichier : ici social_poste.json (le job live le pousse déjà ; un fichier à part
# serait perdu à chaque relance du job). Côté Tirs-nhl : data/social/ig_garde.json.
MAINTENANT = None          # l'heure simulée des tests (main(maintenant)) ; sinon l'heure réelle


def _json(f):
    try:
        return json.loads(Path(f).read_text(encoding="utf-8")) or {}
    except (OSError, ValueError):
        return {}


def _ig_lire(f):
    return _json(f).get("_ig") or {}


def ig_ok(f=None, max_jour=None, ecart_min=None, story=False):
    """-> (True, "") ou (False, la raison). Une story ne regarde que la pause (pas le quota ni l'écart).
    f : le fichier d'état (par défaut social_poste.json du job live)."""
    max_jour = IG_MAX_JOUR if max_jour is None else max_jour
    ecart_min = IG_ECART_MIN if ecart_min is None else ecart_min
    g, n = _ig_lire(f or POSTE), MAINTENANT or datetime.now(TZ)
    for p_ in (g.get("pause_jusqu"), PAUSE_EXTERNE):
        try:
            if p_ and n < datetime.fromisoformat(p_):
                return False, f"Instagram en pause jusqu'à {datetime.fromisoformat(p_).astimezone(TZ):%d/%m %H:%M} (blocage)"
        except (TypeError, ValueError):
            pass
    aujourd = g.get("jour") == n.date().isoformat()
    # (une pause d'avant le 13 nov. n'a pas de date de rodage : 72 h après la fin de sa pause)
    fin_r = g.get("rodage_jusqu") or ((datetime.fromisoformat(g["pause_jusqu"]) + timedelta(hours=IG_RODAGE_H)).isoformat() if g.get("pause_jusqu") else None)
    rodage = bool(fin_r) and n < datetime.fromisoformat(fin_r)
    if story:
        if rodage and aujourd and g.get("n_st", 0) >= IG_RODAGE_STORIES:
            return False, f"rodage après un blocage : déjà {IG_RODAGE_STORIES} stories Instagram aujourd'hui"
        return True, ""
    if rodage:
        max_jour = min(max_jour, IG_RODAGE_MAX)
    if aujourd and g.get("n", 0) >= max_jour:
        return False, f"déjà {max_jour} posts Instagram aujourd'hui"
    if g.get("dernier") and n - datetime.fromisoformat(g["dernier"]) < timedelta(minutes=ecart_min):
        return False, f"moins de {ecart_min} min depuis le dernier post Instagram"
    return True, ""


def ig_noter(resultat, f=None, story=False):
    """Après un essai sur Instagram : compte le post réussi, ou met Instagram en pause si Meta bloque."""
    f = f or POSTE
    g, n = _ig_lire(f), MAINTENANT or datetime.now(TZ)
    r = str(resultat or "")
    if r.startswith("erreur") and ("2207051" in r or "request limit" in r.lower() or "2207042" in r):
        fin_p = n + timedelta(hours=IG_PAUSE_H)
        g["pause_jusqu"] = fin_p.isoformat(timespec="minutes")
        g["rodage_jusqu"] = (fin_p + timedelta(hours=IG_RODAGE_H)).isoformat(timespec="minutes")
        print(f"  Instagram bloque nos posts : pause de {IG_PAUSE_H} h, puis {IG_RODAGE_H} h de rodage")
    elif r and not r.startswith("erreur"):
        if g.get("jour") != n.date().isoformat():
            g["jour"], g["n"], g["n_st"] = n.date().isoformat(), 0, 0
        if story:
            g["n_st"] = g.get("n_st", 0) + 1
        else:
            g["n"] = g.get("n", 0) + 1
            g["dernier"] = n.isoformat(timespec="minutes")
    try:
        tout = _json(f)
        tout["_ig"] = g
        Path(f).parent.mkdir(parents=True, exist_ok=True)
        Path(f).write_text(json.dumps(tout, ensure_ascii=False, indent=1), encoding="utf-8")
    except OSError:
        pass


def _commenter(objet, message, nom):
    if not message:
        return None
    try:
        cid = _graph(f"{objet}/comments", {"message": message}).get("id")
        print(f"  {nom} : commentaire OK")
        return cid
    except Exception as ex:  # noqa: BLE001
        print(f"  {nom} : commentaire raté ({str(ex)[:160]})")
        return None


def _attendre_ig(cid):
    for _ in range(15):
        st = _graph(str(cid), {"fields": "status_code"}, methode="GET").get("status_code")
        if st in ("FINISHED", None):
            return
        if st == "ERROR":
            raise RuntimeError("Instagram n'a pas pu lire une image")
        time.sleep(3)


def _rupload(url, donnees):
    """Envoie une vidéo d'un coup à l'adresse de téléversement de Meta (rupload.facebook.com)."""
    req = urllib.request.Request(url, data=donnees, method="POST", headers={
        "Authorization": f"OAuth {os.environ['META_PAGE_TOKEN']}", "offset": "0", "file_size": str(len(donnees)),
        "Content-Type": "application/octet-stream"})
    try:
        with urllib.request.urlopen(req, timeout=300) as rep:
            r = json.loads(rep.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as ex:
        raise RuntimeError(f"Meta {ex.code} (téléversement) : {ex.read().decode('utf-8', 'replace')[:300]}") from None
    if r.get("success") is False:
        raise RuntimeError(f"téléversement refusé : {str(r)[:200]}")
    return r


def publier_story_video(chemin, f_ig=None, instagram=True):
    """Une story vidéo (src/story_match.py : les matchs 10 min avant, avec musique), Facebook et Instagram.
    Facebook : video_stories (start -> téléversement -> finish). Instagram : conteneur STORIES « resumable », la vidéo
    envoyée directement (pas besoin d'adresse publique), on attend que Meta l'ait traitée, puis media_publish.
    Chacune peut rater sans bloquer l'autre. -> {"fb": ..., "ig": ...}"""
    page, ig = os.environ.get("META_PAGE_ID", "").strip(), os.environ.get("META_IG_ID", "").strip()
    if not instagram:                      # le Run workflow « story test » : Facebook seulement (on laisse Instagram tranquille)
        ig = ""
    donnees = Path(chemin).read_bytes()
    out = {}
    try:
        d = _graph(f"{page}/video_stories", {"upload_phase": "start"})
        _rupload(d["upload_url"], donnees)
        r = _graph(f"{page}/video_stories", {"upload_phase": "finish", "video_id": d["video_id"]})
        out["fb"] = r.get("post_id") or "ok"
        print(f"  story Facebook OK ({out['fb']})")
    except Exception as ex:  # noqa: BLE001
        out["fb"] = f"erreur : {str(ex)[:200]}"
        print(f"  story Facebook {out['fb']}")
    ok, raison = ig_ok(f_ig, story=True) if ig else (False, "")
    if ig and not ok:
        out["ig"] = f"sauté : {raison}"
        print(f"  story Instagram {out['ig']}")
    if ig and ok:
        try:
            c = _graph(f"{ig}/media", {"media_type": "STORIES", "upload_type": "resumable"})
            _rupload(c.get("uri") or f"https://rupload.facebook.com/ig-api-upload/{API}/{c['id']}", donnees)
            # Une vidéo prend plus de temps qu'une photo à être traitée : jusqu'à 3 min
            for _ in range(60):
                st = _graph(str(c["id"]), {"fields": "status_code"}, methode="GET").get("status_code")
                if st == "FINISHED":
                    break
                if st == "ERROR":
                    raise RuntimeError("Instagram n'a pas pu lire la vidéo")
                time.sleep(3)
            out["ig"] = _graph(f"{ig}/media_publish", {"creation_id": c["id"]}).get("id")
            print(f"  story Instagram OK ({out['ig']})")
        except Exception as ex:  # noqa: BLE001
            out["ig"] = f"erreur : {str(ex)[:200]}"
            print(f"  story Instagram {out['ig']}")
        ig_noter(out.get("ig"), f_ig, story=True)
    if all(str(v).startswith("erreur") for v in out.values()):
        raise RuntimeError(f"story ratée partout : {out}")
    return out


def story(it):
    """Un item « story » du fil : la vidéo est faite ici, au moment de publier, à partir du cadre poussé par le calcul
    (live_code/story_match.py : le cadre + la musique rock -> .mp4, quelques secondes), puis publiée."""
    import tempfile
    import story_match
    with tempfile.TemporaryDirectory() as tmp:
        # La toune : choisie par le id de la story (chaque match a la sienne, en rotation entre les tounes déposées)
        # Les stories des posts du matin (it["jingle"]) : un des 3 jingles PuckProb, pas la musique des matchs
        if it.get("jingle"):
            mp4 = story_match.video_jingle((RACINE / it["cadre"]).read_bytes(), Path(tmp) / "story.mp4", it["id"])
        else:
            mp4 = story_match.video((RACINE / it["cadre"]).read_bytes(), Path(tmp) / "story.mp4", it["id"])
        return publier_story_video(mp4)


def publier_plusieurs(it):
    """2 photos et plus (l'image habituelle + le popup d'un joueur) : un post Facebook qui attache des photos pas
    publiées, et un carrousel Instagram. Même recette que social.publier_plusieurs()."""
    page, ig = os.environ.get("META_PAGE_ID", "").strip(), os.environ.get("META_IG_ID", "").strip()
    ids = [_graph(f"{page}/photos", {"published": "false"}, fichier=(RACINE / f).read_bytes()).get("id") for f in it["images"]]
    champs = {"message": it["texte"]}
    for i, pid in enumerate(ids):
        champs[f"attached_media[{i}]"] = json.dumps({"media_fbid": pid})
    out = {"fb": _graph(f"{page}/feed", champs).get("id")}
    print(f"  Facebook OK, {len(ids)} photos ({out['fb']})")
    out["fb_com"] = _commenter(out["fb"], it.get("com"), "Facebook")
    if not ig:
        return out
    ok, raison = ig_ok()
    if not ok:
        out["ig"] = f"sauté : {raison}"
        print(f"  Instagram {out['ig']}")
        return out
    try:
        pieces = []
        for pid in ids:
            imgs = _graph(str(pid), {"fields": "images"}, methode="GET").get("images") or []
            src = max(imgs, key=lambda x: x.get("width", 0)).get("source") if imgs else None
            if not src:
                raise RuntimeError("pas d'adresse d'image sur une photo Facebook")
            c = _graph(f"{ig}/media", {"image_url": src, "is_carousel_item": "true"})
            _attendre_ig(c["id"])
            pieces.append(c["id"])
        c = _graph(f"{ig}/media", {"media_type": "CAROUSEL", "children": ",".join(pieces), "caption": it.get("texte_ig") or it["texte"]})
        _attendre_ig(c["id"])
        out["ig"] = _graph(f"{ig}/media_publish", {"creation_id": c["id"]}).get("id")
        print(f"  Instagram OK, carrousel de {len(pieces)} ({out['ig']})")
        if IG_COMMENTAIRE:
            out["ig_com"] = _commenter(out["ig"], it.get("com_ig") or it.get("com"), "Instagram")
    except Exception as ex:  # noqa: BLE001
        out["ig"] = f"erreur : {str(ex)[:200]}"
        print(f"  Instagram {out['ig']}")
    ig_noter(out.get("ig"))
    return out


def publier_diapo(it):
    """Le post du mod en vidéo (Mitch, 14 nov. 2026) : les 3 cartes poussées par le calcul (it["diapo"]) deviennent ici
    une vidéo (live_code/story_match.video_diapo : 2 flips de pierre avec leur son, la toune du mod), publiée en vidéo
    Facebook puis en Reel Instagram. -> {"fb": ..., "ig": ...}, ou None si la vidéo n'a pas pu être faite ou envoyée
    à Facebook (publier() sort alors la photo, comme avant). Facebook sans réponse (délai) : on ne republie pas en
    photo (la vidéo a peut-être passé : pas de doublon)."""
    import tempfile
    import story_match
    page, ig = os.environ.get("META_PAGE_ID", "").strip(), os.environ.get("META_IG_ID", "").strip()
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        try:
            mp4 = story_match.video_diapo([(RACINE / f).read_bytes() for f in it["diapo"]], Path(tmp) / "post.mp4", it["id"])
            donnees = Path(mp4).read_bytes()
        except Exception as ex:  # noqa: BLE001
            print(f"  vidéo du mod pas faite ({str(ex)[:160]}) : la photo à la place")
            return None
        try:
            r = _graph(f"{page}/videos", {"description": it["texte"]}, fichier=donnees, mime="video/mp4", nom_fichier="puckprob.mp4", hote="graph-video")
        except Exception as ex:  # noqa: BLE001
            if "timed out" in str(ex).lower():
                print(f"  vidéo envoyée mais pas de réponse de Meta ({str(ex)[:100]}) : on ne republie pas en photo")
                return {"fb": "incertain (pas de réponse de Meta)", "video": True}
            print(f"  vidéo Facebook ratée ({str(ex)[:160]}) : la photo à la place")
            return None
        out["fb"], out["video"] = r.get("post_id") or r.get("id"), True
        print(f"  Facebook OK, vidéo du mod ({out['fb']})")
        out["fb_com"] = _commenter(out["fb"], it.get("com"), "Facebook")
        if not ig:
            return out
        ok, raison = ig_ok()
        if not ok:
            out["ig"] = f"sauté : {raison}"
            print(f"  Instagram {out['ig']}")
            return out
        try:
            c = _graph(f"{ig}/media", {"media_type": "REELS", "upload_type": "resumable", "caption": it.get("texte_ig") or it["texte"], "share_to_feed": "true"})
            _rupload(c.get("uri") or f"https://rupload.facebook.com/ig-api-upload/{API}/{c['id']}", donnees)
            for _ in range(60):                       # une vidéo : jusqu'à 3 min de traitement chez Meta
                st = _graph(str(c["id"]), {"fields": "status_code"}, methode="GET").get("status_code")
                if st in ("FINISHED", None):
                    break
                if st == "ERROR":
                    raise RuntimeError("Instagram n'a pas pu lire la vidéo")
                time.sleep(3)
            out["ig"] = _graph(f"{ig}/media_publish", {"creation_id": c["id"]}).get("id")
            print(f"  Instagram OK, Reel du mod ({out['ig']})")
            if IG_COMMENTAIRE:
                out["ig_com"] = _commenter(out["ig"], it.get("com_ig") or it.get("com"), "Instagram")
        except Exception as ex:  # noqa: BLE001
            out["ig"] = f"erreur : {str(ex)[:200]}"
            print(f"  Instagram {out['ig']}")
        ig_noter(out.get("ig"))
    return out


def publier(it):
    """Facebook (fichier), puis Instagram (adresse de la photo Facebook). Même recette que social.publier()."""
    if it.get("diapo"):
        out = publier_diapo(it)
        if out:
            return out
    if it.get("images") and len(it["images"]) > 1:
        return publier_plusieurs(it)
    page, ig = os.environ.get("META_PAGE_ID", "").strip(), os.environ.get("META_IG_ID", "").strip()
    jpeg = (RACINE / it["image"]).read_bytes()
    out = {}
    r = _graph(f"{page}/photos", {"caption": it["texte"]}, fichier=jpeg)
    out["fb"] = r.get("post_id") or r.get("id")
    print(f"  Facebook OK ({out['fb']})")
    out["fb_com"] = _commenter(out["fb"], it.get("com"), "Facebook")
    if not ig:
        return out
    ok, raison = ig_ok()
    if not ok:
        out["ig"] = f"sauté : {raison}"
        print(f"  Instagram {out['ig']}")
        return out
    try:
        imgs = _graph(str(r.get("id")), {"fields": "images"}, methode="GET").get("images") or []
        src = max(imgs, key=lambda x: x.get("width", 0)).get("source") if imgs else None
        if not src:
            raise RuntimeError("pas d'adresse d'image sur la photo Facebook")
        c = _graph(f"{ig}/media", {"image_url": src, "caption": it.get("texte_ig") or it["texte"]})
        for _ in range(10):
            st = _graph(str(c["id"]), {"fields": "status_code"}, methode="GET").get("status_code")
            if st in ("FINISHED", None):
                break
            if st == "ERROR":
                raise RuntimeError("Instagram n'a pas pu lire l'image")
            time.sleep(3)
        out["ig"] = _graph(f"{ig}/media_publish", {"creation_id": c["id"]}).get("id")
        print(f"  Instagram OK ({out['ig']})")
        if IG_COMMENTAIRE:
            out["ig_com"] = _commenter(out["ig"], it.get("com_ig") or it.get("com"), "Instagram")
    except Exception as ex:  # noqa: BLE001
        out["ig"] = f"erreur : {str(ex)[:200]}"
        print(f"  Instagram {out['ig']}")
    ig_noter(out.get("ig"))
    return out


def _ecrire_poste(poste):
    """Les GARDER derniers posts + l'état de la garde d'Instagram (« _ig », écrit sur le disque par ig_noter pendant
    le passage : on le relit pour ne pas l'écraser avec la copie en mémoire)."""
    ig = _ig_lire(POSTE) or poste.get("_ig")
    garde = dict([kv for kv in poste.items() if kv[0] != "_ig"][-GARDER:])
    if ig:
        garde["_ig"] = ig
    POSTE.write_text(json.dumps(garde, ensure_ascii=False, indent=1), encoding="utf-8")


def main(maintenant=None):
    if not os.environ.get("META_PAGE_TOKEN") or not os.environ.get("META_PAGE_ID"):
        print("fil : pas de secrets Meta, rien à faire")
        return 0
    global MAINTENANT
    MAINTENANT = maintenant
    now = maintenant or datetime.now(TZ)
    jour = now.date().isoformat()
    F = _lire(RACINE / "social" / "fil" / f"{jour}.json", None)
    if not F or not F.get("items"):
        print("fil : rien de prévu aujourd'hui")
        return 0
    if not F.get("publier"):
        print("fil : file en aperçu seulement (config social_actif), rien de publié")
        return 0
    global PAUSE_EXTERNE
    PAUSE_EXTERNE = F.get("ig_pause_jusqu")          # la pause Instagram du calcul (s'il s'est fait bloquer de son bord)
    poste = _lire(POSTE, {})
    dus = [it for it in F["items"] if it["id"] not in poste and datetime.fromisoformat(it["quand"]) <= now]
    n = 0
    # Les stories des matchs passent toutes (plusieurs matchs à 19 h = plusieurs stories à 18 h 50) : elles ne comptent
    # pas dans MAX_PAR_PASSAGE, sinon les dernières seraient sautées à la mise au jeu
    for it in sorted(dus, key=lambda x: (not x.get("story"), x["quand"])):
        if n >= MAX_PAR_PASSAGE and not it.get("story"):
            break
        if it.get("avant") and now >= datetime.fromisoformat(it["avant"]) - timedelta(minutes=2):
            poste[it["id"]] = {"saute": "match commencé", "quand": now.isoformat(timespec="minutes")}
            print(f"fil : {it['id']} sauté (match commencé)")
            continue
        try:
            out = story(it) if it.get("story") else publier(it)
        except Exception as ex:  # noqa: BLE001
            if it.get("story"):                # une story ratée : notée, pas réessayée (elle ne bloque pas les posts)
                poste[it["id"]] = {"erreur": str(ex)[:200], "type": "story", "quand": now.isoformat(timespec="minutes")}
                print(f"fil : {it['id']} raté ({str(ex)[:200]})")
                continue
            print(f"fil : {it['id']} raté ({str(ex)[:200]}) : on réessaie au prochain passage")
            break
        if it.get("story"):                    # une story : pas sur la page des liens (pas de « lien »)
            poste[it["id"]] = {**out, "type": "story", "titre": it.get("titre"), "publie": True,
                               "quand": datetime.now(TZ).isoformat(timespec="minutes")}
        else:
            poste[it["id"]] = {**out, "type": it.get("type"), "opt": it.get("opt"), "lien": it.get("lien"),
                               "lien_en": it.get("lien_en"), "titre": it.get("titre"), "publie": True,
                               "quand": datetime.now(TZ).isoformat(timespec="minutes")}
        n += 0 if it.get("story") else 1
        _ecrire_poste(poste)
        if n < MAX_PAR_PASSAGE:
            time.sleep(5)
    _ecrire_poste(poste)
    reste = [it for it in F["items"] if it["id"] not in poste]
    print(f"fil : {n} publié(s), {len(reste)} à venir" + (f" (prochain à {reste[0]['quand'][11:16]})" if reste else ""))
    return n


if __name__ == "__main__":
    main()

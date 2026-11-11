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


def _graph(chemin, champs=None, fichier=None, methode="POST"):
    url = f"https://graph.facebook.com/{API}/{chemin.lstrip('/')}"
    champs = dict(champs or {})
    champs["access_token"] = os.environ["META_PAGE_TOKEN"]
    if methode == "GET":
        req = urllib.request.Request(url + "?" + urllib.parse.urlencode(champs))
    elif fichier:
        sep = uuid.uuid4().hex
        corps = b""
        for k, val in champs.items():
            corps += f'--{sep}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{val}\r\n'.encode()
        corps += (f'--{sep}\r\nContent-Disposition: form-data; name="source"; filename="puckprob.jpg"\r\n'
                  f"Content-Type: image/jpeg\r\n\r\n").encode() + fichier + f"\r\n--{sep}--\r\n".encode()
        req = urllib.request.Request(url, data=corps, headers={"Content-Type": f"multipart/form-data; boundary={sep}"})
    else:
        req = urllib.request.Request(url, data=urllib.parse.urlencode(champs).encode())
    try:
        with urllib.request.urlopen(req, timeout=90) as rep:
            return json.loads(rep.read().decode("utf-8"))
    except urllib.error.HTTPError as ex:
        raise RuntimeError(f"Meta {ex.code} : {ex.read().decode('utf-8', 'replace')[:300]}") from None


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


def publier_story_video(chemin):
    """Une story vidéo (src/story_match.py : les matchs 10 min avant, avec musique), Facebook et Instagram.
    Facebook : video_stories (start -> téléversement -> finish). Instagram : conteneur STORIES « resumable », la vidéo
    envoyée directement (pas besoin d'adresse publique), on attend que Meta l'ait traitée, puis media_publish.
    Chacune peut rater sans bloquer l'autre. -> {"fb": ..., "ig": ...}"""
    page, ig = os.environ.get("META_PAGE_ID", "").strip(), os.environ.get("META_IG_ID", "").strip()
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
    if ig:
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
    if all(str(v).startswith("erreur") for v in out.values()):
        raise RuntimeError(f"story ratée partout : {out}")
    return out


def story(it):
    """Un item « story » du fil : la vidéo est faite ici, au moment de publier, à partir du cadre poussé par le calcul
    (live_code/story_match.py : le cadre + la musique rock -> .mp4, quelques secondes), puis publiée."""
    import tempfile
    import story_match
    with tempfile.TemporaryDirectory() as tmp:
        mp4 = story_match.video((RACINE / it["cadre"]).read_bytes(), Path(tmp) / "story.mp4", it["id"][:10])
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
        out["ig_com"] = _commenter(out["ig"], it.get("com_ig") or it.get("com"), "Instagram")
    except Exception as ex:  # noqa: BLE001
        out["ig"] = f"erreur : {str(ex)[:200]}"
        print(f"  Instagram {out['ig']}")
    return out


def publier(it):
    """Facebook (fichier), puis Instagram (adresse de la photo Facebook). Même recette que social.publier()."""
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
        out["ig_com"] = _commenter(out["ig"], it.get("com_ig") or it.get("com"), "Instagram")
    except Exception as ex:  # noqa: BLE001
        out["ig"] = f"erreur : {str(ex)[:200]}"
        print(f"  Instagram {out['ig']}")
    return out


def main(maintenant=None):
    if not os.environ.get("META_PAGE_TOKEN") or not os.environ.get("META_PAGE_ID"):
        print("fil : pas de secrets Meta, rien à faire")
        return 0
    now = maintenant or datetime.now(TZ)
    jour = now.date().isoformat()
    F = _lire(RACINE / "social" / "fil" / f"{jour}.json", None)
    if not F or not F.get("items"):
        print("fil : rien de prévu aujourd'hui")
        return 0
    if not F.get("publier"):
        print("fil : file en aperçu seulement (config social_actif), rien de publié")
        return 0
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
        POSTE.write_text(json.dumps(dict(list(poste.items())[-GARDER:]), ensure_ascii=False, indent=1), encoding="utf-8")
        if n < MAX_PAR_PASSAGE:
            time.sleep(5)
    POSTE.write_text(json.dumps(dict(list(poste.items())[-GARDER:]), ensure_ascii=False, indent=1), encoding="utf-8")
    reste = [it for it in F["items"] if it["id"] not in poste]
    print(f"fil : {n} publié(s), {len(reste)} à venir" + (f" (prochain à {reste[0]['quand'][11:16]})" if reste else ""))
    return n


if __name__ == "__main__":
    main()

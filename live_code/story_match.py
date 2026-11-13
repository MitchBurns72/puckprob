"""Les stories des matchs (demande de Mitch, 11 nov. 2026) : chaque match du soir en story Facebook et Instagram,
10 minutes avant la mise au jeu, en petite vidéo avec de la musique rock libre de droit.

  - l'image : celle du post du match (les % du match), posée dans un cadre 1080 x 1920 (format story) aux couleurs du
    site : le logo, « DANS 10 MIN / IN 10 MIN », l'heure de la mise au jeu, puckprob.ca en bas ;
  - la musique : un riff rock composé ici même, note par note (batterie, basse, deux guitares saturées). Rien de
    copié de personne : libre de droit par définition. Pour une vraie toune à la place, déposer un .mp3 ou un .wav
    libre de droit (ex. la bibliothèque audio de YouTube ou Pixabay Music) dans assets/musique/ de Tirs-nhl : il est pris
    à la place (un différent chaque jour s'il y en a plusieurs) ;
  - la vidéo : 15 s, le cadre fixe puis le flip vers la fin PuckProb, H.264 + AAC 48 kHz stéréo (les specs des stories de Meta).
    ffmpeg vient du paquet imageio-ffmpeg (installé au besoin, rien à ajouter au workflow).

La file du soir (social.preparer_fil) ajoute un item « story » par match avec son cadre (une image : léger à pousser) ;
live_code/poster.py (job live de puckprob) fait la vidéo au moment de publier (video(), quelques secondes) et la publie
avec publier_story_video(). Les vidéos ne sont jamais poussées dans un dépôt (trop lourdes pour l'historique git). Run workflow, case « story_test » : les stories
déjà sorties aujourd'hui (matin + matchs), refaites au style actuel et republiées, Facebook seulement (social.stories_du_jour).
"""
import base64
import hashlib
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
# Les tounes déposées (Tirs-nhl : assets/musique/ ; dans puckprob, le calcul les copie dans live_code/musique/)
DIRS_MUSIQUE = [RACINE / "assets" / "musique", Path(__file__).resolve().parent / "musique"]
# Les jingles des stories AUTRES que les matchs (Mitch, 11 nov. 2026 : les 3 « Peaceful Broadcast ») : dossier à part,
# pour qu'ils ne se mélangent jamais aux tounes rock des matchs
DIRS_JINGLES = [RACINE / "assets" / "jingles", Path(__file__).resolve().parent / "jingles"]


def _np():
    """numpy (le job live de puckprob n'a que Python : installé au besoin, comme ffmpeg)."""
    try:
        import numpy
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "numpy"], check=True)
        import numpy
    return numpy
DUREE = 15.0              # secondes (les stories : 3 à 60 s)
SR = 48000                # Meta : AAC 48 kHz stéréo, 128 kb/s et plus
AVANT = 10                # minutes avant la mise au jeu


# =================================================================================
# ffmpeg (le binaire du paquet imageio-ffmpeg : pas besoin de l'installer dans le workflow)
# =================================================================================
def _ffmpeg():
    try:
        import imageio_ffmpeg
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "imageio-ffmpeg"], check=True)
        import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


# =================================================================================
# La musique : un riff punk-rock à 150 BPM, composé ici (aucune toune de personne)
# =================================================================================
def _passe_bas(x, fc):
    """Filtre passe-bas doux (par FFT : rapide, sans scipy). Enlève le « frisé » de la saturation."""
    np = _np()
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    return np.fft.irfft(X / np.sqrt(1 + (f / fc) ** 4), n)


def _passe_haut(x, fc):
    np = _np()
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    return np.fft.irfft(X * (1 - 1 / np.sqrt(1 + (f / fc) ** 4)), n)


def _scie(f, t, phase=0.0):
    return 2 * ((f * t + phase) % 1.0) - 1


def synth_rock(duree=DUREE, graine=0):
    """-> tableau (n, 2) float32 entre -1 et 1. Progression E5 - C5 - G5 - D5 (deux mesures chacune), guitares en
    croches (étouffées au début de la mesure, ouvertes à la fin), basse sur la fondamentale, batterie rock classique.
    graine : change un peu le riff d'un jour à l'autre (ordre des accords), jamais le style."""
    np = _np()
    rng = np.random.default_rng(graine)
    bpm = 150
    noire = 60 / bpm
    croche = noire / 2
    n = int(duree * SR)
    t_all = np.arange(n) / SR
    g_l, g_r, basse, batt = (np.zeros(n) for _ in range(4))
    progs = [[82.41, 65.41, 98.00, 73.42], [82.41, 73.42, 65.41, 98.00], [110.0, 87.31, 65.41, 98.00]]
    prog = progs[graine % len(progs)]
    mesure = 4 * noire
    n_mes = int(np.ceil(duree / mesure))

    def poser(buf, debut, son):
        i = int(debut * SR)
        if i >= n:
            return
        k = min(len(son), n - i)
        buf[i:i + k] += son[:k]

    # Guitares : un accord de puissance (fondamentale, quinte, octave), saturé ; 2 guitares un peu désaccordées (L / R)
    for m in range(n_mes):
        f0 = prog[(m // 2) % len(prog)]
        for c in range(8):
            debut = m * mesure + c * croche
            ouvert = c >= 6 or (m % 2 == 1 and c >= 4)              # la fin de la mesure sonne, le début est étouffé
            long_ = croche * (2.0 if ouvert else 0.9)
            t = np.arange(int(long_ * SR)) / SR
            env = np.exp(-t * (2.5 if ouvert else 18)) * np.minimum(1, t * 400)
            for buf, det in ((g_l, 1.0), (g_r, 1.004)):
                s = sum(a * _scie(f0 * r * det, t, ph) for a, r, ph in ((1, 1, 0), (.8, 1.5, .3), (.5, 2, .6)))
                buf_note = np.tanh(s * 6) * env * (0.9 if ouvert else 0.75)
                poser(buf, debut, buf_note)
            # Basse : la fondamentale une octave plus bas, en croches
            tb = np.arange(int(croche * 0.95 * SR)) / SR
            poser(basse, debut, (np.sin(2 * np.pi * f0 / 2 * tb) + 0.3 * _scie(f0 / 2, tb)) * np.exp(-tb * 4) * np.minimum(1, tb * 300))

    # Batterie
    def grosse():
        t = np.arange(int(0.35 * SR)) / SR
        f = 45 + 110 * np.exp(-t * 30)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)

    def caisse():
        t = np.arange(int(0.25 * SR)) / SR
        bruit = rng.uniform(-1, 1, len(t))
        return (0.8 * bruit * np.exp(-t * 16) + 0.5 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 28))

    def charley():
        t = np.arange(int(0.06 * SR)) / SR
        b = np.diff(rng.uniform(-1, 1, len(t) + 1))
        return b * np.exp(-t * 70) * 0.35

    def crash():
        t = np.arange(int(1.6 * SR)) / SR
        b = np.diff(rng.uniform(-1, 1, len(t) + 1))
        return b * np.exp(-t * 2.2) * 0.35

    G, C, H, X = grosse(), caisse(), charley(), crash()
    for m in range(n_mes):
        d = m * mesure
        if m % 4 == 0:
            poser(batt, d, X)
        for b in (0, 2):
            poser(batt, d + b * noire, G)
        poser(batt, d + 2.5 * noire, G * 0.8)
        for b in (1, 3):
            poser(batt, d + b * noire, C)
        for c in range(8):
            poser(batt, d + c * croche, H * (1.0 if c % 2 == 0 else 0.6))
        if m % 4 == 3:                                              # petit roulement de caisse à la fin des phrases
            for k in range(4):
                poser(batt, d + 3 * noire + k * noire / 4, C * (0.5 + k * 0.15))

    g_l, g_r = _passe_bas(g_l, 5200), _passe_bas(g_r, 5200)
    basse = _passe_bas(basse, 900)
    batt = _passe_haut(batt, 35)
    gauche = 0.55 * g_l + 0.18 * g_r + 0.55 * basse + 0.75 * batt
    droite = 0.18 * g_l + 0.55 * g_r + 0.55 * basse + 0.75 * batt
    st = np.stack([gauche, droite], axis=1)
    st /= (np.max(np.abs(st)) or 1) / 0.89                          # -1 dB
    fondu = np.ones(n)
    k = int(1.5 * SR)
    fondu[-k:] = np.linspace(1, 0, k)
    fondu[:int(0.02 * SR)] = np.linspace(0, 1, int(0.02 * SR))
    return (st * fondu[:, None]).astype(np.float32)


def _wav(st):
    """float32 (n, 2) -> octets d'un .wav 16 bits."""
    import io
    import wave
    np = _np()
    b = io.BytesIO()
    with wave.open(b, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(st, -1, 1) * 32767).astype("<i2").tobytes())
    return b.getvalue()


def musique(cle=None, dirs=None):
    """Chemin d'un fichier audio pour la story : une des tounes déposées dans assets/musique/, en rotation (cle = le id
    de la story : chaque match tire la sienne, toujours la même pour un même match), sinon notre riff."""
    cle = cle or datetime.now().date().isoformat()
    graine = int(hashlib.sha1(cle.encode()).hexdigest()[:6], 16)
    tounes = sorted(p for d in (dirs or DIRS_MUSIQUE) if d.is_dir() for p in d.glob("*") if p.suffix.lower() in (".mp3", ".wav", ".m4a", ".ogg"))
    if tounes:
        return tounes[graine % len(tounes)]
    f = Path(tempfile.gettempdir()) / f"pp-riff-{graine % 3}.wav"
    if not f.exists():
        f.write_bytes(_wav(synth_rock(DUREE, graine)))
    return f


# =================================================================================
# Le cadre 1080 x 1920 (dessiné par le navigateur de l'atelier : mêmes polices que le site)
# =================================================================================
def _heure(debut, en):
    if not debut:
        return ""
    if en:
        h = debut.hour % 12 or 12
        return f"{h}:{debut.minute:02d} {'PM' if debut.hour >= 12 else 'AM'} ET"
    return f"{debut.hour} h {debut.minute:02d}"


def _data(f, mime):
    """Un fichier du site en data: (une page faite avec set_content n'a pas le droit de charger les polices d'ailleurs)."""
    try:
        return f"data:{mime};base64," + base64.b64encode(Path(f).read_bytes()).decode()
    except OSError:
        return ""


def cadre_html(jpeg, debut, site):
    """site = le dossier du site (polices, logo)."""
    site = Path(site)
    img = "data:image/jpeg;base64," + base64.b64encode(jpeg).decode()
    bc = _data(site / "fonts" / "barlow-condensed-latin-800-italic.woff2", "font/woff2")
    bb = _data(site / "fonts" / "barlow-latin-600-normal.woff2", "font/woff2")
    logo = _data(site / "logo.png", "image/png") or _data(RACINE / "docs" / "logo.png", "image/png")
    hfr, hen = _heure(debut, False), _heure(debut, True)
    mise = f"Mise au jeu {hfr} · Puck drop {hen}" if debut else "Ce soir · Tonight"
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:BC;src:url({bc}) format("woff2");font-weight:800;font-style:italic}}
@font-face{{font-family:B;src:url({bb}) format("woff2");font-weight:600}}
html,body{{margin:0;width:1080px;height:1920px;overflow:hidden}}
body{{position:relative;background:linear-gradient(180deg,rgba(255,255,255,.10),rgba(0,0,0,0) 30%,rgba(0,0,0,.35)),
  radial-gradient(120% 80% at 15% 0%,#2B4A73 0%,#0A2342 50%,#061629 100%);font-family:B,Arial,sans-serif;color:#fff}}
.bandes{{position:absolute;left:30%;width:110%;height:150px;bottom:150px;transform:rotate(-24deg);transform-origin:left bottom;
  background:linear-gradient(180deg,rgba(255,255,255,.4),rgba(255,255,255,.06) 25%,rgba(0,0,0,0) 50%,rgba(0,0,0,.3)),
  linear-gradient(180deg,#FFB81C 0 27%,#0A2342 27% 34%,#fff 34% 66%,#0A2342 66% 73%,#FFB81C 73% 100%);box-shadow:0 -10px 30px rgba(0,0,0,.5)}}
.haut{{position:absolute;top:70px;left:0;right:0;text-align:center}}
.logo{{width:760px;filter:drop-shadow(0 6px 14px rgba(0,0,0,.5))}}
.dans{{margin-top:26px;font:italic 800 112px/1 BC,Arial;color:#FFB81C;text-transform:uppercase;letter-spacing:.01em;text-shadow:0 6px 0 rgba(0,0,0,.35)}}
.dans small{{display:block;font-size:56px;color:#fff;margin-top:6px}}
.mise{{margin-top:16px;font:600 34px B,Arial;color:#C9D6EE}}
.img{{position:absolute;left:50%;top:560px;transform:translateX(-50%);width:960px;border-radius:26px;box-shadow:0 22px 60px rgba(0,0,0,.6),0 0 0 4px rgba(255,255,255,.12)}}
.bas{{position:absolute;bottom:64px;left:0;right:0;text-align:center;font:italic 800 58px BC,Arial;text-transform:uppercase;text-shadow:0 4px 0 rgba(0,0,0,.4)}}
.bas b{{color:#FFB81C}}
</style></head><body><div class="bandes"></div>
<div class="haut"><img class="logo" src="{logo}"><div class="dans">Dans {AVANT} min<small>In {AVANT} min</small></div><div class="mise">{mise}</div></div>
<img class="img" src="{img}">
<div class="bas">Tous les % · All the % <b>puckprob.ca</b></div></body></html>"""


def cadre(atelier, jpeg, debut):
    """-> octets JPEG 1080 x 1920."""
    page = atelier.b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    try:
        page.set_content(cadre_html(jpeg, debut, atelier.dossier), wait_until="load")
        page.evaluate("() => document.fonts.ready")
        # L'image du match ne doit pas descendre sur « puckprob.ca » : on la réduit au besoin
        page.evaluate("""() => { const i = document.querySelector('.img'), b = document.querySelector('.bas');
          const max = b.getBoundingClientRect().top - 40 - i.getBoundingClientRect().top;
          if (i.getBoundingClientRect().height > max) i.style.width = Math.floor(960 * max / i.getBoundingClientRect().height) + 'px'; }""")
        return page.screenshot(type="jpeg", quality=92)
    finally:
        page.close()


# =================================================================================
# La vidéo
# =================================================================================
# La fin de chaque story (Mitch, 11 nov. 2026 : la « classique », en français et en anglais) : les FIN dernières
# secondes, le logo, le slogan et puckprob.ca, comme une pub. Une image fixe 1080 x 1920 : assets/story/fin.jpg dans
# Tirs-nhl ; le calcul la copie dans live_code/story_fin.jpg de puckprob.
# Le passage (Mitch, 11 nov. 2026) : une seconde plus tôt (FIN 4 -> 5 s), et la carte FLIPPE vers la fin au lieu
# d'un fondu. 3e version : « comme si tu vires une grosse pierre » : une dalle épaisse qui démarre lentement, prend
# son élan et retombe lourde (petite secousse), avec un grondement de pierre qui frotte et un gros boum à l'arrivée.
FIN, FLIP, SECOUSSE = 5.0, 0.8, 0.3
# Les fins en rotation (Mitch, 11 nov. 2026 : les 3 propositions, l'anglais en gros) : assets/story/fin-1.jpg, fin-2.jpg,
# fin-3.jpg dans Tirs-nhl ; live_code/story_fin-1.jpg... chez puckprob. L'ancienne fin.jpg seule sert juste de secours.
DIRS_FIN = [(RACINE / "assets" / "story", "fin-*.jpg"), (Path(__file__).resolve().parent, "story_fin-*.jpg")]
FICHIERS_FIN = [RACINE / "assets" / "story" / "fin.jpg", Path(__file__).resolve().parent / "story_fin.jpg"]


def _pil():
    """Pillow (le job live de puckprob n'a que Python : installé au besoin, comme numpy et ffmpeg)."""
    try:
        from PIL import Image
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pillow"], check=True)
        from PIL import Image
    return Image


def _images_flip(a, b, n, n_sec=0):
    """Les n images du flip, de la story (a) vers la fin (b), deux images PIL 1080 x 1920, puis n_sec images de
    secousse (la dalle qui retombe) -> liste d'images PIL.
    Une dalle de pierre qui tourne sur l'axe vertical : lente au départ, élan au milieu, lente à l'arrivée (cosinus) ;
    1re moitié la story (0 à 90°), 2e moitié la fin (90° à 0). Largeur apparente |cos| ; perspective forte (le bord
    qui s'en vient grossit, l'autre rapetisse) ; la tranche de la dalle (épaisseur, grain de pierre) se voit du côté
    proche ; la face s'assombrit de profil. Autour, le fond noir bleuté du site (#05080F). Calcul vectorisé."""
    np = _np()
    Image = _pil()
    A, B = np.asarray(a.convert("RGB")), np.asarray(b.convert("RGB"))
    H, W = A.shape[:2]
    u = (np.arange(W) + 0.5 - W / 2) / (W / 2)                 # -1 .. 1, par colonne
    Y = (np.arange(H) + 0.5 - H / 2)[:, None]                  # par rangée
    fond = np.array([5, 8, 15], dtype=np.float32)
    K, EP = 0.34, 0.11                                          # force de la perspective ; épaisseur de la dalle (en largeur)
    rng = np.random.default_rng(7)
    grain = (rng.standard_normal((H, 64)) * 9).astype(np.float32)   # le grain de la pierre sur la tranche
    out = []
    for k in range(n):
        t = (k + 0.5) / n
        q = 0.5 - 0.5 * np.cos(np.pi * t)                       # lent, élan, lent
        c, sn = abs(np.cos(np.pi * q)), np.sin(np.pi * q)
        cote, src = (1, A) if q < 0.5 else (-1, B)
        xs = u / max(c, 1e-3)
        v = 1 + K * sn * xs * cote                              # hauteur apparente de chaque colonne
        ys = Y / v[None, :]
        dedans = (np.abs(u)[None, :] <= c) & (np.abs(ys) <= H / 2)
        sx = np.clip(((xs + 1) * W / 2).astype(int), 0, W - 1)
        sy = np.clip((ys + H / 2).astype(int), 0, H - 1)
        img = src[sy, sx[None, :].repeat(H, 0)].astype(np.float32) * (0.45 + 0.55 * c)
        img = np.where(dedans[..., None], img, fond)
        # La tranche : du bord proche (cote) vers l'extérieur, largeur EP·sin ; même hauteur que ce bord
        lt = EP * sn
        if lt > 0.004:
            d = (u * cote - c) / lt                             # 0 au bord de la face, 1 au bout de la tranche
            hv = (1 + K * sn) * H / 2
            tr = (d >= 0) & (d <= 1)
            tr2 = tr[None, :] & (np.abs(Y) <= hv)
            gx = (np.clip(d, 0, 1) * 63).astype(int)
            ton = 62 - 30 * np.clip(d, 0, 1)                    # plus sombre vers le fond
            pierre = np.stack([ton * 0.92, ton * 0.95, ton * 1.05], -1)[None, :, :] + grain[:, gx][..., None]
            pierre = pierre * (0.75 + 0.25 * (1 - c))                  # plus clair quand on la voit bien de côté
            img = np.where(tr2[..., None], np.clip(pierre, 0, 255), img)
        out.append(Image.fromarray(img.astype(np.uint8)))
    # La dalle retombe : la fin sautille de quelques pixels, de moins en moins
    for k in range(n_sec):
        dy = int(round(16 * np.exp(-k / 2.2) * (1 if k % 2 == 0 else -1)))
        im = Image.new("RGB", (W, H), (5, 8, 15))
        im.paste(b.convert("RGB"), (0, dy))
        out.append(im)
    return out


# L'impact quand la pierre se met en place (Mitch, 11 nov. 2026 : plus d'impact à la fin, 3 choix en mp4) :
#   "creux" = le boum 2 fois plus fort avec une sous-basse ; "craque" = un coup sec de pierre juste avant le boum ;
#   "rebond" = le gros boum + 2 petits coups sourds sur les rebonds de la secousse ; "" = l'ancien boum.
IMPACT = "creux"


def son_mecanisme(impact=None):
    """Le son du flip, composé ici (aucun son de personne) : « une grosse pierre qu'on vire ». Un grondement grave de
    pierre qui frotte (bruit brun filtré, grains irréguliers) qui enfle pendant que la dalle tourne, puis un gros
    boum sourd à l'arrivée et quelques petits cailloux qui retombent. -> chemin d'un .wav (FLIP + 1 s)."""
    impact = IMPACT if impact is None else impact
    f = Path(tempfile.gettempdir()) / f"pp-pierre-v2-{impact or 'base'}.wav"
    if f.exists():
        return f
    np = _np()
    rng = np.random.default_rng(72)
    n = int((FLIP + 1.0) * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    # 1) Le frottement : bruit brun (grave), grains irréguliers 18-45 Hz, enfle puis lâche à l'arrivée
    brun = np.cumsum(rng.standard_normal(n))
    brun = _passe_haut(_passe_bas(brun - brun.mean(), 260), 35)
    grains = _passe_bas(np.abs(rng.standard_normal(n)), 30)
    grains = 0.35 + grains / (grains.max() or 1)
    env = np.clip(t / (FLIP * 0.6), 0, 1) ** 1.3 * np.clip((FLIP + 0.08 - t) / 0.12, 0, 1)
    x += 0.9 * brun / (np.abs(brun).max() or 1) * grains * env
    gravier = _passe_bas(_passe_haut(rng.standard_normal(n), 700), 2600) * grains ** 2
    x += 0.12 * gravier / (np.abs(gravier).max() or 1) * env
    # 2) Le boum : sinus qui descend de 75 à 38 Hz + bruit grave, long déclin
    i0 = int(FLIP * SR)
    tt = t[i0:] - FLIP
    fr = 38 + 37 * np.exp(-tt / 0.09)
    boum = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt / 0.28)
    choc = _passe_bas(rng.standard_normal(len(tt)), 180) * np.exp(-tt / 0.06)
    x[i0:] += 1.3 * boum + 0.9 * choc / (np.abs(choc).max() or 1)
    # 3) Des petits cailloux qui retombent après le boum
    for t0 in rng.uniform(0.06, 0.45, 7):
        j = int((FLIP + t0) * SR)
        m = min(n - j, int(0.03 * SR))
        cl = _passe_bas(rng.standard_normal(m), 1800) * np.exp(-np.arange(m) / (0.006 * SR))
        x[j:j + m] += rng.uniform(0.05, 0.14) * cl / (np.abs(cl).max() or 1)
    # La force de tout le son (grondement + boum de base) : fixée AVANT d'ajouter l'impact, pour que le frottement
    # reste exactement pareil et que seul l'impact monte ; un limiteur doux empêche la saturation
    g = 0.95 / (np.abs(_passe_haut(x, 28)).max() or 1)
    tt = t[i0:] - FLIP

    def thud(t0, gain, f0=58, f1=40, d=0.12):
        j = int((FLIP + t0) * SR)
        m = n - j
        tl = np.arange(m) / SR
        fr = f1 + (f0 - f1) * np.exp(-tl / 0.05)
        y = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tl / d)
        y += 0.6 * _passe_bas(rng.standard_normal(m), 220) / 3 * np.exp(-tl / 0.04)
        x[j:] += gain * y

    if impact == "creux":
        x[i0:] += 1.3 * boum + 0.9 * choc / (np.abs(choc).max() or 1)          # le boum en double
        x[i0:] += 1.4 * np.sin(2 * np.pi * 31 * tt) * np.exp(-tt / 0.45) * (1 - np.exp(-tt / 0.004))   # sous-basse
    elif impact == "craque":
        j = int((FLIP - 0.012) * SR)
        m = int(0.08 * SR)
        cr = _passe_haut(_passe_bas(rng.standard_normal(m), 5500), 1200) * np.exp(-np.arange(m) / (0.012 * SR))
        x[j:j + m] += 1.1 * cr / (np.abs(cr).max() or 1)
        x[i0:] += 0.5 * boum
    elif impact == "rebond":
        x[i0:] += 0.5 * boum
        thud(0.11, 0.85)
        thud(0.21, 0.5, 52, 38, 0.1)
    x = _passe_haut(x, 28) * g
    x = np.tanh(1.15 * x) / np.tanh(1.15)
    st = np.stack([x, np.concatenate([np.zeros(5), x[:-5]])], axis=1)      # un brin de largeur stéréo
    f.write_bytes(_wav(st))
    return f



def image_fin(cle=None):
    """L'image de fin de la story : une des fins en rotation (cle = le id de la story : toujours la même pour une même
    story, mais tirée à part de la musique, pour que les paires toune + fin changent), sinon l'ancienne fin seule."""
    for d, motif in DIRS_FIN:
        fins = sorted(d.glob(motif)) if d.is_dir() else []
        if fins:
            cle = cle or datetime.now().isoformat()
            return fins[int(hashlib.sha1((cle + "|fin").encode()).hexdigest()[:6], 16) % len(fins)]
    return next((f for f in FICHIERS_FIN if f.exists()), None)


def duree_audio(f):
    """La durée d'un fichier audio en secondes (lue dans la sortie de ffmpeg : pas besoin de ffprobe). None si illisible."""
    import re
    r = subprocess.run([_ffmpeg(), "-hide_banner", "-i", str(f)], capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr or "")
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]) if m else None


def video(jpeg_cadre, sortie, jour=None, son=None, duree=None, image=False, fondu_son=1.5, cle_fin=None):
    """Le cadre (fixe) puis, les FIN dernières secondes, la fin PuckProb, arrivée par un flip avec le son du
    mécanisme ; la musique dessous. -> .mp4 de `duree` secondes (DUREE par défaut). Sans image de fin : le cadre tout
    le long. image=True : une image qui n'est pas en 9:16 (un post carré, un classement...) est centrée sur sa propre
    copie agrandie, floutée et assombrie, pour remplir l'écran de la story sans rien couper."""
    import io
    Image = _pil()
    from PIL import ImageEnhance, ImageFilter
    sortie = Path(sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    fin = image_fin(cle_fin or jour)
    D = float(duree or DUREE)
    base = Image.open(io.BytesIO(jpeg_cadre)).convert("RGB")
    if base.size != (1080, 1920):           # déjà en 9:16 (la fiche story de src/cartes.py) : plein écran, pas de fond flouté
        r = max(1080 / base.width, 1920 / base.height)
        fond = base.resize((int(base.width * r) + 1, int(base.height * r) + 1), Image.BILINEAR)
        x, y = (fond.width - 1080) // 2, (fond.height - 1920) // 2
        fond = ImageEnhance.Brightness(fond.crop((x, y, x + 1080, y + 1920)).filter(ImageFilter.GaussianBlur(36))).enhance(0.62)
        r = min(1020 / base.width, 1860 / base.height)
        im = base.resize((int(base.width * r), int(base.height * r)), Image.LANCZOS)
        fond.paste(im, ((1080 - im.width) // 2, (1920 - im.height) // 2))
        base = fond
    with tempfile.TemporaryDirectory() as tmp:
        img = Path(tmp) / "cadre.jpg"
        base.save(img, quality=94)
        son = son or musique(jour)
        # Image fixe (Mitch, 11 nov. 2026 : le lent zoom de 4 % faisait « descendre » l'image en tremblotant, au pixel
        # près ; ce qui bouge, c'est seulement le flip et la secousse)
        zoom = "scale=1080:1920,format=yuv420p,setsar=1"
        ent = [_ffmpeg(), "-y", "-loglevel", "error"]
        fins = ["-r", "30", "-c:v", "libx264", "-preset", "veryfast", "-profile:v", "high", "-crf", "20",
                "-g", "60", "-keyint_min", "60", "-sc_threshold", "0", "-flags", "+cgop",
                "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-ac", "2",
                "-t", str(D), "-movflags", "+faststart", str(sortie)]
        af = f"afade=t=out:st={D - fondu_son}:d={fondu_son},apad"      # apad : une toune un brin plus courte que la vidéo finit en silence
        if fin:
            debut_fin = D - FIN
            nf, ns = round(FLIP * 30), round(SECOUSSE * 30)
            # Les images du flip : la story -> la fin, puis la secousse
            fin_img = Image.open(fin).convert("RGB").resize((1080, 1920))
            for k, fr in enumerate(_images_flip(base, fin_img, nf, ns)):
                fr.save(Path(tmp) / f"flip{k:03d}.jpg", quality=92)
            reste = D - debut_fin - (nf + ns) / 30
            ms = int(debut_fin * 1000)           # le clanche part avec le flip, sans baisser la musique
            cmd = ent + ["-loop", "1", "-framerate", "30", "-t", f"{debut_fin:.3f}", "-i", str(img),
                         "-framerate", "30", "-i", str(Path(tmp) / "flip%03d.jpg"),
                         "-loop", "1", "-framerate", "30", "-t", f"{reste:.3f}", "-i", str(fin),
                         "-i", str(son), "-i", str(son_mecanisme()),
                         "-filter_complex", f"[0:v]{zoom}[v0];[1:v]format=yuv420p,setsar=1[v1];[2:v]scale=1080:1920,format=yuv420p,setsar=1[v2];"
                                            f"[v0][v1][v2]concat=n=3:v=1:a=0[v];"
                                            f"[4:a]adelay={ms}|{ms},volume=2.2[m];[3:a][m]amix=inputs=2:duration=first:normalize=0,{af}[s]",
                         "-map", "[v]", "-map", "[s]"] + fins
        else:
            cmd = ent + ["-loop", "1", "-framerate", "30", "-i", str(img), "-i", str(son),
                         "-filter_complex", f"[0:v]{zoom}[v]",
                         "-map", "[v]", "-map", "1:a", "-af", af] + fins      # (un .mp3 peut avoir une pochette : on ne la prend pas)
        subprocess.run(cmd, check=True, timeout=300)
    return sortie


def video_jingle(jpeg, sortie, cle=None):
    """Les stories AUTRES que les matchs (post sur mesure, case « story ») : l'image du post sur son fond flouté, un des
    jingles en rotation (cle = le id du post : toujours le même jingle pour un même post), la fin PuckProb en fondu.
    La vidéo dure le temps du jingle (11 à 14 s), au plus DUREE. Sans jingle déposé : la musique des matchs."""
    son = musique(cle, DIRS_JINGLES)
    if not any(d.is_dir() and any(d.glob("*.mp3")) for d in DIRS_JINGLES):
        son = musique(cle)
    d = duree_audio(son) or DUREE
    d = max(FIN + 3, min(DUREE, int(d * 10) / 10))
    return video(jpeg, sortie, son=son, duree=d, image=True, fondu_son=0.4, cle_fin=cle)


def faire(atelier, jpeg_match, debut, sortie, jour=None):
    """Tout d'un coup : cadre + vidéo. -> (chemin du .mp4, octets du cadre JPEG)."""
    c = cadre(atelier, jpeg_match, debut)
    return video(c, sortie, jour), c

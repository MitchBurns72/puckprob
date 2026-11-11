"""Les stories des matchs (demande de Mitch, 11 nov. 2026) : chaque match du soir en story Facebook et Instagram,
10 minutes avant la mise au jeu, en petite vidéo avec de la musique rock libre de droit.

  - l'image : celle du post du match (les % du match), posée dans un cadre 1080 x 1920 (format story) aux couleurs du
    site : le logo, « DANS 10 MIN / IN 10 MIN », l'heure de la mise au jeu, puckprob.ca en bas ;
  - la musique : un riff rock composé ici même, note par note (batterie, basse, deux guitares saturées). Rien de
    copié de personne : libre de droit par définition. Pour une vraie toune à la place, déposer un .mp3 ou un .wav
    libre de droit (ex. la bibliothèque audio de YouTube ou Pixabay Music) dans assets/musique/ de Tirs-nhl : il est pris
    à la place (un différent chaque jour s'il y en a plusieurs) ;
  - la vidéo : 15 s, un zoom lent sur le cadre, H.264 + AAC 48 kHz stéréo (les specs des stories de Meta).
    ffmpeg vient du paquet imageio-ffmpeg (installé au besoin, rien à ajouter au workflow).

La file du soir (social.preparer_fil) ajoute un item « story » par match avec son cadre (une image : léger à pousser) ;
live_code/poster.py (job live de puckprob) fait la vidéo au moment de publier (video(), quelques secondes) et la publie
avec publier_story_video(). Les vidéos ne sont jamais poussées dans un dépôt (trop lourdes pour l'historique git). Run workflow, case « story_test » : la dernière game du soir,
publiée tout de suite (social.story_test).
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


def musique(cle=None):
    """Chemin d'un fichier audio pour la story : une des tounes déposées dans assets/musique/, en rotation (cle = le id
    de la story : chaque match tire la sienne, toujours la même pour un même match), sinon notre riff."""
    cle = cle or datetime.now().date().isoformat()
    graine = int(hashlib.sha1(cle.encode()).hexdigest()[:6], 16)
    tounes = sorted(p for d in DIRS_MUSIQUE if d.is_dir() for p in d.glob("*") if p.suffix.lower() in (".mp3", ".wav", ".m4a", ".ogg"))
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
# secondes passent en fondu au logo, au slogan et à puckprob.ca, comme une pub. Une image fixe 1080 x 1920 :
# assets/story/fin.jpg dans Tirs-nhl ; le calcul la copie dans live_code/story_fin.jpg de puckprob.
FIN, FONDU = 4.0, 0.6
FICHIERS_FIN = [RACINE / "assets" / "story" / "fin.jpg", Path(__file__).resolve().parent / "story_fin.jpg"]


def image_fin():
    return next((f for f in FICHIERS_FIN if f.exists()), None)


def video(jpeg_cadre, sortie, jour=None):
    """Le cadre (zoom lent) puis, les FIN dernières secondes, l'image de fin en fondu ; la musique dessous.
    -> .mp4 de DUREE secondes. Sans image de fin : le cadre tout le long."""
    sortie = Path(sortie)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    fin = image_fin()
    with tempfile.TemporaryDirectory() as tmp:
        img = Path(tmp) / "cadre.jpg"
        img.write_bytes(jpeg_cadre)
        son = musique(jour)
        # Zoom de 0 à 4 % sur la durée (recalculé à chaque image), recoupé au centre en 1080 x 1920
        zoom = (f"scale=w='trunc(1080*(1+0.04*t/{DUREE})/2)*2':h='trunc(1920*(1+0.04*t/{DUREE})/2)*2':eval=frame,"
                "crop=1080:1920,format=yuv420p,setsar=1")
        ent = [_ffmpeg(), "-y", "-loglevel", "error"]
        fins = ["-r", "30", "-c:v", "libx264", "-preset", "veryfast", "-profile:v", "high", "-crf", "20",
                "-g", "60", "-keyint_min", "60", "-sc_threshold", "0", "-flags", "+cgop",
                "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-ac", "2",
                "-af", f"afade=t=out:st={DUREE - 1.5}:d=1.5", "-t", str(DUREE), "-movflags", "+faststart", str(sortie)]
        if fin:
            debut_fin = DUREE - FIN
            cmd = ent + ["-loop", "1", "-framerate", "30", "-t", str(debut_fin + FONDU), "-i", str(img),
                         "-loop", "1", "-framerate", "30", "-t", str(FIN), "-i", str(fin), "-i", str(son),
                         "-filter_complex", f"[0:v]{zoom}[a];[1:v]scale=1080:1920,format=yuv420p,setsar=1[b];"
                                            f"[a][b]xfade=transition=fade:duration={FONDU}:offset={debut_fin},format=yuv420p[v]",
                         "-map", "[v]", "-map", "2:a"] + fins
        else:
            cmd = ent + ["-loop", "1", "-framerate", "30", "-i", str(img), "-i", str(son),
                         "-map", "0:v", "-map", "1:a",      # (un .mp3 peut avoir une pochette : on ne la prend pas)
                         "-vf", zoom] + fins
        subprocess.run(cmd, check=True, timeout=300)
    return sortie


def faire(atelier, jpeg_match, debut, sortie, jour=None):
    """Tout d'un coup : cadre + vidéo. -> (chemin du .mp4, octets du cadre JPEG)."""
    c = cadre(atelier, jpeg_match, debut)
    return video(c, sortie, jour), c

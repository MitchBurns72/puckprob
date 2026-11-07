/* « Mon club » (PuckProb) : le visiteur choisit son équipe une fois, on la garde dans SON navigateur (localStorage,
   aucune donnée envoyée nulle part) et on la met en premier :
   - un bouton dans l'en-tête de chaque page (son club ou « Mon club ») pour choisir ou changer ;
   - sur l'accueil : une petite bande « C'est quoi ton club? » tant qu'il n'a pas choisi (ou fermé), puis le bloc
     « Ton club ce soir » (match, chance de gagner, ses 3 marqueurs les plus probables, chance de Coupe) ;
   - partout : ses joueurs et son équipe légèrement surlignés, ses nouvelles en premier dans le bandeau.
   Données : club.json (bâti par site_public.py), à côté de ce fichier, lu seulement quand on en a besoin. */
(function(){
  "use strict";
  const FR = (document.documentElement.lang || "").toLowerCase().startsWith("fr");
  const L = (fr, en) => FR ? fr : en;
  const CLE = "pp_club";
  const RACINE = (() => { try { return new URL(".", document.currentScript.src).href; } catch (e) { return ""; } })();
  const lire = () => { try { return localStorage.getItem(CLE) || ""; } catch (e) { return ""; } };
  const ecrire = (v) => { try { localStorage.setItem(CLE, v); } catch (e) { /* navigation privée : tant pis */ } };
  const club = () => { const c = lire(); return c && c !== "-" ? c : ""; };
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const pc = (p) => { if (p == null) return "–"; const v = p * 100; const t = v < 10 ? v.toFixed(1) : String(Math.round(v));
    return (FR ? t.replace(".", ",") + " " : t) + "%"; };
  const EQ_ORDRE = ["ANA", "BOS", "BUF", "CGY", "CAR", "CHI", "COL", "CBJ", "DAL", "DET", "EDM", "FLA", "LAK", "MIN", "MTL", "NSH",
                    "NJD", "NYI", "NYR", "OTT", "PHI", "PIT", "SJS", "SEA", "STL", "TBL", "TOR", "UTA", "VAN", "VGK", "WSH", "WPG"];

  let DATA = null;
  const donnees = () => DATA ? Promise.resolve(DATA)
    : fetch(RACINE + "club.json", { cache: "no-cache" }).then(r => r.json()).then(d => (DATA = d)).catch(() => ({ eq: {} }));
  const nomEq = (t) => (DATA?.eq?.[t]?.n || [t, t])[FR ? 1 : 0];
  const coulEq = (t) => DATA?.eq?.[t]?.c || "#6B7C8C";

  // ---- Thème du site : il suit « Mon club » (idée de Mitch). Règle : les 3 couleurs du club, pas d'autres.
  //   D = sa couleur foncée (fond, en-tête, onglets ; les fonds de la page et des cartes = des ombres de D),
  //   A = sa couleur vive (boutons choisis, soulignés, liens, chiffres en évidence),
  //   B = sa 3e couleur (bandeau « Ce soir », pastilles du ticker, avertissements).
  // Le texte reste blanc / un pâle de D. Seuls le vert et le rouge des hausses/baisses restent (ils veulent dire quelque chose).
  // Sans club : le thème neutre PuckProb (marine, rouge, ambre), inchangé. Gardé sur l'appareil pour s'afficher tout de suite.
  const NEUTRE = { b1: "#0A2342", acc: "#D3202B", led: "#FFB81C", sa: "#FFB81C", sw: "#FFFFFF", neutre: 1 };
  const blanc = (x) => /^#fff(fff)?$/i.test(x || "");
  const themeDe = (t) => {
    const p = DATA?.eq?.[t]?.pal; if (!p) return NEUTRE;
    const acc = !blanc(p.texte) ? p.texte : !blanc(p.contour) ? p.contour : "#FFFFFF";
    const led = acc === p.texte ? p.contour : p.texte;            // l'autre des deux (peut être le blanc du club)
    return { b1: p.fond, acc, led, sa: acc, sw: led };
  };
  const lumHex = (h) => { const c = (h || "#000000").replace("#", "").match(/../g).map(x => parseInt(x, 16) / 255).map(x => x <= 0.03928 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; };
  const contr = (a, b) => { const x = lumHex(a), y = lumHex(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const ombre = (c, k) => "#" + c.replace("#", "").match(/../g).map(x => Math.round(parseInt(x, 16) * k).toString(16).padStart(2, "0")).join("");
  // Le texte qui va sur une couleur du club : blanc ou sa couleur foncée, celui qui ressort le plus
  const encre = (c, d) => contr(c, "#FFFFFF") >= contr(c, d) ? "#FFFFFF" : d;
  const vars = (t) => {
    if (t.neutre || t.b1 === NEUTRE.b1) return "--bg:#0B1220;--surface:#121B2D;--surface2:#17223A;--card:#121B2D;--chip:#1A2740;--ice:#6CC0F5;--muted:#93A4B8;--us:#BCA5EC;--us-bg:#251E38;--warn:#F4C14C;--warn-bg:#33290F;";
    const D = t.b1, noir = lumHex(D) < 0.01;
    // Les fonds : des ombres de D (du noir pur au D lui-même). Pour une équipe noire : des noirs.
    const f = noir ? ["#000000", "#0D0D0D", "#141414", "#1C1C1C"] : [ombre(D, 0.38), ombre(D, 0.55), ombre(D, 0.68), ombre(D, 0.82)];
    // La couleur des liens / chiffres en évidence : A, sinon B, sinon le blanc — la première qui se lit sur les cartes
    const ice = [t.acc, t.led, "#FFFFFF"].find(c => c && contr(c, f[1]) >= 4.2);
    const warn = [t.led, t.acc, "#FFFFFF"].find(c => c && contr(c, f[1]) >= 4.2);
    return `--bg:${f[0]};--surface:${f[1]};--surface2:${f[2]};--card:${f[1]};--chip:${f[3]};--ice:${ice};--muted:color-mix(in srgb,#fff 58%,${noir ? "#000" : D});`
      + `--us:${ice};--us-bg:color-mix(in srgb,${ice} 16%,${f[1]});--warn:${warn};--warn-bg:color-mix(in srgb,${warn} 16%,${f[1]});`;
  };
  const cssTheme = (t) => {
    const D = t.b1, eA = encre(t.acc, D), eB = encre(t.led, D);
    const extra = t.neutre || D === NEUTRE.b1 ? "" : `
.chip[aria-pressed="true"],.chip.big[aria-pressed="true"],.sv-btn,.lien-plus,.btn-main,.tag.reel{color:${eA}}
.ticker .tk-lbl,.ticker .tk-tag.prob,header.bug .beta,.rk{color:${eB}}
.ticker .tk-tag,.ticker .tk-tag.serie,.ticker .tk-tag.jalon,.ticker .tk-tag.equipe{background:${t.acc};color:${eA}}
.ticker .tk-tag.blesse,.ticker .tk-tag.seche{background:${t.led};color:${eB}}
.ticker .tk-it::before{background:${t.led}}`;
    return `
:root,:root[data-theme]{${vars(t)}--ink:#F2F5F8;--line:#ffffff1c;
  --bande:${D};--bande2:color-mix(in srgb,${D} 82%,#fff);--goal:${t.acc};--led:${t.led};--chipon:${t.acc};--good:#3DDC84;--good-bg:#10301F;--bad:#FF7B6A;--bad-bg:#3A1915;
  --rayure:transparent;color-scheme:dark}
body{background:var(--bg) radial-gradient(120% 60% at 50% 0%, color-mix(in srgb,${D} 60%,transparent), transparent 60%) no-repeat fixed}
header.bug{background:radial-gradient(120% 140% at 10% 0%, color-mix(in srgb,${D} 80%,#fff) 0%, ${D} 50%, color-mix(in srgb,${D} 75%,#000) 100%);overflow:hidden}
header.bug::before{content:"";position:absolute;left:52%;width:70%;height:54px;bottom:-34px;transform:rotate(-24deg);transform-origin:left bottom;pointer-events:none;
  background:linear-gradient(180deg,${t.sa} 0 27%,${D} 27% 34%,${t.sw} 34% 66%,${D} 66% 73%,${t.sa} 73% 100%);box-shadow:0 0 14px #0008}
header.bug > *{position:relative;z-index:1}
header.bug .lang,header.bug .livebtn{background:color-mix(in srgb,${D} 70%,#000);box-shadow:0 2px 8px #0006}
header.bug::after{background:linear-gradient(90deg,${t.acc} 0 70%,${t.led} 70% 100%)}
nav.tabs,nav.menu{background:${D}} nav.tabs button[aria-selected="true"]{color:#fff}
.ticker{background:color-mix(in srgb,${D} 70%,#000)}${extra}`;
  };
  const theme = (t) => {
    let st = document.getElementById("pp-theme");
    if (!st){ st = document.createElement("style"); st.id = "pp-theme"; document.head.appendChild(st); }
    st.textContent = cssTheme(t);
    document.querySelector('meta[name="theme-color"]')?.setAttribute("content", t.b1);   // la barre du navigateur aussi
    try { localStorage.setItem("pp_theme", JSON.stringify(t)); } catch (e) { /* tant pis */ }
  };
  // Tout de suite (avant de lire club.json) : le dernier thème gardé, sinon le neutre
  try { theme(JSON.parse(localStorage.getItem("pp_theme") || "null") || NEUTRE); } catch (e) { theme(NEUTRE); }
  const majTheme = () => { const c = club(); if (!c) return theme(NEUTRE); donnees().then(() => theme(themeDe(c))); };

  // ---- Style (une seule fois) ----
  const css = document.createElement("style");
  css.textContent = `
.club-btn{display:inline-flex;align-self:flex-start;align-items:center;gap:5px;margin:2px 0 4px;padding:3px 9px 3px 4px;border-radius:14px;border:1.5px solid rgba(255,255,255,.5);
  background:rgba(255,255,255,.08);color:#fff;font:800 11.5px/1 var(--f-display);text-transform:uppercase;letter-spacing:.04em;cursor:pointer;white-space:nowrap}
.club-btn:not(:has(.club-pas)){padding-left:9px}
.club-btn .club-pas{width:20px;height:20px;border-radius:50%;background:var(--c);display:inline-grid;place-items:center;font:800 8px/1 var(--f-body);color:#fff;box-shadow:0 0 0 1.5px #fff}
.club-ov{position:fixed;inset:0;z-index:60;background:rgba(5,15,30,.72);display:flex;align-items:center;justify-content:center;padding:14px}
.club-boite{background:var(--card,#fff);color:var(--ink,#111);width:min(560px,100%);max-height:88vh;overflow:auto;border-radius:12px;padding:16px;box-shadow:0 18px 50px rgba(0,0,0,.5)}
.club-boite h2{margin:0 0 4px;font:italic 800 24px/1.1 var(--f-display);text-transform:uppercase}
.club-boite p{margin:0 0 12px;color:var(--muted,#667)}
.club-grille{display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:6px}
.club-ch{display:flex;align-items:center;gap:8px;padding:7px 8px;border-radius:8px;border:1px solid var(--line,#ddd);background:transparent;color:inherit;cursor:pointer;text-align:left;font:600 13px/1.1 var(--f-body)}
.club-ch[aria-pressed="true"]{outline:2.5px solid var(--c);outline-offset:-1px}
.club-ch i{flex:none;width:26px;height:26px;border-radius:50%;background:var(--c);display:grid;place-items:center;font:800 9px/1 var(--f-body);font-style:normal;color:#fff}
.club-pied{display:flex;justify-content:space-between;gap:8px;margin-top:12px}
.club-pied button{border:0;background:transparent;color:var(--muted,#667);font:600 13px var(--f-body);cursor:pointer;text-decoration:underline}
.club-bande{display:flex;align-items:center;gap:10px;margin:10px 0;padding:10px 12px;border-radius:10px;background:var(--card,#fff);border:1px solid var(--line,#ddd)}
.club-bande b{flex:none;font:italic 800 17px/1.1 var(--f-display);text-transform:uppercase}
.club-rang{display:flex;gap:6px;overflow-x:auto;padding:2px;flex:1;scrollbar-width:none}
.club-rang button{flex:none;width:34px;height:34px;border-radius:50%;border:0;background:var(--c);color:#fff;font:800 10px/1 var(--f-body);cursor:pointer}
.club-bande .club-x{flex:none;border:0;background:transparent;color:var(--muted,#667);font:600 12px var(--f-body);cursor:pointer;text-decoration:underline}
.club-bloc{margin:12px 0;border-left:6px solid var(--c);padding:14px}
.club-bloc .club-hd{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.club-bloc .club-hd i{flex:none;width:36px;height:36px;border-radius:50%;background:var(--c);display:grid;place-items:center;font:800 11px/1 var(--f-body);font-style:normal;color:#fff}
.club-bloc h2{margin:0;font:italic 800 22px/1.1 var(--f-display);text-transform:uppercase}
.club-bloc h2 a{color:inherit;text-decoration:none}
.club-bloc .club-chg{margin-left:auto;border:0;background:transparent;color:var(--muted,#667);font:600 12px var(--f-body);cursor:pointer;text-decoration:underline}
.club-soir{display:flex;align-items:baseline;justify-content:space-between;gap:10px;padding:8px 0;border-top:1px solid var(--line,#ddd)}
.club-soir .club-p{font:italic 800 34px/1 var(--f-display)}
.club-soir small{display:block;color:var(--muted,#667);font-size:12px}
.club-top{margin:6px 0 0;padding:0;list-style:none}
.club-top li{display:flex;align-items:center;gap:10px;padding:6px 0;border-top:1px solid var(--line,#ddd)}
.club-top .ph{flex:none;width:34px;height:34px}
.club-top a{color:inherit;font-weight:600}
.club-top b{margin-left:auto;font:italic 800 20px/1 var(--f-display)}
.club-coupe{margin:8px 0 0;font-size:13px;color:var(--muted,#667)}
.club-coupe a{color:inherit}`;
  document.head.appendChild(css);

  // ---- Surlignage de son équipe + son bandeau en premier ----
  const surligne = document.createElement("style");
  document.head.appendChild(surligne);
  function appliquer(){
    const c = club();
    const r = c ? `:is(.wi-l,.j,.tr,.cp)[data-c="${c}"]{background-image:linear-gradient(90deg,color-mix(in srgb,var(--eq) 16%,transparent),transparent 70%)}` : "";
    if (surligne.textContent !== r) surligne.textContent = r;
    if (!c) return;
    document.querySelectorAll(".tk-piste").forEach(p => {
      const k = [...p.children], n = Math.floor(k.length / 2);
      if (!n || p.dataset.club === c) return;
      const tri = (L) => [...L.filter(x => x.dataset.c === c), ...L.filter(x => x.dataset.c !== c)];
      [...tri(k.slice(0, n)), ...tri(k.slice(n))].forEach(x => p.appendChild(x));
      p.dataset.club = c;
    });
  }

  // ---- Bouton dans l'en-tête ----
  let btn = null;
  function bouton(){
    const h = document.querySelector("header.bug");
    if (!h) return;
    if (!btn){
      btn = document.createElement("button");
      btn.type = "button"; btn.className = "club-btn";
      btn.addEventListener("click", choisir);
      // Sous la date de mise à jour (petite pastille) : ne pousse jamais le logo, même sur un petit cell
      const maj = h.querySelector(".maj");
      if (maj) maj.insertAdjacentElement("afterend", btn); else h.appendChild(btn);
    }
    const c = club();
    btn.style.setProperty("--c", coulEq(c));
    btn.innerHTML = c ? `<span class="club-pas">${esc(c)}</span>${esc(c)}` : esc(L("Mon club", "My team"));
    btn.setAttribute("aria-label", c ? L(`Ton club : ${nomEq(c)}. Changer`, `Your team: ${nomEq(c)}. Change`) : L("Choisir mon club", "Pick my team"));
  }

  // ---- Choisir (fenêtre) ----
  function choisir(){
    donnees().then(() => {
      const c = club();
      const ov = document.createElement("div");
      ov.className = "club-ov";
      ov.innerHTML = `<div class="club-boite" role="dialog" aria-modal="true" aria-label="${esc(L("Mon club", "My team"))}">
        <h2>${esc(L("C'est quoi ton club?", "Who's your team?"))}</h2>
        <p>${esc(L("On le met en premier partout sur le site. Gardé seulement sur ton appareil.", "We'll put it first everywhere on the site. Saved on your device only."))}</p>
        <div class="club-grille">${EQ_ORDRE.map(t => `<button type="button" class="club-ch" data-club="${t}" aria-pressed="${t === c}" style="--c:${coulEq(t)}"><i>${t}</i>${esc(nomEq(t))}</button>`).join("")}</div>
        <div class="club-pied"><button type="button" data-club="-">${esc(L("Aucun club", "No team"))}</button><button type="button" data-fermer>${esc(L("Fermer", "Close"))}</button></div></div>`;
      const fermer = () => { ov.remove(); document.removeEventListener("keydown", esc_); };
      const esc_ = (e) => { if (e.key === "Escape") fermer(); };
      ov.addEventListener("click", (e) => {
        const b = e.target.closest("[data-club]");
        if (b){ fixer(b.dataset.club); fermer(); return; }
        if (e.target === ov || e.target.closest("[data-fermer]")) fermer();
      });
      document.addEventListener("keydown", esc_);
      document.body.appendChild(ov);
      ov.querySelector('[aria-pressed="true"], .club-ch')?.focus();
    });
  }
  function fixer(v){
    ecrire(v);
    document.querySelectorAll(".tk-piste").forEach(p => delete p.dataset.club);
    appliquer(); bouton(); accueil(); majTheme();
    document.dispatchEvent(new CustomEvent("pp-club", { detail: club() }));
  }

  // ---- Accueil : la bande, puis le bloc « Ton club ce soir » ----
  function accueil(){
    const bande = document.getElementById("club-bande"), bloc = document.getElementById("club");
    if (!bande && !bloc) return;
    const v = lire();
    if (bande){
      if (v){ bande.innerHTML = ""; }
      else donnees().then(() => {
        bande.innerHTML = `<div class="club-bande"><b>${esc(L("Ton club?", "Your team?"))}</b>
          <div class="club-rang">${EQ_ORDRE.map(t => `<button type="button" data-club="${t}" style="--c:${coulEq(t)}" title="${esc(nomEq(t))}">${t}</button>`).join("")}</div>
          <button type="button" class="club-x" data-club="-">${esc(L("Plus tard", "Later"))}</button></div>`;
        bande.onclick = (e) => { const b = e.target.closest("[data-club]"); if (b) fixer(b.dataset.club); };
      });
    }
    if (!bloc) return;
    const c = club();
    if (!c){ bloc.innerHTML = ""; return; }
    donnees().then((D) => {
      const x = D?.eq?.[c];
      if (!x){ bloc.innerHTML = ""; return; }
      const lienEq = RACINE + (FR ? "equipes/" : "teams/") + c.toLowerCase() + "/";
      const m = x.m;
      const heure = m?.h ? new Date(m.h).toLocaleTimeString(FR ? "fr-CA" : "en-CA", { hour: "numeric", minute: "2-digit" }) : "";
      const soir = m ? `<div class="club-soir"><div><b>${esc(L("Ce soir", "Tonight"))}</b> ${m.dom ? "vs" : "@"} ${esc(nomEq(m.adv))}<small>${esc(heure)}</small></div>
          <div style="text-align:right"><span class="club-p">${pc(m.p)}</span><small>${esc(L("chance de gagner", "chance to win"))}</small></div></div>`
        : `<div class="club-soir"><div>${esc(L("Pas de match ce soir.", "No game tonight."))}</div></div>`;
      const pos = (p) => ({ D: "D", G: "G" })[String(p || "").toUpperCase()] || L("AV", "F");
      const top = (x.top || []).length ? `<ul class="club-top">${x.top.map(([n, no, p, pr, slug]) => `<li><span class="ph"><span class="plaque" style="--eq:${x.c}"><b>${esc(no ?? "")}</b><i>${pos(p)}</i></span></span>
          ${slug ? `<a href="${RACINE}${FR ? "joueurs/" : "players/"}${encodeURIComponent(slug)}/">${esc(n)}</a>` : esc(n)}<b>${pc(pr)}</b></li>`).join("")}</ul>
          <p class="club-coupe">${esc(L("Chance de marquer un but ce soir.", "Chance to score a goal tonight."))}</p>` : "";
      const cp = x.coupe ? `<p class="club-coupe"><a href="${RACINE}${FR ? "coupe-stanley/" : "stanley-cup/"}">${esc(L("Coupe Stanley", "Stanley Cup"))}</a> : ${pc(x.coupe.p)}
          · ${esc(L("séries", "playoffs"))} ${pc(x.coupe.ps)}${x.coupe.pts != null ? ` · ${x.coupe.pts} pts ${esc(L("en", "in"))} ${x.coupe.pj} ${esc(L("matchs", "games"))}` : ""}</p>` : "";
      bloc.innerHTML = `<section class="card club-bloc" style="--c:${x.c}"><div class="club-hd"><i>${c}</i><h2><a href="${lienEq}">${esc(L("Ton club : ", "Your team: "))}${esc(nomEq(c))}</a></h2>
          <button type="button" class="club-chg">${esc(L("Changer", "Change"))}</button></div>${soir}${top}${cp}</section>`;
      bloc.querySelector(".club-chg").onclick = choisir;
    });
  }

  function demarrer(){
    if (club()) donnees().then(bouton); else bouton();
    appliquer(); accueil(); majTheme();
    // L'app redessine ses listes et son bandeau : on réapplique (le surlignage est en CSS, le bandeau se retrie)
    new MutationObserver(() => appliquer()).observe(document.body, { childList: true, subtree: true });
  }
  window.ppClub = club;
  window.ppChoisirClub = choisir;
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", demarrer); else demarrer();
})();

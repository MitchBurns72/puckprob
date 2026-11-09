/* PuckProb : la barre du bas + les pastilles du haut + le tiroir « Tout » (généré par src/nav_site.py) */
(function(){
  if (window.__ppNav) return; window.__ppNav = 1;
  var S = [["soir", "joueurs", "t-joueurs", ["Joueurs", "fr/ce-soir/#joueurs"], ["Players", "tonight/#players"], "🎯", ["% du soir", "tonight's %"]], ["soir", "matchs", "t-matchs", ["Matchs", "fr/ce-soir/#matchs"], ["Games", "tonight/#games"], "🏒", ["duels du soir", "tonight's games"]], ["soir", "sim", "t-sim", ["PB SIM", "fr/ce-soir/#sim"], ["PB SIM", "tonight/#sim"], "🎲", ["joue la saison", "play the season"]], ["soir", "suivi", "t-suivi", ["Suivi", "fr/ce-soir/#suivi"], ["Tracking", "tonight/#tracking"], "📡", ["en direct", "live"]], ["soir", "bets", "t-bets", ["Bets", "#bets"], ["Bets", "#bets"], "💵", ["premium", "premium"]], ["courses", "trophees", null, ["Trophées", "fr/ce-soir/#trophees"], ["Trophies", "tonight/#trophies"], "🏆", ["Art Ross, Hart...", "Art Ross, Hart..."]], ["courses", "coupe", null, ["Coupe", "fr/coupe-stanley/"], ["Cup", "stanley-cup/"], "🥇", ["chances de Coupe", "Cup chances"]], ["courses", "classement", "t-coupe", ["Classement", "fr/ce-soir/#classement"], ["Standings", "tonight/#standings"], "📋", ["fin de saison", "final standings"]], ["courses", "projections", "t-prj", ["Projections", "fr/ce-soir/#projections"], ["Projections", "tonight/#projections"], "📈", ["buts, points", "goals, points"]], ["stats", "whatif", "t-whatif", ["What if", "fr/ce-soir/#what-if"], ["What if", "tonight/#what-if"], "❓", ["carrières", "careers"]], ["stats", "salaires", "t-salaires", ["Salaires", "fr/ce-soir/#salaires"], ["Salaries", "tonight/#salaries"], "💰", ["salaire mérité", "deserved salary"]], ["stats", "enforcers", "t-enf", ["Enforcers", "fr/ce-soir/#enforcers"], ["Enforcers", "tonight/#enforcers"], "🥊", ["les durs", "tough guys"]], ["stats", "duos", "t-duo", ["Duos", "fr/ce-soir/#duos"], ["Duos", "tonight/#duos"], "🤝", ["chimie", "chemistry"]], ["stats", "gcr", "t-gcr", ["GCR", "fr/ce-soir/#gcr"], ["GCR", "tonight/#gcr"], "🧤", ["gardiens", "goalies"]], ["stats", "arbitres", "t-arb", ["Arbitres", "fr/ce-soir/#arbitres"], ["Refs", "tonight/#refs"], "🦓", ["pénalités", "penalties"]], ["equipes", "equipes", null, ["Équipes", "fr/equipes/"], ["Teams", "teams/"], "🛡️", ["32 équipes", "32 teams"]], ["plus", "bilan", null, ["Bilan", "fr/bilan/"], ["Track record", "track-record/"], "✅", ["nos % vérifiés", "our % checked"]], ["plus", "nouveautes", null, ["Quoi de neuf", "fr/nouveautes/"], ["What's new", "whats-new/"], "✨", ["", ""]], ["plus", "liens", null, ["Liens", "liens/"], ["Links", "liens/"], "🔗", ["nos posts", "our posts"]], ["plus", "apropos", null, ["À propos", "fr/a-propos/"], ["About", "about/"], "ℹ️", ["", ""]]], F = [["soir", ["Ce soir", "Tonight"], "🏒"], ["courses", ["Courses", "Races"], "🏆"], ["stats", ["Stats", "Stats"], "📊"], ["equipes", ["Équipes", "Teams"], "🛡️"], ["plus", ["Équipes et plus", "Teams and more"], ""]];
  var FR = /^fr/i.test(document.documentElement.lang || ""), K = FR ? 0 : 1;
  var prive = document.documentElement.hasAttribute("data-prive");
  var app = !!document.querySelector("nav.tabs");
  // La racine du site (le chemin de nav.js moins « nav.js » et « fr/ ») : marche en ligne et en test local
  var src = (document.currentScript && document.currentScript.src) || "";
  var racine = src ? new URL(".", src).pathname.replace(/fr\/$/, "") : "/";
  var appPath = prive ? location.pathname : null;
  function lien(x){
    var p = x[K + 3][1];
    if (x[2] && app) return (appPath || location.pathname) + p.replace(/^[^#]*/, "");    // onglet de l'app : même page
    if (x[2] && prive) return location.pathname + p.replace(/^[^#]*/, "");
    return racine + p;
  }
  // Bets : seulement dans ta version premium ; un onglet de l'app absent de cette page (ex. une vieille version) : caché
  var dispo = S.filter(function(x){
    if (x[2] === "t-bets") return app && prive && !!document.getElementById("t-bets");
    return !app || !x[2] || !!document.getElementById(x[2]);
  });
  function courant(){
    if (app){
      var t = document.querySelector('nav.tabs [aria-selected="true"]'), id = t ? t.id : "t-joueurs";
      if (id === "t-coupe") return "classement";          // dans l'app, l'onglet Trophées sert au classement (#classement)
      var x = dispo.filter(function(y){ return y[2] === id; })[0]; return x ? x[1] : "joueurs";
    }
    var p = location.pathname.slice(racine.length).replace(/^fr\//, "");
    if (/^(trophees|trophies)\//.test(p)) return "trophees";
    if (/^(coupe-stanley|stanley-cup)\//.test(p)) return "coupe";
    if (/^(equipes|teams|joueurs|players)\//.test(p)) return "equipes";
    if (/^(bilan|track-record)\//.test(p)) return "bilan";
    if (/^(nouveautes|whats-new)\//.test(p)) return "nouveautes";
    if (/^liens\//.test(p)) return "liens";
    if (/^(a-propos|about)\//.test(p)) return "apropos";
    return "";                                            // l'accueil : famille Ce soir, aucune pastille allumée
  }
  function famDe(id){ var x = dispo.filter(function(y){ return y[1] === id; })[0]; return x ? x[0] : "soir"; }
  function memo(f, id){ try { localStorage.setItem("pp-nav-" + f, id); } catch (e) {} }
  function lu(f){ try { return localStorage.getItem("pp-nav-" + f); } catch (e) { return null; } }
  var css = document.createElement("style");
  css.textContent =
    "nav.menu{display:none!important} nav.tabs{display:none!important}" +
    "#temoins{bottom:calc(66px + env(safe-area-inset-bottom,0px))!important;padding-bottom:12px!important}.pt-attente{bottom:calc(92px + env(safe-area-inset-bottom,0px))!important}" +
    "body{padding-bottom:calc(74px + env(safe-area-inset-bottom,0px))}" +
    ".ppn-chips{display:flex;gap:7px;overflow-x:auto;scrollbar-width:none;padding:9px 2px 8px;margin:4px 0 6px;position:sticky;top:env(safe-area-inset-top,0px);z-index:6;background:var(--bg)}" +
    ".ppn-chips::-webkit-scrollbar{display:none}" +
    ".ppn-chips a{flex:none;border:1px solid var(--line);border-radius:16px;padding:6px 12px;font:600 14px/1 var(--f-body);color:var(--ink);text-decoration:none;background:var(--surface)}" +
    ".ppn-chips a[aria-current]{background:var(--led,#FFB81C);border-color:var(--led,#FFB81C);color:#0B1220;font-weight:800}" +
    ".ppn-bas{position:fixed;left:0;right:0;bottom:0;z-index:50;display:flex;justify-content:space-around;background:var(--bande,#0A2342);border-top:2px solid var(--led,#FFB81C);padding:6px 0 calc(8px + env(safe-area-inset-bottom,0px))}" +
    ".ppn-bas a,.ppn-bas button{flex:1;display:flex;flex-direction:column;align-items:center;gap:2px;font:700 11.5px/1.1 var(--f-body);color:#9FB3CB;text-decoration:none;background:none;border:0;padding:2px 0;cursor:pointer}" +
    ".ppn-bas i{font-style:normal;font-size:21px;line-height:1.15}.ppn-bas [aria-current]{color:var(--led,#FFB81C)}" +
    ".ppn-voile{position:fixed;inset:0;z-index:48;background:rgba(0,0,0,.6)}" +
    ".ppn-tiroir{position:fixed;left:0;right:0;bottom:0;top:max(48px,env(safe-area-inset-top,0px));z-index:49;background:var(--bande,#0A2342);border-radius:18px 18px 0 0;border-top:2px solid var(--led,#FFB81C);overflow-y:auto;padding:8px 14px calc(86px + env(safe-area-inset-bottom,0px))}" +
    ".ppn-tiroir .poi{width:44px;height:5px;border-radius:3px;background:rgba(255,255,255,.25);margin:0 auto 4px}" +
    ".ppn-tiroir h3{font:italic 800 15px var(--f-display);color:var(--led,#FFB81C);text-transform:uppercase;margin:12px 2px 7px;letter-spacing:.02em}" +
    ".ppn-tuiles{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;max-width:640px}" +
    ".ppn-tuiles a{display:flex;flex-direction:column;align-items:center;gap:3px;text-align:center;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:9px;padding:10px 6px;color:#fff;text-decoration:none;font:700 13.5px/1.15 var(--f-body)}" +
    ".ppn-tuiles a i{font-style:normal;font-size:21px}.ppn-tuiles a small{font:500 11px var(--f-body);color:#9FB3CB}" +
    ".ppn-tuiles a[aria-current]{border-color:var(--led,#FFB81C);color:var(--led,#FFB81C)}" +
    "@media (min-width:900px){.ppn-tiroir{left:50%;right:auto;width:680px;transform:translateX(-50%)}.ppn-tuiles{grid-template-columns:repeat(4,minmax(0,1fr))}}";
  document.head.appendChild(css);
  var chips = document.createElement("nav"); chips.className = "ppn-chips"; chips.setAttribute("aria-label", FR ? "Sections" : "Sections");
  var bas = document.createElement("nav"); bas.className = "ppn-bas"; bas.setAttribute("aria-label", FR ? "Menu" : "Menu");
  function rendre(){
    var id = courant(), fam = id ? famDe(id) : "soir";
    if (id && fam !== "plus") memo(fam, id);
    var items = dispo.filter(function(x){ return x[0] === fam; });
    chips.innerHTML = fam === "plus" ? "" : items.map(function(x){
      return '<a href="' + lien(x) + '"' + (x[1] === id ? ' aria-current="page"' : "") + ">" + x[K + 3][0] + "</a>"; }).join("");
    chips.hidden = fam === "plus" || items.length < 2;
    bas.innerHTML = F.filter(function(f){ return f[0] !== "plus"; }).map(function(f){
      var der = lu(f[0]), x = dispo.filter(function(y){ return y[0] === f[0] && y[1] === der; })[0] || dispo.filter(function(y){ return y[0] === f[0]; })[0];
      return '<a href="' + (x ? lien(x) : racine) + '"' + (f[0] === fam && id ? ' aria-current="page"' : "") + "><i>" + f[2] + "</i>" + f[1][K] + "</a>"; }).join("")
      + '<button type="button" class="ppn-tout"' + (fam === "plus" ? ' aria-current="page"' : "") + '><i>☰</i>' + (FR ? "Tout" : "All") + "</button>";
    var a = chips.querySelector("[aria-current]"); if (a && a.scrollIntoView) a.scrollIntoView({ block: "nearest", inline: "center" });
  }
  function tiroir(){
    var id = courant(), v = document.createElement("div"), t = document.createElement("div");
    v.className = "ppn-voile"; t.className = "ppn-tiroir"; t.setAttribute("role", "dialog"); t.setAttribute("aria-label", FR ? "Toutes les sections" : "All sections");
    t.innerHTML = '<div class="poi"></div>' + F.map(function(f){
      var L = dispo.filter(function(x){ return x[0] === f[0] || (f[0] === "plus" && x[0] === "equipes"); });
      if (f[0] === "equipes" || !L.length) return "";
      return "<h3>" + f[1][K] + '</h3><div class="ppn-tuiles">' + L.map(function(x){
        return '<a href="' + lien(x) + '"' + (x[1] === id ? ' aria-current="page"' : "") + "><i>" + x[5] + "</i>" + x[K + 3][0] + (x[6][K] ? "<small>" + x[6][K] + "</small>" : "") + "</a>"; }).join("") + "</div>";
    }).join("");
    var fermer = function(){ v.remove(); t.remove(); document.removeEventListener("keydown", esc); rendre(); };
    var esc = function(e){ if (e.key === "Escape") fermer(); };
    v.addEventListener("click", fermer); t.addEventListener("click", function(e){ if (e.target.closest("a")) setTimeout(fermer, 0); });
    document.addEventListener("keydown", esc);
    document.body.appendChild(v); document.body.appendChild(t);
    bas.querySelectorAll("[aria-current]").forEach(function(b){ b.removeAttribute("aria-current"); });
    bas.querySelector(".ppn-tout").setAttribute("aria-current", "page");
  }
  bas.addEventListener("click", function(e){ if (e.target.closest(".ppn-tout")){ var o = document.querySelector(".ppn-tiroir"); o ? (document.querySelector(".ppn-voile").remove(), o.remove(), rendre()) : tiroir(); } });
  function poser(){
    var ancre = document.querySelector("nav.tabs") || document.querySelector("nav.menu") || document.querySelector("main");
    if (ancre && ancre.parentNode) ancre.parentNode.insertBefore(chips, ancre);
    document.body.appendChild(bas);
    rendre();
    window.addEventListener("hashchange", function(){ setTimeout(rendre, 30); });
    var tabs = document.querySelector("nav.tabs");
    if (tabs && window.MutationObserver) new MutationObserver(function(){ rendre(); }).observe(tabs, { attributes: true, subtree: true, attributeFilter: ["aria-selected"] });
  }
  document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", poser) : poser();
})();

/* PuckProb : la barre du bas + les pastilles du haut + le tiroir « Tout » (généré par src/nav_site.py) */
(function(){
  if (window.__ppNav) return; window.__ppNav = 1;
  var S = [["soir", "joueurs", "t-joueurs", ["G.P. Joueurs", "fr/ce-soir/#joueurs"], ["G.P. Players", "tonight/#players"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#C8102E\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M30 22l-6 4 3 6 3-2v13h12V30l3 2 3-6-6-4q-3 3-6 3t-6-3z\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2.6\"/></g></svg>", ["% du soir", "tonight's %"]], ["soir", "matchs", "t-matchs", ["G.P. Matchs", "fr/ce-soir/#matchs"], ["G.P. Games", "tonight/#games"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#C8102E\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><text x=\"36\" y=\"37.4\" text-anchor=\"middle\" font-family=\"Arial Black,Arial\" font-weight=\"900\" font-size=\"15\" fill=\"#fff\">VS</text></g></svg>", ["duels du soir", "tonight's games"]], ["tools", "sim", "t-sim", ["PB Manager PA: Season Sim", "fr/ce-soir/#sim"], ["PB Manager PA: Season Sim", "tonight/#sim"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#7B4FC9\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><rect x=\"26\" y=\"22\" width=\"20\" height=\"20\" rx=\"4\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/><circle cx=\"31\" cy=\"27\" r=\"1.9\" fill=\"#fff\"/><circle cx=\"36\" cy=\"32\" r=\"1.9\" fill=\"#fff\"/><circle cx=\"41\" cy=\"37\" r=\"1.9\" fill=\"#fff\"/></g></svg>", ["joue la saison", "play the season"]], ["news", "rumeurs", "t-rum", ["Nouvelles", "fr/ce-soir/#nouvelles"], ["News", "tonight/#news"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#1E8A4C\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M25 23h22a3 3 0 0 1 3 3v11a3 3 0 0 1-3 3H35l-6 5v-5h-4a3 3 0 0 1-3-3V26a3 3 0 0 1 3-3z\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3\" stroke-linejoin=\"round\"/><text x=\"36\" y=\"36\" text-anchor=\"middle\" font-family=\"Arial Black,Arial\" font-weight=\"900\" font-size=\"11\" fill=\"#fff\">?!</text></g></svg>", ["échanges et rumeurs", "trades and rumors"]], ["news", "wire", "t-wire", ["PB On The Wire", "fr/ce-soir/#sur-le-fil"], ["PB On The Wire", "tonight/#on-the-wire"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#1E8A4C\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M26 23h17v19H28a2 2 0 0 1-2-2z M43 28h4v12a2 2 0 0 1-4 0 M30 28h9 M30 33h9 M30 38h6\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></g></svg>", ["l'article du jour", "today's article"]], ["news", "ligue", "t-cls", ["Classement", "fr/ce-soir/#classement-lnh"], ["Standings", "tonight/#league-standings"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#1E8A4C\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M33 25h13 M33 32h13 M33 39h13\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/><text x=\"28\" y=\"28.5\" text-anchor=\"middle\" font-family=\"Arial Black,Arial\" font-weight=\"900\" font-size=\"9\" fill=\"#fff\">1</text><text x=\"28\" y=\"35.5\" text-anchor=\"middle\" font-family=\"Arial Black,Arial\" font-weight=\"900\" font-size=\"9\" fill=\"#fff\">2</text><text x=\"28\" y=\"42.5\" text-anchor=\"middle\" font-family=\"Arial Black,Arial\" font-weight=\"900\" font-size=\"9\" fill=\"#fff\">3</text></g></svg>", ["la ligue en ce moment", "the league right now"]], ["news", "transactions", "t-trx", ["Transactions", "fr/ce-soir/#transactions"], ["Transactions", "tonight/#transactions"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#1E8A4C\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M26 28h18l-5-5 M46 36H28l5 5\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></g></svg>", ["échanges notés sur 100 %", "trades graded out of 100%"]], ["soir", "suivi", "t-suivi", ["Suivi", "fr/ce-soir/#suivi"], ["Tracking", "tonight/#tracking"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#C8102E\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><circle cx=\"27\" cy=\"32\" r=\"3\" fill=\"#fff\"/><text x=\"39\" y=\"35.5\" text-anchor=\"middle\" font-family=\"Arial Black,Arial\" font-weight=\"900\" font-size=\"10\" fill=\"#fff\">LIVE</text></g></svg>", ["en direct", "live"]], ["soir", "bets", "t-bets", ["Bets", "#bets"], ["Bets", "#bets"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#C8102E\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M25 25h22v5a2 2 0 0 0 0 4v5H25v-5a2 2 0 0 0 0-4z\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2.6\"/><path d=\"M33 35l6-6\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2.2\"/></g></svg>", ["premium", "premium"]], ["courses", "classement", "t-coupe", ["PB Awards Projections", "fr/ce-soir/#classement"], ["PB Awards Projections", "tonight/#standings"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#D99A0B\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M30 22h12v5q0 7-6 7t-6-7z M36 34v5 M32 42h8 M33 39h6\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/><path d=\"M36 15l1.5 3 3 .4-2.2 2 .6 3-2.9-1.5-2.9 1.5.6-3-2.2-2 3-.4z\" fill=\"#fff\"/></g></svg>", ["fin de saison, Art Ross, Hart...", "final standings, Art Ross, Hart..."]], ["courses", "power", "t-pwr", ["Power rankings", "fr/ce-soir/#power"], ["Power rankings", "tonight/#power"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#D99A0B\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><text x=\"36\" y=\"38.5\" text-anchor=\"middle\" font-family=\"Arial Black,Arial\" font-weight=\"900\" font-size=\"18\" fill=\"#fff\">#1</text></g></svg>", ["la semaine", "this week"]], ["courses", "projections", "t-prj", ["PB Season Projections", "fr/ce-soir/#projections"], ["PB Season Projections", "tonight/#projections"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#D99A0B\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M25 41l7-7 5 4 9-11 M40 27h6v6\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></g></svg>", ["buts, points", "goals, points"]], ["stats", "whatif", "t-whatif", ["PB Stats", "fr/ce-soir/#what-if"], ["PB Stats", "tonight/#what-if"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#2E6FD8\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M25 24h22v18H25z M25 30h22 M25 36h22 M33 24v18\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></g></svg>", ["carrières", "careers"]], ["stats", "salaires", "t-salaires", ["PB Market Value", "fr/ce-soir/#salaires"], ["PB Market Value", "tonight/#salaries"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#2E6FD8\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><text x=\"36\" y=\"40.6\" text-anchor=\"middle\" font-family=\"Arial Black,Arial\" font-weight=\"900\" font-size=\"24\" fill=\"#fff\">$</text></g></svg>", ["ce que chacun vaut", "what each player is worth"]], ["stats", "enforcers", "t-enf", ["PB Intimidation %", "fr/ce-soir/#enforcers"], ["PB Intimidation %", "tonight/#enforcers"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#2E6FD8\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M28 34v-6q0-6 7-6h3q7 0 7 7v5q0 6-6 6h-6q-5 0-5-6z M28 31q-3 0-3 3t3 3 M30 40v4h12v-4\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2.6\"/></g></svg>", ["les durs", "tough guys"]], ["stats", "duos", "t-duo", ["PB Chemistry %", "fr/ce-soir/#duos"], ["PB Chemistry %", "tonight/#duos"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#2E6FD8\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><circle cx=\"30\" cy=\"27\" r=\"4\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/><circle cx=\"42\" cy=\"27\" r=\"4\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/><path d=\"M23 42c0-5 3-8 7-8s7 3 7 8 M35 42c0-5 3-8 7-8s7 3 7 8\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></g></svg>", ["chimie", "chemistry"]], ["stats", "gcr", "t-gcr", ["PB Goalie Confidence %", "fr/ce-soir/#gcr"], ["PB Goalie Confidence %", "tonight/#gcr"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#2E6FD8\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M27 26q9-7 18 0v8q0 9-9 10q-9-1-9-10z M30 33h12 M30 38h12 M34 31v11 M38 31v11\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></g></svg>", ["confiance", "confidence"]], ["tools", "correlation", "t-cor", ["PB Correlation Trend", "fr/ce-soir/#correlation"], ["PB Correlation Trend", "tonight/#correlation"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#7B4FC9\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M24 42l24-18\" fill=\"none\" stroke=\"#fff\" stroke-width=\"2.4\" stroke-linecap=\"round\" stroke-dasharray=\"3 3\"/><circle cx=\"27\" cy=\"36\" r=\"2.6\" fill=\"#fff\"/><circle cx=\"33\" cy=\"38\" r=\"2.6\" fill=\"#fff\"/><circle cx=\"36\" cy=\"30\" r=\"2.6\" fill=\"#fff\"/><circle cx=\"42\" cy=\"31\" r=\"2.6\" fill=\"#fff\"/><circle cx=\"45\" cy=\"23\" r=\"2.6\" fill=\"#fff\"/></g></svg>", ["deux stats face à face", "two stats head to head"]], ["stats", "arbitres", "t-arb", ["PB Ref Bias %", "fr/ce-soir/#arbitres"], ["PB Ref Bias %", "tonight/#refs"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#2E6FD8\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M30 22l-6 4 3 6 3-2v13h12V30l3 2 3-6-6-4q-3 3-6 3t-6-3z\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2.4\"/><path d=\"M33 26v17 M39 26v17\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2.6\"/></g></svg>", ["pénalités", "penalties"]], ["stats", "forme", "t-forme", ["PB Heat %", "fr/ce-soir/#forme"], ["PB Heat %", "tonight/#heat-index"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#2E6FD8\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M36 19c1 6 9 9 9 17a9 9 0 0 1-18 0c0-4 2-7 4-9 0 3 1 5 3 5 0-5-1-9 2-13z\" fill=\"#fff\"/></g></svg>", ["en forme", "hot and cold"]], ["stats", "coach", "t-coach", ["PB Coach Boost %", "fr/ce-soir/#coach"], ["PB Coach Boost %", "tonight/#coach"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#2E6FD8\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M29 22h14a2 2 0 0 1 2 2v19a2 2 0 0 1-2 2H29a2 2 0 0 1-2-2V24a2 2 0 0 1 2-2z M33 20h6v4h-6z M31 31l3 3 6-6 M31 39h10\" fill=\"none\" stroke=\"#fff\" stroke-width=\"2.6\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></g></svg>", ["les coachs", "the coaches"]], ["stats", "dev", "t-dev", ["PB Dev %", "fr/ce-soir/#dev"], ["PB Dev %", "tonight/#dev"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#2E6FD8\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M36 44V28 M36 33c-6 0-10-4-10-10 6 0 10 4 10 10z M36 30c0-6 4-10 10-10 0 6-4 10-10 10z\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></g></svg>", ["les jeunes vs leur rang", "youngsters vs their slot"]], ["news", "fa", "t-fa", ["Upcoming FA", "fr/ce-soir/#agents-libres"], ["Upcoming FA", "tonight/#free-agents"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#1E8A4C\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M28 21h11l6 6v16H28z M39 21v6h6 M31 32h10 M31 36h10 M31 40h5\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></g></svg>", ["les contrats qui finissent", "expiring contracts"]], ["plus", "bilan", null, ["Contrôle de qualité", "fr/bilan/"], ["Quality Control", "track-record/"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#4A5D78\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M27 27l2 2 4-4 M36 27h10 M27 36l2 2 4-4 M36 36h10\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2.8\"/></g></svg>", ["chaque modèle vérifié", "every model checked"]], ["plus", "nouveautes", null, ["Quoi de neuf", "fr/nouveautes/"], ["What's new", "whats-new/"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#4A5D78\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M36 20l3 9 9 3-9 3-3 9-3-9-9-3 9-3z\" fill=\"#fff\"/></g></svg>", ["", ""]], ["plus", "liens", null, ["Liens", "liens/"], ["Links", "liens/"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#4A5D78\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><path d=\"M33 35l6-6 M30 32l-3 3a4 4 0 0 0 6 6l3-3 M42 32l3-3a4 4 0 0 0-6-6l-3 3\" fill=\"none\" stroke=\"#fff\" stroke-width=\"3.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></g></svg>", ["nos posts", "our posts"]], ["plus", "apropos", null, ["How it works", "fr/a-propos/"], ["How it works", "about/"], "<svg viewBox=\"0 0 64 64\" aria-hidden=\"true\"><rect class=\"an\" x=\"6\" y=\"6\" width=\"52\" height=\"52\" rx=\"14\" fill=\"#4A5D78\" stroke=\"none\" stroke-width=\"5\"/><g transform=\"translate(-4 0)\"><text x=\"36\" y=\"40.6\" text-anchor=\"middle\" font-family=\"Arial Black,Arial\" font-weight=\"900\" font-size=\"24\" fill=\"#fff\">i</text></g></svg>", ["", ""]]], F = [["soir", ["Gameday Probs", "Gameday Probs"], "<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.1\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M5 3.5l6.5 12.5H18\"/><ellipse cx=\"7.5\" cy=\"19.2\" rx=\"3.6\" ry=\"1.7\"/></svg>", ["Gameday", "Gameday"]], ["courses", ["26/27 Season Probs", "26/27 Season Probs"], "<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.1\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M8 4h8v4.5a4 4 0 0 1-8 0z M8 6H5.2a3 3 0 0 0 3 3.8 M16 6h2.8a3 3 0 0 1-3 3.8 M12 12.6V16 M8.5 20h7 M9.5 16h5v4h-5z\"/></svg>", ["Saison", "Season"]], ["stats", ["Stats", "Stats"], "<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.1\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M5 20v-6 M10 20V9 M15 20v-8 M20 20V4\"/></svg>", ["Stats", "Stats"]], ["news", ["League news", "League news"], "<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.1\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M5 5h11v13a2 2 0 0 0 2 2H6a1 1 0 0 1-1-1z M16 9h3v9a2 2 0 0 1-4 0 M8 9h5 M8 12.5h5 M8 16h3\"/></svg>", ["Ligue", "League"]], ["tools", ["Tools", "Tools"], "<svg viewBox=\"0 0 24 24\" aria-hidden=\"true\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.1\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M14.5 6.5a4 4 0 0 0 5 5L12 19a2.1 2.1 0 0 1-3-3l7.5-7.5 M14.5 6.5L17 4l3 3-2.5 2.5\"/></svg>", ["Outils", "Tools"]], ["plus", ["Plus", "More"], "", ["Plus", "More"]]], PB = {"power": "PBDR", "gcr": "PBGC", "salaires": "PBMV", "enforcers": "PBIR", "duos": "PBCS", "arbitres": "PBRB", "projections": "PBSP", "whatif": "Era-Adj.", "coach": "PBCB", "forme": "PBHI", "dev": "PBDV"};
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
    // Suivi (la note de chaque recette) : seulement dans ta version privée. Sur le site public, l'app le cache
    // (data-cache) et le bouton menait nulle part (Mitch, 8 nov. 2026 : « tracking fonctionne pas »)
    var el = x[2] ? document.getElementById(x[2]) : null;
    if (x[2] === "t-suivi") return app && !!el && el.dataset.cache !== "1";
    return !app || !x[2] || (!!el && el.dataset.cache !== "1");
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
    /* Le finder : la loupe dans l'en-tête (une colonne de plus dans la grille de l'en-tête A, docs/carte.css) et sa
       fenêtre plein écran, au thème du site (--bg suit Mon club). */
    "html header.bug.bug.ppf-h{grid-template-columns:auto 1fr auto auto auto;grid-template-areas:'logo . f d club' 'maj . f d club'}" +
    "@media (max-width:380px){html header.bug.bug.ppf-h{column-gap:4px;padding-left:10px;padding-right:10px}html header.bug.ppf-h .livebtn{padding:6px 7px}html header.bug.ppf-h .logo-site.logo-site{width:104px}html header.bug.ppf-h .beta{display:none}}" +
    ".ppf-loupe{grid-area:f;width:30px;height:30px;border-radius:15px;border:0;background:rgba(255,255,255,.12);color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;padding:0;margin:0}" +
    ".ppf-loupe svg{width:18px;height:18px}.ppf-bar svg{width:20px;height:20px}.ppf-loupe svg,.ppf-bar svg{fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round}" +
    ".ppf-loupe.ppf-flot{position:fixed;top:10px;right:12px;z-index:54;background:var(--bande,#0A2342);box-shadow:0 4px 12px rgba(0,0,0,.35)}" +
    "html.ppf-ouvert{overflow:hidden}" +
    "#pp-find{position:fixed;inset:0;z-index:90;background:var(--bg,#0B1C33);color:#EAF1F8;overflow-y:auto;-webkit-overflow-scrolling:touch;padding:max(12px,env(safe-area-inset-top,0px)) 14px 40px;font-family:var(--f-body,system-ui)}" +
    "#pp-find .ppf-bar{position:sticky;top:0;display:flex;align-items:center;gap:10px;background:#fff;color:#0A2342;border-radius:12px;padding:10px 12px;box-shadow:0 6px 18px rgba(0,0,0,.35);max-width:720px;margin:0 auto}" +
    "#pp-find input{flex:1;min-width:0;border:0;outline:0;background:none;font:700 17px var(--f-body,system-ui);color:#0A2342}" +
    "#pp-find input::-webkit-search-cancel-button{display:none}" +
    "#pp-find .ppf-x{border:0;background:none;font:800 20px/1 system-ui;color:#4A5D78;cursor:pointer;padding:2px 4px}" +
    "#pp-find .ppf-res{max-width:720px;margin:0 auto}" +
    "#pp-find .ppf-aide{color:#9FB3CB;font:500 14px/1.4 var(--f-body,system-ui);margin:18px 4px}" +
    "#pp-find .ppf-g{margin:18px 2px 7px;font:800 13px var(--f-display,system-ui);letter-spacing:1.2px;color:var(--or,#FFB81C);text-transform:uppercase}" +
    "#pp-find .ppf-it{display:flex;gap:10px;align-items:flex-start;background:rgba(255,255,255,.07);border-radius:10px;padding:10px;margin-bottom:7px;color:inherit;text-decoration:none;box-shadow:inset 0 0 0 1px rgba(255,255,255,.08)}" +
    "#pp-find .ppf-tu{flex:none;width:38px;height:38px;border-radius:7px;display:flex;align-items:center;justify-content:center;box-shadow:inset 0 -6px 0 rgba(0,0,0,.25)}#pp-find .ppf-tu b{font:800 13px var(--f-display,system-ui);color:#fff;margin-top:-4px}" +
    "#pp-find .ppf-ic{flex:none;width:38px;height:38px;border-radius:7px;background:rgba(0,0,0,.25);display:flex;align-items:center;justify-content:center;font-size:20px}#pp-find .ppf-ic svg{width:34px;height:34px}" +
    "#pp-find .ppf-tx{min-width:0;flex:1}#pp-find .ppf-n{font:700 15.5px var(--f-body,system-ui);color:#fff;text-decoration:none}" +
    "#pp-find .ppf-tx small{display:block;font:500 12px var(--f-body,system-ui);color:#9FB3CB;margin-top:2px}#pp-find i{font-style:normal;color:var(--or-txt,#FFB81C);font-weight:700}" +
    "#pp-find .ppf-ch{display:flex;flex-wrap:wrap;gap:5px;margin-top:7px}" +
    "#pp-find .ppf-p{background:rgba(0,0,0,.25);border:1px solid rgba(255,255,255,.14);border-radius:12px;padding:4px 8px;font:700 11.5px var(--f-body,system-ui);color:#DCE6F2;text-decoration:none}#pp-find .ppf-p small{display:inline;color:#9FB3CB;font-weight:500;margin:0}" +
    "nav.menu{display:none!important} nav.tabs{display:none!important}" +
    "#temoins{bottom:calc(80px + env(safe-area-inset-bottom,0px))!important;padding-bottom:12px!important}.pt-attente{bottom:calc(116px + env(safe-area-inset-bottom,0px))!important}" +
    "body{padding-bottom:calc(90px + env(safe-area-inset-bottom,0px))}" +
    ".ppn-chips{display:flex;gap:7px;overflow-x:auto;scrollbar-width:none;padding:9px 2px 8px;margin:4px 0 6px;position:sticky;top:env(safe-area-inset-top,0px);z-index:6;background:var(--bg)}" +
    ".ppn-chips::-webkit-scrollbar{display:none}" +
    ".ppn-chips a{flex:none;border:1px solid var(--line);border-radius:16px;padding:6px 12px;font:600 14px/1 var(--f-body);color:var(--ink);text-decoration:none;background:var(--surface)}" +
    ".ppn-chips a[aria-current]{background:var(--or,#FFB81C);border-color:var(--or,#FFB81C);color:var(--sur-or,#0B1220);font-weight:800}" +
    /* Le sous-menu de chaque famille, la 2e couche (Mitch, 11 nov. 2026, maquette « Grille » approuvée) : toutes les
       sections de la famille visibles d'un coup, en boutons texte de même largeur (rien à glisser), le vrai nom de la stat
       (l'acronyme PB) en petit dessous ; celle où on est est jaune. 4 par rangée au max, 3 quand il y en a 6. L'accueil garde ses pastilles. */
    "section[role=tabpanel]{scroll-margin-top:var(--ppn-h,96px)}" +
    ".ppn-chips[hidden]{display:none!important}.ppn-chips.ppn-g{display:grid;gap:6px;overflow:visible;padding:8px 2px}" +
    ".ppn-g a{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;min-height:42px;padding:5px 4px;border-radius:10px;text-align:center;" +
      "background:var(--surface);border:1px solid rgba(255,255,255,.13);color:var(--ink);font:700 12.5px/1.1 var(--f-body);min-width:0}" +
    ".ppn-g a b{font-weight:inherit;max-width:100%;overflow-wrap:anywhere;font-size:12px;line-height:1.1}" +     /* les noms longs (PB Goalie Confidence %) passent sur 2 lignes */
    ".ppn-g a small{font:800 9.5px/1 var(--f-body);color:var(--or-txt,#FFB81C);letter-spacing:.04em}" +
    ".ppn-g a[aria-current]{background:var(--or,#FFB81C);border-color:var(--or,#FFB81C);color:var(--sur-or,#0B1220);font-weight:800}.ppn-g a[aria-current] small{color:var(--sur-or,#0B1220)}" +
    /* La capsule flottante (Mitch, 14 nov. 2026, maquette C) : des icônes au trait ; le bouton où on est devient une
       pilule jaune avec son nom court ; les autres, l'icône seule. Le fond suit le thème de l'équipe choisie (--bande). */
    ".ppn-bas{position:fixed;left:12px;right:12px;bottom:calc(10px + env(safe-area-inset-bottom,0px));z-index:53;display:flex;align-items:center;justify-content:space-between;" +
      "height:60px;padding:0 8px;border-radius:30px;background:var(--bande,#0A2342);box-shadow:0 10px 28px rgba(0,0,0,.5),inset 0 0 0 1px rgba(255,255,255,.1)}" +
    /* Chaque bouton a son nom sous l'icône (Mitch, 20 nov. 2026 : « faut comme deviner c'est quoi ») */
    ".ppn-bas a,.ppn-bas button{flex:0 0 auto;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;height:50px;min-width:50px;padding:0 7px;border-radius:16px;" +
      "font:700 10.5px/1 var(--f-body);letter-spacing:.02em;color:#C9D6EE;text-decoration:none;background:none;border:0;cursor:pointer;white-space:nowrap;-webkit-tap-highlight-color:transparent}" +
    ".ppn-bas i{font-style:normal;display:flex}.ppn-bas i svg{display:block;width:24px;height:24px}" +
    ".ppn-bas b{font-weight:inherit}.ppn-bas .l{display:none}" +
    ".ppn-bas [aria-current]{background:var(--or,#FFB81C);color:var(--sur-or,#0B1220);padding:0 9px}" +
    /* 6 boutons depuis Tools (Mitch, 14 nov. 2026) : sur un cell étroit, plus serrés pour que « Tout » rentre */
    "@media (max-width:430px){.ppn-bas{padding:0 4px;left:8px;right:8px}.ppn-bas a,.ppn-bas button{min-width:44px;padding:0 4px;gap:3px;font-size:10px}.ppn-bas [aria-current]{padding:0 7px}.ppn-bas i svg{width:22px;height:22px}}" +
    ".ppn-tuiles a i svg{display:block;width:48px;height:48px;margin:0 auto}[aria-current] svg .an{stroke:var(--or-txt,#FFB81C)}" +
    /* Tiroir « Tout » (52) et son voile (51) au-dessus de la bannière des témoins (50) ; la barre (53) reste cliquable pour le refermer */
    ".ppn-voile{position:fixed;inset:0;z-index:51;background:rgba(0,0,0,.6)}" +
    ".ppn-tiroir{position:fixed;left:0;right:0;bottom:0;top:max(48px,env(safe-area-inset-top,0px));z-index:52;background:var(--bande,#0A2342);border-radius:18px 18px 0 0;border-top:2px solid var(--or,#FFB81C);overflow-y:auto;padding:8px 14px calc(86px + env(safe-area-inset-bottom,0px))}" +
    ".ppn-fav{display:flex;align-items:center;justify-content:space-between;gap:10px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:9px;padding:8px 10px;color:#C9D6EE;font:500 13px var(--f-body)}" +
    ".ppn-fav select{background:#0B1220;color:#fff;border:1px solid var(--or,#FFB81C);border-radius:7px;padding:6px 8px;font:700 14px var(--f-body)}" +
    ".ppn-tiroir .poi{width:44px;height:5px;border-radius:3px;background:rgba(255,255,255,.25);margin:0 auto 4px}" +
    ".ppn-tiroir h3{font:italic 800 15px var(--f-display);color:var(--or-txt,#FFB81C);text-transform:uppercase;margin:12px 2px 7px;letter-spacing:.02em}" +
    ".ppn-tuiles{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;max-width:640px}" +
    ".ppn-tuiles a{display:flex;flex-direction:column;align-items:center;gap:3px;text-align:center;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:9px;padding:10px 6px;color:#fff;text-decoration:none;font:700 13.5px/1.15 var(--f-body)}" +
    ".ppn-tuiles a i{font-style:normal;font-size:21px}.ppn-tuiles a small{font:500 11px var(--f-body);color:#9FB3CB}" +
    ".ppn-tuiles a[aria-current]{border-color:var(--or,#FFB81C);color:var(--or-txt,#FFB81C)}" +
    "@media (min-width:900px){.ppn-tiroir{left:50%;right:auto;width:680px;transform:translateX(-50%)}.ppn-tuiles{grid-template-columns:repeat(4,minmax(0,1fr))}}" +
    /* Ordi (Mitch, 12 nov. 2026, maquette approuvée) : le menu du bas devient une barre en haut (icône + nom sur une ligne,
       soulignée en jaune là où on est), les sections de la famille en rangée de pastilles, le tiroir « Tout » descend d'en haut.
       Le cell (moins de 1024 px) ne change pas. */
    "@media (min-width:1024px){" +
      "body{padding-bottom:0!important;padding-top:58px}" +
      ".ppn-bas{left:0;right:0;top:0;bottom:auto;justify-content:center;gap:4px;border-radius:0;border-bottom:2px solid var(--or,#FFB81C);padding:0 16px;height:56px;align-items:stretch;box-shadow:0 4px 18px rgba(0,0,0,.35)}" +
      ".ppn-bas a,.ppn-bas button{flex-direction:row;height:auto;gap:9px;font:700 14.5px/1 var(--f-body);padding:0 18px;border-radius:0;color:#9FB3CB;border-bottom:3px solid transparent;margin-bottom:-2px}" +
      ".ppn-bas i svg{width:22px;height:22px}.ppn-bas .c{display:none!important}.ppn-bas .l{display:inline!important}" +
      ".ppn-bas a:hover,.ppn-bas button:hover{color:#fff;background:rgba(255,255,255,.05)}" +
      ".ppn-bas [aria-current]{background:none;color:var(--or-txt,#FFB81C);padding:0 18px;border-bottom-color:var(--or,#FFB81C)}" +
      ".ppn-chips{top:56px}" +
      ".ppn-chips.ppn-g{display:flex;flex-wrap:wrap;gap:6px;padding:10px 2px}" +
      ".ppn-g a{flex:none;flex-direction:row;gap:7px;min-height:36px;padding:6px 16px;border-radius:18px}" +
      ".ppn-g a b{font-size:13.5px}" +
      "#temoins{bottom:16px!important}.pt-attente{bottom:24px!important}" +
      ".ppn-tiroir{top:64px;bottom:auto;max-height:calc(100vh - 80px);border-radius:14px;border:2px solid var(--or,#FFB81C);padding-bottom:18px}" +
      "section[role=tabpanel]{scroll-margin-top:calc(var(--ppn-h,96px) + 56px)}" +
    "}";
  document.head.appendChild(css);
  var chips = document.createElement("nav"); chips.className = "ppn-chips"; chips.setAttribute("aria-label", FR ? "Sections" : "Sections");
  var bas = document.createElement("nav"); bas.className = "ppn-bas"; bas.setAttribute("aria-label", FR ? "Menu" : "Menu");
  // La page d'accueil (racine ou fr/) garde ses pastilles simples ; partout ailleurs, la grille de boutons
  var accueil = !app && /^(fr\/)?(index\.html)?$/.test(location.pathname.slice(racine.length));
  function rendre(){
    var id = courant(), fam = id ? famDe(id) : "soir";
    if (id && fam !== "plus") memo(fam, id);
    var items = dispo.filter(function(x){ return x[0] === fam; });
    chips.className = "ppn-chips" + (accueil ? "" : " ppn-g");
    // 5 : 3 + 2 (« Transactions » ne tient pas dans un 5e de cell) ; 4 : 2 + 2 (ni dans un 4e : League news depuis le
    // retrait de Season Probs Finder, 20 nov. 2026)
    var n = items.length, col = n <= 3 ? n : n === 4 ? 2 : n === 5 || n === 6 ? 3 : 4;
    chips.style.gridTemplateColumns = accueil ? "" : "repeat(" + col + ",minmax(0,1fr))";
    chips.innerHTML = fam === "plus" ? "" : items.map(function(x){
      var cur = x[1] === id ? ' aria-current="page"' : "";
      if (accueil) return '<a href="' + lien(x) + '"' + cur + ">" + x[K + 3][0] + "</a>";
      // Le nom complet de la section, sur 2 lignes au besoin (Mitch, 20 nov. 2026 : « partout où y'a Power, écris
      // Power ranking au complet » : plus de court nom « Power »)
      var nom = x[K + 3][0];
      return '<a href="' + lien(x) + '"' + cur + "><b>" + nom + "</b>" + (PB[x[1]] ? "<small>" + PB[x[1]] + "</small>" : "") + "</a>"; }).join("");
    // L'accueil n'a plus la rangée de pastilles sous l'en-tête (Mitch, 12 nov. 2026 : « enlève juste ça ») : ses tuiles suffisent
    chips.hidden = accueil || fam === "plus" || items.length < 2;
    bas.innerHTML = F.filter(function(f){ return f[0] !== "plus"; }).map(function(f){
      var der = lu(f[0]), x = dispo.filter(function(y){ return y[0] === f[0] && y[1] === der; })[0] || dispo.filter(function(y){ return y[0] === f[0]; })[0];
      return '<a href="' + (x ? lien(x) : racine) + '"' + (f[0] === fam && id ? ' aria-current="page"' : "") + ' aria-label="' + f[1][K] + '"><i>' + f[2] + '</i><b class="c">' + f[3][K] + '</b><b class="l">' + f[1][K] + "</b></a>"; }).join("")
      + '<button type="button" class="ppn-tout"' + (fam === "plus" ? ' aria-current="page"' : "") + ' aria-label="' + (FR ? "Tout" : "All") + '"><i><svg viewBox=\"0 0 24 24\" aria-hidden=\"true\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.1\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><rect x=\"4\" y=\"4\" width=\"6.5\" height=\"6.5\" rx=\"1.6\"/><rect x=\"13.5\" y=\"4\" width=\"6.5\" height=\"6.5\" rx=\"1.6\"/><rect x=\"4\" y=\"13.5\" width=\"6.5\" height=\"6.5\" rx=\"1.6\"/><rect x=\"13.5\" y=\"13.5\" width=\"6.5\" height=\"6.5\" rx=\"1.6\"/></svg></i><b class="c">' + (FR ? "Tout" : "All") + '</b><b class="l">' + (FR ? "Tout" : "All") + "</b></button>";
    // Une section ouverte par son adresse (#projections) ne glisse plus sous la grille collée en haut
    document.documentElement.style.setProperty("--ppn-h", (chips.hidden ? 8 : chips.offsetHeight + 10) + "px");
    var a = !accueil ? null : chips.querySelector("[aria-current]"); if (a && a.scrollIntoView) a.scrollIntoView({ block: "nearest", inline: "center" });
  }
  // Mon équipe (demande de Mitch, 10 nov. 2026) : choisie dans « Tout », gardée sur cet appareil ; ses joueurs et son
  // équipe sont encadrés en jaune avec une étoile dans toutes les listes (les lignes portent data-c = l'équipe)
  var EQS = ["ANA","BOS","BUF","CAR","CBJ","CGY","CHI","COL","DAL","DET","EDM","FLA","LAK","MIN","MTL","NJD","NSH","NYI","NYR","OTT","PHI","PIT","SEA","SJS","STL","TBL","TOR","UTA","VAN","VGK","WPG","WSH"];
  // Même choix que « Mon club » (club.js, bouton de l'en-tête) : une seule équipe favorite pour tout le site
  function favLire(){ try { var c = localStorage.getItem("pp_club") || ""; return c === "-" ? "" : c; } catch (e) { return ""; } }
  function favEcrire(t){ try { localStorage.setItem("pp_club", t || "-"); } catch (e) {} }
  function favAppliquer(){
    var t = favLire(), st = document.getElementById("ppn-fav");
    if (!st){ st = document.createElement("style"); st.id = "ppn-fav"; document.head.appendChild(st); }
    if (!/^[A-Z]{3}$/.test(t)){ st.textContent = ""; return; }
    var s = '[data-c="' + t + '"]';
    st.textContent = ".wi-r" + s + ",.cp" + s + ",.tr" + s + "{box-shadow:inset 0 0 0 2px var(--or,#FFB81C),0 0 14px rgba(255,184,28,.25)!important}" +
      ".wi-r" + s + " .nm::before,.cp" + s + " .nm::before,.tr" + s + " .nm::before{content:'\\2605  ';color:var(--or-txt,#FFB81C)}";
  }
  favAppliquer();
  function tiroir(){
    var id = courant(), v = document.createElement("div"), t = document.createElement("div");
    v.className = "ppn-voile"; t.className = "ppn-tiroir"; t.setAttribute("role", "dialog"); t.setAttribute("aria-label", FR ? "Toutes les sections" : "All sections");
    var fav = favLire();
    t.innerHTML = '<div class="poi"></div><h3>' + (FR ? "Mon équipe" : "My team") + '</h3><label class="ppn-fav">' +
      '<span>' + (FR ? "Ses joueurs ressortent dans toutes les listes" : "Its players stand out in every list") + '</span><select>' +
      '<option value="">' + (FR ? "Aucune" : "None") + "</option>" + EQS.map(function(e){ return '<option value="' + e + '"' + (e === fav ? " selected" : "") + ">" + e + "</option>"; }).join("") +
      "</select></label>" + F.map(function(f){
      var L = dispo.filter(function(x){ return x[0] === f[0]; });
      if (!L.length) return "";
      return "<h3>" + f[1][K] + '</h3><div class="ppn-tuiles">' + L.map(function(x){
        return '<a href="' + lien(x) + '"' + (x[1] === id ? ' aria-current="page"' : "") + "><i>" + x[5] + "</i>" + x[K + 3][0] + (x[6][K] ? "<small>" + x[6][K] + "</small>" : "") + "</a>"; }).join("") + "</div>";
    }).join("");
    var fermer = function(){ v.remove(); t.remove(); document.removeEventListener("keydown", esc); rendre(); };
    var esc = function(e){ if (e.key === "Escape") fermer(); };
    v.addEventListener("click", fermer); t.addEventListener("click", function(e){ if (e.target.closest("a")) setTimeout(fermer, 0); });
    t.querySelector(".ppn-fav select").addEventListener("change", function(e){ favEcrire(e.target.value); favAppliquer(); if (window.ppClub) setTimeout(function(){ location.reload(); }, 150); });
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
    // La grille change de hauteur toute seule (rotation de l'écran, polices chargées après coup) : --ppn-h suit, pour
    // que les menus de section collés juste dessous (docs/carte.css, .ctrls.c3) ne glissent pas en dessous d'elle
    if (window.ResizeObserver) new ResizeObserver(function(){
      document.documentElement.style.setProperty("--ppn-h", (chips.hidden ? 8 : chips.offsetHeight + 10) + "px"); }).observe(chips);
    var tabs = document.querySelector("nav.tabs");
    if (tabs && window.MutationObserver) new MutationObserver(function(){ rendre(); }).observe(tabs, { attributes: true, subtree: true, attributeFilter: ["aria-selected"] });
  }
  document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", poser) : poser();

  // ---- Le finder (Mitch, 14 nov. 2026 : « un finder qui trouve absolument tout sur le site » ; maquette C : la
  // loupe dans l'en-tête, toujours là). Joueurs (avec leurs meilleurs rangs PuckProb et leur % de but ce soir),
  // équipes, coachs, sections et stats, Quoi de neuf. L'index (recherche.json, src/site_public.py) se charge
  // seulement au 1er tap sur la loupe : rien de plus à télécharger pour ceux qui ne cherchent pas.
  var IDX = null, IDXp = null, PBI = null, PBIp = null;
  var APP = FR ? "ce-soir/" : "tonight/";
  var SURNOM = { ANA: "Ducks", BOS: "Bruins", BUF: "Sabres", CGY: "Flames", CAR: "Hurricanes", CHI: "Blackhawks", COL: "Avalanche", CBJ: "Blue Jackets",
    DAL: "Stars", DET: "Red Wings", EDM: "Oilers", FLA: "Panthers", LAK: "Kings", MIN: "Wild", MTL: "Canadiens", NSH: "Predators", NJD: "Devils",
    NYI: "Islanders", NYR: "Rangers", OTT: "Senators", PHI: "Flyers", PIT: "Penguins", SJS: "Sharks", SEA: "Kraken", STL: "Blues", TBL: "Lightning",
    TOR: "Maple Leafs", UTA: "Mammoth", VAN: "Canucks", VGK: "Golden Knights", WSH: "Capitals", WPG: "Jets" };
  // « Canadiens de Montréal » / « Montreal Canadiens »
  function nomEq(x){ var s_ = SURNOM[x[0]]; if (!s_) return FR ? x[1] : x[2]; return FR ? s_ + (x[1] === "Utah" ? " de l'Utah" : " de " + x[1]) : x[2] + " " + s_; }
  function slug(n){ return nrmQ(n).replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, ""); }
  // Tous les joueurs de l'histoire (le même index que PB Stats) : chargé au 1er tap, en même temps que recherche.json
  function chargerPbi(){
    return PBIp || (PBIp = fetch(racine + "pbstats/index.json").then(function(r){ return r.ok ? r.json() : null; })
      .then(function(d){ PBI = d; return d; }).catch(function(){ PBIp = null; return null; }));
  }
  function chargerIdx(){
    return IDXp || (IDXp = fetch(racine + "recherche.json", { cache: "no-cache" }).then(function(r){ return r.ok ? r.json() : null; })
      .then(function(d){ IDX = d; return d; }).catch(function(){ IDXp = null; return null; }));
  }
  function nrmQ(t){ return String(t || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim(); }
  function esc(t){ return String(t == null ? "" : t).replace(/[&<>"]/g, function(c){ return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function vaA(h){ return racine + (FR ? "fr/" : "") + h; }
  // Un joueur ou une équipe touché n'importe où sur le site -> sa fenêtre (Mitch, 20 nov. 2026 : « partout partout
  // partout, on clique sur un joueur ou une équipe, c'est les nouvelles pages »). Les liens gardent leur adresse vers
  // les vieilles pages texte (players/<nom>/, teams/<équipe>/) : Google les suit encore ; seul le clic d'une personne
  // est détourné. Dans l'application : la fenêtre s'ouvre sur place ; ailleurs : on va à l'application, fenêtre ouverte.
  // Un joueur a besoin de son numéro (data-pid sur le lien ou sur sa rangée) ; sans numéro, le lien fait comme avant.
  document.addEventListener("click", function(ev){
    if (ev.defaultPrevented || ev.button || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;
    var a = ev.target.closest && ev.target.closest("a[href]"); if (!a || a.target === "_blank") return;
    var h = a.getAttribute("href") || "";
    var mj = /(?:^|\/)(?:players|joueurs)\/([a-z0-9-]+)\/?$/i.exec(h), me = /(?:^|\/)(?:teams|equipes)\/([a-z]{3})\/?$/i.exec(h);
    var pid = mj ? (a.getAttribute("data-pid") || (a.closest("[data-pid]") || { getAttribute: function(){ return ""; } }).getAttribute("data-pid") || "") : "";
    pid = String(pid).replace(/[^0-9]/g, "");
    if (!(mj && pid) && !me) return;
    ev.preventDefault(); ev.stopPropagation();
    if (mj && typeof window.ouvrirJoueur === "function"){ window.ouvrirJoueur(pid); return; }
    if (me && typeof window.ouvrirEquipe === "function"){ window.ouvrirEquipe(me[1].toUpperCase()); return; }
    location.href = vaA(APP + "#" + (mj ? (FR ? "joueur/" : "player/") + mj[1] + "-" + pid : (FR ? "equipe/" : "team/") + me[1].toLowerCase()));
  }, true);
  // Un mot cherché colle si un mot du nom commence par lui (« suz » -> Suzuki), ou le nom au complet le contient
  function colle(nom, q){
    var n = nrmQ(nom); if (!q) return 0;
    if (n === q) return 3;
    if (n.split(/[\s\-'.]+/).some(function(w){ return w.indexOf(q) === 0; })) return 2;
    return n.indexOf(q) >= 0 ? 1 : 0;
  }
  function tuileEq(t){ return '<span class="ppf-tu" style="background:' + esc(((IDX && IDX.k) || {})[t] || "#13335E") + '"><b>' + esc(t || "") + "</b></span>"; }
  function pct(p){ var v = Math.round(p * 1000) / 10; return (FR ? String(v).replace(".", ",") + " %" : v + "%"); }
  function chercher(q, box){
    q = nrmQ(q);
    if (q.length < 2){ box.innerHTML = '<p class="ppf-aide">' + (FR ? "Un joueur (toute l'histoire), une équipe, un coach…" : "A player (all-time), a team, a coach…") + "</p>"; return; }
    if (!IDX){ box.innerHTML = '<p class="ppf-aide">' + (FR ? "Chargement…" : "Loading…") + "</p>"; chargerIdx().then(function(){ chercher(q, box); }); return; }
    // Le Finder sert à une seule chose (Mitch, 20 nov. 2026 : « que ça soit pour trouver les pages de joueur, d'équipe
    // ou de coach, juste ça ») : un nom -> sa page (la fenêtre joueur ou équipe de l'application). Les joueurs : toute
    // l'histoire (pbstats/index.json), les actifs d'abord ; les équipes et les coachs : recherche.json.
    if (!PBI){ chargerPbi().then(function(){ chercher(q, box); }); }
    var groupes = [], an = new Date().getFullYear() - 1;
    var J = [].concat((PBI && PBI.j || []).map(function(r){ return { id: r[0], n: r[1], pos: r[2], t: r[3], a0: r[4], a1: r[5], v: r[6] }; }),
                      (PBI && PBI.g || []).map(function(r){ return { id: r[0], n: r[1], pos: "G", t: r[2], a0: r[3], a1: r[4], v: r[5] }; }))
      .map(function(x){ return [colle(x.n, q), x]; }).filter(function(t){ return t[0]; })
      .sort(function(a, b){ return b[0] - a[0] || ((b[1].a1 >= an) - (a[1].a1 >= an)) || (b[1].v - a[1].v); }).slice(0, 10);
    if (J.length) groupes.push([FR ? "Joueurs" : "Players", J.map(function(t){ var x = t[1];
      return '<a class="ppf-it" href="' + vaA(APP + "#" + (FR ? "joueur/" : "player/") + slug(x.n) + "-" + x.id) + '">' + tuileEq(x.t) + '<div class="ppf-tx"><b class="ppf-n">' + esc(x.n) + "</b><small>"
        + esc([x.t, x.pos, x.a1 >= an ? (FR ? "actif" : "active") : x.a0 + "–" + (x.a1 + 1)].filter(Boolean).join(" · ")) + "</small></div></a>"; }).join("")]);
    var E = (IDX.e || []).filter(function(x){ return nrmQ(x[0]) === q || colle(x[1], q) || colle(x[2], q) || colle(SURNOM[x[0]] || "", q); }).slice(0, 4);
    if (E.length) groupes.push([FR ? "Équipes" : "Teams", E.map(function(x){
      return '<a class="ppf-it" href="' + vaA(APP + "#" + (FR ? "equipe/" : "team/") + x[0].toLowerCase()) + '">' + tuileEq(x[0]) + '<div class="ppf-tx"><b class="ppf-n">' + esc(nomEq(x)) + "</b><small>" + esc(x[0]) + "</small></div></a>"; }).join("")]);
    var C = (IDX.c || []).filter(function(x){ return colle(x[0], q); }).slice(0, 4);
    if (C.length) groupes.push([FR ? "Coachs" : "Coaches", C.map(function(x){
      return '<a class="ppf-it" href="' + vaA(APP + "#" + (FR ? "equipe/" : "team/") + String(x[1] || "").toLowerCase() + "/coach") + '">' + tuileEq(x[1]) + '<div class="ppf-tx"><b class="ppf-n">' + esc(x[0]) + "</b><small>" + esc((FR ? "Coach · " : "Coach · ") + (x[1] || "")) + "</small></div></a>"; }).join("")]);
    box.innerHTML = groupes.length ? groupes.map(function(g){ return '<div class="ppf-g">' + g[0] + "</div>" + g[1]; }).join("")
      : '<p class="ppf-aide">' + (FR ? "Rien trouvé pour « " + esc(q) + " »." : "Nothing found for \u201c" + esc(q) + "\u201d.") + "</p>";
  }
  function ouvrirFinder(){
    if (document.getElementById("pp-find")) return;
    chargerIdx(); chargerPbi();
    var o = document.createElement("div");
    o.id = "pp-find"; o.setAttribute("role", "dialog"); o.setAttribute("aria-modal", "true");
    o.innerHTML = '<div class="ppf-bar"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.2"/><path d="M15.2 15.2L20 20"/></svg>'
      + '<input type="search" autocomplete="off" enterkeyhint="search" placeholder="' + (FR ? "Joueur, équipe, coach…" : "Player, team, coach…") + '">'
      + '<button type="button" class="ppf-x" aria-label="' + (FR ? "Fermer" : "Close") + '">✕</button></div><div class="ppf-res"></div>';
    var inp = o.querySelector("input"), box = o.querySelector(".ppf-res");
    var fermer = function(){ o.remove(); document.documentElement.classList.remove("ppf-ouvert"); document.removeEventListener("keydown", escF); };
    var escF = function(e){ if (e.key === "Escape") fermer(); };
    inp.addEventListener("input", function(){ chercher(inp.value, box); });
    o.querySelector(".ppf-x").addEventListener("click", fermer);
    o.addEventListener("click", function(e){ if (e.target.closest("a")) setTimeout(fermer, 0); });   // un lien vers un onglet de la même page : on ferme
    document.addEventListener("keydown", escF);
    document.body.appendChild(o); document.documentElement.classList.add("ppf-ouvert");
    chercher("", box); setTimeout(function(){ inp.focus(); }, 30);
  }
  window.ppFinder = ouvrirFinder;
  function poserLoupe(){
    var h = document.querySelector("header.bug");
    var b = document.createElement("button");
    b.type = "button"; b.className = "ppf-loupe"; b.setAttribute("aria-label", FR ? "Chercher sur le site" : "Search the site");
    b.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.2"/><path d="M15.2 15.2L20 20"/></svg>';
    b.addEventListener("click", ouvrirFinder);
    if (h){ h.classList.add("ppf-h"); h.appendChild(b); } else { b.classList.add("ppf-flot"); document.body.appendChild(b); }
  }
  document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", poserLoupe) : poserLoupe();
})();

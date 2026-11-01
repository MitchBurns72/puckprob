// PuckProb (site public) : bannière de consentement (Loi 25 du Québec) + chargement des pubs Google AdSense.
//
// Règles :
//  - Rien ne se charge tant que le numéro AdSense est vide (data-client="") : site sans pub, sans bannière.
//  - Avec un numéro : la bannière demande la permission. Aucun script publicitaire n'est chargé avant « Accepter ».
//    « Refuser » = aucune pub du tout (rien n'est déposé dans le navigateur à part le choix lui-même).
//  - Le choix est gardé sur l'appareil ; le lien « Témoins / Cookie settings » en bas de page permet de le changer.
(function () {
  const moi = document.currentScript;
  const client = (moi && moi.dataset.client || "").trim();
  if (!client) return;                                  // pas encore de compte AdSense : on ne fait rien
  const EN = (document.documentElement.lang || "").startsWith("en");
  const T = EN ? {
    titre: "Ads and cookies",
    texte: "PuckProb is free. With your permission, Google will show ads and use cookies to choose and measure them (data processed outside Quebec, including in the United States). Refuse = no ads at all.",
    oui: "Accept", non: "Refuse", plus: "Privacy policy", lienPol: "privacy/", gerer: "Cookie settings",
  } : {
    titre: "Publicité et témoins",
    texte: "PuckProb est gratuit. Avec ta permission, Google affiche des pubs et utilise des témoins (cookies) pour les choisir et les mesurer (données traitées hors Québec, notamment aux États-Unis). Refuser = aucune pub.",
    oui: "Accepter", non: "Refuser", plus: "Politique de confidentialité", lienPol: "confidentialite/", gerer: "Témoins (cookies)",
  };
  const CLE = "puckprob-consentement";
  const lire = () => { try { return localStorage.getItem(CLE); } catch (e) { return null; } };
  const ecrire = (v) => { try { localStorage.setItem(CLE, v); } catch (e) {} };
  // Racine du site de la langue courante (les pages texte sont à 1 ou 2 niveaux de profondeur)
  const racine = (moi.getAttribute("src") || "pub.js").replace(/pub\.js.*$/, "");

  function chargerPubs() {
    if (document.querySelector("script[data-adsense]")) return;
    const s = document.createElement("script");
    s.async = true;
    s.crossOrigin = "anonymous";
    s.dataset.adsense = "1";
    s.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=" + encodeURIComponent(client);
    document.head.appendChild(s);
  }

  function banniere() {
    if (document.getElementById("temoins")) return;
    const b = document.createElement("div");
    b.id = "temoins";
    b.setAttribute("role", "dialog");
    b.setAttribute("aria-label", T.titre);
    b.innerHTML = `<div class="tm-box"><b>${T.titre}</b><p>${T.texte} <a href="${racine}${T.lienPol}">${T.plus}</a></p>
      <div class="tm-b"><button type="button" data-v="non">${T.non}</button><button type="button" data-v="oui" class="tm-oui">${T.oui}</button></div></div>`;
    b.addEventListener("click", (e) => {
      const v = e.target.closest("button")?.dataset.v;
      if (!v) return;
      const avant = lire();
      ecrire(v);
      b.remove();
      if (v === "oui") chargerPubs();
      else if (avant === "oui") location.reload();      // retrait du consentement : on recharge sans pub
    });
    document.body.appendChild(b);
  }

  // Style de la bannière (mêmes couleurs que le site, en bas de l'écran)
  const st = document.createElement("style");
  st.textContent = `#temoins{position:fixed;left:0;right:0;bottom:0;z-index:50;padding:10px max(12px,env(safe-area-inset-left,0px)) max(12px,env(safe-area-inset-bottom,0px))}
  #temoins .tm-box{max-width:720px;margin:0 auto;background:#0A2342;color:#fff;border-radius:8px;padding:12px 14px;box-shadow:0 8px 30px rgba(0,0,0,.45);border-top:3px solid #FFB81C;font:14px/1.45 "Barlow",system-ui,sans-serif}
  #temoins b{font:italic 800 17px/1 "Barlow Condensed","Arial Narrow",sans-serif;text-transform:uppercase;letter-spacing:.03em}
  #temoins p{margin:6px 0 10px;color:#D5E0EC} #temoins a{color:#FFB81C}
  #temoins .tm-b{display:flex;gap:8px;justify-content:flex-end}
  #temoins button{font:italic 800 16px/1 "Barlow Condensed","Arial Narrow",sans-serif;text-transform:uppercase;padding:10px 16px;border-radius:4px;border:2px solid rgba(255,255,255,.4);background:transparent;color:#fff;cursor:pointer}
  #temoins button.tm-oui{background:#D3202B;border-color:#D3202B}
  .lien-temoins{background:none;border:0;padding:0;color:inherit;text-decoration:underline;cursor:pointer;font:inherit}`;
  document.head.appendChild(st);

  // Lien « gérer les témoins » ajouté au pied de page (retirer ou donner son consentement en tout temps)
  function lienPied() {
    const pied = document.querySelector("footer.pied, .pied");
    if (!pied || pied.querySelector(".lien-temoins")) return;
    const l = document.createElement("button");
    l.type = "button";
    l.className = "lien-temoins";
    l.textContent = T.gerer;
    l.addEventListener("click", banniere);
    pied.appendChild(document.createTextNode(" · "));
    pied.appendChild(l);
  }

  function demarrer() {
    lienPied();
    // Le pied de page de l'application est ajouté par son code : on réessaie un peu plus tard
    setTimeout(lienPied, 1500);
    const c = lire();
    if (c === "oui") chargerPubs();
    else if (c !== "non") banniere();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", demarrer);
  else demarrer();
})();

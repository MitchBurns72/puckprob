// Le check automatique du site (Mitch, 27 nov. 2026 : « je te fais confiance ») : après chaque publication du calcul,
// un navigateur ouvre puckprob.ca en anglais et en français, touche chaque section et les fenêtres principales, et
// note chaque erreur JavaScript et chaque fichier de données qui ne se charge pas. Une erreur = le check échoue (X
// rouge dans Actions) et le résumé dit où. Les pubs, les images et les logos manquants ne comptent pas.
import { chromium } from "playwright";
import fs from "node:fs";

const BASE = process.env.SITE || "https://puckprob.ca";
const PAGES = [["EN", BASE + "/tonight/"], ["FR", BASE + "/fr/ce-soir/"]];
const BRUIT = /adsbygoogle|googlesyndication|doubleclick|google-analytics|gtag|fundingchoices|ResizeObserver loop|Failed to load resource/i;
const erreurs = [], faits = [];
const pause = (ms) => new Promise(r => setTimeout(r, ms));

async function verifier(lang, url){
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 420, height: 900 } });
  let etape = "chargement";
  const note = (quoi) => erreurs.push(`${lang} · ${etape} · ${String(quoi).slice(0, 300)}`);
  p.on("pageerror", e => note(e.message));
  p.on("console", m => { if (m.type() === "error" && !BRUIT.test(m.text())) note(m.text()); });
  p.on("response", r => { const u = r.url(); if (u.startsWith(BASE) && /\.json(\?|$)/.test(u) && r.status() >= 400 && !/live\.json/.test(u)) note(`${r.status()} ${u}`); });
  const pas = async (nom, fn) => { etape = nom; try { await fn(); faits.push(`${lang} · ${nom}`); } catch (e) { note(e.message); } };
  await pas("chargement", async () => { await p.goto(url, { waitUntil: "networkidle", timeout: 60000 }); await pause(3000); });
  // Chaque section (les onglets de l'application)
  const onglets = await p.$$eval('nav.tabs button[role="tab"]', x => x.map(b => b.id).filter(Boolean));
  for (const id of onglets){
    await pas(`section ${id}`, async () => { await p.evaluate(i => document.getElementById(i)?.click(), id); await pause(1800); });
  }
  // Un match : la fenêtre du match (Gameday Probs et la bande des pointages)
  await pas("fenêtre de match", async () => {
    await p.evaluate(() => document.getElementById("t-matchs")?.click()); await pause(1000);
    const ok = await p.evaluate(() => { const c = document.querySelector("#slate .sb, #matchs .mc[data-g]"); if (!c) return "aucun match"; c.click(); return ""; });
    await pause(1500);
    if (!ok && !(await p.$("#wi-modal .mpop"))) throw new Error("la fenêtre du match ne s'ouvre pas");
    await p.evaluate(() => { const m = document.getElementById("wi-modal"); if (m) m.hidden = true; });
  });
  // Un joueur, un gardien, une équipe, un club disparu : chaque onglet de leur fenêtre
  const fenetre = async (nom, ouvrir) => pas(nom, async () => {
    await p.evaluate(ouvrir); await pause(3500);
    const tabs = await p.$$eval("#fenetre .fen-ongl button", x => x.map(b => b.dataset.fo));
    if (!tabs.length) throw new Error("la fenêtre ne s'ouvre pas");
    for (const o of tabs){ etape = `${nom} · ${o}`; await p.evaluate(k => document.querySelector(`#fenetre .fen-ongl [data-fo="${k}"]`)?.click(), o); await pause(1500); }
    await p.evaluate(() => document.querySelector("#fenetre .fen-ret")?.click()); await pause(800);
  });
  await fenetre("fenêtre joueur", () => window.ouvrirJoueur?.("8478402"));          // Connor McDavid
  await fenetre("fenêtre gardien", () => window.ouvrirJoueur?.("8478048"));          // Igor Shesterkin
  await fenetre("fenêtre équipe", () => window.ouvrirEquipe?.("MTL"));
  await fenetre("club disparu", () => window.ouvrirEquipe?.("QUE"));
  // P.B Stats DB : patineurs, gardiens, équipes, PB Analytics
  for (const t of ["j", "g", "e", "a"]){
    await pas(`StatsDB ${t}`, async () => {
      await p.evaluate(() => document.getElementById("t-whatif")?.click()); await pause(1500);
      await p.evaluate(k => document.querySelector(`[data-px="px_t"][data-pv="${k}"]`)?.click(), t); await pause(2500);
      if (!(await p.$("#whatif .wi-l, #whatif .card"))) throw new Error("StatsDB vide");
    });
  }
  // Le finder
  await pas("finder", async () => {
    await p.evaluate(() => window.ppFinder?.()); await pause(800);
    await p.fill("#pp-find input", "suzuki"); await pause(2500);
    if (!(await p.$("#pp-find .ppf-it"))) throw new Error("le finder ne trouve rien pour « suzuki »");
  });
  await b.close();
}

for (const [lang, url] of PAGES) await verifier(lang, url);
const resume = [`## Check du site ${new Date().toISOString().slice(0, 16)} UTC`, "",
  erreurs.length ? `**${erreurs.length} erreur(s)**` : "**Aucune erreur**", "", ...erreurs.map(e => `- ${e}`), "",
  `<details><summary>${faits.length} étapes faites</summary>\n\n${faits.map(f => `- ${f}`).join("\n")}\n</details>`].join("\n");
console.log(resume);
if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, resume + "\n");
process.exit(erreurs.length ? 1 : 0);

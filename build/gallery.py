#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generates the gallery index.html at project root (white, Apple-style)."""
import json, os, html
from build import THEMES, ROOT, CONTENT_DIR

def meta_for(theme):
    jp = os.path.join(CONTENT_DIR, theme["slug"].split("-")[0] + ".json")
    with open(jp, encoding="utf-8") as f:
        d = json.load(f)
    return d.get("lang", "cs"), len(d["slides"])

CARD = """      <a class="card" href="templates/{slug}/index.html" data-kind="{kind}" data-lang="{lang}">
        <div class="thumb">
          <img class="cover" src="gallery/shots/{nn}.png" alt="{name}" loading="lazy">
          <img class="alt" src="gallery/shots/{nn}-b.png" alt="" loading="lazy">
        </div>
        <div class="meta">
          <div class="row">
            <span class="name">{name}</span>
            <span class="dots"><i style="background:{c1}"></i><i style="background:{c2}"></i><i style="background:{c3}"></i></span>
          </div>
          <div class="subj">{subject}</div>
          <div class="tags"><span>{lang}</span><span>{kind}</span><span>{count} slides</span></div>
        </div>
      </a>"""

PAGE = """<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Prezentační šablony</title>
<meta name="description" content="{count} prezentačních šablon na jednom sdíleném HTML enginu. Ukázkový obsah.">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='13' height='13' x='2.5' y='2.5' rx='3' fill='%23ff5a1f'/%3E%3Crect width='13' height='13' x='16.5' y='2.5' rx='3' fill='%235853eb'/%3E%3Crect width='13' height='13' x='2.5' y='16.5' rx='3' fill='%230e9e8e'/%3E%3Crect width='13' height='13' x='16.5' y='16.5' rx='3' fill='%23e11d74'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#fbfbfd;--card:#ffffff;--ink:#1d1d1f;--ink2:#6e6e73;--ink3:#86868b;--line:#e6e6eb;--blue:#0071e3}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Inter","Segoe UI",Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased;line-height:1.47}
.nav{position:sticky;top:0;z-index:50;background:rgba(251,251,253,.82);backdrop-filter:saturate(180%) blur(20px);border-bottom:1px solid var(--line)}
.nav .in{max-width:1200px;margin:0 auto;padding:0 22px;height:52px;display:flex;align-items:center;justify-content:space-between}
.nav .brand{display:flex;align-items:center;gap:10px;font-weight:600;font-size:16px;letter-spacing:-.01em}
.nav .logo{display:grid;grid-template-columns:1fr 1fr;gap:2px;width:20px;height:20px}
.nav .logo i{border-radius:3px}
.nav a{color:var(--ink2);text-decoration:none;font-size:14px}
.nav a:hover{color:var(--ink)}
.wrap{max-width:1200px;margin:0 auto;padding:0 22px}
.hero{text-align:center;padding:96px 0 30px}
.hero h1{font-size:clamp(44px,7vw,88px);font-weight:800;letter-spacing:-.035em;line-height:1.04}
.hero .grad{background:linear-gradient(110deg,#ff5a1f,#e11d74 38%,#5853eb 72%,#0e9e8e);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero p{margin:22px auto 0;max-width:620px;font-size:clamp(18px,2.4vw,23px);color:var(--ink2);letter-spacing:-.01em}
.note{display:inline-flex;align-items:center;gap:8px;margin-top:26px;background:#fff5e9;color:#9a5a12;border:1px solid #f3dcc0;border-radius:999px;padding:8px 16px;font-size:13.5px}
.note b{color:#7a4408}
.stats{display:flex;justify-content:center;flex-wrap:wrap;gap:34px;margin-top:34px;color:var(--ink2);font-size:14px}
.stats b{display:block;font-size:30px;font-weight:700;color:var(--ink);letter-spacing:-.02em}
.filters{display:flex;justify-content:center;gap:8px;margin:46px 0 8px;flex-wrap:wrap}
.filters button{font:inherit;font-size:14px;color:var(--ink2);background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 16px;cursor:pointer;transition:.15s}
.filters button:hover{color:var(--ink)}
.filters button.on{background:var(--ink);color:#fff;border-color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:22px;padding:22px 0 30px}
.card{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-radius:18px;overflow:hidden;text-decoration:none;color:inherit;transition:transform .25s cubic-bezier(.2,.7,.2,1),box-shadow .25s,border-color .25s}
.card:hover{transform:translateY(-6px);box-shadow:0 18px 40px rgba(0,0,0,.10);border-color:#dadadf}
.thumb{position:relative;aspect-ratio:16/9;overflow:hidden;background:#f0f0f3}
.thumb img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity .4s ease}
.thumb .alt{opacity:0}
.card:hover .cover{opacity:0}
.card:hover .alt{opacity:1}
.meta{padding:15px 17px 17px}
.row{display:flex;align-items:center;justify-content:space-between;gap:10px}
.name{font-weight:600;font-size:18px;letter-spacing:-.01em}
.dots{display:flex;gap:5px;flex:none}
.dots i{width:13px;height:13px;border-radius:4px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.08)}
.subj{color:var(--ink2);font-size:14.5px;margin-top:3px}
.tags{display:flex;gap:6px;margin-top:13px;font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--ink3)}
.tags span{border:1px solid var(--line);border-radius:6px;padding:3px 8px}
.how{border-top:1px solid var(--line);margin-top:24px;padding:64px 0 30px;text-align:center}
.how h2{font-size:clamp(28px,4vw,40px);font-weight:700;letter-spacing:-.025em}
.how .steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px;max-width:980px;margin:40px auto 0;text-align:left}
.how .step{background:#fff;border:1px solid var(--line);border-radius:16px;padding:22px}
.how .step b{display:block;font-size:17px;margin-bottom:6px}
.how .step span{color:var(--ink2);font-size:14.5px}
.how code{font-family:ui-monospace,"SF Mono",Menlo,monospace;font-size:.85em;background:#f0f0f3;border-radius:5px;padding:2px 6px}
.how .links{display:flex;justify-content:center;flex-wrap:wrap;gap:12px;margin-top:34px}
.how .links a{color:var(--blue);text-decoration:none;font-size:15px;border:1px solid var(--line);border-radius:999px;padding:9px 18px;background:#fff}
.how .links a:hover{border-color:#cdd0d6}
footer{border-top:1px solid var(--line);padding:26px 0 50px;color:var(--ink3);font-size:12.5px;text-align:center}
@media (max-width:640px){.hero{padding:60px 0 20px}}
</style>
</head>
<body>
<div class="nav"><div class="in">
  <div class="brand"><span class="logo"><i style="background:#ff5a1f"></i><i style="background:#5853eb"></i><i style="background:#0e9e8e"></i><i style="background:#e11d74"></i></span> Prezentační šablony</div>
  <a href="#how">Jak to použít</a>
</div></div>
<div class="wrap">
  <section class="hero">
    <h1>Jedna kostra.<br><span class="grad">{count} stylů.</span></h1>
    <p>Sdílený HTML engine pro prezentace v prohlížeči. Vyberte vzhled, vyměňte obsah, máte hotovo.</p>
    <div class="note">⚠︎ <span><b>Ukázkový (dummy) obsah.</b> Jména, čísla i citace jsou smyšlené, slouží jen k předvedení stylů.</span></div>
    <div class="stats"><div><b>{count}</b>šablon</div><div><b>16</b>typů slidů</div><div><b>0</b>závislostí za běhu</div><div><b>1</b>soubor = deck</div></div>
    <div class="filters">
      <button class="on" data-f="all">Vše</button>
      <button data-f="light">Světlé</button>
      <button data-f="dark">Tmavé</button>
      <button data-f="cs">Česky</button>
      <button data-f="en">English</button>
    </div>
  </section>
  <div class="grid" id="grid">
{cards}
  </div>
  <section class="how" id="how">
    <h2>Jak z toho udělat vlastní prezentaci</h2>
    <div class="steps">
      <div class="step"><b>1 · Otevřít</b><span>Otevřete <code>templates/&lt;slug&gt;/index.html</code> v prohlížeči. Šipky listují, <b>F</b> celá obrazovka, <b>N</b> poznámky řečníka.</span></div>
      <div class="step"><b>2 · Vyměnit obsah</b><span>Upravte <code>build/content/&lt;NN&gt;.json</code> a spusťte <code>python3 build/build.py</code>. Vznikne nový samostatný HTML.</span></div>
      <div class="step"><b>3 · Změnit vzhled</b><span>Barvy a fonty jsou v <code>THEMES</code> v <code>build/build.py</code> (<code>c1/c2/c3</code>, fonty, <code>radius</code>, styl karet).</span></div>
      <div class="step"><b>4 · Jeden soubor</b><span>Výsledný <code>index.html</code> má veškerý CSS i JS uvnitř. Zkopírujte ho kamkoli, funguje offline.</span></div>
    </div>
    <div class="links"><a href="README.md">README</a><a href="GUIDE.md">Průvodce typy slidů</a><a href="https://github.com/kereptom/presentation-templates">GitHub</a></div>
  </section>
</div>
<footer>Prezentační šablony &middot; sdílený engine převzatý z reálných decků a očištěný od obsahu &middot; ukázkový obsah</footer>
<script>
const grid=document.getElementById('grid');
document.querySelectorAll('.filters button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('.filters button').forEach(x=>x.classList.remove('on'));
  b.classList.add('on');
  const f=b.dataset.f;
  grid.querySelectorAll('.card').forEach(c=>{
    const show = f==='all' || c.dataset.kind===f || c.dataset.lang===f;
    c.style.display = show ? '' : 'none';
  });
});
</script>
</body>
</html>"""

def main():
    cards = []
    for t in THEMES:
        lang, count = meta_for(t)
        cards.append(CARD.format(
            slug=t["slug"], nn=t["slug"].split("-")[0], name=html.escape(t["name"]),
            subject=html.escape(t["subject"]), c1=t["c1"], c2=t["c2"], c3=t["c3"],
            lang=lang, count=count, kind=("dark" if t.get("dark") else "light")))
    out = PAGE.replace("{cards}", "\n".join(cards)).replace("{count}", str(len(THEMES)))
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)
    print("wrote index.html with", len(cards), "cards")

if __name__ == "__main__":
    main()

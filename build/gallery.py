#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generates the gallery index.html at project root from THEMES + content."""
import json, os, html
from build import THEMES, ROOT, CONTENT_DIR

def meta_for(theme):
    jp = os.path.join(CONTENT_DIR, theme["slug"].split("-")[0] + ".json")
    with open(jp, encoding="utf-8") as f:
        d = json.load(f)
    return d.get("lang", "cs"), len(d["slides"]), d.get("title", theme["name"])

CARD = """    <a class="card{darkcls}" href="templates/{slug}/index.html">
      <div class="thumb">
        <img class="cover" src="gallery/shots/{nn}.png" alt="{name} cover" loading="lazy">
        <img class="alt" src="gallery/shots/{nn}-b.png" alt="{name} slide" loading="lazy">
        <span class="open">Otevřít &rarr;</span>
      </div>
      <div class="body">
        <div class="swatches"><i style="background:{c1}"></i><i style="background:{c2}"></i><i style="background:{c3}"></i></div>
        <div class="name">{name}</div>
        <div class="subj">{subject}</div>
        <div class="tags"><span>{lang}</span><span>{count} slidů</span><span>{kind}</span></div>
      </div>
    </a>"""

PAGE = """<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Prezentační šablony · galerie</title>
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='14' height='14' x='2' y='2' rx='3' fill='%23ff5a1f'/%3E%3Crect width='14' height='14' x='16' y='2' rx='3' fill='%235853eb'/%3E%3Crect width='14' height='14' x='2' y='16' rx='3' fill='%230e9e8e'/%3E%3Crect width='14' height='14' x='16' y='16' rx='3' fill='%23e11d74'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400..800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..600;1,8..60,400&family=JetBrains+Mono:wght@400..600&display=swap" rel="stylesheet">
<style>
:root{--bg:#0c0c10;--panel:#15151c;--panel2:#1c1c25;--rule:#2a2a35;--ink:#f2f2f5;--ink2:#b6b6c2;--ink3:#7c7c8a;--accent:#ff5a1f}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--bg);color:var(--ink);font-family:"Source Serif 4",Georgia,serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:1240px;margin:0 auto;padding:0 28px}
.disclaim{background:#3a1d0c;color:#ffd9c4;border-bottom:1px solid #5a3216;font-family:"JetBrains Mono",monospace;font-size:12.5px;letter-spacing:0.02em;text-align:center;padding:9px 14px}
.disclaim b{color:#ff8a4d}
header{padding:64px 0 30px}
.kick{font-family:"JetBrains Mono",monospace;font-size:13px;letter-spacing:0.14em;text-transform:uppercase;color:var(--ink3)}
.kick::before{content:"";display:inline-block;width:26px;height:3px;background:linear-gradient(90deg,#ff5a1f,#5853eb,#0e9e8e,#e11d74);vertical-align:middle;margin-right:12px;border-radius:2px}
h1{font-family:"Inter Tight",system-ui,sans-serif;font-weight:800;font-size:clamp(38px,6vw,72px);letter-spacing:-0.03em;line-height:1.0;margin:18px 0 14px}
h1 em{font-style:normal;background:linear-gradient(120deg,#ff5a1f,#e11d74 45%,#5853eb);-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{font-size:clamp(17px,2.2vw,21px);color:var(--ink2);max-width:660px;line-height:1.5;font-style:italic}
.facts{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px;font-family:"JetBrains Mono",monospace;font-size:12.5px}
.facts span{border:1px solid var(--rule);border-radius:999px;padding:7px 14px;color:var(--ink2)}
.facts span b{color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:22px;padding:24px 0 30px}
.card{display:flex;flex-direction:column;background:var(--panel);border:1px solid var(--rule);border-radius:16px;overflow:hidden;text-decoration:none;color:inherit;transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease}
.card:hover{transform:translateY(-4px);border-color:#3a3a48;box-shadow:0 20px 50px rgba(0,0,0,.45)}
.thumb{position:relative;aspect-ratio:16/9;overflow:hidden;background:#000;border-bottom:1px solid var(--rule)}
.thumb img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity .35s ease}
.thumb .alt{opacity:0}
.card:hover .cover{opacity:0}
.card:hover .alt{opacity:1}
.thumb .open{position:absolute;left:12px;bottom:12px;font-family:"JetBrains Mono",monospace;font-size:11.5px;color:#fff;background:rgba(0,0,0,.6);backdrop-filter:blur(4px);border:1px solid rgba(255,255,255,.18);border-radius:999px;padding:6px 12px;opacity:0;transform:translatey(6px);transition:.2s}
.card:hover .open{opacity:1;transform:none}
.body{padding:16px 18px 18px}
.swatches{display:flex;gap:6px;margin-bottom:10px}
.swatches i{width:16px;height:16px;border-radius:5px;display:block;box-shadow:inset 0 0 0 1px rgba(255,255,255,.12)}
.name{font-family:"Inter Tight",system-ui,sans-serif;font-weight:700;font-size:20px;letter-spacing:-0.01em}
.subj{color:var(--ink2);font-size:14.5px;margin-top:2px}
.tags{display:flex;gap:7px;margin-top:12px;font-family:"JetBrains Mono",monospace;font-size:11px;text-transform:uppercase;letter-spacing:0.04em;color:var(--ink3)}
.tags span{border:1px solid var(--rule);border-radius:6px;padding:3px 8px}
.how{border-top:1px solid var(--rule);margin-top:18px;padding:40px 0 70px;color:var(--ink2)}
.how h2{font-family:"Inter Tight",system-ui,sans-serif;font-weight:700;color:var(--ink);font-size:26px;letter-spacing:-0.01em;margin:0 0 16px}
.how ol{margin:0;padding-left:22px;line-height:1.7;max-width:760px}
.how code{font-family:"JetBrains Mono",monospace;font-size:.86em;background:var(--panel2);border:1px solid var(--rule);border-radius:5px;padding:2px 7px;color:#ffd9c4}
.how a{color:#ff8a4d}
.how .links{display:flex;flex-wrap:wrap;gap:12px;margin-top:18px;font-family:"JetBrains Mono",monospace;font-size:13px}
.how .links a{border:1px solid var(--rule);border-radius:8px;padding:9px 14px;text-decoration:none;color:var(--ink)}
.how .links a:hover{border-color:var(--accent)}
footer{border-top:1px solid var(--rule);padding:22px 0 40px;color:var(--ink3);font-family:"JetBrains Mono",monospace;font-size:12px;text-align:center}
</style>
</head>
<body>
<div class="disclaim">Galerie obsahuje <b>ukázkový (dummy) obsah</b>. Jména, čísla a citace jsou smyšlené a slouží jen k předvedení vizuálních stylů.</div>
<div class="wrap">
  <header>
    <div class="kick">// knihovna prezentačních šablon</div>
    <h1>Jedna kostra,<br><em>dvanáct stylů</em>.</h1>
    <p class="sub">Sdílený HTML engine pro prezentace v prohlížeči: auto-fit textu, poznámky řečníka, klávesová navigace a 16 typů slidů. Vyberte vzhled, vyměňte obsah, máte hotovo.</p>
    <div class="facts"><span><b>12</b> šablon</span><span><b>16</b> typů slidů</span><span><b>0</b> závislostí za běhu</span><span>jeden soubor = celá prezentace</span></div>
  </header>
  <div class="grid">
{cards}
  </div>
  <div class="how">
    <h2>Jak z toho udělat vlastní prezentaci</h2>
    <ol>
      <li>Vyberte šablonu a otevřete <code>templates/&lt;slug&gt;/index.html</code> v prohlížeči (dvojklik). Šipky listují, <b>F</b> je celá obrazovka, <b>N</b> poznámky řečníka.</li>
      <li>Chcete jen rychle upravit obsah? Editujte <code>build/content/&lt;NN&gt;.json</code> a spusťte <code>python3 build/build.py</code>. Vznikne nový self-contained HTML soubor.</li>
      <li>Chcete jiný vzhled? Změňte barvy a fonty v <code>THEMES</code> v <code>build/build.py</code> (proměnné <code>c1/c2/c3</code>, <code>display/serif/mono</code>).</li>
      <li>Stačí jeden soubor: vygenerovaný <code>index.html</code> má veškerý CSS i JS uvnitř. Zkopírujte ho kamkoli.</li>
    </ol>
    <div class="links"><a href="README.md">README</a><a href="GUIDE.md">Průvodce typy slidů</a><a href="build/content/01.json">Příklad obsahu (JSON)</a></div>
  </div>
</div>
<footer>Prezentační šablony &middot; sdílený engine převzatý z reálných decků a očištěný od obsahu &middot; ukázkový obsah</footer>
</body>
</html>"""

def kind(t):
    return "dark" if t.get("dark") else "light"

def main():
    cards = []
    for t in THEMES:
        lang, count, _title = meta_for(t)
        cards.append(CARD.format(
            slug=t["slug"], nn=t["slug"].split("-")[0], name=html.escape(t["name"]),
            subject=html.escape(t["subject"]), c1=t["c1"], c2=t["c2"], c3=t["c3"],
            lang=lang, count=count, kind=kind(t), darkcls=""))
    out = PAGE.replace("{cards}", "\n".join(cards))
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(out)
    print("wrote index.html with", len(cards), "cards")

if __name__ == "__main__":
    main()

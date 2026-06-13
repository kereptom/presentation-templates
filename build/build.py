#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builder for the presentation template gallery.
Source of truth = this file (framework CSS+JS) + themes (below) + content/NN.json.
Output = self-contained, copy-paste-ready templates/NN-slug/index.html.
No em dashes anywhere (global rule).
"""
import json, os, html, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(ROOT, "build", "content")
TPL_DIR = os.path.join(ROOT, "templates")

# ----------------------------------------------------------------------------
# THEMES : each is one template variant. Layout is identical, look is not.
# ----------------------------------------------------------------------------
THEMES = [
 dict(slug="01-industrial-orange", name="Industrial Orange", subject="Průmysl a výroba",
   font="Inter+Tight:wght@300..800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..600;1,8..60,400&family=JetBrains+Mono:wght@400..600",
   display='"Inter Tight", system-ui, sans-serif', serif='"Source Serif 4", Georgia, serif', mono='"JetBrains Mono", ui-monospace, monospace',
   c1="#ff5a1f", c2="#ff8a1f", c3="#ff3b1f", soft="#fff3ec", line="#ffd9c4",
   paper="#ffffff", papersoft="#fbfaf7", ink="#0e0e10", ink2="#3a3a40", ink3="#6b6b73", rule="#e6e6ea", rulesoft="#f1f1f4",
   divider="linear-gradient(140deg,#ff7a3c 0%,#e2551d 60%,#c8431a 100%)", dark=False),

 dict(slug="02-academia-indigo", name="Academia Indigo", subject="Věda a vzdělávání",
   font="Inter+Tight:wght@300..800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..600;1,8..60,400&family=JetBrains+Mono:wght@400..600",
   display='"Inter Tight", system-ui, sans-serif', serif='"Source Serif 4", Georgia, serif', mono='"JetBrains Mono", ui-monospace, monospace',
   c1="#5853eb", c2="#7b78f0", c3="#4a45d6", soft="#eeedfd", line="#d3d1f7",
   paper="#ffffff", papersoft="#faf9ff", ink="#16151f", ink2="#3a3950", ink3="#6b6a7e", rule="#e7e6f0", rulesoft="#f2f1f8",
   divider="linear-gradient(140deg,#7b78f0 0%,#5853eb 55%,#4038c0 100%)", dark=False),

 dict(slug="03-corporate-navy", name="Corporate Navy", subject="Finance a poradenství",
   font="Inter:wght@300..800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..600;1,8..60,400&family=IBM+Plex+Mono:wght@400..600",
   display='"Inter", system-ui, sans-serif', serif='"Source Serif 4", Georgia, serif', mono='"IBM Plex Mono", ui-monospace, monospace',
   c1="#1f4e8c", c2="#3a72bf", c3="#16365f", soft="#eaf1fb", line="#c5d8f0",
   paper="#ffffff", papersoft="#f8fafd", ink="#0f1b2d", ink2="#33425a", ink3="#647386", rule="#e1e7f0", rulesoft="#eef2f8",
   divider="linear-gradient(140deg,#2c5e9e 0%,#1f4e8c 55%,#13325a 100%)", dark=False),

 dict(slug="04-midnight-tech", name="Midnight Tech", subject="SaaS a startupy",
   font="Space+Grotesk:wght@400..700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..600;1,8..60,400&family=JetBrains+Mono:wght@400..600",
   display='"Space Grotesk", system-ui, sans-serif', serif='"Source Serif 4", Georgia, serif', mono='"JetBrains Mono", ui-monospace, monospace',
   c1="#2dd4bf", c2="#5eead4", c3="#14b8a6", soft="#10302e", line="#1c4744",
   paper="#0c1116", papersoft="#121922", ink="#eef2f6", ink2="#aeb8c4", ink3="#74808e", rule="#26313d", rulesoft="#1a232d",
   divider="linear-gradient(140deg,#14b8a6 0%,#0d9488 55%,#0a6f66 100%)", dark=True),

 dict(slug="05-editorial-serif", name="Editorial Serif", subject="Média a žurnalistika",
   font="Fraunces:opsz,wght@9..144,500..800&family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400&family=JetBrains+Mono:wght@400..600",
   display='"Fraunces", Georgia, serif', serif='"Newsreader", Georgia, serif', mono='"JetBrains Mono", ui-monospace, monospace',
   c1="#b3361f", c2="#cf5a3a", c3="#8f2516", soft="#fbeeea", line="#f0cfc6",
   paper="#fcfaf6", papersoft="#f6f2ea", ink="#211c16", ink2="#48413a", ink3="#7a7066", rule="#e6ddcf", rulesoft="#efe9dd",
   divider="linear-gradient(140deg,#c44a2e 0%,#b3361f 55%,#882012 100%)", dark=False),

 dict(slug="06-health-teal", name="Health Teal", subject="Zdravotnictví a biotech",
   font="Inter+Tight:wght@300..800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..600;1,8..60,400&family=JetBrains+Mono:wght@400..600",
   display='"Inter Tight", system-ui, sans-serif', serif='"Source Serif 4", Georgia, serif', mono='"JetBrains Mono", ui-monospace, monospace',
   c1="#0e9e8e", c2="#2bbdab", c3="#0a7f73", soft="#e6f6f3", line="#bfe7e1",
   paper="#ffffff", papersoft="#f6fbfa", ink="#0d1f1c", ink2="#324743", ink3="#5f7470", rule="#dcebe8", rulesoft="#ebf4f2",
   divider="linear-gradient(140deg,#19b1a0 0%,#0e9e8e 55%,#0a6f66 100%)", dark=False),

 dict(slug="07-legal-charcoal", name="Legal Charcoal", subject="Právo a profesní služby",
   font="Libre+Franklin:wght@300..800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..600;1,8..60,400&family=JetBrains+Mono:wght@400..600",
   display='"Libre Franklin", system-ui, sans-serif', serif='"Source Serif 4", Georgia, serif', mono='"JetBrains Mono", ui-monospace, monospace',
   c1="#a8843f", c2="#c4a45f", c3="#8a6c2f", soft="#f6f0e3", line="#e6d6b6",
   paper="#ffffff", papersoft="#faf8f4", ink="#1c1d22", ink2="#3d3f47", ink3="#6d6f78", rule="#e4e2dc", rulesoft="#f0eee8",
   divider="linear-gradient(140deg,#33353d 0%,#23242a 60%,#16171b 100%)", dark=False, divider_ink="#f3ead4"),

 dict(slug="08-creative-magenta", name="Creative Magenta", subject="Design a kreativní agentura",
   font="Space+Grotesk:wght@400..700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..600;1,8..60,400&family=Space+Mono:wght@400;700",
   display='"Space Grotesk", system-ui, sans-serif', serif='"Source Serif 4", Georgia, serif', mono='"Space Mono", ui-monospace, monospace',
   c1="#e11d74", c2="#f25ca0", c3="#b3175c", soft="#fdeaf3", line="#f8c4dd",
   paper="#ffffff", papersoft="#fdf8fb", ink="#1a0f16", ink2="#43303a", ink3="#7a6470", rule="#efe2ea", rulesoft="#f7eef3",
   divider="linear-gradient(140deg,#f0408a 0%,#e11d74 55%,#a8125a 100%)", dark=False),

 dict(slug="09-eco-green", name="Eco Green", subject="Udržitelnost a energetika",
   font="Inter+Tight:wght@300..800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..600;1,8..60,400&family=JetBrains+Mono:wght@400..600",
   display='"Inter Tight", system-ui, sans-serif', serif='"Source Serif 4", Georgia, serif', mono='"JetBrains Mono", ui-monospace, monospace',
   c1="#3f9e44", c2="#65bd62", c3="#2f7f37", soft="#ecf6ec", line="#cbe7c9",
   paper="#ffffff", papersoft="#f7fbf6", ink="#15201400"[:7], ink2="#34452f", ink3="#61735c", rule="#deeadc", rulesoft="#ecf3eb",
   divider="linear-gradient(140deg,#56b257 0%,#3f9e44 55%,#2a7733 100%)", dark=False),

 dict(slug="10-mono-minimal", name="Mono Minimal", subject="Architektura a minimalismus",
   font="Archivo:wght@400..800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..600;1,8..60,400&family=JetBrains+Mono:wght@400..600",
   display='"Archivo", system-ui, sans-serif', serif='"Source Serif 4", Georgia, serif', mono='"JetBrains Mono", ui-monospace, monospace',
   c1="#111114", c2="#3a3a40", c3="#000000", soft="#f0f0f0", line="#d8d8d8",
   paper="#ffffff", papersoft="#f7f7f6", ink="#111114", ink2="#3a3a40", ink3="#787880", rule="#e3e3e3", rulesoft="#eeeeee",
   divider="linear-gradient(140deg,#26262b 0%,#141417 60%,#000000 100%)", dark=False),

 dict(slug="11-warm-education", name="Warm Education", subject="Vzdělávání a školení",
   font="Quicksand:wght@400..700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..600;1,8..60,400&family=JetBrains+Mono:wght@400..600",
   display='"Quicksand", system-ui, sans-serif', serif='"Source Serif 4", Georgia, serif', mono='"JetBrains Mono", ui-monospace, monospace',
   c1="#e0820f", c2="#f0a63a", c3="#c06806", soft="#fdf2e1", line="#f6dcb4",
   paper="#fffdfa", papersoft="#fbf6ee", ink="#241c12", ink2="#46392b", ink3="#766656", rule="#ece2d3", rulesoft="#f4ece0",
   divider="linear-gradient(140deg,#f0a23a 0%,#e0820f 55%,#b96706 100%)", dark=False),

 dict(slug="12-vibrant-gradient", name="Vibrant Gradient", subject="Marketing a eventy",
   font="Sora:wght@400..800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..600;1,8..60,400&family=JetBrains+Mono:wght@400..600",
   display='"Sora", system-ui, sans-serif', serif='"Source Serif 4", Georgia, serif', mono='"JetBrains Mono", ui-monospace, monospace',
   c1="#7b2ff7", c2="#f12daa", c3="#5b1fd0", soft="#f3ecfe", line="#dccbf9",
   paper="#ffffff", papersoft="#faf7fe", ink="#170f24", ink2="#3b3050", ink3="#6c6080", rule="#e9e2f2", rulesoft="#f2eef8",
   divider="linear-gradient(120deg,#7b2ff7 0%,#b32fe0 50%,#f12daa 100%)", dark=False),
]

# ---- font library (safe Google Fonts axis specs) -------------------------
FONTS = {
 "inter_tight":("Inter+Tight:wght@400..700",'"Inter Tight", system-ui, sans-serif'),
 "inter":("Inter:wght@400..700",'"Inter", system-ui, sans-serif'),
 "space_grotesk":("Space+Grotesk:wght@400..700",'"Space Grotesk", system-ui, sans-serif'),
 "sora":("Sora:wght@400..700",'"Sora", system-ui, sans-serif'),
 "archivo":("Archivo:wght@400..700",'"Archivo", system-ui, sans-serif'),
 "manrope":("Manrope:wght@400..700",'"Manrope", system-ui, sans-serif'),
 "jakarta":("Plus+Jakarta+Sans:wght@400..700",'"Plus Jakarta Sans", system-ui, sans-serif'),
 "outfit":("Outfit:wght@400..700",'"Outfit", system-ui, sans-serif'),
 "hanken":("Hanken+Grotesk:wght@400..700",'"Hanken Grotesk", system-ui, sans-serif'),
 "figtree":("Figtree:wght@400..700",'"Figtree", system-ui, sans-serif'),
 "albert":("Albert+Sans:wght@400..700",'"Albert Sans", system-ui, sans-serif'),
 "epilogue":("Epilogue:wght@400..700",'"Epilogue", system-ui, sans-serif'),
 "red_hat":("Red+Hat+Display:wght@400..700",'"Red Hat Display", system-ui, sans-serif'),
 "libre_franklin":("Libre+Franklin:wght@400..700",'"Libre Franklin", system-ui, sans-serif'),
 "schibsted":("Schibsted+Grotesk:wght@400..700",'"Schibsted Grotesk", system-ui, sans-serif'),
 "bricolage":("Bricolage+Grotesque:wght@400..700",'"Bricolage Grotesque", system-ui, sans-serif'),
 "quicksand":("Quicksand:wght@400..700",'"Quicksand", system-ui, sans-serif'),
 "unbounded":("Unbounded:wght@400..700",'"Unbounded", system-ui, sans-serif'),
 "fraunces":("Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400",'"Fraunces", Georgia, serif'),
 "playfair":("Playfair+Display:ital,wght@0,400..800;1,400..600",'"Playfair Display", Georgia, serif'),
 "source_serif":("Source+Serif+4:ital,opsz,wght@0,8..60,400..600;1,8..60,400",'"Source Serif 4", Georgia, serif'),
 "newsreader":("Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400",'"Newsreader", Georgia, serif'),
 "lora":("Lora:ital,wght@0,400..700;1,400..600",'"Lora", Georgia, serif'),
 "bodoni":("Bodoni+Moda:ital,opsz,wght@0,6..96,400..700;1,6..96,400",'"Bodoni Moda", Georgia, serif'),
 "jetbrains":("JetBrains+Mono:wght@400..600",'"JetBrains Mono", ui-monospace, monospace'),
 "plex_mono":("IBM+Plex+Mono:wght@400;500;600",'"IBM Plex Mono", ui-monospace, monospace'),
 "space_mono":("Space+Mono:wght@400;700",'"Space Mono", ui-monospace, monospace'),
 "fira_code":("Fira+Code:wght@400..600",'"Fira Code", ui-monospace, monospace'),
 "dm_mono":("DM+Mono:wght@400;500",'"DM Mono", ui-monospace, monospace'),
}

def _hex2rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def _rgb2hex(t):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(v)))) for v in t)
def mix(a, b, t):
    ra, rb = _hex2rgb(a), _hex2rgb(b)
    return _rgb2hex(tuple(ra[i] * t + rb[i] * (1 - t) for i in range(3)))

def mk(slug, name, subj, lang, disp, body, mono, c1, *, c2=None, c3=None,
       paper="#ffffff", ink="#15151b", dark=False, radius=1.0, bodyclass="",
       divider=None, divink="#ffffff"):
    if c2 is None: c2 = mix(c1, "#ffffff", 0.74)
    if c3 is None: c3 = mix(c1, "#000000", 0.80)
    df, bf, mf = FONTS[disp], FONTS[body], FONTS[mono]
    frags = []
    for fr in (df[0], bf[0], mf[0]):
        if fr not in frags: frags.append(fr)
    font = "&family=".join(frags)
    papersoft = mix(paper, ink, 0.965 if not dark else 0.93)
    soft = mix(c1, paper, 0.13 if not dark else 0.17)
    line = mix(c1, paper, 0.30 if not dark else 0.42)
    ink2 = mix(ink, paper, 0.78); ink3 = mix(ink, paper, 0.52)
    rule = mix(ink, paper, 0.13); rulesoft = mix(ink, paper, 0.06)
    if divider is None:
        divider = f"linear-gradient(140deg,{c2} 0%,{c1} 55%,{c3} 100%)"
    return dict(slug=slug, name=name, subject=subj, lang=lang, font=font,
        display=df[1], serif=bf[1], mono=mf[1], c1=c1, c2=c2, c3=c3, soft=soft, line=line,
        paper=paper, papersoft=papersoft, ink=ink, ink2=ink2, ink3=ink3, rule=rule, rulesoft=rulesoft,
        divider=divider, divider_ink=divink, dark=dark, radius=radius, bodyclass=bodyclass)

THEMES += [
 mk("13-slate-consulting","Slate Consulting","Strategie a poradenství","cs","inter_tight","source_serif","jetbrains","#3b5bdb"),
 mk("14-forest-outdoor","Forest Outdoor","Outdoorová značka","cs","hanken","lora","jetbrains","#2f7d4f",paper="#f7faf7",ink="#16201a",radius=1.3),
 mk("15-rose-beauty","Rose Beauty","Kosmetika a péče","en","jakarta","newsreader","dm_mono","#d6446e",paper="#fdf7f9",ink="#20141a",radius=1.5),
 mk("16-amber-stay","Amber Stay","Hotelnictví","cs","outfit","source_serif","jetbrains","#c8862a",paper="#fffdf8",ink="#211a10",radius=1.2),
 mk("17-crimson-sport","Crimson Sport","Sport a fitness","en","archivo","source_serif","space_mono","#d62828",ink="#15110f",radius=0.5,bodyclass="em-solid"),
 mk("18-teal-data","Teal Data","Data a analytika","cs","space_grotesk","source_serif","jetbrains","#0e8f9e",paper="#f5fbfc",ink="#0d1b1f"),
 mk("19-violet-audio","Violet Audio","Hudba a zvuk","en","sora","source_serif","fira_code","#6d4aff",paper="#faf8ff",ink="#16121f",radius=1.2),
 mk("20-sand-estate","Sand Estate","Reality","cs","manrope","lora","jetbrains","#a8763f",paper="#faf7f1",ink="#1d1812",radius=0.8),
 mk("21-sky-travel","Sky Travel","Cestování a letectví","en","figtree","source_serif","jetbrains","#2a8fd6",paper="#f6fbff",ink="#0f1922",radius=1.4),
 mk("22-plum-atelier","Plum Atelier","Móda","cs","epilogue","playfair","dm_mono","#7d2e5f",paper="#fdf7fb",ink="#1c121a",bodyclass="em-solid"),
 mk("23-carbon-lime","Carbon Lime","Kyberbezpečnost","en","space_grotesk","source_serif","jetbrains","#9bd62a",paper="#0c0f0a",ink="#eef3e6",dark=True,radius=0.4,bodyclass="em-solid"),
 mk("24-deep-space","Deep Space","Letectví a kosmonautika","cs","sora","source_serif","jetbrains","#5b8def",paper="#080b14",ink="#e7ecf6",dark=True),
 mk("25-noir-gold","Noir Gold","Luxusní zboží","en","jakarta","bodoni","jetbrains","#c9a24a",paper="#0d0c0a",ink="#f1ece0",dark=True,radius=0.6),
 mk("26-midnight-rose","Midnight Rose","Noční život","cs","outfit","source_serif","space_mono","#ff4f8b",paper="#0e0a0e",ink="#f3e9ef",dark=True,radius=1.5),
 mk("27-terminal-green","Terminal Green","Vývojářské nástroje","en","space_grotesk","source_serif","jetbrains","#36d399",paper="#0a0e0c",ink="#e6f2ec",dark=True,radius=0.3,bodyclass="em-solid"),
 mk("28-obsidian-blue","Obsidian Blue","Fintech","cs","inter_tight","source_serif","plex_mono","#4f8bff",paper="#0a0e16",ink="#e8edf5",dark=True,radius=0.8),
 mk("29-broadsheet","Broadsheet","Vydavatelství","en","playfair","newsreader","jetbrains","#b32417",paper="#fbfaf6",ink="#1a1813",radius=0.3,bodyclass="em-solid"),
 mk("30-manifesto","Manifesto","Politika a veřejná správa","cs","fraunces","source_serif","jetbrains","#b5371f",paper="#fbf8f3",ink="#1c1712",radius=0.4),
 mk("31-gallery","Gallery","Umění a muzea","en","bodoni","lora","jetbrains","#9a3412",paper="#fdfcfa",ink="#17151a",radius=0.25,bodyclass="em-solid"),
 mk("32-almanac","Almanac","Zemědělství","cs","bricolage","lora","jetbrains","#6f8f1f",paper="#f9faf2",ink="#1b1d12"),
 mk("33-bubblegum","Bubblegum","Děti a hračky","en","quicksand","source_serif","dm_mono","#ff5ca8",paper="#fff8fc",ink="#281826",radius=2.2),
 mk("34-sunrise-wellness","Sunrise Wellness","Wellness aplikace","cs","quicksand","source_serif","jetbrains","#ff8a3d",paper="#fffaf4",ink="#241a12",radius=2.0),
 mk("35-pop-kitchen","Pop Kitchen","Rozvoz jídla","en","unbounded","source_serif","space_mono","#ff3d54",paper="#fffaf6",ink="#20120f",radius=1.8,bodyclass="em-solid"),
 mk("36-blueprint","Blueprint","Inženýrství","cs","space_grotesk","source_serif","jetbrains","#2563c9",paper="#f4f7fb",ink="#0f1722",radius=0.3,bodyclass="cs-outline"),
 mk("37-wireframe","Wireframe","UX výzkum","en","archivo","source_serif","jetbrains","#4b4b55",paper="#fafafb",ink="#18181d",radius=0.4,bodyclass="cs-outline em-solid"),
 mk("38-mono-red","Mono Red","Architektonické studio","en","archivo","source_serif","space_mono","#e23b2e",ink="#111114",radius=0.2,bodyclass="cs-outline em-solid"),
 mk("39-pastel-mint","Pastel Mint","Papírnictví","cs","jakarta","source_serif","jetbrains","#3bbd8f",paper="#f6fbf9",ink="#15201b",radius=1.4,bodyclass="cs-flat"),
 mk("40-cloud-infra","Cloud Infra","Cloudová infrastruktura","en","inter_tight","source_serif","jetbrains","#3a86ff",paper="#f6f9ff",ink="#101522",radius=1.2,bodyclass="cs-flat"),
 mk("41-copper-works","Copper Works","Strojírenství","cs","libre_franklin","source_serif","jetbrains","#b5651d",paper="#fdfaf6",ink="#1c1610",radius=0.6),
 mk("42-indigo-learn","Indigo Learn","E-learning","en","figtree","source_serif","jetbrains","#6366f1",paper="#0c0d16",ink="#e9eaf6",dark=True,radius=1.2),
 mk("43-coral-hr","Coral HR","Nábor a HR","cs","manrope","source_serif","jetbrains","#ff6b5e",paper="#fff8f6",ink="#201513",radius=1.4),
 mk("44-olive-table","Olive Table","Potraviny a nápoje","en","outfit","lora","jetbrains","#7a8b2a",paper="#faf9f0",ink="#1a1c12"),
 mk("45-berry-retail","Berry Retail","Maloobchod","cs","albert","source_serif","jetbrains","#b5246b",paper="#fdf6fa",ink="#1d1219",radius=1.1),
 mk("46-steel-logistics","Steel Logistics","Logistika","en","red_hat","source_serif","jetbrains","#4a6275",paper="#f5f7f9",ink="#11161b",radius=0.5),
 mk("47-mustard-podcast","Mustard","Podcast","cs","schibsted","source_serif","space_mono","#d6a019",paper="#fffdf6",ink="#1e1a10",radius=1.2),
 mk("48-ocean-lines","Ocean Lines","Námořní doprava","en","inter_tight","source_serif","jetbrains","#1d6fa5",paper="#f4f9fc",ink="#0e1820",radius=0.8),
 mk("49-lavender-mind","Lavender Mind","Duševní zdraví","cs","outfit","newsreader","jetbrains","#8b7bd8",paper="#faf9fd",ink="#1a1622",radius=1.6),
 mk("50-graphite-auto","Graphite Auto","Automobilový průmysl","en","archivo","source_serif","jetbrains","#d24a2a",paper="#0e0e10",ink="#ededf0",dark=True,radius=0.5,bodyclass="em-solid"),
 mk("51-sunset-tourism","Sunset Tourism","Turistika","cs","hanken","lora","jetbrains","#f2683c",paper="#fffaf5",ink="#201410",radius=1.4),
 mk("52-emerald-bank","Emerald Bank","Bankovnictví","en","jakarta","source_serif","plex_mono","#0f7a52",paper="#f5fbf8",ink="#0f1a15",radius=0.7),
 mk("53-clay-craft","Clay and Craft","Keramika a řemeslo","cs","bricolage","lora","jetbrains","#b0573f",paper="#fbf6f1",ink="#1f160f",radius=1.6,bodyclass="cs-flat"),
 mk("54-neon-cyan","Neon Cyan","Gaming","en","unbounded","source_serif","space_mono","#22e0d6",paper="#07090d",ink="#e6f6f5",dark=True,radius=1.0,bodyclass="em-solid"),
 mk("55-vintage-wine","Vintage Wine","Vinařství","cs","fraunces","newsreader","jetbrains","#7b1e3a",paper="#fbf6f4",ink="#1c1213",radius=0.5,bodyclass="em-solid"),
 mk("56-aqua-utility","Aqua Utility","Vodárenství","en","inter_tight","source_serif","jetbrains","#1ba0c4",paper="#f4fbfd",ink="#0d1a20",radius=0.9),
 mk("57-saffron","Saffron","Restaurace","cs","epilogue","playfair","jetbrains","#e0851a",paper="#fffaf2",ink="#201810",bodyclass="em-solid"),
 mk("58-slate-gov","Slate Gov","Veřejná správa","en","libre_franklin","source_serif","jetbrains","#3a4a63",paper="#f6f7f9",ink="#12161e",radius=0.4),
 mk("59-magenta-social","Magenta Social","Sociální sítě","cs","sora","source_serif","jetbrains","#e0249a",paper="#fdf6fb",ink="#1c1019",radius=1.5),
 mk("60-pine-forestry","Pine Forestry","Lesnictví","en","hanken","lora","jetbrains","#2c6e49",paper="#f6faf6",ink="#14201a",radius=0.9),
 mk("61-bronze-exhibit","Bronze Exhibit","Muzejní výstava","cs","fraunces","lora","jetbrains","#9c6b30",paper="#fbf8f2",ink="#1c170f",radius=0.4,bodyclass="em-solid"),
 mk("62-electric-robotics","Electric Robotics","Robotika","en","space_grotesk","source_serif","jetbrains","#2f6bff",paper="#0a0d14",ink="#e8ecf6",dark=True,radius=0.6,bodyclass="em-solid"),
]

# ----------------------------------------------------------------------------
# ICONS (lucide-style line icons for KPI cards / cards3)
# ----------------------------------------------------------------------------
ICONS = {
 "trend_up":'<path d="M16 7h6v6"/><path d="m22 7-8.5 8.5-5-5L2 17"/>',
 "trend_down":'<path d="M16 17h6v-6"/><path d="m22 17-8.5-8.5-5 5L2 7"/>',
 "bars":'<path d="M3 3v18h18"/><rect x="7" y="11" width="3" height="7"/><rect x="12" y="7" width="3" height="11"/><rect x="17" y="4" width="3" height="14"/>',
 "dollar":'<line x1="12" y1="2" x2="12" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
 "grid":'<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
 "pie":'<path d="M21 12A9 9 0 1 1 9 3.5"/><path d="M21 12 12 12 12 3a9 9 0 0 1 9 9z"/>',
 "alert":'<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
 "activity":'<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
 "clock":'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "calendar":'<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
 "shield":'<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
 "users":'<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9"/><path d="M16 3.1A4 4 0 0 1 16 11"/>',
 "target":'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
 "zap":'<path d="M13 2 3 14h8l-1 8 10-12h-8l1-8z"/>',
 "globe":'<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18 14 14 0 0 1 0-18z"/>',
 "leaf":'<path d="M11 20A7 7 0 0 1 4 13c0-6 7-10 16-10 0 8-4 15-9 17z"/><path d="M4 21c3-4 6-6 10-7"/>',
 "cpu":'<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 2v2M15 2v2M9 20v2M15 20v2M2 9h2M2 15h2M20 9h2M20 15h2"/>',
 "doc":'<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M8 13h8M8 17h6"/>',
 "lock":'<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
 "heart":'<path d="M19 14c1.5-1.5 3-3.3 3-5.5A4.5 4.5 0 0 0 12 5 4.5 4.5 0 0 0 2 8.5c0 2.2 1.5 4 3 5.5l7 7z"/>',
 "compass":'<circle cx="12" cy="12" r="9"/><path d="m16 8-2 6-6 2 2-6 6-2z"/>',
 "rocket":'<path d="M5 13c-2 1-3 5-3 5s4-1 5-3"/><path d="M15 7a8 8 0 0 1 5-2 8 8 0 0 1-2 5l-7 7-3-3z"/><circle cx="15" cy="9" r="1"/>',
 "network":'<circle cx="6" cy="6" r="2.3"/><circle cx="18" cy="6" r="2.3"/><circle cx="12" cy="18" r="2.3"/><path d="M7.7 7.7 11 15.5M16.3 7.7 13 15.5M8.3 6h7.4"/>',
 "gears":'<circle cx="9" cy="9" r="3"/><path d="M9 3.5v1.7M9 12.8v1.7M3.5 9h1.7M12.8 9h1.7M5.6 5.6l1.2 1.2M11.2 11.2l1.2 1.2"/><circle cx="17" cy="16.5" r="2.2"/>',
 "growth":'<path d="M3 3v18h18"/><path d="m7 14 4-4 3 3 5-6"/><path d="M17 7h3v3"/>',
 "brain":'<path d="M12 5.5a3 3 0 0 0-5 2.2 3 3 0 0 0-1 5 3 3 0 0 0 4 2.8h2z"/><path d="M12 5.5a3 3 0 0 1 5 2.2 3 3 0 0 1 1 5 3 3 0 0 1-4 2.8h-2z"/><path d="M12 5.5v10"/>',
 "cloud":'<path d="M7 17.5a4 4 0 0 1 0-8 5 5 0 0 1 9.5-1A3.5 3.5 0 0 1 17 17.5z"/>',
 "layers":'<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>',
 "branch":'<circle cx="6" cy="12" r="2"/><path d="M8 12h3.5M12 12 18 7M12 12l6 5"/><circle cx="18.5" cy="6.5" r="1.6"/><circle cx="18.5" cy="17.5" r="1.6"/>',
 "chip":'<rect x="7" y="7" width="10" height="10" rx="1.5"/><rect x="10" y="10" width="4" height="4"/><path d="M10 7V4.5M14 7V4.5M10 19.5V17M14 19.5V17M7 10H4.5M7 14H4.5M19.5 10H17M19.5 14H17"/>',
 "people":'<circle cx="9" cy="8" r="3"/><path d="M4 19a5 5 0 0 1 10 0"/><circle cx="17.5" cy="9" r="2"/><path d="M15.5 19a4 4 0 0 1 5.5-3.2"/>',
 "chat":'<path d="M21 12a8 8 0 0 1-11.5 7.2L4 21l1.8-5.5A8 8 0 1 1 21 12z"/>',
 "flask":'<path d="M9 3.5h6M10 3.5v5.5l-5 8.5a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-8.5V3.5"/><path d="M7.5 15h9"/>',
 "scale":'<path d="M12 3.5v17M7 20.5h10"/><path d="M12 6 6.2 7.8M12 6l5.8 1.8"/><path d="M3.6 12a2.6 2 0 0 0 5.2 0zM15.2 12a2.6 2 0 0 0 5.2 0z"/>',
 "megaphone":'<path d="M4 9.5V13l2 0.6 1.6 3.9 2.2-0.9-1.2-3 9.4 3.4V6L8.8 10H6a2 2 0 0 0-2 -0.5z"/><path d="M17 8.5a3 3 0 0 1 0 6"/>',
}

# ----------------------------------------------------------------------------
# SPARKLINES (for scenario cards)
# ----------------------------------------------------------------------------
SPARKS = {
 "plateau":'<line class="ax" x1="2" y1="47" x2="98" y2="47"/><path class="ln" d="M3,44 C18,44 27,13 47,12 C67,11 85,12 97,12"/><circle class="dot" cx="97" cy="12" r="3.4"/>',
 "expo":'<line class="ax" x1="2" y1="47" x2="98" y2="47"/><path class="ln" d="M3,47 C45,46 66,43 80,33 C88,27 94,16 97,4"/><circle class="dot" cx="97" cy="4" r="3.4"/>',
 "selfimp":'<line class="ax" x1="2" y1="47" x2="98" y2="47"/><line class="asy" x1="89.5" y1="3" x2="89.5" y2="46"/><path class="ln" d="M3,44 L63,42 C78,41 85,39 88,30 C89.3,23 89.5,13 89.5,3"/><circle class="dot" cx="89.5" cy="3" r="3.4"/>',
 "linear":'<line class="ax" x1="2" y1="47" x2="98" y2="47"/><path class="ln" d="M3,44 L97,8"/><circle class="dot" cx="97" cy="8" r="3.4"/>',
 "decline":'<line class="ax" x1="2" y1="47" x2="98" y2="47"/><path class="ln" d="M3,8 C30,8 45,30 60,34 C75,38 88,40 97,42"/><circle class="dot" cx="97" cy="42" r="3.4"/>',
}

# ----------------------------------------------------------------------------
# ILLUSTRATIONS (abstract inline SVG line-art, themed via var(--c-1))
# stroke uses currentColor pattern through an .ill wrapper colour.
# ----------------------------------------------------------------------------
def _ill(body, vb="0 0 240 200", sw=6):
    return (f'<svg class="ill" viewBox="{vb}" fill="none" stroke="var(--c-1)" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')

ILLUS = {
 "network": _ill('<circle cx="120" cy="100" r="20"/><circle cx="40" cy="50" r="13"/><circle cx="200" cy="55" r="13"/><circle cx="50" cy="160" r="13"/><circle cx="195" cy="155" r="13"/><path d="M104 88 53 60M136 90 188 62M106 114 60 150M134 113 182 145"/>'),
 "gears": _ill('<circle cx="95" cy="95" r="34"/><circle cx="95" cy="95" r="12"/><path d="M95 50v-14M95 154v-14M50 95H36M154 95h-14M64 64 54 54M126 126l10 10M126 64l10-10M64 126l-10 10"/><circle cx="170" cy="150" r="22"/><circle cx="170" cy="150" r="8"/><path d="M170 122v-9M170 187v-9M142 150h-9M207 150h-9"/>'),
 "growth": _ill('<path d="M30 170h180M30 170V40"/><rect x="55" y="120" width="26" height="50"/><rect x="100" y="92" width="26" height="78"/><rect x="145" y="60" width="26" height="110"/><path d="M50 110 95 80l30 18 60-50"/><path d="M165 48h22v22" stroke-width="5"/>', sw=6),
 "shield": _ill('<path d="M120 30 50 56v52c0 44 70 74 70 74s70-30 70-74V56z"/><path d="m92 104 20 20 40-44"/>'),
 "doc": _ill('<rect x="55" y="34" width="100" height="132" rx="8"/><path d="M78 70h54M78 96h54M78 122h36"/><circle cx="158" cy="150" r="26"/><path d="m176 168 18 18" stroke-width="7"/>'),
 "brain": _ill('<path d="M120 40c-26 0-40 18-40 36-18 4-26 20-20 38 4 12 16 18 16 30 0 16 18 26 36 20"/><path d="M120 40c26 0 40 18 40 36 18 4 26 20 20 38-4 12-16 18-16 30 0 16-18 26-36 20"/><path d="M120 40v124M96 88h-8M152 88h8M104 132h-8M144 132h8"/>'),
 "cloud": _ill('<path d="M70 140a34 34 0 0 1 4-68 44 44 0 0 1 84 6 30 30 0 0 1-6 62z"/><path d="M100 150v34M120 150v44M140 150v34" stroke-width="5"/>'),
 "layers": _ill('<path d="m120 36 86 44-86 44-86-44z"/><path d="m34 118 86 44 86-44M34 152l86 44 86-44" stroke-width="5"/>'),
 "target": _ill('<circle cx="110" cy="105" r="62"/><circle cx="110" cy="105" r="36"/><circle cx="110" cy="105" r="10"/><path d="m150 65 40-40M178 25h12v12" stroke-width="5"/>'),
 "branch": _ill('<path d="M40 100h60"/><path d="M100 100 180 45M168 40l16 4-4 16" stroke-width="6"/><path d="M100 100 180 155M180 139l4 16-16 4" stroke-width="6"/><circle cx="40" cy="100" r="10"/>'),
 "chip": _ill('<rect x="62" y="62" width="86" height="86" rx="10"/><rect x="92" y="92" width="26" height="26"/><path d="M85 62V42M125 62V42M85 168v-20M125 168v-20M62 92H42M62 122H42M168 92h-20M168 122h-20"/>'),
 "people": _ill('<circle cx="80" cy="74" r="22"/><path d="M44 150a36 36 0 0 1 72 0"/><circle cx="158" cy="84" r="18"/><path d="M128 150a30 30 0 0 1 60 0"/>'),
 "chat": _ill('<rect x="34" y="44" width="120" height="84" rx="14"/><path d="M64 128v22l26-22"/><path d="M62 74h64M62 98h40"/><circle cx="170" cy="140" r="30"/><path d="M158 140h24M170 128v24" stroke-width="5"/>'),
 "flask": _ill('<path d="M100 34h40M108 34v44l-44 78a14 14 0 0 0 12 22h88a14 14 0 0 0 12-22l-44-78V34"/><path d="M84 132h72"/><circle cx="108" cy="150" r="5" stroke-width="4"/><circle cx="140" cy="166" r="5" stroke-width="4"/>'),
 "scale": _ill('<path d="M120 36v140M70 176h100"/><path d="M120 56 60 84M120 56l60 28"/><path d="M40 84a20 14 0 0 0 40 0zM140 84a20 14 0 0 0 40 0z"/>'),
 "megaphone": _ill('<path d="M40 88v28l18 4 18 40 18-6-12-30 70 22V52L58 84z"/><path d="M168 78a24 24 0 0 1 0 48" stroke-width="5"/>'),
}

# ----------------------------------------------------------------------------
# RENDERERS
# ----------------------------------------------------------------------------
def notes(s):
    n = s.get("notes", "")
    return f'<aside class="notes-data">{n}</aside>' if n else ""

def foot(s):
    f = s.get("footnote", "")
    return f'<p class="footnote">{f}</p>' if f else ""

def kicker(s):
    k = s.get("kicker", "")
    return f'<div class="kicker">{k}</div>' if k else ""

def meta_block(items):
    cells = "".join(f'<div><strong>{k}</strong><span>{v}</span></div>' for k, v in items)
    return f'<div class="meta">{cells}</div>'

def r_title(s):
    return (f'<section class="slide title-slide">{kicker(s)}<h1>{s["h1"]}</h1>'
            f'<p class="lead">{s.get("lead","")}</p>{meta_block(s.get("meta",[]))}{notes(s)}</section>')

def r_closing(s):
    return (f'<section class="slide title-slide">{kicker(s)}<h1>{s["h1"]}</h1>'
            f'<p class="lead">{s.get("lead","")}</p>{meta_block(s.get("meta",[]))}{notes(s)}</section>')

def r_team(s):
    mem = "".join(
        f'<div class="lector"><div class="lector-photo lector-initials" data-initials="{i}"></div>'
        f'<div class="lector-name">{n}</div><div class="lector-title">{role}</div></div>'
        for i, n, role in s.get("members", []))
    return (f'<section class="slide">{kicker(s)}<h2>{s["h2"]}</h2>'
            f'<p class="lead">{s.get("lead","")}</p><div class="lector-grid">{mem}</div>{notes(s)}</section>')

def r_agenda(s):
    blocks = "".join(f'<div class="af-b">{b}</div>' for b in s.get("blocks", []))
    return (f'<section class="slide">{kicker(s)}<h2>{s["h2"]}</h2>'
            f'<p class="lead">{s.get("lead","")}</p><div class="agenda-flow">{blocks}</div>{notes(s)}</section>')

def r_divider(s):
    return (f'<section class="slide section-divider">{kicker(s)}<h1>{s["h1"]}</h1>'
            f'<p class="lead">{s.get("lead","")}</p>{notes(s)}</section>')

def r_hero(s):
    ill = ILLUS.get(s.get("illus", "network"), ILLUS["network"])
    return (f'<section class="slide bk">{kicker(s)}<h1>{s["h1"]}</h1>'
            f'<div class="bk-img">{ill}</div><p class="lead">{s.get("lead","")}</p>{foot(s)}{notes(s)}</section>')

def r_kpi(s):
    cells = ""
    for ic, num, lbl in s.get("items", []):
        cells += (f'<div class="kpi"><svg viewBox="0 0 24 24">{ICONS.get(ic, ICONS["bars"])}</svg>'
                  f'<div class="kpi-num">{num}</div><div class="kpi-lbl">{lbl}</div></div>')
    bl = s.get("bullets", [])
    ul = ""
    if bl:
        lis = "".join(f'<li style="font-size:calc(2.1cqw*var(--fs,1))">{b}</li>' for b in bl)
        ul = f'<ul style="line-height:1.5; margin-top:0.6cqw">{lis}</ul>'
    return (f'<section class="slide">{kicker(s)}<h2>{s["h2"]}</h2>'
            f'<div class="kpi-grid">{cells}</div>{ul}{foot(s)}{notes(s)}</section>')

def r_twocol(s):
    ill = ILLUS.get(s.get("illus", "gears"), ILLUS["gears"])
    lis = "".join(f'<li><strong>{a}</strong> {b}</li>' for a, b in s.get("bullets", []))
    return (f'<section class="slide">{kicker(s)}<h2>{s["h2"]}</h2>'
            f'<p class="lead">{s.get("lead","")}</p>'
            f'<div class="grid-2" style="grid-template-columns:1fr 0.6fr; align-items:center">'
            f'<div><ul style="line-height:1.65; font-size:calc(2.32cqw*var(--fs,1))">{lis}</ul></div>'
            f'<div class="illust-col">{ill}</div></div>{foot(s)}{notes(s)}</section>')

def r_cards2(s):
    cards = "".join(f'<div class="card"><strong>{t}</strong><span>{x}</span></div>' for t, x in s.get("cards", []))
    return (f'<section class="slide">{kicker(s)}<h2>{s["h2"]}</h2>'
            f'<p class="lead">{s.get("lead","")}</p><div class="grid-2">{cards}</div>{foot(s)}{notes(s)}</section>')

def r_cards3(s):
    cards = ""
    for c in s.get("cards", []):
        ic, t, x = (c + ["", "", ""])[:3] if isinstance(c, list) else ("", "", "")
        icon = f'<svg class="card-ic" viewBox="0 0 24 24">{ICONS.get(ic,"")}</svg>' if ic else ""
        cards += f'<div class="card"><strong>{icon}{t}</strong><span>{x}</span></div>'
    return (f'<section class="slide">{kicker(s)}<h2>{s["h2"]}</h2>'
            f'<p class="lead">{s.get("lead","")}</p><div class="grid-3">{cards}</div>{foot(s)}{notes(s)}</section>')

def r_scenarios(s):
    ill = ILLUS.get(s.get("illus", "branch"), ILLUS["branch"])
    rows = ""
    for num, sp, t, x in s.get("items", []):
        rows += (f'<div class="scn-card"><div class="scn-num">{num}</div>'
                 f'<svg class="scn-spark" viewBox="0 0 100 50" preserveAspectRatio="none" aria-hidden="true">{SPARKS.get(sp,SPARKS["linear"])}</svg>'
                 f'<div class="scn-txt"><strong>{t}</strong><span>{x}</span></div></div>')
    return (f'<section class="slide">{kicker(s)}<h2>{s["h2"]}</h2>'
            f'<div class="grid-2" style="grid-template-columns:1.34fr 0.66fr; align-items:center">'
            f'<div class="scn-list">{rows}</div>'
            f'<div class="illust-col">{ill}</div></div>{foot(s)}{notes(s)}</section>')

def r_flow(s):
    parts = []
    steps = s.get("steps", [])
    for i, st in enumerate(steps):
        t, sub = (st + [""])[:2] if isinstance(st, list) else (st, "")
        parts.append(f'<div class="flow-b">{t}<small>{sub}</small></div>')
        if i < len(steps) - 1:
            parts.append('<div class="flow-a">&rarr;</div>')
    return (f'<section class="slide">{kicker(s)}<h2>{s["h2"]}</h2>'
            f'<p class="lead">{s.get("lead","")}</p><div class="flow">{"".join(parts)}</div>{foot(s)}{notes(s)}</section>')

def r_statement(s):
    return (f'<section class="slide statement">{kicker(s)}<h1>{s["h1"]}</h1>'
            f'<p class="lead">{s.get("lead","")}</p>{notes(s)}</section>')

def r_bullets(s):
    lis = "".join(f'<li><strong>{a}</strong> {b}</li>' for a, b in s.get("bullets", []))
    return (f'<section class="slide">{kicker(s)}<h2>{s["h2"]}</h2>'
            f'<p class="lead">{s.get("lead","")}</p>'
            f'<ul style="line-height:1.6; font-size:calc(2.3cqw*var(--fs,1)); max-width:86%">{lis}</ul>{foot(s)}{notes(s)}</section>')

def r_quote(s):
    return (f'<section class="slide">{kicker(s)}<h2>{s.get("h2","")}</h2>'
            f'<div class="quote">{s["quote"]}</div>'
            f'<p class="lead" style="font-style:normal; font-size:calc(1.7cqw*var(--fs,1))">{s.get("by","")}</p>{notes(s)}</section>')

def r_demo(s):
    return (f'<section class="slide placeholder-slide">{kicker(s)}<h1>{s["h1"]}</h1>'
            f'<p class="lead">{s.get("lead","")}</p>{foot(s)}{notes(s)}</section>')

RENDER = {
 "title": r_title, "closing": r_closing, "team": r_team, "agenda": r_agenda,
 "divider": r_divider, "hero": r_hero, "kpi": r_kpi, "twocol": r_twocol,
 "cards2": r_cards2, "cards3": r_cards3, "scenarios": r_scenarios, "flow": r_flow,
 "statement": r_statement, "bullets": r_bullets, "quote": r_quote, "demo": r_demo,
}

# ----------------------------------------------------------------------------
# FRAMEWORK CSS (themeable). {V} placeholders filled from theme.
# ----------------------------------------------------------------------------
CSS = r"""
:root{
  --c-1:{c1}; --c-2:{c2}; --c-3:{c3};
  --accent:var(--c-1); --accent-soft:{soft}; --accent-line:{line};
  --paper:{paper}; --paper-soft:{papersoft};
  --ink:{ink}; --ink-2:{ink2}; --ink-3:{ink3};
  --rule:{rule}; --rule-soft:{rulesoft};
  --divider-bg:{divider}; --divider-ink:{divink};
  --r:{radius};
  --display:{display}; --serif:{serif}; --mono:{mono};
}
*{box-sizing:border-box; -webkit-font-smoothing:antialiased}
html{margin:0; padding:0; background:#0b0b0d; height:100%; overflow:hidden}
body{margin:0; padding:0; background:#0b0b0d; color:var(--ink); font-family:var(--serif); height:100vh; overflow-y:auto; overflow-x:hidden; display:flex; flex-direction:column}
body > .stage, body > .notes, body > .controls{flex:0 0 auto}
.stage{position:relative; background:var(--paper); overflow:hidden; aspect-ratio:16/9; max-height:calc(100vh - 170px); margin:18px auto 0; width:min(96vw, calc((100vh - 170px) * 16/9)); border-radius:8px; box-shadow:0 18px 60px rgba(0,0,0,0.4)}
.slides-host{position:absolute; top:0; left:0; width:1280px; height:720px; transform-origin:top left; transform:scale(var(--scale,1)); container-type:size; container-name:stage}
.slide{position:absolute; inset:0; padding:4.6% 7% 8.6%; display:none; flex-direction:column; justify-content:center; gap:2%; font-family:var(--serif)}
.slide.active{display:flex}
.slide h1{font-family:var(--display); font-weight:700; font-size:calc(5.29cqw*var(--fs,1)); letter-spacing:-0.02em; line-height:1.02; margin:0 0 1cqw}
.slide h2{font-family:var(--display); font-weight:600; font-size:calc(3.45cqw*var(--fs,1)); letter-spacing:-0.015em; line-height:1.1; margin:0 0 1.2cqw}
.slide h3{font-family:var(--display); font-weight:500; font-size:calc(1.95cqw*var(--fs,1)); color:var(--ink-2); margin:0 0 0.8cqw}
.slide p,.slide li{font-size:calc(1.78cqw*var(--fs,1)); line-height:1.5; color:var(--ink-2); margin:0 0 0.6cqw}
.slide ul,.slide ol{margin:0.6cqw 0 0; padding-left:1.2em}
.slide li{margin:0 0 0.6cqw}
.slide em{font-style:normal; background:linear-gradient(135deg,var(--c-2),var(--c-1) 55%,var(--c-3)); -webkit-background-clip:text; background-clip:text; color:transparent; padding-right:0.08em; margin-right:-0.08em}
.slide code{font-family:var(--mono); font-size:0.9em; background:var(--paper-soft); padding:0.1em 0.35em; border-radius:0.3em}
.slide .kicker{font-family:var(--mono); font-size:1.21cqw; color:var(--ink-3); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:1.1cqw}
.slide .kicker::before{content:""; display:inline-block; width:1.4cqw; height:0.16cqw; background:linear-gradient(90deg,var(--c-2),var(--c-1)); vertical-align:middle; margin-right:0.8cqw}
.slide .footnote{font-family:var(--mono); font-size:1.12cqw; color:var(--ink-3); position:absolute; left:7%; right:7%; bottom:3.2%; margin:0}
.slide .lead{font-family:var(--serif); font-style:italic; font-size:calc(2.24cqw*var(--fs,1)); color:var(--ink-2); max-width:80%}
.slide .grid-2{display:grid; grid-template-columns:1fr 1fr; gap:3%; margin-top:1.1cqw}
.slide .grid-3{display:grid; grid-template-columns:1fr 1fr 1fr; gap:2.5%; margin-top:1.1cqw}
.slide .card{padding:1.4cqw 1.6cqw; border:1px solid var(--rule); border-radius:0.8cqw; background:var(--paper-soft)}
.slide .card strong{font-family:var(--display); font-weight:600; display:flex; align-items:center; margin-bottom:0.4cqw; font-size:calc(1.78cqw*var(--fs,1)); color:var(--ink)}
.slide .card span{font-size:calc(1.49cqw*var(--fs,1)); color:var(--ink-2); line-height:1.45}
.slide .card-ic{width:1.5em; height:1.5em; flex:none; margin-right:0.5em; stroke:var(--c-1); fill:none; stroke-width:1.9; stroke-linecap:round; stroke-linejoin:round}
.slide .scn-list{display:flex; flex-direction:column; gap:1.35cqw}
.slide .scn-card{display:flex; align-items:center; gap:1.7cqw; padding:1.5cqw 1.9cqw; border:1px solid var(--rule); border-left:0.45cqw solid var(--c-1); border-radius:0.9cqw; background:var(--paper-soft)}
.slide .scn-num{flex:none; width:3.1cqw; height:3.1cqw; border-radius:0.75cqw; background:linear-gradient(135deg,var(--c-2),var(--c-1) 60%,var(--c-3)); color:#fff; font-family:var(--display); font-weight:700; font-size:1.85cqw; display:flex; align-items:center; justify-content:center; line-height:1}
.slide .scn-spark{flex:none; width:8.5cqw; height:4cqw; overflow:visible}
.slide .scn-spark .ax{stroke:var(--rule); stroke-width:1.4}
.slide .scn-spark .ln{fill:none; stroke:var(--c-1); stroke-width:4; stroke-linecap:round; stroke-linejoin:round}
.slide .scn-spark .dot{fill:var(--c-1)}
.slide .scn-spark .asy{stroke:var(--c-1); stroke-width:1.6; stroke-dasharray:2.6 2.6; opacity:0.4}
.slide .scn-txt{display:flex; flex-direction:column; gap:0.15cqw}
.slide .scn-txt strong{font-family:var(--display); font-weight:600; font-size:calc(2.2cqw*var(--fs,1)); color:var(--ink)}
.slide .scn-txt span{font-size:calc(1.72cqw*var(--fs,1)); color:var(--ink-2); line-height:1.4}
.slide .kpi-grid{display:grid; grid-template-columns:repeat(3,1fr); gap:1.6cqw; margin-top:2.4cqw}
.slide .kpi{display:flex; flex-direction:column; align-items:center; text-align:center; gap:1cqw; padding:2.4cqw 1cqw 2cqw; border:1px solid var(--rule); border-radius:1cqw; background:var(--paper-soft)}
.slide .kpi svg{width:3.6cqw; height:3.6cqw; stroke:var(--c-1); fill:none; stroke-width:1.8; stroke-linecap:round; stroke-linejoin:round}
.slide .kpi-num{font-family:var(--display); font-weight:700; font-size:4cqw; color:var(--c-1); line-height:1}
.slide .kpi-lbl{font-size:1.28cqw; color:var(--ink-3); line-height:1.3}
.slide .quote{font-family:var(--serif); font-style:italic; font-size:calc(2.7cqw*var(--fs,1)); color:var(--ink); padding-left:1.6cqw; border-left:4px solid var(--accent); margin:1.4cqw 0; max-width:84%; line-height:1.35}
.slide .tag{display:inline-block; font-family:var(--mono); font-size:calc(1.09cqw*var(--fs,1)); padding:0.24cqw 0.6cqw; border-radius:999px; background:var(--accent-soft); color:var(--accent); margin-right:0.5cqw}
.slide.title-slide{justify-content:flex-start; padding-top:7.5%}
.slide.title-slide .lead{max-width:60%}
.slide.title-slide h1{max-width:66%; font-size:calc(7.36cqw*var(--fs,1)); line-height:0.98}
.slide.title-slide .meta{margin-top:auto; display:grid; grid-template-columns:repeat(4,1fr); gap:1.1cqw; padding-top:1.4cqw; border-top:1px solid var(--rule)}
.slide.title-slide .meta strong{font-family:var(--mono); font-size:calc(1.09cqw*var(--fs,1)); color:var(--ink-3); text-transform:uppercase; letter-spacing:0.05em; display:block; margin-bottom:0.24cqw; font-weight:500}
.slide.title-slide .meta span{font-family:var(--display); font-size:calc(1.55cqw*var(--fs,1)); color:var(--ink); font-weight:500}
.slide.section-divider{background:var(--divider-bg); color:var(--divider-ink); text-align:center; align-items:center}
.slide.section-divider .kicker{color:var(--divider-ink); opacity:0.8}
.slide.section-divider .kicker::before{background:var(--divider-ink); opacity:0.6}
.slide.section-divider h1{color:var(--divider-ink); font-size:calc(7.36cqw*var(--fs,1)); max-width:88%}
.slide.section-divider h1 em{background:none; -webkit-text-fill-color:var(--divider-ink); color:var(--divider-ink); font-style:italic}
.slide.section-divider .lead{color:var(--divider-ink); opacity:0.92; font-style:italic; font-size:calc(2.95cqw*var(--fs,1)); max-width:80%; margin-left:auto; margin-right:auto}
.slide .illust-col{display:flex; align-items:center; justify-content:center; align-self:center}
.slide .illust-col .ill{width:auto; height:auto; max-width:30cqw; max-height:42cqh}
.slide .lector-grid{display:grid; grid-template-columns:repeat(5, 1fr); gap:1.6cqw; margin-top:2.2cqw}
.slide .lector{display:flex; flex-direction:column; align-items:center; text-align:center; gap:0.8cqw}
.slide .lector-photo{width:11cqw; height:11cqw; border-radius:50%; overflow:hidden; display:flex; align-items:center; justify-content:center; min-height:0; background:var(--accent-soft); border:2px solid var(--accent-line)}
.slide .lector-initials{position:relative; background:linear-gradient(135deg, var(--c-2), var(--c-1) 60%, var(--c-3))}
.slide .lector-initials::after{content:attr(data-initials); font-family:var(--display); font-weight:700; font-size:calc(3.6cqw*var(--fs,1)); color:#fff; letter-spacing:-0.02em}
.slide .lector-name{font-family:var(--display); font-weight:600; font-size:calc(1.55cqw*var(--fs,1)); line-height:1.15; color:var(--ink)}
.slide .lector-title{font-family:var(--mono); font-size:calc(1.05cqw*var(--fs,1)); color:var(--ink-3); text-transform:uppercase; letter-spacing:0.04em; line-height:1.3}
.slide.placeholder-slide{justify-content:center; align-items:center; text-align:center}
.slide.placeholder-slide h1{font-size:calc(5.06cqw*var(--fs,1))}
.slide.placeholder-slide .kicker{margin-bottom:1.6cqw}
.slide.placeholder-slide .lead{margin:0 auto; text-align:center; max-width:70%}
.slide.placeholder-slide .footnote{position:absolute; left:7%; right:7%; bottom:5.2%; margin:0; text-align:center}
.slide.bk{justify-content:flex-start}
.slide.bk h1{font-size:calc(4.6cqw*var(--fs,1)); margin:0 0 0.6cqw}
.slide.bk .bk-img{flex:1 1 auto; min-height:0; display:flex; align-items:center; justify-content:center; margin:0.5cqw 0}
.slide.bk .bk-img .ill{max-height:38cqh; max-width:54%}
.slide.bk .lead{max-width:none; font-size:1.98cqw; margin:0; line-height:1.4}
.agenda-flow{display:grid; grid-template-columns:repeat(3,1fr); gap:1.4cqw; align-items:stretch; margin-top:2.6cqw}
.af-b{background:var(--paper-soft); border:1px solid var(--accent-line); border-radius:1cqw; padding:1.5cqw 1.2cqw; font-family:var(--display); font-weight:600; font-size:1.85cqw; text-align:center; line-height:1.2; color:var(--ink); display:flex; align-items:center; justify-content:center}
.flow{display:flex; flex-wrap:nowrap; align-items:center; justify-content:center; gap:0.7cqw; margin:2cqw 0}
.flow-b{flex:1 1 0; min-width:0; background:var(--paper-soft); border:1px solid var(--accent-line); border-radius:1cqw; padding:1cqw 0.8cqw; font-family:var(--display); font-weight:600; font-size:calc(1.42cqw*var(--fs,1)); text-align:center; line-height:1.2; color:var(--ink)}
.flow-b small{display:block; margin-top:0.25cqw; font-family:var(--mono); font-weight:400; font-size:0.78em; color:var(--ink-3)}
.flow-a{flex:0 0 auto; font-family:var(--display); font-weight:700; font-size:calc(1.9cqw*var(--fs,1)); color:var(--accent)}
.slide .notes-data{display:none}
.notes{background:#15131a; color:#d7d2cb; padding:14px 24px; font-family:var(--serif); font-size:14.5px; line-height:1.5; max-height:150px; overflow-y:auto; border-top:1px solid #2a2630}
.notes .label{font-family:var(--mono); font-size:10.5px; color:var(--c-2); text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px}
.notes p{margin:0 0 6px}
.notes:empty,.notes.hidden{display:none}
.controls{background:#0e0e10; padding:10px 24px; display:flex; align-items:center; gap:12px; font-family:var(--mono); color:#cbcbd3; font-size:12px; border-top:1px solid #2a2630; flex-wrap:wrap}
.controls button,.controls a.home-link{font-family:var(--mono); font-size:12px; padding:6px 12px; border-radius:6px; border:1px solid #2a2630; background:#181520; color:#cbcbd3; cursor:pointer; text-decoration:none}
.controls button:hover,.controls a.home-link:hover{background:#221d2b; border-color:var(--c-1)}
.controls .counter{margin-left:auto; font-weight:500}
.controls .hint{color:#6b6b73; font-size:11px}
.progress{position:absolute; left:0; top:0; height:3px; background:linear-gradient(90deg,var(--c-2),var(--c-1)); transition:width 0.3s; z-index:10}
.slide.statement{justify-content:center; align-items:center; text-align:center}
.slide.statement h1{font-size:calc(5.2cqw*var(--fs,1)); max-width:90%}
.slide.statement .lead{margin:1cqw auto 0; max-width:74%; font-size:calc(2.5cqw*var(--fs,1))}
.slide .card,.slide .kpi,.slide .scn-card,.slide .flow-b,.af-b{border-radius:calc(0.95cqw*var(--r,1))}
.slide .scn-num{border-radius:calc(0.7cqw*var(--r,1))}
body.cs-outline .slide .card,body.cs-outline .slide .kpi,body.cs-outline .slide .scn-card,body.cs-outline .slide .flow-b,body.cs-outline .af-b{background:transparent}
body.cs-flat .slide .card,body.cs-flat .slide .kpi,body.cs-flat .slide .scn-card,body.cs-flat .slide .flow-b,body.cs-flat .af-b{border-color:transparent}
body.em-solid .slide em{background:none;-webkit-text-fill-color:var(--c-1);color:var(--c-1)}
@media (max-width:640px){ .controls{gap:6px; padding:8px 12px; font-size:11px} .controls .hint{display:none} }
"""

JS = r"""
const slides = document.querySelectorAll('.slide');
const notesEl = document.getElementById('notes');
const cur = document.getElementById('cur');
const total = document.getElementById('total');
const progress = document.getElementById('progress');
total.textContent = slides.length;
let idx = 0, gotoBuffer = '';
function showSlide(n){
  idx = Math.max(0, Math.min(slides.length - 1, n));
  slides.forEach((s, i) => s.classList.toggle('active', i === idx));
  cur.textContent = idx + 1;
  progress.style.width = ((idx + 1) / slides.length * 100) + '%';
  const nd = slides[idx].querySelector('.notes-data');
  notesEl.innerHTML = (nd && nd.textContent.trim() && !notesEl.classList.contains('hidden'))
    ? '<div class="label">// poznamka recnika</div><p>' + nd.innerHTML + '</p>' : '';
  if(notesEl.classList.contains('hidden')) notesEl.innerHTML='';
  history.replaceState(null,'','#'+(idx+1));
  fitActive();
}
const next=()=>showSlide(idx+1), prev=()=>showSlide(idx-1);
document.getElementById('next').onclick=next;
document.getElementById('prev').onclick=prev;
document.getElementById('first').onclick=()=>showSlide(0);
document.getElementById('last').onclick=()=>showSlide(slides.length-1);
document.getElementById('fs').onclick=()=>{ if(!document.fullscreenElement) document.documentElement.requestFullscreen?.(); else document.exitFullscreen?.(); };
document.addEventListener('fullscreenchange',()=>setTimeout(fitActive,80));
document.getElementById('toggleNotes').onclick=()=>{
  notesEl.classList.toggle('hidden');
  document.getElementById('toggleNotes').textContent = notesEl.classList.contains('hidden') ? 'Poznamky' : 'Skryt poznamky';
  showSlide(idx);
};
const stageEl=document.querySelector('.stage');
const hostEl=document.getElementById('slidesHost');
function fitStage(){ if(stageEl&&hostEl) hostEl.style.setProperty('--scale',(stageEl.clientWidth/1280)||1); }
function fitSlide(slide){
  if(!slide) return;
  slide.style.setProperty('--fs','1');
  const cl=slide.classList;
  if(cl.contains('title-slide')||cl.contains('section-divider')||cl.contains('placeholder-slide')||cl.contains('bk')||cl.contains('statement')
     || slide.querySelector('.stat-row, .agenda-flow, .lector-grid')) return;
  const isTwocol=!!slide.querySelector('.illust-col');
  const isFlow=!!slide.querySelector('.flow');
  const capFs=isTwocol?1.45:isFlow?1.5:1.9;
  const savedT=hostEl?hostEl.style.transform:''; if(hostEl) hostEl.style.transform='none';
  const cs=getComputedStyle(slide);
  const availH=slide.clientHeight-parseFloat(cs.paddingTop)-parseFloat(cs.paddingBottom);
  const availW=slide.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
  const prevJ=slide.style.justifyContent; slide.style.justifyContent='flex-start';
  const fns=[].slice.call(slide.querySelectorAll('.footnote')); fns.forEach(f=>f.style.marginTop='0');
  const measure=()=>{ let t=Infinity,b=-Infinity,l=Infinity,r=-Infinity;
    for(const c of slide.children){ if(c.classList.contains('notes-data')||c.classList.contains('footnote'))continue;
      const q=c.getBoundingClientRect(); if(q.height<1)continue; t=Math.min(t,q.top);b=Math.max(b,q.bottom);l=Math.min(l,q.left);r=Math.max(r,q.right);}
    return {h:b-t,w:r-l}; };
  const fits=(m)=>{ slide.style.setProperty('--fs',m); const z=measure(); return z.h<=availH*0.95 && z.w<=availW+1; };
  let best=1;
  if(fits(capFs)) best=capFs;
  else if(fits(1)){ let lo=1,hi=capFs; for(let i=0;i<12;i++){const m=(lo+hi)/2; if(fits(m)){best=m;lo=m;}else hi=m;} }
  else { let lo=0.6,hi=1; best=0.6; for(let i=0;i<12;i++){const m=(lo+hi)/2; if(fits(m)){best=m;lo=m;}else hi=m;} }
  slide.style.setProperty('--fs',best.toFixed(3));
  slide.style.justifyContent=prevJ; fns.forEach(f=>f.style.marginTop='');
  if(hostEl) hostEl.style.transform=savedT;
}
function fitActive(){ requestAnimationFrame(()=>{ fitStage(); fitSlide(slides[idx]); }); }
window.addEventListener('load', fitActive);
window.addEventListener('resize', fitActive);
fitStage();
document.addEventListener('keydown', e => {
  if(e.target.tagName==='INPUT'||e.target.tagName==='TEXTAREA') return;
  if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){ next(); e.preventDefault(); }
  else if(e.key==='ArrowLeft'||e.key==='PageUp'){ prev(); e.preventDefault(); }
  else if(e.key==='Home'){ showSlide(0); e.preventDefault(); }
  else if(e.key==='End'){ showSlide(slides.length-1); e.preventDefault(); }
  else if(e.key==='f'||e.key==='F'){ document.getElementById('fs').click(); }
  else if(e.key==='n'||e.key==='N'){ document.getElementById('toggleNotes').click(); }
  else if(e.key>='0'&&e.key<='9'){ gotoBuffer+=e.key; }
  else if(e.key==='Enter'&&gotoBuffer){ showSlide(parseInt(gotoBuffer)-1); gotoBuffer=''; }
  else if(e.key==='Escape'){ gotoBuffer=''; }
});
showSlide((parseInt(location.hash.replace('#',''))||1)-1);
"""

PAGE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='{favhex}'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family={font}&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body class="{bodyclass}">
<div class="stage">
  <div class="progress" id="progress"></div>
  <div class="slides-host" id="slidesHost">
{slides}
  </div>
</div>
<div class="notes" id="notes"></div>
<div class="controls">
  <button id="first">&laquo;</button>
  <button id="prev">&lsaquo; Zpet</button>
  <button id="next">Dal &rsaquo;</button>
  <button id="last">&raquo;</button>
  <button id="fs">Fullscreen (F)</button>
  <button id="toggleNotes">Skryt poznamky</button>
  <a class="home-link" href="../../index.html">Galerie sablon</a>
  <span class="hint">sipky / mezernik &middot; N poznamky &middot; F cela obrazovka &middot; cislo+Enter skok</span>
  <span class="counter"><span id="cur">1</span> / <span id="total">0</span></span>
</div>
<script>{js}</script>
</body>
</html>"""


def build_css(t):
    return (CSS
        .replace("{c1}", t["c1"]).replace("{c2}", t["c2"]).replace("{c3}", t["c3"])
        .replace("{soft}", t["soft"]).replace("{line}", t["line"])
        .replace("{paper}", t["paper"]).replace("{papersoft}", t["papersoft"])
        .replace("{ink}", t["ink"]).replace("{ink2}", t["ink2"]).replace("{ink3}", t["ink3"])
        .replace("{rule}", t["rule"]).replace("{rulesoft}", t["rulesoft"])
        .replace("{divider}", t["divider"]).replace("{divink}", t.get("divider_ink", "#ffffff"))
        .replace("{radius}", str(t.get("radius", 1)))
        .replace("{display}", t["display"]).replace("{serif}", t["serif"]).replace("{mono}", t["mono"]))


def render_deck(content):
    out = []
    for s in content["slides"]:
        fn = RENDER.get(s["type"])
        if not fn:
            continue
        out.append("    " + fn(s))
    return "\n".join(out)


def build_one(theme):
    path = os.path.join(CONTENT_DIR, theme["slug"].split("-")[0] + ".json")
    with open(path, encoding="utf-8") as f:
        content = json.load(f)
    # mark first slide active
    slides_html = render_deck(content)
    slides_html = slides_html.replace('<section class="slide ', '<section class="slide active ', 1) \
                             .replace('<section class="slide title-slide">', '<section class="slide active title-slide">', 1) \
        if 'class="slide active' not in slides_html else slides_html
    # robust active injection: first <section class="slide ...
    import re
    slides_html = re.sub(r'<section class="slide(?![^"]*active)', '<section class="slide active', slides_html, count=1)
    page = (PAGE
        .replace("{lang}", content.get("lang", "cs"))
        .replace("{title}", html.escape(content.get("title", theme["name"])))
        .replace("{favhex}", theme["c1"].replace("#", "%23"))
        .replace("{font}", theme["font"])
        .replace("{css}", build_css(theme))
        .replace("{bodyclass}", theme.get("bodyclass", ""))
        .replace("{slides}", slides_html)
        .replace("{js}", JS))
    outdir = os.path.join(TPL_DIR, theme["slug"])
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    return len(content["slides"])


if __name__ == "__main__":
    built = []
    for t in THEMES:
        jp = os.path.join(CONTENT_DIR, t["slug"].split("-")[0] + ".json")
        if not os.path.exists(jp):
            print("skip (no content):", t["slug"])
            continue
        n = build_one(t)
        built.append((t["slug"], n))
        print(f"built {t['slug']}: {n} slides")
    print(f"\nTotal templates built: {len(built)}")

# CLAUDE.md  (read this first, then stop)

Knihovna prezentačních šablon. **62 hotových decků na jednom sdíleném enginu.**
Tahle stránka je celý kontext, který potřebuješ. Needituj a nečti všechno, najdi
si v tabulce níže to jedno číslo (`NN`) a jdi rovnou na jeho soubory.

## Jak to funguje (30 sekund)

- `templates/NN-slug/index.html` jsou **vygenerované výstupy**. NIKDY je needituj ručně.
- Zdroj pravdy = `build/build.py` (engine + CSS/JS + `THEMES` = vzhledy) a
  `build/content/NN.json` (obsah jednoho decku, čistá data).
- Build: `python3 build/build.py` přepíše VŠECHNY `templates/*/index.html`.
  Galerie: `python3 build/gallery.py` přepíše kořenový `index.html`.

## Nejčastější úkol: upravit jeden konkrétní deck

1. Najdi `NN` v tabulce dole (uživatel ti řekne jméno nebo téma šablony).
2. Obsah (text, čísla, odrážky): edituj jen `build/content/NN.json`.
   Schéma a typy slidů jsou v `GUIDE.md` (otevři jen když potřebuješ shape).
3. Vzhled (barvy, fonty, radius, styl karet): edituj řádek `mk("NN-slug", ...)`
   resp. dict v `THEMES` v `build/build.py`. Pomocník `mk()` dopočítá odstíny;
   stačí `c1`, paper/ink, `dark`, `radius`, `bodyclass`.
4. Spusť `python3 build/build.py`. Hotovo. (Volitelně náhled: otevři ten
   `templates/NN-slug/index.html`.)
5. Deploy (jen na vyžádání): `vercel deploy --prod --yes` z kořene projektu.
   Web: https://27prestemplates.vercel.app  GitHub: kereptom/presentation-templates

## Co NEČÍST (šetři tokeny)

- Neotevírej všech 62 `templates/*/index.html` ani všech 62 `content/*.json`.
  Pracuj jen s tím jedním `NN`, které uživatel zadal.
- Nechoď do jiných projektů (21_, 23_ atd.). Engine sem byl převzat a očištěn,
  originály nepotřebuješ.
- `README.md` = uživatelský přehled, `GUIDE.md` = schéma slidů. Čti je jen
  cíleně, ne pro orientaci (tu máš tady).

## Pravidla (tvrdá)

- Obsah je ZÁMĚRNĚ ukázkový (dummy). Když přidáváš text, drž ten styl,
  pokud uživatel nechce reálná data.
- NIKDY dlouhou pomlčku (em dash, U+2014). Místo něj `:` `,` `.` nebo závorka.
  Platí i pro JSON obsah, CSS, commit zprávy, vše.
- Velikosti písma ve slidu jen v `cqw`, akcent jedním `<em>` v nadpisu.
- Ikony/ilustrace/grafy = jen klíče ze sad v `build/build.py` (`ICONS`,
  `ILLUS`, `SPARKS`); seznam je i v `GUIDE.md`.

## Engine: pár faktů, ať nehledáš

- 16 typů slidů (title, team, agenda, divider, hero, kpi, twocol, cards2,
  cards3, scenarios, flow, quote, bullets, statement, demo, closing).
- Auto-fit: textové slidy se zvětší; hero typy (title/divider/statement/
  placeholder) se jen zmenší při přetečení; `bk`/stat/agenda/lector se nefitují.
- Témata: světlá i tmavá (`dark=True`), `radius` škáluje rohy, `bodyclass`
  může být `cs-outline` (průhledné karty), `cs-flat` (bez rámečku), `em-solid`
  (plný akcent místo gradientu).
- Vše inline: vygenerovaný HTML je samostatný (CSS+JS uvnitř), bez závislostí.

## Index šablon (NN -> slug)

| NN | slug | název | téma | jazyk | režim |
|----|------|-------|------|-------|-------|
| 01 | `01-industrial-orange` | Industrial Orange | Průmysl a výroba | cs | light |
| 02 | `02-academia-indigo` | Academia Indigo | Věda a vzdělávání | cs | light |
| 03 | `03-corporate-navy` | Corporate Navy | Finance a poradenství | cs | light |
| 04 | `04-midnight-tech` | Midnight Tech | SaaS a startupy | en | dark |
| 05 | `05-editorial-serif` | Editorial Serif | Média a žurnalistika | cs | light |
| 06 | `06-health-teal` | Health Teal | Zdravotnictví a biotech | cs | light |
| 07 | `07-legal-charcoal` | Legal Charcoal | Právo a profesní služby | cs | light |
| 08 | `08-creative-magenta` | Creative Magenta | Design a kreativní agentura | en | light |
| 09 | `09-eco-green` | Eco Green | Udržitelnost a energetika | cs | light |
| 10 | `10-mono-minimal` | Mono Minimal | Architektura a minimalismus | en | light |
| 11 | `11-warm-education` | Warm Education | Vzdělávání a školení | cs | light |
| 12 | `12-vibrant-gradient` | Vibrant Gradient | Marketing a eventy | cs | light |
| 13 | `13-slate-consulting` | Slate Consulting | Strategie a poradenství | cs | light |
| 14 | `14-forest-outdoor` | Forest Outdoor | Outdoorová značka | cs | light |
| 15 | `15-rose-beauty` | Rose Beauty | Kosmetika a péče | en | light |
| 16 | `16-amber-stay` | Amber Stay | Hotelnictví | cs | light |
| 17 | `17-crimson-sport` | Crimson Sport | Sport a fitness | en | light |
| 18 | `18-teal-data` | Teal Data | Data a analytika | cs | light |
| 19 | `19-violet-audio` | Violet Audio | Hudba a zvuk | en | light |
| 20 | `20-sand-estate` | Sand Estate | Reality | cs | light |
| 21 | `21-sky-travel` | Sky Travel | Cestování a letectví | en | light |
| 22 | `22-plum-atelier` | Plum Atelier | Móda | cs | light |
| 23 | `23-carbon-lime` | Carbon Lime | Kyberbezpečnost | en | dark |
| 24 | `24-deep-space` | Deep Space | Letectví a kosmonautika | cs | dark |
| 25 | `25-noir-gold` | Noir Gold | Luxusní zboží | en | dark |
| 26 | `26-midnight-rose` | Midnight Rose | Noční život | cs | dark |
| 27 | `27-terminal-green` | Terminal Green | Vývojářské nástroje | en | dark |
| 28 | `28-obsidian-blue` | Obsidian Blue | Fintech | cs | dark |
| 29 | `29-broadsheet` | Broadsheet | Vydavatelství | en | light |
| 30 | `30-manifesto` | Manifesto | Politika a veřejná správa | cs | light |
| 31 | `31-gallery` | Gallery | Umění a muzea | en | light |
| 32 | `32-almanac` | Almanac | Zemědělství | cs | light |
| 33 | `33-bubblegum` | Bubblegum | Děti a hračky | en | light |
| 34 | `34-sunrise-wellness` | Sunrise Wellness | Wellness aplikace | cs | light |
| 35 | `35-pop-kitchen` | Pop Kitchen | Rozvoz jídla | en | light |
| 36 | `36-blueprint` | Blueprint | Inženýrství | cs | light |
| 37 | `37-wireframe` | Wireframe | UX výzkum | en | light |
| 38 | `38-mono-red` | Mono Red | Architektonické studio | en | light |
| 39 | `39-pastel-mint` | Pastel Mint | Papírnictví | cs | light |
| 40 | `40-cloud-infra` | Cloud Infra | Cloudová infrastruktura | en | light |
| 41 | `41-copper-works` | Copper Works | Strojírenství | cs | light |
| 42 | `42-indigo-learn` | Indigo Learn | E-learning | en | dark |
| 43 | `43-coral-hr` | Coral HR | Nábor a HR | cs | light |
| 44 | `44-olive-table` | Olive Table | Potraviny a nápoje | en | light |
| 45 | `45-berry-retail` | Berry Retail | Maloobchod | cs | light |
| 46 | `46-steel-logistics` | Steel Logistics | Logistika | en | light |
| 47 | `47-mustard-podcast` | Mustard | Podcast | cs | light |
| 48 | `48-ocean-lines` | Ocean Lines | Námořní doprava | en | light |
| 49 | `49-lavender-mind` | Lavender Mind | Duševní zdraví | cs | light |
| 50 | `50-graphite-auto` | Graphite Auto | Automobilový průmysl | en | dark |
| 51 | `51-sunset-tourism` | Sunset Tourism | Turistika | cs | light |
| 52 | `52-emerald-bank` | Emerald Bank | Bankovnictví | en | light |
| 53 | `53-clay-craft` | Clay and Craft | Keramika a řemeslo | cs | light |
| 54 | `54-neon-cyan` | Neon Cyan | Gaming | en | dark |
| 55 | `55-vintage-wine` | Vintage Wine | Vinařství | cs | light |
| 56 | `56-aqua-utility` | Aqua Utility | Vodárenství | en | light |
| 57 | `57-saffron` | Saffron | Restaurace | cs | light |
| 58 | `58-slate-gov` | Slate Gov | Veřejná správa | en | light |
| 59 | `59-magenta-social` | Magenta Social | Sociální sítě | cs | light |
| 60 | `60-pine-forestry` | Pine Forestry | Lesnictví | en | light |
| 61 | `61-bronze-exhibit` | Bronze Exhibit | Muzejní výstava | cs | light |
| 62 | `62-electric-robotics` | Electric Robotics | Robotika | en | dark |

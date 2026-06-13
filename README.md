# Prezentační šablony

Knihovna **12 prezentačních šablon** postavených na jednom sdíleném HTML enginu.
Engine pochází z reálných decků a je očištěný od obsahu: zůstaly jen styly,
komponenty a logika. Každá šablona je **samostatný HTML soubor** (veškerý CSS i
JS uvnitř), takže ji stačí zkopírovat a otevřít v prohlížeči. Žádný build krok
ani závislosti za běhu.

> **Pozor:** všechny šablony obsahují **ukázkový (dummy) obsah**. Jména, čísla
> i citace jsou smyšlené a slouží pouze k předvedení vizuálních stylů. Před
> reálným použitím obsah nahraďte vlastním.

Živá galerie: viz `index.html` (po nasazení na Vercel kořen webu).

---

## Co umí

- **16 typů slidů**: titulní, tým, agenda, předěl bloku, hero s ilustrací,
  KPI dashboard, dvousloupcový s ilustrací, karty 2x2, karty 3x2 s ikonami,
  číslované scénáře s mini grafy, procesní tok, citát, odrážky, statement,
  placeholder pro demo a závěrečný.
- **Auto-fit textu**: skript zvětší text tak, aby slide hezky zaplnil plochu.
- **Poznámky řečníka** pod prezentací (klávesa `N`).
- **Klávesová navigace**: šipky / mezerník listují, `F` celá obrazovka,
  `číslo + Enter` skočí na slide, `Home` / `End` na začátek a konec.
- **Container queries**: text škáluje s plátnem 16:9 na libovolné velikosti.
- **Inline SVG ilustrace a ikony** barvené přes téma, takže není potřeba žádný
  obrázkový asset.

---

## Struktura repozitáře

```
27_pres_templates/
├── index.html                 # galerie všech šablon (kořen webu)
├── README.md                  # tento soubor
├── GUIDE.md                   # referenční průvodce všemi typy slidů
├── templates/
│   └── NN-slug/index.html     # 12 hotových, samostatných šablon
├── gallery/shots/             # náhledy do galerie (PNG)
└── build/
    ├── build.py               # generátor: téma + obsah -> samostatný HTML
    ├── gallery.py             # generátor galerie index.html
    └── content/NN.json        # obsah každé šablony (data, ne kód)
```

Šablony v `templates/` jsou **vygenerované výstupy**. Zdrojem pravdy je
`build/build.py` (engine + témata) a `build/content/*.json` (obsah).

---

## Tři způsoby použití

### 1. Jen prezentovat
Otevřete `templates/<slug>/index.html` v prohlížeči. Hotovo. Soubor funguje
offline, obsahuje vše uvnitř.

### 2. Vyměnit obsah (doporučeno)
1. Najděte si šablonu se vzhledem, který se vám líbí (číslo `NN` v názvu složky).
2. Upravte text v `build/content/NN.json` (struktura viz `GUIDE.md`).
3. Spusťte:
   ```
   python3 build/build.py
   ```
   Přegeneruje se `templates/NN-slug/index.html` s vaším obsahem.

### 3. Nový vzhled (téma)
V `build/build.py` v seznamu `THEMES` přidejte nebo upravte záznam:
- `c1` `c2` `c3`: hlavní barva a gradient (akcenty, čísla, ilustrace).
- `display` `serif` `mono` a `font`: fonty (Google Fonts).
- `paper` `papersoft` `ink` `ink2` `ink3` `rule`: papír a text.
- `divider`: gradient na předělových slidech. `dark: True` pro tmavý režim.

Potom `python3 build/build.py`. Galerii obnovíte přes `python3 build/gallery.py`.

---

## Klávesové zkratky

| Klávesa | Akce |
|---|---|
| `→` / `mezerník` / `PageDown` | další slide |
| `←` / `PageUp` | předchozí slide |
| `Home` / `End` | první / poslední |
| `F` | celá obrazovka |
| `N` | poznámky řečníka |
| `číslo` + `Enter` | skok na slide |

---

## Nasazení (Vercel)

Repozitář je čistě statický. Stačí:
```
vercel deploy --prod
```
Kořen webu = galerie (`index.html`). Jednotlivé šablony jsou na
`/templates/<slug>/index.html`.

---

## Pravidla stylu (ať deck zůstane konzistentní)

- Velikosti písma v `cqw` (container query units), nikdy `px` pro text ve slidu.
- Jeden akcentní výraz na nadpis přes `<em>…</em>` (dostane barvu tématu).
- Nikdy nepoužívejte dlouhou pomlčku (em dash, U+2014). Místo něj `:` `,` `.` nebo závorku.
- Méně textu na slidu, detail do poznámek řečníka (`notes`).

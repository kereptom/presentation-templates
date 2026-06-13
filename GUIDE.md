# Průvodce typy slidů

Obsah každé šablony je jeden JSON soubor `build/content/NN.json`:

```json
{
  "lang": "cs",
  "title": "Titulek do záložky prohlížeče",
  "slides": [ { "type": "title", ... }, { "type": "kpi", ... } ]
}
```

Pořadí v poli `slides` = pořadí v prezentaci. Každý slide má `type` a pole podle
typu (níže). Skoro každý slide může mít `notes` (poznámka řečníka, na slidu není
vidět) a obsahové slidy `footnote` (drobná poznámka dole).

**Akcent:** do `h1` / `h2` dejte jeden `<em>výraz</em>`, dostane barvu tématu.
**Pomlčka:** nikdy nepoužívejte dlouhou pomlčku (em dash, U+2014), jen `:` `,` `.` nebo závorku.

---

## 1. `title` · titulní slide
Velký nadpis, podtitul, metařádek o čtyřech polích.
```json
{"type":"title","kicker":"// kontext","h1":"Název akce<br><em>podtitul</em>.","lead":"Jedna věta navíc.","meta":[["ŠTÍTEK","hodnota"],["ŠTÍTEK","hodnota"],["ŠTÍTEK","hodnota"],["ŠTÍTEK","hodnota"]],"notes":"..."}
```

## 2. `team` · tým / přednášející
Pět členů, místo fotek barevné kolečko s iniciálami (2 písmena).
```json
{"type":"team","kicker":"// tým","h2":"Kdo vás <em>provede</em>.","lead":"Podtitul.","members":[["JN","Jan Novák","Role"],["EK","Eva Krátká","Role"],["PM","Petr Malý","Role"],["LH","Lucie Horká","Role"],["TS","Tomáš Sýkora","Role"]],"notes":"..."}
```

## 3. `agenda` · agenda
Tři velké dlaždice.
```json
{"type":"agenda","kicker":"// program","h2":"Jak to <em>poběží</em>.","lead":"Podtitul.","blocks":["1 · První část","2 · Druhá část","3 · Třetí část"],"notes":"..."}
```

## 4. `divider` · předěl bloku
Velký nadpis na barevném gradientu. Používejte mezi bloky.
```json
{"type":"divider","kicker":"// blok 1","h1":"Název <em>bloku</em>.","lead":"Podtitul.","notes":"..."}
```

## 5. `hero` · hero s ilustrací
Velký nadpis, výrazná ilustrace, krátký popisek. `illus` viz seznam níže.
```json
{"type":"hero","kicker":"// myšlenka","h1":"Velká <em>pointa</em>.","illus":"network","lead":"Krátký popisek pod obrázkem.","footnote":"// zdroj","notes":"..."}
```

## 6. `kpi` · KPI dashboard
Tři karty (ikona, velké číslo, popisek) a pod nimi tři odrážky. `items` = trojice `[ikona, číslo, popisek]`.
```json
{"type":"kpi","kicker":"// čísla","h2":"Tři <em>čísla</em>.","items":[["trend_down","-32 %","popisek"],["clock","4 h","popisek"],["target","+18 %","popisek"]],"bullets":["Odrážka jedna.","Odrážka dvě.","Odrážka tři."],"footnote":"// zdroj","notes":"..."}
```

## 7. `twocol` · dvousloupcový s ilustrací
Odrážky vlevo (silné úvodní slovo + zbytek), ilustrace vpravo. Text se sám zvětší.
```json
{"type":"twocol","kicker":"// jak to funguje","h2":"Věc <em>v kostce</em>.","lead":"Podtitul.","bullets":[["Sbírá.","zbytek věty"],["Učí se.","zbytek věty"],["Varuje.","zbytek věty"]],"illus":"gears","footnote":"// pozn.","notes":"..."}
```

## 8. `cards2` · karty 2x2
Čtyři karty (nadpis + text).
```json
{"type":"cards2","kicker":"// varianty","h2":"Dva <em>přístupy</em>.","lead":"Podtitul.","cards":[["Nadpis","Text."],["Nadpis","Text."],["Nadpis","Text."],["Nadpis","Text."]],"footnote":"// pozn.","notes":"..."}
```

## 9. `cards3` · karty 3x2 s ikonami
Šest karet, každá s ikonou v záhlaví. `cards` = trojice `[ikona, nadpis, text]`.
```json
{"type":"cards3","kicker":"// nástroje","h2":"Co kde <em>nasadit</em>.","lead":"Podtitul.","cards":[["cpu","Nadpis","Text."],["activity","Nadpis","Text."],["alert","Nadpis","Text."],["doc","Nadpis","Text."],["shield","Nadpis","Text."],["users","Nadpis","Text."]],"footnote":"// pozn.","notes":"..."}
```

## 10. `scenarios` · číslované scénáře s mini grafy
Tři karty s číslem, mini trendovým grafem a textem, vedle ilustrace. `items` = `[číslo, graf, nadpis, text]`.
```json
{"type":"scenarios","kicker":"// kam to míří","h2":"Tři <em>scénáře</em>.","items":[["1","plateau","Plató","Text."],["2","expo","Zrychlení","Text."],["3","selfimp","Skok","Text."]],"illus":"branch","footnote":"// pozn.","notes":"..."}
```

## 11. `flow` · procesní tok
Pět kroků se šipkami. `steps` = `[nadpis, malý popisek]`.
```json
{"type":"flow","kicker":"// postup","h2":"Od A k <em>Z</em>.","lead":"Podtitul.","steps":[["Krok 1","popisek"],["Krok 2","popisek"],["Krok 3","popisek"],["Krok 4","popisek"],["Krok 5","popisek"]],"footnote":"// pozn.","notes":"..."}
```

## 12. `quote` · citát
Výrazný citát s levou linkou. `h2` nechte prázdné.
```json
{"type":"quote","kicker":"// myšlenka","h2":"","quote":"Text citátu.","by":"Autor citátu","notes":"..."}
```

## 13. `bullets` · odrážky s důrazem
Jednoduchý seznam, silné úvodní slovo + zbytek. Text se sám zvětší.
```json
{"type":"bullets","kicker":"// na co myslet","h2":"Tři <em>pravidla</em>.","lead":"Podtitul.","bullets":[["Vlastník.","zbytek"],["Cíl.","zbytek"],["Schválení.","zbytek"]],"footnote":"// pozn.","notes":"..."}
```

## 14. `statement` · statement
Jedna velká věta vycentrovaná na stránce.
```json
{"type":"statement","kicker":"// pointa","h1":"Vyhrává <em>disciplína</em>.","lead":"Podtitul.","notes":"..."}
```

## 15. `demo` · placeholder pro demo / přestávku
Vycentrovaný velký nadpis.
```json
{"type":"demo","kicker":"// živá ukázka","h1":"Demo za <em>30 sekund</em>.","lead":"Podtitul.","footnote":"// pozn.","notes":"..."}
```

## 16. `closing` · závěrečný slide
Stejný styl jako titulní, vhodný na kontakt a výzvu k akci.
```json
{"type":"closing","kicker":"// děkujeme","h1":"Jdeme do toho <em>společně</em>.","lead":"Podtitul.","meta":[["Kontakt","mail"],["Web","url"],["Krok","akce"],["Materiály","odkaz"]],"notes":"..."}
```

---

## Klíče ikon (pro `kpi` a `cards3`)

```
trend_up  trend_down  bars  dollar  grid  pie  alert  activity
clock  calendar  shield  users  target  zap  globe  leaf
cpu  doc  lock  heart  compass  rocket
```

## Klíče ilustrací (pro `hero`, `twocol`, `scenarios`)

```
network  gears  growth  shield  doc  brain  cloud  layers
target  branch  chip  people  chat  flask  scale  megaphone
```

## Klíče mini grafů (pro `scenarios`)

```
plateau   náběh a zastavení (plató)
expo      exponenciální růst
selfimp   prudký růst k asymptotě
linear    rovnoměrný růst
decline   pokles
```

---

## Přidání nové ikony nebo ilustrace

V `build/build.py`:
- ikona: přidejte do slovníku `ICONS` SVG `path`/`rect` (viewBox 0 0 24 24, jen tahy).
- ilustrace: přidejte do `ILLUS` přes pomocnou funkci `_ill(body)` (tahy v barvě `var(--c-1)`).
- mini graf: přidejte do `SPARKS` (viewBox 0 0 100 50).

Pak `python3 build/build.py`.

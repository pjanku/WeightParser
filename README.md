# Váženky

Jednoduchý nástroj pro hromadné zpracování PDF váženek (vážních lístků / dodacích listů).
Z každého PDF ve vybrané složce vytáhne klíčové údaje a uloží je do jedné Excel tabulky.

## Co skript dělá

1. Otevře dialog pro výběr složky s PDF váženkami.
2. Projde všechny soubory `*.pdf` ve složce (bez podsložek).
3. Z textu každého PDF vyčte:
   - **Číslo váženky** – např. `2026/0031966` → `31966`
   - **Kód dodavatele** – kód ve formátu písmeno + číslice, např. `E201`
   - **Datum** – bez času, např. `02.10.2026 14:07` → `02.10.2026`
   - **Netto** – hodnotu `Netto [kg]` převede na tuny (např. `27480` → `27.480`)
4. Výsledky seřadí podle čísla váženky a uloží do souboru `vazenky.xlsx`
   ve stejné složce, kde jsou PDF.
5. V konzoli vypíše souhrn: počet zpracovaných souborů a seznam souborů, které se
   nepodařilo zpracovat, včetně důvodu.

Výstupní Excel má sloupce: `Číslo`, `Kód dodavatele`, `Datum`, `Netto [t]`.

> PDF musí obsahovat textovou vrstvu. Naskenované obrázky bez OCR zpracovat nejdou.

## Stažení (Windows)

Hotový `.exe` je ke stažení v sekci [Releases](https://github.com/pjanku/WeightParser/releases/latest):

- [`Vazenky-Windows.zip`](https://github.com/pjanku/WeightParser/releases/latest/download/Vazenky-Windows.zip) – doporučeno (exe + licence)
- [`Vazenky.exe`](https://github.com/pjanku/WeightParser/releases/latest/download/Vazenky.exe)

Exe není podepsané certifikátem, proto při prvním spuštění může Windows SmartScreen
zobrazit varování. Spustíte ho přes „Další informace“ → „Přesto spustit“.

## Spuštění ze zdrojového kódu

Vyžaduje Python 3.13 (s Tkinter).

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Build

Exe se sestavuje přes GitHub Actions (`.github/workflows/build-widnows.yml`) pomocí PyInstalleru:

- **ruční spuštění** (`workflow_dispatch`) – exe se nahraje jako artefakt buildu
  (ke stažení jen po přihlášení na GitHub),
- **push tagu `v*`** – navíc se vytvoří GitHub Release s `Vazenky.exe` a `Vazenky-Windows.zip`.

```bash
git tag v1.0.0
git push origin v1.0.0
```

Lokální build:

```bash
pyinstaller --onefile --name Vazenky main.py
```

## Licence použitých knihoven

Všechny použité knihovny jsou open source a jejich licence umožňují použití
i distribuci v rámci projektu pod licencí MIT.

| Knihovna | Verze | Licence | Použití | Poznámka |
|----------|-------|---------|---------|----------|
| [pypdf](https://github.com/py-pdf/pypdf) | 6.1.1 | BSD-3-Clause | čtení textu z PDF | permisivní, součástí exe |
| [openpyxl](https://foss.heptapod.net/openpyxl/openpyxl) | 3.1.5 | MIT | zápis Excelu | permisivní, součástí exe |
| [et_xmlfile](https://foss.heptapod.net/openpyxl/et_xmlfile) | 2.0.0 | MIT | závislost openpyxl | permisivní, součástí exe |
| [PyInstaller](https://github.com/pyinstaller/pyinstaller) | 6.16.0 | GPL-2.0-or-later s výjimkou pro bootloader | pouze build exe | viz níže |
| Python + Tkinter | 3.13 | PSF License | runtime, dialog pro výběr složky | permisivní, součástí exe |
| Tcl/Tk | – | Tcl/Tk License (BSD-style) | GUI backend Tkinteru | permisivní, součástí exe |

**PyInstaller:** Přestože je PyInstaller licencován pod GPL, jeho licence obsahuje
výslovnou výjimku: exe soubory, které jím vzniknou, lze šířit pod libovolnou licencí
(včetně MIT nebo proprietární), pokud se nemění samotný PyInstaller. GPL se proto
na tento projekt ani na výsledné `Vazenky.exe` nevztahuje.

**Distribuce exe:** Licence BSD, MIT a PSF vyžadují při šíření binárek zachovat
copyright a text licence. Proto `Vazenky-Windows.zip` obsahuje kromě exe i soubor
`THIRD_PARTY_LICENSES.txt` s plnými texty licencí všech zabalených komponent a soubor
`LICENSE` tohoto projektu. `THIRD_PARTY_LICENSES.txt` se při buildu generuje skriptem
`scripts/third_party_licenses.py` z nainstalovaných balíčků, takže vždy odpovídá
verzím, které jsou v exe skutečně zabalené.

## Licence

Tento projekt je licencován pod licencí MIT, plný text je v souboru [LICENSE](LICENSE).

```
MIT License

Copyright (c) 2026 Peter Janku

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
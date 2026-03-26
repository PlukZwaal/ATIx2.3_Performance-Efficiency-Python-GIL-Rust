# ATIX2.3 — Performance & Efficiency: Python GIL vs Rust

## Versies

| Tool | Versie |
|------|--------|
| Python (met GIL) | 3.13.12 |
| Python (zonder GIL) | 3.13.12t |
| Rust | 1.94.0 |
| Cargo | 1.94.0 |

---

## Vereisten voordat je begint

### 1. Visual Studio Build Tools (verplicht voor Rust op Windows)

Rust heeft een C++ linker nodig op Windows. Zonder deze tools mislukken alle `cargo build` commando's.

1. Ga naar: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Download en start de **Visual Studio Build Tools** installer
3. Vink in het installatiescherm aan: **"Desktop development with C++"**
4. Wacht tot de installatie klaar is en herstart je terminal

> Als je dit al hebt via een volledige Visual Studio installatie, sla dan deze stap over.

---

### 2. Rust & Cargo installeren

1. Ga naar: https://rustup.rs/
2. Download en voer `rustup-init.exe` uit
3. Kies optie 1 (standaard installatie)
4. **Sluit je terminal en open een nieuwe** zodat de PATH-wijzigingen actief worden
5. Controleer de installatie:

```bash
rustc --version
cargo --version
```

---

### 3. Python installeren (twee versies naast elkaar)

Je hebt **twee aparte Python-installaties** nodig:

#### Python 3.13 (met GIL) — de normale versie
1. Ga naar: https://www.python.org/downloads/
2. Download **Python 3.13.x** (de gewone versie, geen "t")
3. Vink bij installatie **"Add Python to PATH"** aan
4. Controleer na installatie:

```bash
python --version
# Verwacht: Python 3.13.x
```

#### Python 3.13t (zonder GIL) — de free-threaded versie
1. Ga naar dezelfde downloadpagina: https://www.python.org/downloads/
2. Scroll naar de gewenste 3.13-release en klik op **"All files"**
3. Download het bestand met **`t`** in de naam, bijv. `python-3.13.0t-amd64.exe`
4. Installeer dit **naast** de normale versie — vink **NIET** "Add to PATH" aan, want dat overschrijft je normale Python
5. Zoek na installatie het installatiepad op. Standaard staat het ergens als:
   ```
   C:\Users\<jouw naam>\AppData\Local\Programs\Python\Python313t\
   ```
   of
   ```
   C:\Program Files\Python313t\
   ```

6. **Voeg dit pad handmatig toe aan je PATH:**
   - Zoek op "omgevingsvariabelen" in het Windows-startmenu
   - Klik op "Omgevingsvariabelen bewerken"
   - Selecteer onder "Gebruikersvariabelen" de variabele `Path` en klik op **Bewerken**
   - Voeg het pad toe naar de map waar `python3.13t.exe` staat (de map, niet het .exe-bestand zelf)
   - Klik OK en **sluit je terminal volledig af**

7. Open een **nieuwe** terminal en controleer:

```bash
python3.13t --version
# Verwacht: Python 3.13.xt (let op de "t" aan het eind)
```

> Als `python3.13t` niet herkend wordt, klopt het PATH nog niet. Controleer of je het juiste mappad hebt toegevoegd en of je een nieuwe terminal hebt geopend.

---

## Installatie & Build

### Stap 1 — Repository clonen

```bash
git clone <repository-url>
cd ATIX2.3_Performance-Efficiency-Python-GIL-Rust
```

### Stap 2 — Rust binaries bouwen

Voer de volgende commando's uit vanuit de **root-directory** van het project. Dit duurt de eerste keer een paar minuten omdat Cargo alle dependencies downloadt en compileert.

```bash
cargo build --release --manifest-path research1/rust/Cargo.toml
cargo build --release --manifest-path research2/rust/Cargo.toml
cargo build --release --manifest-path research3/rust/Cargo.toml
cargo build --release --manifest-path research4/rust/Cargo.toml
```

Na het bouwen staan de binaries hier:

```
research1/rust/target/release/single_thread.exe
research1/rust/target/release/multi_thread.exe
research2/rust/target/release/single_thread.exe
research2/rust/target/release/multi_thread.exe
research3/rust/target/release/single_thread.exe
research3/rust/target/release/multi_thread.exe
research3/rust/target/release/scale_thread.exe
research4/rust/target/release/single_thread.exe
research4/rust/target/release/multi_thread.exe
```

> De `target/` mappen staan in `.gitignore`. Na een nieuwe `git clone` moet je de binaries altijd opnieuw bouwen.

---

### Stap 3 — Python virtuele omgevingen (alleen voor Research 2)

Research 2 gebruikt Pillow voor beeldbewerking. Pillow moet apart geïnstalleerd worden in twee omgevingen — één met GIL, één zonder.

Voer onderstaande commando's uit vanuit de **root-directory**:

```bash
# Omgeving MET GIL (normale Python)
python -m venv research2/.venv-gil
research2\.venv-gil\Scripts\activate
pip install pillow
deactivate
```

```bash
# Omgeving ZONDER GIL (free-threaded Python)
# Vervang het pad als python3.13t niet in je PATH staat:
# "C:\Users\<naam>\AppData\Local\Programs\Python\Python313t\python.exe"
python3.13t -m venv research2/.venv-nogil
research2\.venv-nogil\Scripts\activate
pip install pillow
deactivate
```

> Als `python3.13t` niet werkt, gebruik dan het volledige pad naar de executable, bijvoorbeeld:
> `"C:\Users\Jan\AppData\Local\Programs\Python\Python313t\python.exe" -m venv research2/.venv-nogil`

---

## Datasets

### Research 1 — Sentiment Dataset (1 miljoen tweets)

Download via: https://www.kaggle.com/datasets/tariqsays/sentiment-dataset-with-1-million-tweets

Plaats het gedownloade bestand als volgt (hernoem het indien nodig naar `dataset.csv`):

```
research1/
└── dataset.csv
```

### Research 2 — Intel Image Classification

Download via: https://www.kaggle.com/datasets/puneet6060/intel-image-classification

Pak het archief uit en plaats de afbeeldingen zo (alle .jpg/.png bestanden direct in de `images/` map):

```
research2/
└── images/
    ├── afbeelding1.jpg
    ├── afbeelding2.jpg
    └── ...
```

### Research 3 & 4 — Geen dataset vereist

Deze tests genereren hun eigen data.

---

## Benchmarks uitvoeren

### Hyperfine installeren

De benchmarks gebruiken [Hyperfine](https://github.com/sharkdp/hyperfine). Installeren via:

```bash
# Via winget (aanbevolen op Windows)
winget install sharkdp.hyperfine

# Of via Cargo
cargo install hyperfine
```

Controleer na installatie (in een nieuwe terminal):

```bash
hyperfine --version
```

---

Voer alle benchmarks uit vanuit de **root-directory** van het project. Elke benchmark doet 2 warmup-runs en minimaal 10 meetiteraties.

### Research 1 — Grote dataset verwerking

```bash
hyperfine --warmup 2 "python research1/python/single_thread.py"
hyperfine --warmup 2 "python3.13t -X gil=0 research1/python/single_thread.py"
hyperfine --warmup 2 ".\research1\rust\target\release\single_thread.exe"
hyperfine --warmup 2 "python research1/python/multi_thread.py"
hyperfine --warmup 2 "python3.13t -X gil=0 research1/python/multi_thread.py"
hyperfine --warmup 2 ".\research1\rust\target\release\multi_thread.exe"
```

### Research 2 — Parallelle beeldbewerking

```bash
hyperfine --warmup 2 "research2\.venv-gil\Scripts\python research2\python\single_thread.py"
hyperfine --warmup 2 "research2\.venv-nogil\Scripts\python research2\python\single_thread.py"
hyperfine --warmup 2 ".\research2\rust\target\release\single_thread.exe"
hyperfine --warmup 2 "research2\.venv-gil\Scripts\python research2\python\multi_thread.py"
hyperfine --warmup 2 "research2\.venv-nogil\Scripts\python research2\python\multi_thread.py"
hyperfine --warmup 2 ".\research2\rust\target\release\multi_thread.exe"
```

### Research 3 — Priemgetalberekening

```bash
hyperfine --warmup 2 "python research3/python/single_thread.py"
hyperfine --warmup 2 "python3.13t -X gil=0 research3/python/single_thread.py"
hyperfine --warmup 2 ".\research3\rust\target\release\single_thread.exe"
hyperfine --warmup 2 "python research3/python/multi_thread.py"
hyperfine --warmup 2 "python3.13t -X gil=0 research3/python/multi_thread.py"
hyperfine --warmup 2 ".\research3\rust\target\release\multi_thread.exe"
```

#### Research 3 — Schaalbaarheidstest (1 t/m 6 threads)

Voor de schaalbaarheidstest pas je `NUM_THREADS` bovenaan in beide bestanden aan en run je onderstaande commando's voor elke waarde (1, 2, 3, 4, 5 en 6). Bouw na elke aanpassing van het Rust-bestand opnieuw met `cargo build --release`.

```bash
# Python NO-GIL schaalbaarheid
hyperfine --warmup 2 "python3.13t -X gil=0 research3/python/scale_thread.py"

# Rust schaalbaarheid
hyperfine --warmup 2 ".\research3\rust\target\release\scale_thread.exe"
```

### Research 4 — Monte Carlo Pi

```bash
hyperfine --warmup 2 "python research4/python/single_thread.py"
hyperfine --warmup 2 "python3.13t -X gil=0 research4/python/single_thread.py"
hyperfine --warmup 2 ".\research4\rust\target\release\single_thread.exe"
hyperfine --warmup 2 "python research4/python/multi_thread.py"
hyperfine --warmup 2 "python3.13t -X gil=0 research4/python/multi_thread.py"
hyperfine --warmup 2 ".\research4\rust\target\release\multi_thread.exe"
```

---

## Veelvoorkomende problemen

| Fout | Oorzaak | Oplossing |
|------|---------|-----------|
| `error: linker 'link.exe' not found` | Visual Studio Build Tools ontbreken | Installeer "Desktop development with C++" via VS Build Tools |
| `python3.13t` wordt niet herkend | python3.13t staat niet in PATH | Voeg het installatiepad van Python 3.13t handmatig toe aan je PATH |
| `python` wijst naar de verkeerde versie | Meerdere Python-versies in PATH | Controleer met `where python` welk pad als eerste gevonden wordt |
| `cargo build` mislukt na clonen | `target/` staat in `.gitignore` | Voer alle vier `cargo build` commando's opnieuw uit |
| `Error: dataset.csv not found` | Dataset staat op de verkeerde plek | Zorg dat het bestand direct in `research1/` staat, niet in een submap |
| `Error: input directory not found` | `images/` map ontbreekt | Zorg dat afbeeldingen in `research2/images/` staan |
| `hyperfine` wordt niet herkend | Hyperfine niet geïnstalleerd of niet in PATH | Installeer via `winget install sharkdp.hyperfine` en herstart terminal |
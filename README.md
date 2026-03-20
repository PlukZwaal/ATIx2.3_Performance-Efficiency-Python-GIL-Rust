# ATIX2.3_Performance-Efficiency-Python-GIL-Rust

## Versies

| Tool | Versie |
|------|--------|
| Python (met GIL) | 3.13.12 |
| Python (zonder GIL) | 3.13.12t |
| Rust | 1.94.0 |
| Cargo | 1.94.0 |

---

## Installatie & Build

### Rust binaries bouwen

Voer deze commando's uit vanuit de **root-directory** van het project.

```bash
cargo build --release --manifest-path research1/rust/Cargo.toml
cargo build --release --manifest-path research2/rust/Cargo.toml
cargo build --release --manifest-path research3/rust/Cargo.toml
cargo build --release --manifest-path research4/rust/Cargo.toml
```

De gecompileerde binaries komen terecht in:
```
research1/rust/target/release/single_thread.exe
research1/rust/target/release/multi_thread.exe
research2/rust/target/release/single_thread.exe
research2/rust/target/release/multi_thread.exe
research3/rust/target/release/single_thread.exe
research3/rust/target/release/multi_thread.exe
research4/rust/target/release/single_thread.exe
research4/rust/target/release/multi_thread.exe
```

> De `target/` mappen staan in `.gitignore` en worden niet meegenomen in de repository. Bouw de binaries altijd lokaal na het clonen.

### Python virtuele omgevingen (alleen Research 2)

Research 2 vereist twee aparte omgevingen voor Pillow — één met GIL, één zonder.

```bash
python -m venv research2/.venv-gil
research2/.venv-gil/Scripts/activate
pip install pillow
deactivate

python3.13t -m venv research2/.venv-nogil
research2/.venv-nogil/Scripts/activate
pip install pillow
deactivate
```

---

## Datasets

### Research 1 — Sentiment Dataset (1 miljoen tweets)
Download: https://www.kaggle.com/datasets/tariqsays/sentiment-dataset-with-1-million-tweets

Plaats het bestand als volgt:
```
research1/
└── dataset.csv
```

### Research 2 — Intel Image Classification
Download: https://www.kaggle.com/datasets/puneet6060/intel-image-classification

Plaats de afbeeldingen als volgt:
```
research2/
└── images/
    ├── afbeelding1.jpg
    ├── afbeelding2.jpg
    └── ...
```

### Research 3 & 4 — Geen dataset vereist
Deze tests zijn volledig self-contained.

---

## Benchmarks uitvoeren

Voer alle commando's uit vanuit de **root-directory**. Elke benchmark heeft 2 warmup-runs en minimaal 10 meetiteraties.

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

### Research 4 — Monte Carlo Pi

```bash
hyperfine --warmup 2 "python research4/python/single_thread.py"
hyperfine --warmup 2 "python3.13t -X gil=0 research4/python/single_thread.py"
hyperfine --warmup 2 ".\research4\rust\target\release\single_thread.exe"
hyperfine --warmup 2 "python research4/python/multi_thread.py"
hyperfine --warmup 2 "python3.13t -X gil=0 research4/python/multi_thread.py"
hyperfine --warmup 2 ".\research4\rust\target\release\multi_thread.exe"
```
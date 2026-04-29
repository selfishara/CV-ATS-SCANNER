# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ATS CV Scanner is a CLI tool that reads CVs (`.txt`, `.pdf`, `.docx`) and scores them against predefined job profiles using keyword and section matching.

## Running the App

```bash
pip install -r requirements.txt
python main.py
```

## Architecture

The project has four modules with a clear separation of responsibilities:

- **[lector.py](lector.py)** — File I/O layer. `leer_cv(ruta)` dispatches to format-specific readers (`leer_txt`, `leer_pdf`, `leer_docx`). `listar_cvs(carpeta)` returns sorted filenames for `.txt`, `.pdf`, `.docx` files.

- **[analizador.py](analizador.py)** — Analysis engine. `PERFILES_TRABAJO` is a dict of job profiles (currently: `"Desarrollador Python"`, `"Marketing Digital"`, `"Administracion"`), each with `palabras_clave` and `secciones_esperadas`. `analizar_cv(texto, perfil)` returns a dict with `puntuacion` (0–100), `categoria` (`"excelente"` ≥85, `"bueno"` ≥65, else `"mejorable"`), and found/missing keywords and sections. Scoring weights: 70% keywords, 30% sections. All text matching is accent-insensitive and case-insensitive via `normalizar_texto()`.

- **[utilidades.py](utilidades.py)** — Regex utilities and report generation. `extraer_email`, `extraer_telefono`, `extraer_url` extract contact info via `re.findall`. `generar_reporte(nombre_cv, resultados, info_contacto)` writes a formatted `.txt` report to `reportes/`.

- **[main.py](main.py)** — Interactive CLI menu. Reads CVs from `cvs/` and outputs reports to `reportes/` (both auto-created). All 5 menu options are fully implemented: list CVs, select profile, analyze one CV, analyze all CVs, view generated reports.

## Adding Job Profiles

Add entries directly to `PERFILES_TRABAJO` in [analizador.py](analizador.py). Each profile needs `palabras_clave` (list of strings) and `secciones_esperadas` (list of strings). No other changes required — `obtener_perfiles_trabajo()` and the menu selection pick them up automatically.

## Sample CVs

Three sample CVs are included in `cvs/`:

| File | Format | Target profile |
|------|--------|----------------|
| `ana_garcia_cv.txt` | .txt | Desarrollador Python |
| `carlos_mendoza_cv.docx` | .docx | Marketing Digital |
| `maria_lopez_cv.pdf` | .pdf | Administración |

Los CVs de ejemplo fueron generados con un script Node.js de un solo uso (ya eliminado).

## Project Status

All 5 phases from [PHASES.md](PHASES.md) are complete.

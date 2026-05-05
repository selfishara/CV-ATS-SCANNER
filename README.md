# ATS CV Scanner

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-27%20passing-brightgreen)](#tests)
[![Status](https://img.shields.io/badge/status-stable-success)](#estado-del-proyecto)

Aplicación de consola en Python que actúa como un **ATS (Applicant Tracking System)** simplificado: lee currículums en `.txt`, `.pdf` y `.docx`, los puntúa contra perfiles de trabajo predefinidos, extrae información de contacto y genera reportes en texto plano.

---

## Tabla de contenidos

- [Características](#características)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Uso](#uso)
  - [Menú principal](#menú-principal)
  - [Ejemplo de salida](#ejemplo-de-salida)
  - [Ejemplo de reporte generado](#ejemplo-de-reporte-generado)
- [Perfiles de trabajo incluidos](#perfiles-de-trabajo-incluidos)
- [Cómo añadir tu propio perfil](#cómo-añadir-tu-propio-perfil)
- [Algoritmo de puntuación](#algoritmo-de-puntuación)
- [CVs de ejemplo](#cvs-de-ejemplo)
- [Tests](#tests)
- [Troubleshooting](#troubleshooting)
- [Estado del proyecto](#estado-del-proyecto)

---

## Características

- **Multi-formato**: lee `.txt`, `.pdf` y `.docx` con un único punto de entrada (`leer_cv`).
- **6 perfiles** predefinidos (tech y no-tech): Desarrollador Python, Marketing Digital, Administración, DAM, DAW, QA Automation.
- **Puntuación 0–100** ponderada (70% palabras clave + 30% secciones) y categorización en `excelente / bueno / mejorable`.
- **Matching robusto**: insensible a mayúsculas y acentos, con *word boundaries* para evitar falsos positivos (`SQL` ya no matchea dentro de `MySQL`).
- **Detección automática de mejor perfil**: clasifica un CV contra los 6 perfiles y muestra el ranking.
- **Extracción de contacto** vía regex: emails, teléfonos españoles (+34), URLs de LinkedIn y GitHub.
- **Reportes** en texto plano por CV en la carpeta `reportes/`.
- **Output en color** en consola (verde/amarillo/rojo según categoría) gracias a `colorama`.
- **Tests automatizados** con `pytest` (27 tests).

---

## Estructura del proyecto

```
cv-ats-scanner/
├── main.py              # Menú interactivo + integración
├── lector.py            # Lectura de archivos por formato
├── analizador.py        # Perfiles, análisis, puntuación, ranking
├── utilidades.py        # Regex de contacto y generación de reportes
├── cvs/                 # CVs de entrada (6 ejemplos incluidos)
├── reportes/            # Reportes generados (creada automáticamente)
├── tests/               # Suite pytest
│   ├── test_analizador.py
│   ├── test_utilidades.py
│   └── test_lector.py
├── requirements.txt
├── PHASES.md            # Plan original de desarrollo (5 fases)
└── README.md
```

---

## Instalación

Requiere Python 3.10 o superior.

```bash
git clone https://github.com/selfishara/CV-ATS-SCANNER.git
cd CV-ATS-SCANNER
pip install -r requirements.txt
```

Dependencias:

| Paquete | Uso |
|---------|-----|
| `PyPDF2` | Lectura de PDFs |
| `python-docx` | Lectura de archivos `.docx` |
| `colorama` | Colores en consola (cross-platform) |
| `pytest` | Ejecución de tests |

---

## Uso

```bash
python main.py
```

### Menú principal

```
==================================================
       ATS CV SCANNER - MENU PRINCIPAL
==================================================
  1. Listar CVs disponibles
  2. Seleccionar perfil de trabajo
  3. Analizar un CV
  4. Analizar todos los CVs
  5. Ver reportes generados
  6. Detectar mejor perfil para un CV
  0. Salir
==================================================
Perfil actual: Desarrollador Python
Selecciona una opcion:
```

Coloca tus CVs en la carpeta `cvs/` (acepta `.txt`, `.pdf` y `.docx`). Los reportes se generan automáticamente en `reportes/`.

### Ejemplo de salida

Analizando `ana_garcia_cv.txt` contra el perfil **Desarrollador Python**:

```
--------------------------------------------------
CV: ana_garcia_cv.txt
Perfil: Desarrollador Python
Puntuacion: 100/100
Categoria: EXCELENTE
Palabras clave encontradas: 11/11
Palabras clave faltantes: 0
Secciones encontradas: 4/4
Secciones faltantes: 0
--------------------------------------------------
Reporte guardado en: reportes/ana_garcia_cv_reporte.txt
```

Detectar mejor perfil para `david_perez_cv.pdf`:

```
--------------------------------------------------
CV: david_perez_cv.pdf
Ranking de perfiles (mejor match arriba):
  1. Desarrollo Aplicaciones Multiplataforma (DAM)  100/100  [EXCELENTE] <- mejor match
  2. Desarrollo Aplicaciones Web (DAW)               53/100  [MEJORABLE]
  3. Desarrollador Python                            49/100  [MEJORABLE]
  4. QA Automation                                   42/100  [MEJORABLE]
  5. Administracion                                  20/100  [MEJORABLE]
  6. Marketing Digital                                7/100  [MEJORABLE]
--------------------------------------------------
```

### Ejemplo de reporte generado

```
==================================================
  REPORTE ATS - ana_garcia_cv.txt
==================================================
Fecha: 04/05/2026 18:42
Perfil analizado: Desarrollador Python

--- INFORMACION DE CONTACTO ---
Email(s):    ana.garcia@email.com
Telefono(s): +34 612 345 678
URL(s):      https://www.linkedin.com/in/ana-garcia, https://github.com/anagarcia

--- PUNTUACION ---
Puntuacion: 100/100
Categoria:  EXCELENTE

--- PALABRAS CLAVE ---
Encontradas (11/11): Python, Django, FastAPI, Flask, SQL, PostgreSQL, Git, Docker, pytest, APIs REST, Scrum
Faltantes: Ninguna

--- SECCIONES ---
Encontradas (4/4): perfil profesional, experiencia laboral, educacion, habilidades tecnicas
Faltantes: Ninguna

==================================================
```

---

## Perfiles de trabajo incluidos

| Perfil | Palabras clave | Secciones esperadas |
|--------|----------------|---------------------|
| **Desarrollador Python** | Python, Django, FastAPI, Flask, SQL, PostgreSQL, Git, Docker, pytest, APIs REST, Scrum | perfil profesional, experiencia laboral, educación, habilidades técnicas |
| **Marketing Digital** | SEO, SEM, Google Ads, Meta Ads, Social Media, Analytics, Email Marketing, Copywriting, Conversion, Branding | perfil profesional, experiencia laboral, educación, habilidades |
| **Administración** | Excel, Contabilidad, Facturación, ERP, Atención al cliente, Gestión documental, Ofimática, SAP, Power BI, Administración | perfil profesional, experiencia laboral, educación, competencias |
| **DAM** (Desarrollo Aplicaciones Multiplataforma) | Java, Kotlin, Android, Android Studio, Flutter, React Native, Ionic, XML, Gradle, SQLite, Git, Scrum | perfil profesional, experiencia laboral, educación, habilidades técnicas |
| **DAW** (Desarrollo Aplicaciones Web) | HTML, CSS, JavaScript, TypeScript, React, Vue, Node.js, PHP, Laravel, MySQL, Git, Scrum | perfil profesional, experiencia laboral, educación, habilidades técnicas |
| **QA Automation** | Selenium, Cypress, Playwright, JUnit, TestNG, pytest, Cucumber, Jenkins, Postman, BDD, Git, Scrum | perfil profesional, experiencia laboral, educación, habilidades técnicas |

---

## Cómo añadir tu propio perfil

Edita el diccionario `PERFILES_TRABAJO` en [analizador.py](analizador.py) y añade una nueva entrada:

```python
PERFILES_TRABAJO = {
    # ... perfiles existentes ...
    "Mi Perfil Custom": {
        "palabras_clave": [
            "Habilidad 1",
            "Habilidad 2",
            "Tecnología X",
        ],
        "secciones_esperadas": [
            "perfil profesional",
            "experiencia laboral",
            "educacion",
            "habilidades",
        ],
    },
}
```

No hace falta tocar nada más: el menú y la función de "mejor perfil" lo recogen automáticamente vía `obtener_perfiles_trabajo()`.

**Tips para diseñar palabras clave:**

- Usa los términos exactos que esperas en el CV (la búsqueda es insensible a mayúsculas y acentos, pero respeta los espacios).
- Para términos con puntuación o multi-palabra (`Node.js`, `APIs REST`, `Power BI`), escríbelos tal cual: el matcher usa lookarounds en lugar de `\b`, así que funcionan correctamente.
- Términos genéricos como `SQL` solo matchearán como palabra completa (no dentro de `MySQL` o `PostgreSQL`); incluye ambos si quieres ambos.

---

## Algoritmo de puntuación

```
puntuacion = (% palabras clave encontradas × 0.7) + (% secciones encontradas × 0.3)
```

| Rango | Categoría |
|-------|-----------|
| 85 – 100 | `excelente` (verde) |
| 65 – 84  | `bueno` (amarillo) |
| 0 – 64   | `mejorable` (rojo) |

El matching es **insensible a mayúsculas y acentos** y respeta **límites de palabra** (vía lookarounds `(?<!\w)` y `(?!\w)`), de forma que:

- `SQL` matchea en `"trabajo con SQL"` pero **no** en `"trabajo con MySQL"`.
- `Node.js` matchea en `"backend Node.js"` pero **no** en `"fichero Node.json"`.
- `Educación` y `educacion` se tratan como equivalentes.

---

## CVs de ejemplo

El proyecto incluye 6 CVs ficticios (2 por formato) que cubren los 6 perfiles:

| Archivo | Formato | Perfil objetivo |
|---------|---------|-----------------|
| `cvs/ana_garcia_cv.txt` | .txt | Desarrollador Python |
| `cvs/sergio_jimenez_cv.txt` | .txt | QA Automation |
| `cvs/carlos_mendoza_cv.docx` | .docx | Marketing Digital |
| `cvs/laura_martinez_cv.docx` | .docx | DAW |
| `cvs/maria_lopez_cv.pdf` | .pdf | Administración |
| `cvs/david_perez_cv.pdf` | .pdf | DAM |

Todos los datos personales son ficticios. Los CVs se generaron mediante scripts one-off (Node.js para los originales, Python con `python-docx` y `reportlab` para los nuevos), ya eliminados.

---

## Tests

```bash
pytest tests/ -v
```

Cobertura actual:

- **`test_analizador.py`** (12 tests): normalización, búsqueda de palabras clave (incluye regresión de falsos positivos `SQL`/`MySQL` y matching correcto de `Node.js`), verificación de secciones, ponderación 70/30, categorización, validación de perfil inexistente, ranking multi-perfil.
- **`test_utilidades.py`** (10 tests): extracción de email, teléfono español (con/sin prefijo `+34`, descarte de números no-móvil), URLs (LinkedIn/GitHub, ignora otras redes), generación de reportes con y sin información de contacto.
- **`test_lector.py`** (5 tests): lectura `.txt`, dispatch por extensión, error en formato no soportado, listado y filtrado por extensión.

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'colorama'`**
Instala las dependencias: `pip install -r requirements.txt`.

**Los acentos aparecen mal en consola (Windows)**
PowerShell moderno suele ir bien, pero si ves caracteres extraños prueba `chcp 65001` antes de ejecutar `python main.py`.

**`incorrect startxref pointer` al leer un PDF**
Es un *warning* de PyPDF2 sobre algunos PDFs generados (incluido el de ejemplo `david_perez_cv.pdf`). El texto se extrae correctamente y la puntuación funciona; puedes ignorarlo.

**El reporte sale con caracteres como `Ã©` en lugar de `é`**
Asegúrate de abrir el `.txt` con codificación UTF-8 (Notepad, VS Code, Sublime, etc. lo detectan; en otros editores puede haber que forzarla).

**Mi CV puntúa más bajo de lo esperado**
Revisa la sección "Faltantes" del reporte: indica exactamente qué palabras clave o secciones no se encontraron. El matching respeta límites de palabra, así que `SQL` no cuenta dentro de `MySQL` (incluye ambos en el CV si aplica).

**Quiero analizar CVs sin pasar por el menú interactivo**
Puedes importar las funciones directamente:

```python
from lector import leer_cv
from analizador import analizar_cv, analizar_contra_todos

texto = leer_cv("cvs/ana_garcia_cv.txt")
print(analizar_cv(texto, "Desarrollador Python"))
print(analizar_contra_todos(texto))
```

---

## Estado del proyecto

| Fase | Descripción | Estado |
|------|-------------|--------|
| 1 | Estructura base y lectura de archivos | ✓ Completa |
| 2 | Análisis y puntuación | ✓ Completa |
| 3 | Utilidades: regex y reportes | ✓ Completa |
| 4 | Integración del menú | ✓ Completa |
| 5 | Pulido: CVs de ejemplo y docs | ✓ Completa |
| 6 | Perfiles ampliados (DAM/DAW/QA) + tests + UX | ✓ Completa |

Plan original detallado en [PHASES.md](PHASES.md).

---

## Licencia

Proyecto académico (FP DAM — Optativa). Uso libre con fines educativos.

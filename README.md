# ATS CV Scanner

Aplicación de consola en Python que lee CVs (`.txt`, `.pdf`, `.docx`), los analiza contra perfiles de trabajo predefinidos, extrae información de contacto y genera reportes de puntuación.

## Estructura

```
cv-ats-scanner/
├── main.py          # Menú interactivo
├── lector.py        # Lectura de archivos por formato
├── analizador.py    # Perfiles, análisis y puntuación
├── utilidades.py    # Regex (email, teléfono, URL) y reportes
├── cvs/             # CVs de entrada (colocar aquí los archivos)
├── reportes/        # Reportes generados (se crean automáticamente)
└── requirements.txt
```

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

El menú permite:
1. Listar CVs disponibles en `cvs/`
2. Seleccionar perfil de trabajo (Desarrollador Python, Marketing Digital, Administración)
3. Analizar un CV individual
4. Analizar todos los CVs
5. Ver reportes generados

Los CVs se colocan manualmente en la carpeta `cvs/`. Los reportes `.txt` se guardan en `reportes/`.

## Estado del proyecto

| Fase | Descripción | Estado |
|------|-------------|--------|
| 1 | Estructura base y lectura de archivos | ✓ Completa |
| 2 | Análisis y puntuación | ✓ Completa |
| 3 | Utilidades: regex y reportes | ✓ Completa |
| 4 | Integración del menú | ✓ Completa |
| 5 | Pulido: CVs de ejemplo y docs | ✓ Completa |

## CVs de ejemplo incluidos

| Archivo | Formato | Perfil |
|---------|---------|--------|
| `cvs/ana_garcia_cv.txt` | .txt | Desarrollador Python |
| `cvs/carlos_mendoza_cv.docx` | .docx | Marketing Digital |
| `cvs/maria_lopez_cv.pdf` | .pdf | Administración |

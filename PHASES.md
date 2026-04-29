## Plan: ATS CV Scanner en Python

Aplicación de consola que lee currículums (.txt, .pdf, .docx) de una carpeta, los analiza contra palabras clave de perfiles de trabajo predefinidos, extrae información de contacto con regex, puntúa cada CV y genera reportes. Dividido en 4 módulos.

---

### Estructura del proyecto

```
cv-ats-scanner/
├── main.py              # Menú interactivo (input, while)
├── lector.py            # Lectura de archivos por formato
├── analizador.py        # Perfiles de trabajo, análisis, puntuación
├── utilidades.py        # Regex (email, tel, URL), generación de reportes
├── cvs/                 # CVs de entrada
├── reportes/            # Reportes de salida
├── requirements.txt     # PyPDF2, python-docx
└── README.md
```

---

### Fases

**Fase 1 — Estructura base y lectura de archivos**
1. Crear `requirements.txt` con `PyPDF2` y `python-docx`
2. Crear carpeta `cvs/` con un CV de ejemplo .txt
3. Crear `lector.py`:
   - `leer_txt(ruta)`, `leer_pdf(ruta)`, `leer_docx(ruta)` — cada una lee su formato
   - `leer_cv(ruta)` — detecta extensión con **if/elif/else** y delega
   - `listar_cvs(carpeta)` — usa `os.listdir` con **for** loop, filtra por extensión
4. Crear `main.py` con menú esqueleto (bucle **while** + **input()**)

**Fase 2 — Análisis y puntuación** *(depende de Fase 1)*
5. Crear perfiles de trabajo como **diccionarios** en `analizador.py` (ej: "Desarrollador Python", "Marketing Digital", "Administración") con listas de palabras clave y secciones esperadas
6. `buscar_palabras_clave(texto, palabras_clave)` — **for** loop, devuelve encontradas/faltantes
7. `verificar_secciones(texto, secciones)` — comprueba secciones del CV
8. `calcular_puntuacion(...)` — score 0-100 con **condicionales** para categorías (excelente/bueno/mejorable)
9. `analizar_cv(texto, perfil)` — orquesta todo, devuelve dict con resultados

**Fase 3 — Utilidades: regex y reportes** *(depende de Fase 2)*
10. `extraer_email(texto)` — `re.findall` con patrón de email
11. `extraer_telefono(texto)` — `re.findall` con patrón de teléfono
12. `extraer_url(texto)` — detecta URLs (LinkedIn, GitHub)
13. `generar_reporte(nombre_cv, resultados, info_contacto)` — escribe `.txt` en `reportes/`
14. Crear carpeta `reportes/`

**Fase 4 — Integración del menú** *(depende de Fases 1-3)*
15. Menú completo: (1) Listar CVs, (2) Seleccionar perfil, (3) Analizar un CV, (4) Analizar todos, (5) Ver reportes, (0) Salir
16. Validación de entradas del usuario
17. Mostrar resultados formateados por consola

**Fase 5 — Pulido** *(depende de Fase 4)*
18. Añadir CVs de ejemplo en los 3 formatos
19. Crear `README.md`

---

### Cobertura de requisitos

| Requisito | Dónde |
|---|---|
| Variables y tipos de datos | Todo (strings, ints, floats, bools, listas, dicts) |
| if/elif/else | `lector.py` (extensión), `main.py` (menú), `analizador.py` (umbrales) |
| for/while | `main.py` (while menú), `analizador.py` (for palabras), `lector.py` (for archivos) |
| Listas/diccionarios | Perfiles, palabras clave, resultados |
| ≥2 funciones | Múltiples por módulo |
| input() | Menú interactivo |
| **Investigación** | Manejo archivos, regex (`re`), librerías externas, módulos múltiples |

### Verificación
1. `pip install -r requirements.txt` sin errores
2. `python main.py` → menú funcional, todas las opciones responden
3. Analizar 1 CV de cada formato → puntuación + palabras + contacto correctos
4. Verificar reportes generados en `reportes/`
5. Entradas inválidas manejadas sin crash

### Decisiones
- Solo 2 librerías externas: **PyPDF2** y **python-docx** (mínimo necesario)
- Perfiles de trabajo hardcodeados (no base de datos)
- CVs se colocan manualmente en `cvs/` (sin upload)
- Reportes como .txt plano (sin formato complejo)
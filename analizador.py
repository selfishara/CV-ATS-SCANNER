import re
import unicodedata


PERFILES_TRABAJO = {
    "Desarrollador Python": {
        "palabras_clave": [
            "Python",
            "Django",
            "FastAPI",
            "Flask",
            "SQL",
            "PostgreSQL",
            "Git",
            "Docker",
            "pytest",
            "APIs REST",
            "Scrum",
        ],
        "secciones_esperadas": [
            "perfil profesional",
            "experiencia laboral",
            "educacion",
            "habilidades tecnicas",
        ],
    },
    "Marketing Digital": {
        "palabras_clave": [
            "SEO",
            "SEM",
            "Google Ads",
            "Meta Ads",
            "Social Media",
            "Analytics",
            "Email Marketing",
            "Copywriting",
            "Conversion",
            "Branding",
        ],
        "secciones_esperadas": [
            "perfil profesional",
            "experiencia laboral",
            "educacion",
            "habilidades",
        ],
    },
    "Administracion": {
        "palabras_clave": [
            "Excel",
            "Contabilidad",
            "Facturacion",
            "ERP",
            "Atencion al cliente",
            "Gestion documental",
            "Ofimatica",
            "SAP",
            "Power BI",
            "Administracion",
        ],
        "secciones_esperadas": [
            "perfil profesional",
            "experiencia laboral",
            "educacion",
            "competencias",
        ],
    },
    "Desarrollo Aplicaciones Multiplataforma (DAM)": {
        "palabras_clave": [
            "Java",
            "Kotlin",
            "Android",
            "Android Studio",
            "Flutter",
            "React Native",
            "Ionic",
            "XML",
            "Gradle",
            "SQLite",
            "Git",
            "Scrum",
        ],
        "secciones_esperadas": [
            "perfil profesional",
            "experiencia laboral",
            "educacion",
            "habilidades tecnicas",
        ],
    },
    "Desarrollo Aplicaciones Web (DAW)": {
        "palabras_clave": [
            "HTML",
            "CSS",
            "JavaScript",
            "TypeScript",
            "React",
            "Vue",
            "Node.js",
            "PHP",
            "Laravel",
            "MySQL",
            "Git",
            "Scrum",
        ],
        "secciones_esperadas": [
            "perfil profesional",
            "experiencia laboral",
            "educacion",
            "habilidades tecnicas",
        ],
    },
    "QA Automation": {
        "palabras_clave": [
            "Selenium",
            "Cypress",
            "Playwright",
            "JUnit",
            "TestNG",
            "pytest",
            "Cucumber",
            "Jenkins",
            "Postman",
            "BDD",
            "Git",
            "Scrum",
        ],
        "secciones_esperadas": [
            "perfil profesional",
            "experiencia laboral",
            "educacion",
            "habilidades tecnicas",
        ],
    },
}


def normalizar_texto(texto):
    texto_normalizado = unicodedata.normalize("NFKD", texto)
    texto_sin_acentos = "".join(
        caracter for caracter in texto_normalizado if not unicodedata.combining(caracter)
    )
    return texto_sin_acentos.casefold()


def obtener_perfiles_trabajo():
    return list(PERFILES_TRABAJO.keys())


def _coincide_termino(texto_normalizado, termino):
    """Busca el termino en el texto normalizado respetando limites de palabra.

    Usa lookarounds en lugar de \\b para que terminos como 'Node.js' o 'C#'
    se comporten correctamente: 'SQL' no matchea dentro de 'MySQL', pero
    'Node.js' si matchea aunque vaya seguido de un signo de puntuacion.
    """
    termino_normalizado = normalizar_texto(termino)
    patron = r"(?<!\w)" + re.escape(termino_normalizado) + r"(?!\w)"
    return re.search(patron, texto_normalizado) is not None


def buscar_palabras_clave(texto, palabras_clave):
    texto_normalizado = normalizar_texto(texto)
    encontradas = []
    faltantes = []

    for palabra in palabras_clave:
        if _coincide_termino(texto_normalizado, palabra):
            encontradas.append(palabra)
        else:
            faltantes.append(palabra)

    total = len(palabras_clave)
    porcentaje = round((len(encontradas) / total) * 100, 2) if total else 0

    return {
        "encontradas": encontradas,
        "faltantes": faltantes,
        "total": total,
        "porcentaje": porcentaje,
    }


def verificar_secciones(texto, secciones):
    texto_normalizado = normalizar_texto(texto)
    encontradas = []
    faltantes = []

    for seccion in secciones:
        if normalizar_texto(seccion) in texto_normalizado:
            encontradas.append(seccion)
        else:
            faltantes.append(seccion)

    total = len(secciones)
    porcentaje = round((len(encontradas) / total) * 100, 2) if total else 0

    return {
        "encontradas": encontradas,
        "faltantes": faltantes,
        "total": total,
        "porcentaje": porcentaje,
    }


def calcular_puntuacion(resultados_palabras_clave, resultados_secciones):
    puntuacion_clave = resultados_palabras_clave["porcentaje"] * 0.7
    puntuacion_secciones = resultados_secciones["porcentaje"] * 0.3
    puntuacion = round(puntuacion_clave + puntuacion_secciones)

    if puntuacion >= 85:
        categoria = "excelente"
    elif puntuacion >= 65:
        categoria = "bueno"
    else:
        categoria = "mejorable"

    return {
        "puntuacion": puntuacion,
        "categoria": categoria,
    }


def analizar_cv(texto, perfil):
    if perfil not in PERFILES_TRABAJO:
        perfiles_disponibles = ", ".join(obtener_perfiles_trabajo())
        raise ValueError(
            f"Perfil no encontrado: '{perfil}'. Perfiles disponibles: {perfiles_disponibles}"
        )

    configuracion_perfil = PERFILES_TRABAJO[perfil]
    resultados_palabras_clave = buscar_palabras_clave(
        texto, configuracion_perfil["palabras_clave"]
    )
    resultados_secciones = verificar_secciones(
        texto, configuracion_perfil["secciones_esperadas"]
    )
    puntuacion = calcular_puntuacion(
        resultados_palabras_clave, resultados_secciones
    )

    return {
        "perfil": perfil,
        "palabras_clave": resultados_palabras_clave,
        "secciones": resultados_secciones,
        "puntuacion": puntuacion["puntuacion"],
        "categoria": puntuacion["categoria"],
    }


def analizar_contra_todos(texto):
    """Analiza el CV contra todos los perfiles y los ordena por puntuacion."""
    resultados = [analizar_cv(texto, perfil) for perfil in obtener_perfiles_trabajo()]
    resultados.sort(key=lambda r: r["puntuacion"], reverse=True)
    return resultados

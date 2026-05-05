import pytest

from analizador import (
    PERFILES_TRABAJO,
    analizar_contra_todos,
    analizar_cv,
    buscar_palabras_clave,
    calcular_puntuacion,
    normalizar_texto,
    obtener_perfiles_trabajo,
    verificar_secciones,
)


def test_normalizar_texto_quita_acentos_y_baja_caja():
    assert normalizar_texto("Educación Técnica") == "educacion tecnica"


def test_obtener_perfiles_incluye_los_seis():
    perfiles = obtener_perfiles_trabajo()
    assert "Desarrollador Python" in perfiles
    assert "Desarrollo Aplicaciones Multiplataforma (DAM)" in perfiles
    assert "Desarrollo Aplicaciones Web (DAW)" in perfiles
    assert "QA Automation" in perfiles
    assert len(perfiles) == 6


def test_buscar_palabras_clave_encuentra_y_falta():
    texto = "Trabajo con Python y Django diariamente."
    resultado = buscar_palabras_clave(texto, ["Python", "Django", "Flask"])
    assert resultado["encontradas"] == ["Python", "Django"]
    assert resultado["faltantes"] == ["Flask"]
    assert resultado["total"] == 3
    assert resultado["porcentaje"] == round(2 / 3 * 100, 2)


def test_buscar_palabras_clave_es_acento_insensible():
    texto = "Tengo experiencia en administracíon y atención al cliente."
    resultado = buscar_palabras_clave(texto, ["Administracion", "Atencion al cliente"])
    assert resultado["encontradas"] == ["Administracion", "Atencion al cliente"]


def test_word_boundary_no_falso_positivo_sql_en_mysql():
    """Regresion: 'SQL' no debe matchear dentro de 'MySQL'."""
    texto = "Trabajo con MySQL como base de datos principal."
    resultado = buscar_palabras_clave(texto, ["SQL", "MySQL"])
    assert "MySQL" in resultado["encontradas"]
    assert "SQL" in resultado["faltantes"]


def test_word_boundary_node_js_matchea_correctamente():
    """'Node.js' debe matchear pero no dentro de 'Node.json'."""
    texto1 = "Backend desarrollado en Node.js sobre Express."
    texto2 = "Cargamos un fichero Node.jsonpath con configuracion."

    assert buscar_palabras_clave(texto1, ["Node.js"])["encontradas"] == ["Node.js"]
    assert buscar_palabras_clave(texto2, ["Node.js"])["faltantes"] == ["Node.js"]


def test_verificar_secciones_busca_substring_normalizado():
    texto = "PERFIL PROFESIONAL\nSoy desarrollador.\nEDUCACIÓN\nGrado en Informatica."
    resultado = verificar_secciones(
        texto, ["perfil profesional", "educacion", "experiencia laboral"]
    )
    assert sorted(resultado["encontradas"]) == sorted(["perfil profesional", "educacion"])
    assert resultado["faltantes"] == ["experiencia laboral"]


def test_calcular_puntuacion_categorias():
    excelente = calcular_puntuacion(
        {"porcentaje": 100}, {"porcentaje": 100}
    )
    assert excelente["puntuacion"] == 100
    assert excelente["categoria"] == "excelente"

    bueno = calcular_puntuacion({"porcentaje": 70}, {"porcentaje": 70})
    assert bueno["categoria"] == "bueno"

    mejorable = calcular_puntuacion({"porcentaje": 30}, {"porcentaje": 30})
    assert mejorable["categoria"] == "mejorable"


def test_calcular_puntuacion_pondera_70_30():
    """70% palabras + 30% secciones = puntuacion final."""
    resultado = calcular_puntuacion({"porcentaje": 100}, {"porcentaje": 0})
    assert resultado["puntuacion"] == 70

    resultado = calcular_puntuacion({"porcentaje": 0}, {"porcentaje": 100})
    assert resultado["puntuacion"] == 30


def test_analizar_cv_contiene_todas_las_claves():
    texto = "Python Django Flask SQL PostgreSQL Git Docker pytest APIs REST Scrum FastAPI"
    resultado = analizar_cv(texto, "Desarrollador Python")
    assert "perfil" in resultado
    assert "puntuacion" in resultado
    assert "categoria" in resultado
    assert "palabras_clave" in resultado
    assert "secciones" in resultado


def test_analizar_cv_perfil_invalido_lanza_value_error():
    with pytest.raises(ValueError, match="Perfil no encontrado"):
        analizar_cv("texto cualquiera", "Perfil Inexistente")


def test_analizar_contra_todos_devuelve_todos_los_perfiles_ordenados():
    texto = "Selenium Cypress Playwright JUnit TestNG pytest Cucumber Jenkins Postman BDD Git Scrum"
    resultados = analizar_contra_todos(texto)

    assert len(resultados) == len(PERFILES_TRABAJO)
    puntuaciones = [r["puntuacion"] for r in resultados]
    assert puntuaciones == sorted(puntuaciones, reverse=True)
    assert resultados[0]["perfil"] == "QA Automation"

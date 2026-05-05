import os

import pytest

from utilidades import extraer_email, extraer_telefono, extraer_url, generar_reporte


def test_extraer_email_simple():
    texto = "Contacta conmigo en ana.garcia@email.com para cualquier cosa."
    assert extraer_email(texto) == ["ana.garcia@email.com"]


def test_extraer_email_multiple():
    texto = "Emails: foo@bar.com y otro@dominio.es."
    assert extraer_email(texto) == ["foo@bar.com", "otro@dominio.es"]


def test_extraer_email_no_encuentra():
    assert extraer_email("Sin emails aqui.") == []


def test_extraer_telefono_formato_espanol_con_prefijo():
    texto = "Llamame al +34 612 345 678 cuando puedas."
    assert "+34 612 345 678" in extraer_telefono(texto)


def test_extraer_telefono_sin_prefijo():
    texto = "Mi numero es 678 123 456."
    assert "678 123 456" in extraer_telefono(texto)


def test_extraer_telefono_descarta_no_movil():
    """Los telefonos espanoles validos empiezan por 6, 7, 8 o 9."""
    texto = "Codigo postal 282 456 123 (no es un telefono)."
    resultado = extraer_telefono(texto)
    assert "282 456 123" not in resultado


def test_extraer_url_linkedin_y_github():
    texto = (
        "Perfil: https://www.linkedin.com/in/ana-garcia "
        "Repos: https://github.com/anagarcia/proyecto"
    )
    urls = extraer_url(texto)
    assert any("linkedin" in u for u in urls)
    assert any("github" in u for u in urls)


def test_extraer_url_ignora_otras_redes():
    texto = "Mi twitter: https://twitter.com/usuario"
    assert extraer_url(texto) == []


def test_generar_reporte_crea_archivo(tmp_path):
    resultados = {
        "perfil": "Desarrollador Python",
        "puntuacion": 85,
        "categoria": "excelente",
        "palabras_clave": {
            "encontradas": ["Python", "Django"],
            "faltantes": ["Flask"],
            "total": 3,
        },
        "secciones": {
            "encontradas": ["perfil profesional"],
            "faltantes": ["experiencia laboral"],
            "total": 2,
        },
    }
    info_contacto = {
        "emails": ["test@example.com"],
        "telefonos": ["+34 612 345 678"],
        "urls": ["https://github.com/test"],
    }

    ruta = generar_reporte(
        "test_cv.txt", resultados, info_contacto, carpeta_reportes=str(tmp_path)
    )

    assert os.path.exists(ruta)
    contenido = open(ruta, encoding="utf-8").read()
    assert "test_cv.txt" in contenido
    assert "85/100" in contenido
    assert "EXCELENTE" in contenido
    assert "test@example.com" in contenido
    assert "Python" in contenido


def test_generar_reporte_sin_contacto_muestra_no_detectado(tmp_path):
    resultados = {
        "perfil": "Marketing Digital",
        "puntuacion": 50,
        "categoria": "mejorable",
        "palabras_clave": {"encontradas": [], "faltantes": ["SEO"], "total": 1},
        "secciones": {"encontradas": [], "faltantes": ["habilidades"], "total": 1},
    }
    info_contacto = {"emails": [], "telefonos": [], "urls": []}

    ruta = generar_reporte(
        "vacio_cv.txt", resultados, info_contacto, carpeta_reportes=str(tmp_path)
    )
    contenido = open(ruta, encoding="utf-8").read()
    assert contenido.count("No detectado") == 3

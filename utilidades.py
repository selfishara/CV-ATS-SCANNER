import re
import os
from datetime import datetime


def extraer_email(texto):
    patron = r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
    return re.findall(patron, texto)


def extraer_telefono(texto):
    patron = r"(?:\+34[\s\-]?)?\b[6789]\d{2}[\s\.\-]?\d{3}[\s\.\-]?\d{3}\b"
    return re.findall(patron, texto)


def extraer_url(texto):
    patron = r"https?://(?:www\.)?(?:linkedin\.com|github\.com)/\S+"
    return re.findall(patron, texto)


def generar_reporte(nombre_cv, resultados, info_contacto, carpeta_reportes="reportes"):
    nombre_base = os.path.splitext(nombre_cv)[0]
    ruta_reporte = os.path.join(carpeta_reportes, f"{nombre_base}_reporte.txt")
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    palabras = resultados["palabras_clave"]
    secciones = resultados["secciones"]

    lineas = [
        "=" * 50,
        f"  REPORTE ATS - {nombre_cv}",
        "=" * 50,
        f"Fecha: {fecha}",
        f"Perfil analizado: {resultados['perfil']}",
        "",
        "--- INFORMACION DE CONTACTO ---",
        "Email(s):    " + (", ".join(info_contacto["emails"]) or "No detectado"),
        "Telefono(s): " + (", ".join(info_contacto["telefonos"]) or "No detectado"),
        "URL(s):      " + (", ".join(info_contacto["urls"]) or "No detectado"),
        "",
        "--- PUNTUACION ---",
        f"Puntuacion: {resultados['puntuacion']}/100",
        f"Categoria:  {resultados['categoria'].upper()}",
        "",
        "--- PALABRAS CLAVE ---",
        f"Encontradas ({len(palabras['encontradas'])}/{palabras['total']}): "
        + (", ".join(palabras["encontradas"]) or "Ninguna"),
        "Faltantes: " + (", ".join(palabras["faltantes"]) or "Ninguna"),
        "",
        "--- SECCIONES ---",
        f"Encontradas ({len(secciones['encontradas'])}/{secciones['total']}): "
        + (", ".join(secciones["encontradas"]) or "Ninguna"),
        "Faltantes: " + (", ".join(secciones["faltantes"]) or "Ninguna"),
        "",
        "=" * 50,
    ]

    with open(ruta_reporte, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas))

    return ruta_reporte

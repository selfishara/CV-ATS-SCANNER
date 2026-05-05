import os

import pytest

from lector import leer_cv, leer_txt, listar_cvs


def test_leer_txt_lee_contenido(tmp_path):
    archivo = tmp_path / "ejemplo.txt"
    archivo.write_text("Hola mundo\nSegunda linea", encoding="utf-8")

    contenido = leer_txt(str(archivo))
    assert "Hola mundo" in contenido
    assert "Segunda linea" in contenido


def test_leer_cv_dispatcha_por_extension(tmp_path):
    archivo = tmp_path / "cv.txt"
    archivo.write_text("contenido txt", encoding="utf-8")
    assert leer_cv(str(archivo)) == "contenido txt"


def test_leer_cv_extension_no_soportada(tmp_path):
    archivo = tmp_path / "cv.rtf"
    archivo.write_text("rtf", encoding="utf-8")

    with pytest.raises(ValueError, match="Formato no soportado"):
        leer_cv(str(archivo))


def test_listar_cvs_filtra_por_extension(tmp_path):
    (tmp_path / "uno.txt").write_text("x", encoding="utf-8")
    (tmp_path / "dos.docx").write_text("x", encoding="utf-8")
    (tmp_path / "tres.pdf").write_text("x", encoding="utf-8")
    (tmp_path / "ignorar.md").write_text("x", encoding="utf-8")
    (tmp_path / "ignorar.jpg").write_text("x", encoding="utf-8")

    resultado = listar_cvs(str(tmp_path))
    assert resultado == ["dos.docx", "tres.pdf", "uno.txt"]


def test_listar_cvs_carpeta_real_del_proyecto():
    """Verifica que la carpeta cvs/ del proyecto contiene los CVs esperados."""
    raiz_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    carpeta_cvs = os.path.join(raiz_proyecto, "cvs")
    if not os.path.isdir(carpeta_cvs):
        pytest.skip("Carpeta cvs/ no presente")

    archivos = listar_cvs(carpeta_cvs)
    assert len(archivos) >= 3

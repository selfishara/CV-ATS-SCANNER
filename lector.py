import os


def leer_txt(ruta):
    """Lee el contenido de un archivo .txt y lo devuelve como string."""
    with open(ruta, "r", encoding="utf-8") as archivo:
        return archivo.read()


def leer_pdf(ruta):
    """Lee el contenido de un archivo .pdf y devuelve el texto extraído."""
    import PyPDF2

    texto = ""
    with open(ruta, "rb") as archivo:
        lector = PyPDF2.PdfReader(archivo)
        for pagina in lector.pages:
            texto += pagina.extract_text() or ""
    return texto


def leer_docx(ruta):
    """Lee el contenido de un archivo .docx y devuelve el texto extraído."""
    import docx

    documento = docx.Document(ruta)
    parrafos = []
    for parrafo in documento.paragraphs:
        parrafos.append(parrafo.text)
    return "\n".join(parrafos)


def leer_cv(ruta):
    """Detecta la extensión del archivo y delega la lectura al lector correspondiente."""
    _, extension = os.path.splitext(ruta)
    extension = extension.lower()

    if extension == ".txt":
        return leer_txt(ruta)
    elif extension == ".pdf":
        return leer_pdf(ruta)
    elif extension == ".docx":
        return leer_docx(ruta)
    else:
        raise ValueError(f"Formato no soportado: '{extension}'. Use .txt, .pdf o .docx")


def listar_cvs(carpeta):
    """Lista todos los CVs en la carpeta con extensiones soportadas."""
    extensiones_soportadas = {".txt", ".pdf", ".docx"}
    cvs_encontrados = []

    for nombre_archivo in os.listdir(carpeta):
        _, extension = os.path.splitext(nombre_archivo)
        if extension.lower() in extensiones_soportadas:
            cvs_encontrados.append(nombre_archivo)

    return cvs_encontrados

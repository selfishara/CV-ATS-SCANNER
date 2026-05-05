import os

from colorama import Fore, Style, init as colorama_init

from analizador import (
    analizar_contra_todos,
    analizar_cv,
    obtener_perfiles_trabajo,
)
from lector import leer_cv, listar_cvs
from utilidades import extraer_email, extraer_telefono, extraer_url, generar_reporte


CARPETA_CVS = "cvs"
CARPETA_REPORTES = "reportes"
perfil_seleccionado = obtener_perfiles_trabajo()[0]

colorama_init(autoreset=True)


COLOR_CATEGORIA = {
    "excelente": Fore.GREEN,
    "bueno": Fore.YELLOW,
    "mejorable": Fore.RED,
}


def colorear_categoria(categoria):
    return COLOR_CATEGORIA.get(categoria, "") + categoria.upper() + Style.RESET_ALL


def mostrar_menu():
    print()
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + "       ATS CV SCANNER - MENU PRINCIPAL")
    print(Fore.CYAN + "=" * 50)
    print("  1. Listar CVs disponibles")
    print("  2. Seleccionar perfil de trabajo")
    print("  3. Analizar un CV")
    print("  4. Analizar todos los CVs")
    print("  5. Ver reportes generados")
    print("  6. Detectar mejor perfil para un CV")
    print("  0. Salir")
    print(Fore.CYAN + "=" * 50)


def opcion_listar_cvs():
    cvs = listar_cvs(CARPETA_CVS)
    if not cvs:
        print(Fore.YELLOW + "\nNo se encontraron CVs en la carpeta 'cvs/'.")
        return

    print(f"\nCVs encontrados ({len(cvs)}):")
    for i, cv in enumerate(cvs, start=1):
        print(f"  {i}. {cv}")


def mostrar_perfiles():
    perfiles = obtener_perfiles_trabajo()
    print("\nPerfiles disponibles:")
    for i, perfil in enumerate(perfiles, start=1):
        print(f"  {i}. {perfil}")


def seleccionar_perfil():
    global perfil_seleccionado
    perfiles = obtener_perfiles_trabajo()

    mostrar_perfiles()
    opcion = input("Selecciona un perfil: ").strip()

    if not opcion.isdigit():
        print(Fore.RED + "\nEntrada invalida. Se mantiene el perfil actual.")
        return

    indice = int(opcion)
    if 1 <= indice <= len(perfiles):
        perfil_seleccionado = perfiles[indice - 1]
        print(Fore.GREEN + f"\nPerfil seleccionado: {perfil_seleccionado}")
    else:
        print(Fore.RED + "\nPerfil no valido. Se mantiene el perfil actual.")


def pedir_cv_a_analizar():
    cvs = listar_cvs(CARPETA_CVS)
    if not cvs:
        print(Fore.YELLOW + "\nNo se encontraron CVs en la carpeta 'cvs/'.")
        return None

    print("\nSelecciona un CV:")
    for i, cv in enumerate(cvs, start=1):
        print(f"  {i}. {cv}")

    opcion = input("Numero de CV: ").strip()
    if not opcion.isdigit():
        print(Fore.RED + "\nEntrada invalida.")
        return None

    indice = int(opcion)
    if 1 <= indice <= len(cvs):
        return cvs[indice - 1]

    print(Fore.RED + "\nCV no valido.")
    return None


def mostrar_resultado_analisis(nombre_cv, resultados):
    print("\n" + "-" * 50)
    print(f"CV: {nombre_cv}")
    print(f"Perfil: {resultados['perfil']}")
    print(f"Puntuacion: {resultados['puntuacion']}/100")
    print(f"Categoria: {colorear_categoria(resultados['categoria'])}")
    print(
        "Palabras clave encontradas: "
        f"{len(resultados['palabras_clave']['encontradas'])}"
        f"/{resultados['palabras_clave']['total']}"
    )
    print(
        "Palabras clave faltantes: "
        f"{len(resultados['palabras_clave']['faltantes'])}"
    )
    print(
        f"Secciones encontradas: {len(resultados['secciones']['encontradas'])}"
        f"/{resultados['secciones']['total']}"
    )
    print(f"Secciones faltantes: {len(resultados['secciones']['faltantes'])}")
    print("-" * 50)


def _extraer_contacto(texto):
    return {
        "emails": extraer_email(texto),
        "telefonos": extraer_telefono(texto),
        "urls": extraer_url(texto),
    }


def opcion_analizar_un_cv():
    nombre_cv = pedir_cv_a_analizar()
    if not nombre_cv:
        return

    ruta_cv = os.path.join(CARPETA_CVS, nombre_cv)
    try:
        texto = leer_cv(ruta_cv)
        resultados = analizar_cv(texto, perfil_seleccionado)
        info_contacto = _extraer_contacto(texto)
        mostrar_resultado_analisis(nombre_cv, resultados)
        ruta = generar_reporte(nombre_cv, resultados, info_contacto, CARPETA_REPORTES)
        print(Fore.GREEN + f"Reporte guardado en: {ruta}")
    except Exception as error:
        print(Fore.RED + f"\nNo se pudo analizar el CV: {error}")


def opcion_analizar_todos():
    cvs = listar_cvs(CARPETA_CVS)
    if not cvs:
        print(Fore.YELLOW + "\nNo se encontraron CVs en la carpeta 'cvs/'.")
        return

    for nombre_cv in cvs:
        ruta_cv = os.path.join(CARPETA_CVS, nombre_cv)
        try:
            texto = leer_cv(ruta_cv)
            resultados = analizar_cv(texto, perfil_seleccionado)
            info_contacto = _extraer_contacto(texto)
            mostrar_resultado_analisis(nombre_cv, resultados)
            ruta = generar_reporte(nombre_cv, resultados, info_contacto, CARPETA_REPORTES)
            print(Fore.GREEN + f"Reporte guardado en: {ruta}")
        except Exception as error:
            print(Fore.RED + f"\nNo se pudo analizar '{nombre_cv}': {error}")


def opcion_ver_reportes():
    reportes = sorted(
        f for f in os.listdir(CARPETA_REPORTES) if f.endswith(".txt")
    )
    if not reportes:
        print(Fore.YELLOW + "\nNo hay reportes generados aun.")
        return

    print(f"\nReportes disponibles ({len(reportes)}):")
    for i, nombre in enumerate(reportes, start=1):
        print(f"  {i}. {nombre}")


def opcion_detectar_mejor_perfil():
    nombre_cv = pedir_cv_a_analizar()
    if not nombre_cv:
        return

    ruta_cv = os.path.join(CARPETA_CVS, nombre_cv)
    try:
        texto = leer_cv(ruta_cv)
        resultados = analizar_contra_todos(texto)
    except Exception as error:
        print(Fore.RED + f"\nNo se pudo analizar el CV: {error}")
        return

    print("\n" + "-" * 50)
    print(f"CV: {nombre_cv}")
    print("Ranking de perfiles (mejor match arriba):")
    for i, r in enumerate(resultados, start=1):
        marca = Fore.GREEN + " <- mejor match" + Style.RESET_ALL if i == 1 else ""
        print(
            f"  {i}. {r['perfil']:<48} {r['puntuacion']:>3}/100  "
            f"[{colorear_categoria(r['categoria'])}]{marca}"
        )
    print("-" * 50)


def main():
    print(Fore.CYAN + "Iniciando ATS CV Scanner...")

    os.makedirs(CARPETA_CVS, exist_ok=True)
    os.makedirs(CARPETA_REPORTES, exist_ok=True)

    while True:
        mostrar_menu()
        print(f"Perfil actual: " + Fore.CYAN + perfil_seleccionado)
        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            opcion_listar_cvs()
        elif opcion == "2":
            seleccionar_perfil()
        elif opcion == "3":
            opcion_analizar_un_cv()
        elif opcion == "4":
            opcion_analizar_todos()
        elif opcion == "5":
            opcion_ver_reportes()
        elif opcion == "6":
            opcion_detectar_mejor_perfil()
        elif opcion == "0":
            print(Fore.CYAN + "\nHasta luego.")
            break
        else:
            print(Fore.RED + "\nOpcion no valida. Introduce un numero del 0 al 6.")


if __name__ == "__main__":
    main()

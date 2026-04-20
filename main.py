import os

from analizador import analizar_cv, obtener_perfiles_trabajo
from lector import leer_cv, listar_cvs


CARPETA_CVS = "cvs"
CARPETA_REPORTES = "reportes"
perfil_seleccionado = obtener_perfiles_trabajo()[0]


def mostrar_menu():
    print("\n" + "=" * 45)
    print("       ATS CV SCANNER - MENU PRINCIPAL")
    print("=" * 45)
    print("  1. Listar CVs disponibles")
    print("  2. Seleccionar perfil de trabajo")
    print("  3. Analizar un CV")
    print("  4. Analizar todos los CVs")
    print("  5. Ver reportes generados")
    print("  0. Salir")
    print("=" * 45)


def opcion_listar_cvs():
    cvs = listar_cvs(CARPETA_CVS)
    if not cvs:
        print("\nNo se encontraron CVs en la carpeta 'cvs/'.")
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
        print("\nEntrada invalida. Se mantiene el perfil actual.")
        return

    indice = int(opcion)
    if 1 <= indice <= len(perfiles):
        perfil_seleccionado = perfiles[indice - 1]
        print(f"\nPerfil seleccionado: {perfil_seleccionado}")
    else:
        print("\nPerfil no valido. Se mantiene el perfil actual.")


def pedir_cv_a_analizar():
    cvs = listar_cvs(CARPETA_CVS)
    if not cvs:
        print("\nNo se encontraron CVs en la carpeta 'cvs/'.")
        return None

    print("\nSelecciona un CV:")
    for i, cv in enumerate(cvs, start=1):
        print(f"  {i}. {cv}")

    opcion = input("Numero de CV: ").strip()
    if not opcion.isdigit():
        print("\nEntrada invalida.")
        return None

    indice = int(opcion)
    if 1 <= indice <= len(cvs):
        return cvs[indice - 1]

    print("\nCV no valido.")
    return None


def mostrar_resultado_analisis(nombre_cv, resultados):
    print("\n" + "-" * 45)
    print(f"CV: {nombre_cv}")
    print(f"Perfil: {resultados['perfil']}")
    print(f"Puntuacion: {resultados['puntuacion']}/100")
    print(f"Categoria: {resultados['categoria']}")
    print(
        "Palabras clave encontradas: "
        f"{len(resultados['palabras_clave']['encontradas'])}"
    )
    print(
        "Palabras clave faltantes: "
        f"{len(resultados['palabras_clave']['faltantes'])}"
    )
    print(f"Secciones encontradas: {len(resultados['secciones']['encontradas'])}")
    print(f"Secciones faltantes: {len(resultados['secciones']['faltantes'])}")
    print("-" * 45)


def opcion_analizar_un_cv():
    nombre_cv = pedir_cv_a_analizar()
    if not nombre_cv:
        return

    ruta_cv = os.path.join(CARPETA_CVS, nombre_cv)
    try:
        texto = leer_cv(ruta_cv)
        resultados = analizar_cv(texto, perfil_seleccionado)
        mostrar_resultado_analisis(nombre_cv, resultados)
    except Exception as error:
        print(f"\nNo se pudo analizar el CV: {error}")


def opcion_analizar_todos():
    cvs = listar_cvs(CARPETA_CVS)
    if not cvs:
        print("\nNo se encontraron CVs en la carpeta 'cvs/'.")
        return

    for nombre_cv in cvs:
        ruta_cv = os.path.join(CARPETA_CVS, nombre_cv)
        try:
            texto = leer_cv(ruta_cv)
            resultados = analizar_cv(texto, perfil_seleccionado)
            mostrar_resultado_analisis(nombre_cv, resultados)
        except Exception as error:
            print(f"\nNo se pudo analizar '{nombre_cv}': {error}")


def opcion_no_implementada(numero):
    print(f"\n[Opcion {numero}] Proximamente disponible en la Fase 3.")


def main():
    print("Iniciando ATS CV Scanner...")

    os.makedirs(CARPETA_CVS, exist_ok=True)
    os.makedirs(CARPETA_REPORTES, exist_ok=True)

    while True:
        mostrar_menu()
        print(f"Perfil actual: {perfil_seleccionado}")
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
            opcion_no_implementada(5)
        elif opcion == "0":
            print("\nHasta luego.")
            break
        else:
            print("\nOpcion no valida. Introduce un numero del 0 al 5.")


if __name__ == "__main__":
    main()

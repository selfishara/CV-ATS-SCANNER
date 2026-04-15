import os
from lector import listar_cvs, leer_cv

CARPETA_CVS = "cvs"
CARPETA_REPORTES = "reportes"


def mostrar_menu():
    print("\n" + "=" * 45)
    print("       ATS CV SCANNER — MENÚ PRINCIPAL")
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
    else:
        print(f"\nCVs encontrados ({len(cvs)}):")
        for i, cv in enumerate(cvs, start=1):
            print(f"  {i}. {cv}")


def opcion_no_implementada(numero):
    print(f"\n[Opción {numero}] Próximamente disponible en la Fase 2/3.")


def main():
    print("Iniciando ATS CV Scanner...")

    # Crear carpetas necesarias si no existen
    os.makedirs(CARPETA_CVS, exist_ok=True)
    os.makedirs(CARPETA_REPORTES, exist_ok=True)

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            opcion_listar_cvs()
        elif opcion == "2":
            opcion_no_implementada(2)
        elif opcion == "3":
            opcion_no_implementada(3)
        elif opcion == "4":
            opcion_no_implementada(4)
        elif opcion == "5":
            opcion_no_implementada(5)
        elif opcion == "0":
            print("\nHasta luego.")
            break
        else:
            print("\nOpción no válida. Introduce un número del 0 al 5.")


if __name__ == "__main__":
    main()

import csv
from pathlib import Path
from src.calificacion import es_segmento_objetivo
from src.duplicados import detectar_duplicados
from src.calificacion import calificar_lead
from src.exportacion import (
    generar_csv,
    generar_csv_duplicados
)

BASE_DIR = Path(__file__).resolve().parent.parent

archivo = BASE_DIR / "data" / "leads_test_darhe.csv"


with open(archivo, mode="r", encoding="utf-8-sig", newline="") as csvfile:

    lector = csv.DictReader(csvfile)

    leads = list(lector)


registros_unicos, duplicados = detectar_duplicados(leads)


print("RESULTADOS DEL PROCESAMIENTO")
print("-----------------------------")

print(f"Registros originales: {len(leads)}")
print(f"Registros únicos: {len(registros_unicos)}")
print(f"Duplicados encontrados: {len(duplicados)}")


print("\nDUPLICADOS DETECTADOS")

for duplicado in duplicados:

    print(
        f"ID {duplicado['id']} "
        f"es duplicado del ID {duplicado['duplicado_de']}"
    )
print("\nREGISTROS CONSOLIDADOS")

for lead in registros_unicos:

    if lead["id"] in ["1", "4"]:

        print(f"\nID: {lead['id']}")
        print(f"Nombre: {lead['nombre']}")
        print(f"Empresa: {lead['empresa']}")
        print(f"Correo: {lead['email']}")
        print(f"Empleados: {lead['num_empleados']}")
        print(f"Mensaje: {lead['mensaje']}")

print("\nVALIDACIÓN DE SEGMENTOS")
print("-" * 40)

for lead in registros_unicos:

    segmento = lead["segmento"]

    objetivo = es_segmento_objetivo(segmento)

    print(
        f"ID: {lead['id']} | "
        f"Segmento: {segmento} | "
        f"Objetivo: {'Sí' if objetivo else 'No'}"
    )

print("\nCALIFICACIÓN DE LEADS")
print("-" * 50)

for lead in registros_unicos:

    calificacion, razon, revision = calificar_lead(lead)

    # Comprobar si el registro recibió datos de un duplicado
    tiene_duplicados = any(
        duplicado["duplicado_de"] == lead["id"]
        for duplicado in duplicados
    )

    if tiene_duplicados:
        revision = True

    print(f"\nID: {lead['id']}")
    print(f"Empresa: {lead['empresa']}")
    print(f"Calificación: {calificacion}")
    print(f"Razón: {razon}")
    print(f"Requiere revisión: {'Sí' if revision else 'No'}")

    motivos_revision = []

    if tiene_duplicados:
        motivos_revision.append(
            "Información consolidada de registros duplicados"
        )

    if revision and not tiene_duplicados:
        motivos_revision.append(
            "Información incompleta o decisión comercial por confirmar"
        )

    motivo_revision = "; ".join(motivos_revision)

    print(f"Motivo de revisión: {motivo_revision or 'No requiere'}")

ruta_salida = BASE_DIR / "output" / "leads_calificados.csv"

ruta_duplicados = "output/duplicados.csv"

total_duplicados = generar_csv_duplicados(
    duplicados,
    ruta_duplicados
)

print("\nARCHIVO DE DUPLICADOS GENERADO")
print(f"Ubicación: {ruta_duplicados}")
print(f"Duplicados exportados: {total_duplicados}")

resultados = generar_csv(
    registros_unicos,
    duplicados,
    ruta_salida
)

print("\nARCHIVO GENERADO CORRECTAMENTE")
print(f"Ubicación: {ruta_salida}")
print(f"Leads exportados: {len(resultados)}")
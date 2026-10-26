import csv
from pathlib import Path

from src.limpieza import (
    limpiar_nombre,
    limpiar_telefono,
    limpiar_email,
    limpiar_segmento
)

from src.calificacion import calificar_lead


def generar_csv(registros_unicos, duplicados, ruta_salida):


    resultados = []

    for lead in registros_unicos:

        calificacion, razon, revision = calificar_lead(lead)

        # Identificar duplicados asociados
        ids_duplicados = [
            d["id"]
            for d in duplicados
            if d["duplicado_de"] == lead["id"]
        ]

        motivos_revision = []

        # Revisar si existen registros duplicados
        if ids_duplicados:
            revision = True

            motivos_revision.append(
                "Información consolidada de registros duplicados"
            )

        # Revisar si existen teléfonos contradictorios
        if lead.get("conflicto_telefono", False):
            revision = True

            motivos_revision.append(
                "Teléfonos diferentes en registros duplicados; confirmar contacto"
            )

        # Revisar información incompleta o decisiones pendientes
        if revision and not motivos_revision:
            motivos_revision.append(
                "Validar información incompleta o decisión comercial"
            )
        if lead.get("telefono_corregido", False):
            revision = True

            motivos_revision.append(
                lead.get(
                    "motivo_correccion",
                    "Teléfono corregido durante la consolidación"
                )
            )

        # Determinar siguiente acción
        if calificacion == "A":
            accion = "Christian debe validar y priorizar contacto"

        elif calificacion == "B":
            accion = ("Christian debe validar la necesidad comercial "
            "y completar datos si corresponde")

        elif calificacion == "C":
            accion = "Mantener en seguimiento de baja prioridad"

        else:
            accion = "No contactar; revisar descarte si corresponde"

        resultados.append({
            "id": lead["id"],
            "nombre": limpiar_nombre(lead["nombre"]),
            "empresa": (lead.get("empresa") or "").strip(),
            "email": limpiar_email(lead["email"]),
            "telefono": limpiar_telefono(lead["telefono"]),
            "telefono_alternativo": lead.get(
            "telefono_alternativo", ""
            ),
            "conflicto_telefono": (
                "Sí" if lead.get("conflicto_telefono", False)
                else "No"
            ),
            "segmento": limpiar_segmento(lead["segmento"]),
            "num_empleados": lead["num_empleados"],
            "ciudad": lead["ciudad"],
            "fuente": lead["fuente"],
            "mensaje": lead["mensaje"],
            "duplicado_de": "",
            "ids_consolidados": ",".join(ids_duplicados),
            "calificacion": calificacion,
            "razon": razon,
            "siguiente_accion": accion,
            "requiere_revision": "Sí" if revision else "No",
            "motivo_revision": "; ".join(motivos_revision)
        })

    # Crear directorio de salida si no existe
    ruta_salida = Path(ruta_salida)
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    # Guardar CSV
    if resultados:

        columnas = list(resultados[0].keys())

        with open(
            ruta_salida,
            mode="w",
            newline="",
            encoding="utf-8-sig"
        ) as archivo:

            escritor = csv.DictWriter(
                archivo,
                fieldnames=columnas
            )

            escritor.writeheader()
            escritor.writerows(resultados)

    return resultados

def generar_csv_duplicados(duplicados, ruta_salida):

    # Definir las columnas del archivo
    columnas = [
        "id",
        "duplicado_de"
    ]

    # Crear la ruta de salida
    ruta_salida = Path(ruta_salida)

    # Crear la carpeta si no existe
    ruta_salida.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Generar el archivo CSV
    with open(
        ruta_salida,
        mode="w",
        newline="",
        encoding="utf-8-sig"
    ) as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=columnas
        )

        escritor.writeheader()

        escritor.writerows(duplicados)

    return len(duplicados)
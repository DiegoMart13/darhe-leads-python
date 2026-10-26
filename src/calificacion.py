from src.limpieza import limpiar_segmento


SEGMENTOS_OBJETIVO = {
    "Transportistas",
    "Restauranteros",
    "Construcción",
    "Empresarios"
}


def es_segmento_objetivo(segmento):

    segmento_limpio = limpiar_segmento(segmento)

    return segmento_limpio in SEGMENTOS_OBJETIVO

from src.limpieza import normalizar_comparacion


def detectar_necesidad(mensaje):

    if not mensaje:
        return False

    mensaje = normalizar_comparacion(mensaje)

    palabras_clave = [
        "cotizacion",
        "demo",
        "demostracion",
        "necesitamos controlar",
        "queremos controlar",
        "dejar de pagar",
        "pagamos a cuadrillas"
    ]

    return any(
        palabra in mensaje
        for palabra in palabras_clave
    )

def validar_empleados(valor):

    try:
        empleados = int(valor)

        if empleados < 0:
            return None

        return empleados

    except (ValueError, TypeError):
        return None

from src.limpieza import limpiar_telefono, limpiar_email


def calificar_lead(lead):

    segmento = lead.get("segmento", "")
    empleados = validar_empleados(
        lead.get("num_empleados", "")
    )

    mensaje = lead.get("mensaje", "")

    telefono = limpiar_telefono(
        lead.get("telefono", "")
    )

    email = limpiar_email(
        lead.get("email", "")
    )

    empresa = lead.get("empresa", "").lower()

    requiere_revision = False

    # 1. Detectar spam
    if "gana $$$" in mensaje.lower():
        return (
            "Descartado",
            "Mensaje identificado como spam.",
            False
        )

    # 2. Detectar posibles competidores
    if "competencia" in empresa:
        return (
            "Descartado",
            "Posible competidor.",
            True
        )

    # 3. Comprobar contacto
    if not telefono and not email:
        return (
            "Descartado",
            "No tiene un medio de contacto utilizable.",
            True
        )

    # 4. Comprobar segmento objetivo
    if not es_segmento_objetivo(segmento):
        return (
            "C",
            "Empresa fuera del segmento objetivo.",
            False
        )

    # 5. Comprobar empleados
    if empleados is not None and empleados < 20:
        return (
            "C",
            "Empresa con menos de 20 empleados.",
            False
        )

    # 6. Evaluar necesidad
    necesidad = detectar_necesidad(mensaje)

    if empleados is None:
        requiere_revision = True

    # 7. Clasificación A
    if empleados is not None and empleados >= 20 and necesidad:
        return (
            "A",
            "Segmento objetivo, al menos 20 empleados y necesidad concreta.",
            requiere_revision
        )

    # 8. Clasificación B
    return (
        "B",
        "Segmento objetivo con necesidad vaga o información incompleta.",
        requiere_revision
    )
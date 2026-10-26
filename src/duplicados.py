from src.limpieza import (
    limpiar_nombre,
    limpiar_telefono,
    normalizar_comparacion,
    limpiar_email
)


def detectar_duplicados(leads):

    registros_unicos = []
    duplicados = []

    for lead in leads:

        telefono = limpiar_telefono(lead.get("telefono", ""))

        nombre = normalizar_comparacion(
            limpiar_nombre(lead.get("nombre", ""))
        )

        email = limpiar_email(lead.get("email", ""))

        duplicado_encontrado = None

        for registro in registros_unicos:

            telefono_existente = limpiar_telefono(
                registro.get("telefono", "")
            )

            nombre_existente = normalizar_comparacion(
                limpiar_nombre(registro.get("nombre", ""))
            )

            email_existente = limpiar_email(
                registro.get("email", "")
            )

            mismo_nombre = (
                bool(nombre)
                and nombre == nombre_existente
            )

            mismo_telefono = (
                bool(telefono)
                and telefono == telefono_existente
            )

            mismo_email = (
                bool(email)
                and email == email_existente
            )
            
            if mismo_nombre and (mismo_telefono or mismo_email):

                duplicado_encontrado = registro
                break

        if duplicado_encontrado:

            consolidar_datos(duplicado_encontrado, lead)

            duplicados.append({
                "id": lead["id"],
                "duplicado_de": duplicado_encontrado["id"]
            })

        else:

            registros_unicos.append(lead.copy())

    return registros_unicos, duplicados

from src.limpieza import limpiar_email


def consolidar_datos(principal, duplicado):

    # Normalizar ambos teléfonos
    telefono_principal = limpiar_telefono(
        principal.get("telefono", "")
    )

    telefono_duplicado = limpiar_telefono(
        duplicado.get("telefono", "")
    )

    # Caso 1: El principal es inválido y el duplicado es válido
    if not telefono_principal and telefono_duplicado:

        principal["telefono"] = telefono_duplicado

        principal["telefono_corregido"] = True

        principal["motivo_correccion"] = (
            "Se sustituyó un teléfono inválido o vacío "
            "por uno válido del registro duplicado"
        )

    # Caso 2: Ambos teléfonos son válidos, pero diferentes
    elif (
        telefono_principal
        and telefono_duplicado
        and telefono_principal != telefono_duplicado
    ):

        principal["conflicto_telefono"] = True

        principal["telefono_alternativo"] = telefono_duplicado

    # Completar campos vacíos del registro principal
    campos = [
        "nombre",
        "empresa",
        "email",
        "telefono",
        "segmento",
        "num_empleados",
        "ciudad"
    ]

    for campo in campos:

        valor_principal = principal.get(campo, "").strip()
        valor_duplicado = duplicado.get(campo, "").strip()

        if not valor_principal and valor_duplicado:
            principal[campo] = valor_duplicado

    # Recuperar un correo mejor formado
    def formato_email_valido(email):
        import re

        patron = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

        return bool(re.fullmatch(patron, email.strip()))


    email_principal = principal.get("email", "").strip()
    email_duplicado = duplicado.get("email", "").strip()

    if (
        not formato_email_valido(email_principal)
        and formato_email_valido(email_duplicado)
    ):
        principal["email"] = email_duplicado

    # Conservar mensajes diferentes
    mensaje_principal = principal.get("mensaje", "").strip()
    mensaje_duplicado = duplicado.get("mensaje", "").strip()

    if mensaje_duplicado and mensaje_duplicado != mensaje_principal:

        principal["mensaje"] = (
            mensaje_principal + " | " + mensaje_duplicado
        ).strip(" | ")

    return principal
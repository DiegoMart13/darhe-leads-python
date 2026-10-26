# Limpiar nombres
def limpiar_nombre(nombre):

    if not nombre:
        return ""

    nombre = nombre.strip()

    nombre = " ".join(nombre.split())

    nombre = nombre.title()

    return nombre

import re

# Limpiar telefonos
def limpiar_telefono(telefono):

    if not telefono:
        return ""

    # Eliminar caracteres que no sean números
    telefono = re.sub(r"\D", "", telefono)

    # Si contiene el prefijo internacional 52
    if len(telefono) == 12 and telefono.startswith("52"):
        telefono = telefono[2:]

    # Si no tiene exactamente 10 dígitos
    if len(telefono) != 10:
        return ""

    # Rechazar números compuestos únicamente por ceros
    if telefono == "0000000000":
        return ""

    return "+52" + telefono

# Limpiar emails
import re


def limpiar_email(email):

    if not email:
        return ""

    email = email.strip().lower()

    patron = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    if not re.fullmatch(patron, email):
        return ""

    return email

# Limpiar segmentos
def limpiar_segmento(segmento):

    if not segmento:
        return ""

    segmento = segmento.strip().lower()

    segmentos = {
        "transportista": "Transportistas",
        "transportistas": "Transportistas",

        "restaurante": "Restauranteros",
        "restaurantes": "Restauranteros",
        "restaurant": "Restauranteros",
        "restaurantero": "Restauranteros",
        "restauranteros": "Restauranteros",

        "construccion": "Construcción",
        "construcción": "Construcción",
        "constructora": "Construcción",

        "empresario": "Empresarios",
        "empresarios": "Empresarios",
        "empresarial": "Empresarios",
    }

    return segmentos.get(segmento, segmento.title())

# Encontrar duplicados.

import unicodedata

def normalizar_comparacion(texto):

    if not texto:
        return ""

    texto = texto.strip().lower()

    texto = unicodedata.normalize("NFD", texto)

    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )

    texto = " ".join(texto.split())

    return texto
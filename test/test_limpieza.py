import unittest
import sys
from pathlib import Path


# Permitir importar módulos desde src
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.limpieza import limpiar_nombre, limpiar_telefono, limpiar_segmento
from src.calificacion import calificar_lead
from src.duplicados import detectar_duplicados


class TestLimpieza(unittest.TestCase):

    def test_nombre(self):
        resultado = limpiar_nombre("LAURA MENDEZ")
        self.assertEqual(resultado, "Laura Mendez")

    def test_telefono_valido(self):
        resultado = limpiar_telefono("55 1234 5678")
        self.assertEqual(resultado, "+525512345678")

    def test_telefono_invalido(self):
        resultado = limpiar_telefono("12345")
        self.assertEqual(resultado, "")

    def test_segmento(self):
        resultado = limpiar_segmento("restaurant")
        self.assertEqual(resultado, "Restauranteros")
    def test_lead_a(self):

        lead = {
            "empresa": "Transportes del Norte",
            "segmento": "transportista",
            "num_empleados": "80",
            "mensaje": "Necesitamos una cotización",
            "telefono": "5512345678",
            "email": ""
        }

        calificacion, razon, revision = calificar_lead(lead)

        self.assertEqual(calificacion, "A")


    def test_lead_c(self):

        lead = {
            "empresa": "Restaurante Familiar",
            "segmento": "restaurantero",
            "num_empleados": "10",
            "mensaje": "Necesitamos una cotización",
            "telefono": "5512345678",
            "email": ""
        }

        calificacion, razon, revision = calificar_lead(lead)

        self.assertEqual(calificacion, "C")


    def test_lead_descartado(self):

        lead = {
            "empresa": "Promo Store",
            "segmento": "",
            "num_empleados": "",
            "mensaje": "Gana $$$ desde casa",
            "telefono": "0000000000",
            "email": ""
        }

        calificacion, razon, revision = calificar_lead(lead)

        self.assertEqual(calificacion, "Descartado")

    def test_duplicados_mismo_email(self):

        leads = [
            {
                "id": "20",
                "nombre": "Carlos Pérez",
                "telefono": "5512345678",
                "email": "carlos@empresa.com",
                "empresa": "Transportes del Norte",
                "mensaje": "Solicito información"
            },
            {
                "id": "21",
                "nombre": "Carlos Pérez",
                "telefono": "5587654321",
                "email": "carlos@empresa.com",
                "empresa": "Transportes del Norte",
                "mensaje": "Quiero una cotización"
            }
        ]

        registros_unicos, duplicados = detectar_duplicados(leads)

        self.assertEqual(len(registros_unicos), 1)
        self.assertEqual(len(duplicados), 1)

        self.assertEqual(
            duplicados[0]["duplicado_de"],
            "20"
        )
    def test_no_fusionar_personas_diferentes(self):

        leads = [
            {
                "id": "30",
                "nombre": "Juan Pérez",
                "telefono": "5512345678",
                "email": "juan@empresa.com",
                "empresa": "Empresa Norte",
                "mensaje": "Solicito información"
            },
            {
                "id": "31",
                "nombre": "Ana López",
                "telefono": "5512345678",
                "email": "ana@empresa.com",
                "empresa": "Empresa Norte",
                "mensaje": "Solicito una demostración"
            }
        ]

        registros_unicos, duplicados = detectar_duplicados(leads)

        self.assertEqual(len(registros_unicos), 2)
        self.assertEqual(len(duplicados), 0)

    def test_conflicto_telefonico(self):

        leads = [
            {
                "id": "40",
                "nombre": "Carlos Pérez",
                "telefono": "5512345678",
                "email": "carlos@empresa.com",
                "empresa": "Transportes Norte",
                "mensaje": "Solicito información"
            },
            {
                "id": "41",
                "nombre": "Carlos Pérez",
                "telefono": "5587654321",
                "email": "carlos@empresa.com",
                "empresa": "Transportes Norte",
                "mensaje": "Solicito cotización"
            }
        ]

        registros_unicos, duplicados = detectar_duplicados(leads)

        self.assertEqual(len(registros_unicos), 1)

        self.assertEqual(len(duplicados), 1)

        principal = registros_unicos[0]

        self.assertTrue(
            principal.get("conflicto_telefono", False)
        )

        self.assertEqual(
            principal.get("telefono_alternativo"),
            "+525587654321"
        )
    def test_reemplazar_telefono_invalido(self):

        leads = [
            {
                "id": "1",
                "nombre": "Carlos Pérez",
                "telefono": "12345",
                "email": "carlos@empresa.com",
                "empresa": "Transportes Norte",
                "mensaje": "Solicito información"
            },
            {
                "id": "2",
                "nombre": "Carlos Pérez",
                "telefono": "5512345678",
                "email": "carlos@empresa.com",
                "empresa": "Transportes Norte",
                "mensaje": "Solicito cotización"
            }
        ]

        registros_unicos, duplicados = detectar_duplicados(leads)

        self.assertEqual(len(registros_unicos), 1)

        principal = registros_unicos[0]

        self.assertEqual(
            limpiar_telefono(principal["telefono"]),
            "+525512345678"
        )

        self.assertTrue(
            principal.get("telefono_corregido", False)
        )

if __name__ == "__main__":
    unittest.main()


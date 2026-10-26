# Sistema de Calificación de Leads — DARHE

## Descripción

Sistema desarrollado en Python para automatizar el procesamiento inicial de leads comerciales provenientes de diferentes canales. Su propósito es limpiar la información, detectar registros repetidos, asignar una calificación preliminar y facilitar la priorización comercial, **sin realizar contactos automáticos**.

El programa permite:

- Leer registros desde un archivo CSV.
- Normalizar nombres, teléfonos mexicanos, correos electrónicos y segmentos comerciales.
- Detectar duplicados mediante coincidencia de nombre normalizado y teléfono **o** correo válido coincidente.
- Consolidar información de contactos repetidos y conservar mensajes complementarios.
- Detectar teléfonos distintos asociados a un contacto consolidado, conservando un teléfono alternativo para revisión.
- Clasificar leads como A, B, C o Descartado, con una razón y una acción recomendada.
- Marcar casos que requieren revisión humana.
- Exportar los leads consolidados y la relación de duplicados en archivos CSV separados.

## Tecnologías utilizadas

- Python 3.
- Bibliotecas estándar: `csv`, `re`, `unicodedata` y `pathlib`.
- Pruebas automatizadas con `unittest`.

No se requieren APIs de pago ni dependencias externas.

## Estructura del proyecto

```text
Entrevista de trabajo/
├── data/
│   └── leads_test_darhe.csv
├── output/
│   ├── leads_calificados.csv
│   └── duplicados.csv
├── src/
│   ├── index.py
│   ├── limpieza.py
│   ├── duplicados.py
│   ├── calificacion.py
│   └── exportacion.py
├── test/
│   └── test_limpieza.py
├── README.md
├── BITACORA_IA.md
└── RESUMEN_CHRISTIAN.md
```

`RESUMEN_CHRISTIAN.md` corresponde al resumen comercial de una página, que debe incluirse en la entrega final. El archivo auxiliar `ver_resultados.py`, si se conserva, sirve para inspeccionar el CSV y no forma parte del procesamiento principal.

## Ejecución

Desde la carpeta principal del proyecto:

```bash
python src/index.py
```

**Entrada:** `data/leads_test_darhe.csv`.

**Salidas:**

- `output/leads_calificados.csv`: un registro por lead consolidado, con datos normalizados, calificación, razón, siguiente acción, revisión humana y campos adicionales de trazabilidad.
- `output/duplicados.csv`: correspondencia `id,duplicado_de` de los registros fusionados.

Para consultar los resultados mediante el script auxiliar (si está presente):

```bash
python ver_resultados.py
```

## Resultados del conjunto de prueba

Con los 15 registros ficticios proporcionados:

| Resultado | Cantidad |
|---|---:|
| Registros originales | 15 |
| Duplicados fusionados | 2 |
| Leads consolidados | 13 |
| Calificación A | 2 |
| Calificación B | 5 |
| Calificación C | 4 |
| Descartados | 2 |

Se identificaron las fusiones **ID 3 → ID 1** e **ID 14 → ID 4**. En la última salida revisada, los leads 1, 4, 11 y 12 estaban marcados para revisión humana.

## Pruebas

Desde la raíz del proyecto:

```bash
python -m src.index
python -m unittest discover -s test -v
```

En la última ejecución observada se aprobaron **10 pruebas**. Cubren:

- Normalización de nombres y segmentos.
- Teléfonos válidos e inválidos.
- Clasificaciones A, C y Descartado.
- Duplicados identificados por correo coincidente.
- Prevención de fusión entre personas diferentes.
- Identificación de conflictos entre teléfonos.

Las pruebas comprueban escenarios definidos; no sustituyen pruebas de integración, de carga ni revisión manual de casos ambiguos.

## Reglas de calificación

- **A:** segmento objetivo, 20 empleados o más, necesidad concreta y medio de contacto con formato válido.
- **B:** segmento objetivo y contacto válido, pero necesidad vaga o información insuficiente para A.
- **C:** menos de 20 empleados o segmento fuera del mercado objetivo.
- **Descartado:** spam, posible competidor o ausencia de un medio de contacto válido.

Segmentos objetivo: transportistas, restauranteros, construcción y empresarios en general. Las reglas son provisionales; las decisiones ambiguas deben documentarse y someterse a revisión humana.

## Supuestos y decisiones

1. Los teléfonos se normalizan al formato `+52` seguido de 10 dígitos cuando cumplen la estructura esperada. No se verifica que la línea exista o esté activa.
2. Los correos `.example` del conjunto ficticio se evalúan por formato; no se consideran buzones reales verificados.
3. La detección de duplicados exige **mismo nombre normalizado** y, además, **mismo teléfono válido o mismo correo válido**. Compartir teléfono o dominio de correo por sí solo no basta para fusionar personas distintas.
4. Se conserva un registro principal por contacto; los IDs fusionados quedan documentados en `duplicados.csv` y en los campos de trazabilidad de la salida principal.
5. Si aparecen dos teléfonos válidos diferentes en registros fusionados, se registra el conflicto y el teléfono alternativo para validación humana. No se asume automáticamente cuál es el correcto.
6. Los registros consolidados requieren revisión humana. Una calificación A no equivale a autorización de contacto.
7. Un número de empleados desconocido impide asignar A sin aclaración. Los criterios de prioridad entre leads incluyen necesidad, urgencia y tamaño, de forma provisional.
8. Ningún lead se contacta automáticamente: **Christian valida y autoriza antes de cualquier contacto**.

## Manejo de datos incorrectos

- Los teléfonos que no cumplen la estructura esperada se dejan vacíos tras la normalización.
- Los correos con formato inválido se consideran no válidos; un correo válido de un registro duplicado puede completar el registro principal.
- Si `num_empleados` no puede interpretarse como número, se trata como dato desconocido y puede requerir revisión.
- Los registros incompletos se clasifican según las reglas disponibles; los casos ambiguos se marcan para revisión.
- La detección de duplicados es conservadora para evitar fusionar contactos distintos.

**Límite del alcance probado:** no se ha verificado con pruebas automatizadas el comportamiento frente a archivos inexistentes, encabezados faltantes o CSV corruptos. Esos casos requieren controles adicionales antes de uso productivo.

## Limitaciones actuales

- La detección de duplicados no utiliza similitud difusa y puede omitir variaciones importantes de nombres.
- La identificación de necesidades comerciales depende de reglas y palabras clave.
- No se verifica la existencia real de teléfonos ni correos.
- Los conflictos entre datos consolidados requieren validación humana.
- La priorización es una recomendación, no una decisión comercial definitiva.
- No existe todavía una interfaz de aprobación ni integración con CRM.

## Mejoras con dos semanas adicionales

1. Incorporar validaciones de estructura del CSV y manejo explícito de errores de entrada/salida.
2. Agregar pruebas de integración, casos límite y conjuntos de datos más grandes.
3. Mejorar la detección de duplicados con similitud controlada y revisión de coincidencias dudosas.
4. Interpretar mensajes mediante técnicas de procesamiento de lenguaje natural, con evaluación de resultados.
5. Crear una interfaz para que Christian revise, apruebe o rechace recomendaciones.
6. Guardar los leads y el historial de decisiones en PostgreSQL/Supabase.
7. Recibir nuevos registros mediante webhook y registrar auditoría de cambios.

## Supervisión humana

Las calificaciones y acciones son **recomendaciones preliminares**. `requiere_revision` señala anomalías o decisiones ambiguas; incluso cuando su valor sea `No`, **Christian debe validar antes de autorizar cualquier contacto comercial**.

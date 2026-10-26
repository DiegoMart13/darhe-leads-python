# Bitácora de Inteligencia Artificial

## Proyecto: Sistema de Calificación de Leads — DARHE

### 1. Herramientas utilizadas

**ChatGPT (OpenAI):** apoyo para comprender requisitos, discutir decisiones de diseño, proponer fragmentos de código, explicar errores y diseñar pruebas. Las sugerencias se contrastaron con la ejecución real y con los criterios comerciales solicitados.

**Visual Studio Code:** entorno de desarrollo para editar, ejecutar, depurar y revisar los archivos del proyecto. Es una herramienta de desarrollo, no un modelo de IA.

Se utilizó Python y su biblioteca estándar para implementar y probar el sistema, sin recurrir a APIs de pago.

### 2. Prompts clave

Los siguientes cinco prompts son **representativos y parafraseados**; no son transcripciones literales de todas las conversaciones.

**Prompt 1 — Comprender la prueba técnica**

> Explícame los requisitos de DARHE y ayúdame a resolverlos paso a paso, de modo que pueda comprender las decisiones y defenderlas en una entrevista.

**Prompt 2 — Modularidad y limpieza**

> Quiero separar la limpieza de datos en funciones y archivos independientes para facilitar las modificaciones y las pruebas.

**Prompt 3 — Duplicados y seguridad de la consolidación**

> ¿Cómo podemos detectar duplicados por nombre y teléfono o correo, sin fusionar a personas distintas que compartan un número? ¿Qué hacemos si hay dos teléfonos válidos diferentes?

**Prompt 4 — Calificación y supervisión humana**

> Ayúdame a aplicar las reglas A, B, C y Descartado, explicar cada resultado y marcar los casos ambiguos que Christian deba revisar antes de contactar.

**Prompt 5 — Pruebas y entregables**

> ¿Cómo pruebo con unittest la limpieza, la detección de duplicados y los conflictos telefónicos, y cómo documento y exporto los resultados de forma verificable?

### 3. Errores de IA identificados y correcciones

**Validación de correos.** Durante el desarrollo se propuso una expresión regular incorrecta que afectaba la identificación de direcciones con formato válido. Se revisó el resultado de la consolidación, se corrigió el patrón y se volvió a comprobar la conservación de los correos.

**Flujo de una función de consolidación.** En una revisión apareció un `return principal` antes del bloque que completaba los campos faltantes. Esto habría terminado la función prematuramente y dejado código sin ejecutar. Se detectó al inspeccionar el orden de las instrucciones y se corrigió la posición del `return`.

**Comando de inspección del CSV.** Se sugirió un comando `python -c` con comillas que no funcionó correctamente en PowerShell. Se sustituyó por un script Python sencillo (`ver_resultados.py`), más fácil de leer y depurar.

Estos ejemplos muestran por qué las respuestas de IA se trataron como propuestas y no como código validado automáticamente.

### 4. Decisiones y mejoras durante el desarrollo

- Se organizó el programa en módulos de limpieza, duplicados, calificación y exportación.
- La regla de duplicados pasó de comparar nombre y teléfono a comparar nombre y **teléfono o correo válido**, manteniendo un criterio conservador para no fusionar personas distintas.
- Se incorporó la detección de conflictos entre teléfonos y la conservación de un teléfono alternativo.
- Se separó la trazabilidad de duplicados en `output/duplicados.csv`.
- Se distinguió entre **revisión especial de datos** y **autorización comercial obligatoria**: Christian debe aprobar cualquier contacto, aunque `requiere_revision` sea `No`.

### 5. Validación de resultados

La verificación se realizó mediante ejecución del programa, inspección de los CSV, comparación de IDs duplicados, revisión de clasificaciones y pruebas automatizadas.

En la última ejecución observada:

- **15** registros originales.
- **13** leads consolidados.
- **2** duplicados: ID 3 → ID 1 e ID 14 → ID 4.
- **10 pruebas `unittest` aprobadas**, incluidas pruebas de duplicados por correo, prevención de fusiones indebidas y conflictos telefónicos.

Las pruebas no demuestran que el sistema cubra todos los errores posibles; siguen pendientes pruebas de integración y manejo exhaustivo de entradas dañadas.

### 6. Aprendizajes

La IA aceleró la comprensión y la implementación, pero no reemplazó la revisión del código. Fue necesario entender la diferencia entre una coincidencia de datos y la identidad real de una persona, revisar el alcance de `return`, corregir problemas de importación y rutas, y distinguir la clasificación automática de la decisión comercial humana.

El aprendizaje principal fue **verificar cada propuesta con casos concretos, entender por qué funciona y documentar sus límites**, para poder explicar y modificar la solución durante una entrevista técnica.

# Skill: Respuesta a Consultas

## Propósito
Define cómo el agente debe responder preguntas del usuario usando el contenido de la wiki.

## Regla de Fuente de Verdad
El agente responde **exclusivamente** desde `/wiki/`. No consulta `/raw/` directamente
salvo que el usuario lo solicite de forma explícita.

## Proceso de Consulta

1. **Interpretar la pregunta**: Identificar entidades, conceptos o períodos de tiempo relevantes.
2. **Leer el índice**: Consultar `index.md` para localizar páginas candidatas.
3. **Leer páginas relevantes**: Acceder en profundidad a las páginas identificadas.
4. **Sintetizar respuesta**: Formular la respuesta con citas directas a las fichas de la wiki y enlaces explícitos a las fuentes originales en `wiki/fuentes/` que sustentan la información.
5. **Formato de salida**: Adaptar el formato según la naturaleza de la pregunta:
   - Respuesta narrativa → Markdown
   - Comparación → Tabla Markdown
   - Tendencia temporal → Lista cronológica
   - Datos → Bloque de código o gráfico (si se dispone de script)
6. **Archivar si es valioso**: Si la respuesta tiene valor acumulativo (análisis, comparación),
   proponer guardarla como nueva página en `/wiki/conceptos_financieros/`, `/wiki/tesis_inversion/` o `/wiki/empresas/`.
7. **Registrar**: Añadir entrada en `log.md`.

## Trazabilidad y Enlazado Obligatorio
Toda respuesta que provenga de datos procesados debe incluir abundantes enlaces a la base de conocimiento. Si se nombra una empresa, autor o concepto que tiene ficha (o debería tenerla), **DEBE enlazarse**.
**FORMATO ESTRICTO DE ENLACE:** Siempre se debe usar el formato `[[slug_del_archivo|Nombre Visible Normal]]` (ej. `[[immunity_bio|ImmunityBio]]`, `[[gregorio_hernandez|Gregorio Hernández]]`). Está prohibido usar solo el slug `[[immunity_bio]]` porque arruina la legibilidad, y prohibido no enlazar los conceptos. Al final de la respuesta, incluir una sección de **"Fuentes Consultadas"** con enlaces a los archivos de `wiki/fuentes/` correspondientes.

## Límite de Conocimiento
Si la información no está en `/wiki/`, el agente debe indicarlo claramente y
sugerir fuentes para ingestar en lugar de inventar datos.

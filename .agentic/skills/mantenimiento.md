# Skill: Mantenimiento y Calidad del Grafo

## Propósito
Define las tareas de mantenimiento periódico que el agente debe ejecutar para
garantizar la coherencia, completitud y calidad de la wiki.

## Checks de Validación (post-ingesta y periódico)

### 1. Bidireccionalidad de Enlace
- Si la Nota A enlaza a `[[Nota B]]`, verificar que Nota B tenga enlace de retorno.
- Si falta → añadirlo en la sección `## Relacionados` de Nota B.

### 2. Detección de Menciones sin Enlace
- Al crear o actualizar contenido, buscar términos que coincidan con títulos de páginas existentes.
- Convertirlos en `[[wikilinks]]` activos.

### 3. Páginas Huérfanas
- Identificar páginas sin enlaces entrantes.
- Proponer integración o eliminación al usuario.

### 4. Contradicciones y Síntesis Obsoleta
- Marcar conflictos con:
  ```
  > [!CAUTION] Contradicción
  > Versión A (fuente X, fecha): ...
  > Versión B (fuente Y, fecha): ...
  ```
- Nunca eliminar datos contradictorios sin confirmación del usuario.

### 5. Fusión de Duplicados (Alias)
- Identificar páginas sobre el mismo tema con nombres distintos.
- Proponer fusión al usuario antes de ejecutarla.
- El archivo resultante debe incluir `aliases:` con los nombres anteriores.

### 6. Consistencia del Índice
- `index.md` debe reflejar siempre todas las páginas actuales.
- Actualizar tras cada ingesta o modificación de estructura.

## Frecuencia Recomendada
Ejecutar una revisión completa cada 10 ingestas o a petición del usuario.

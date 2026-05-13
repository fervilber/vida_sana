# Workflow: Revisión Periódica de la Wiki

## Propósito
Mantener la coherencia, calidad y completitud del grafo de conocimiento.

## Activación
El usuario dice: `«Realiza un mantenimiento de la wiki»` o `«Realiza un mantenimiento de los enlaces»`
O automáticamente cada 10 procesos (registrado en el log).

## Pasos

### Paso 1 — Cargar la skill de mantenimiento
Leer `.agentic/skills/mantenimiento.md`.

### Paso 2 — Auditoría estructural
- Verificar que `index.md` lista todas las páginas actuales de `/wiki/`.
- Detectar archivos en `/wiki/` no listados en el índice → añadirlos.

### Paso 3 — Auditoría de enlaces
- Detectar páginas huérfanas (sin enlaces entrantes).
- Detectar menciones de términos existentes sin `[[wikilink]]`.
- Verificar bidireccionalidad de todos los enlaces.

### Paso 4 — Auditoría de contradicciones
- Buscar bloques `[!CAUTION]` sin resolución.
- Listar al usuario las contradicciones pendientes para su decisión.

### Paso 5 — Detección de duplicados
- Identificar páginas con aliases similares o que traten el mismo tema.
- Proponer fusiones sin ejecutarlas hasta confirmación del usuario.

### Paso 6 — Reporte de salud
Generar un informe breve en Markdown con:
- Total páginas por categoría
- Páginas huérfanas encontradas
- Contradicciones activas
- Sugerencias de nuevas fuentes o investigaciones

### Paso 7 — Registrar revisión
Añadir entrada en `log.md`:
```
## [YYYY-MM-DD] mantiene | Revisión Periódica
- Páginas auditadas: X
- Huérfanas: Y
- Contradicciones abiertas: Z
- Acciones tomadas: ...
```

### Paso 8 — Commit local
Si se realizaron cambios (enlaces corregidos, páginas actualizadas, etc.):
```bash
git add -A
git commit -m "mantiene: revisión YYYY-MM-DD — <resumen de acciones>"
```
Si no hubo cambios → informar al usuario y omitir el commit.
El push a GitHub **no es automático** — ejecutar solo si el usuario lo pide.

# Workflow: Inicialización del Proyecto

## Propósito
Secuencia de arranque que el agente debe ejecutar la primera vez que se accede
a este proyecto, o tras una restauración desde Git.

## Pasos

### Paso 1 — Leer el entorno
1. Leer `RULES.md` en la raíz → comprender estructura y reglas operativas.
2. Leer este archivo → cargar el flujo de inicialización.
3. Verificar que todos los directorios definidos en `RULES.md §1` existen:
   - `raw/`, `wiki/alimentacion/`, `wiki/dietas/`, `wiki/recetas/`
   - `wiki/ejercicio/`, `wiki/salud/`, `wiki/conceptos/`
   - `wiki/fuentes/`, `wiki/autores/`, `wiki/blog/`

### Paso 2 — Verificar archivos críticos
Comprobar la existencia de:
- [ ] `index.md`
- [ ] `log.md`
- [ ] `.agentic/templates/nota-fuente.md`
- [ ] `.agentic/templates/nota-tema.md`
- [ ] `.agentic/templates/nota-concepto.md`
- [ ] `.agentic/templates/nota-receta.md`
- [ ] `.agentic/templates/nota-protocolo.md`

Si alguno falta → crearlo usando el template vacío correspondiente.

### Paso 3 — Verificar estado Git
```bash
git status
git log --oneline origin/main..HEAD
git remote -v
```
Informar al usuario de:
- Rama activa (`git branch --show-current`)
- Commits locales pendientes de push (si los hay)
- Remoto configurado (debe apuntar a `github.com/fervilber/vida_sana`)

Si hay commits locales sin push → **preguntar al usuario** si quiere hacer push ahora.
No ejecutar push automáticamente durante la inicialización.

### Paso 4 — Cargar skills activas
El agente debe conocer las skills disponibles:
- `.agentic/skills/ingesta.md` → procesamiento de fuentes
- `.agentic/skills/consulta.md` → respuesta a preguntas
- `.agentic/skills/mantenimiento.md` → calidad del grafo
- `.agentic/skills/evidencia.md` → evaluación de evidencia científica ⭐
- `.agentic/skills/examenes.md` → tests de autoevaluación
- `.agentic/skills/git.md` → sincronización con GitHub
- `.agentic/skills/excalidraw.md` → creación de diagramas

### Paso 5 — Reportar estado al usuario
Informar brevemente:
- Número de páginas en `/wiki/` por sección
- Última entrada en `log.md`
- Estado de sincronización Git
- Cualquier anomalía detectada (páginas huérfanas, índice desactualizado)

### Paso 6 — Confirmar disponibilidad
El agente debe indicar explícitamente que está listo para recibir instrucciones.
Recordar al usuario los comandos principales:

```
«Procesa [fuente]»                    → procesamiento de nueva fuente
«¿Qué sabemos sobre [alimento/dieta]?» → consulta a la wiki
«Dame una receta [especificación]»    → buscar o crear receta
«Realiza un mantenimiento»            → revisión de calidad del grafo
«Crea un examen de [tema]»            → test de autoevaluación
«Crea un diagrama de...»              → Excalidraw
```

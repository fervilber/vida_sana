# Workflow: Procesamiento de Nueva Fuente

## Propósito
Algoritmo completo para procesar un archivo de `/raw/` e integrarlo en la wiki de vida sana.

## Activación
El usuario dice: `«Procesa [ruta o nombre del archivo]»` o `«Analiza y procesa [ruta]»`

## Pasos

### Paso 1 — Cargar la skill
Leer `.agentic/skills/ingesta.md` para aplicar las reglas de procesamiento.

### Paso 2 — Leer la fuente
- Acceder al archivo indicado en `/raw/` (nunca modificarlo).
- Si es una imagen o PDF no procesable, solicitar al usuario una transcripción o descripción.

### Paso 3 — Identificar fecha original
Localizar en la fuente la fecha de publicación original. Si no está en el archivo, buscarla en metadatos o preguntar al usuario. **Esta fecha gobernará todo el análisis.**

### Paso 4 — Analizar y extraer
Identificar en el contenido:
- **Alimentos / Nutrientes / Suplementos** (beneficios, contraindicaciones, dosis)
- **Dietas o Patrones Alimentarios** (descripción, evidencia, objetivo)
- **Recetas** (ingredientes, preparación, perfil nutricional)
- **Protocolos de Ejercicio** (tipo, estructura, frecuencia)
- **Condiciones de Salud y Hábitos** (mecanismos, recomendaciones)
- **Conceptos Científicos** (definiciones, mecanismos biológicos)
- **Autor/Divulgador** y su perfil de recomendaciones
- **Nivel de Evidencia** de cada afirmación (aplicar `skills/evidencia.md`)

### Paso 5 — Confirmar con el usuario
Presentar un resumen breve de lo extraído y preguntar si el enfoque es correcto
(incluyendo la fecha original detectada). *(Opcional: omitir si el usuario ha dado autonomía total.)*

### Paso 6 — Ejecutar escritura
Aplicar la lógica de `ingesta.md`:
- Consultar `index.md` para detectar páginas relacionadas existentes.
- Crear o actualizar páginas en `/wiki/alimentacion/`, `/wiki/dietas/`, `/wiki/recetas/`,
  `/wiki/ejercicio/`, `/wiki/salud/`, `/wiki/conceptos/`, `/wiki/fuentes/`, `/wiki/autores/`.
- Usar los templates de `.agentic/templates/`.
- Insertar `[[wikilinks]]` y verificar bidireccionalidad.
- **CRÍTICO**: Actualizar siempre la página del autor correspondiente en `wiki/autores/`.

### Paso 7 — Validar con linter
Si el script `scripts/lint.py` está disponible, ejecutarlo sobre las páginas modificadas:
```bash
python scripts/lint.py wiki/
```

### Paso 8 — Actualizar registros
- Añadir entrada en `log.md`:
  ```
  ## [YYYY-MM-DD] procesa | Nombre del Archivo
  - Páginas creadas: X
  - Páginas actualizadas: Y
  - Notas: ...
  ```
- Actualizar `index.md` con las nuevas páginas y actualizar los contadores de la tabla de estado.

### Paso 9 — Commit local
Guardar los cambios en git localmente (ver `.agentic/skills/git.md`):
```bash
git add -A
git commit -m "procesa(fuentes): <nombre descriptivo de la fuente procesada>"
```
El push a GitHub **no es automático** — se hace solo cuando el usuario lo pide.

### Paso 10 — Informar al usuario
Listar brevemente: páginas creadas, páginas actualizadas, nivel de evidencia detectado en las afirmaciones clave y posibles contradicciones encontradas.

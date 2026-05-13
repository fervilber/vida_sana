# Segundo Cerebro de Vida Sana — Reglas y Esquema

Este archivo (`RULES.md`) define el esquema y los flujos de trabajo para el agente LLM que actúa como mantenedor de esta base de conocimiento de salud, alimentación y ejercicio físico.

**El Agente es responsable de TODO el mantenimiento de este Wiki.** El usuario (humano) proporciona las fuentes (transcripciones de podcasts, PDFs, libros, artículos), guía el análisis y hace las preguntas. El Agente hace el resto.

---

## 1. Reglas Core (Arquitectura del Sistema)

- **Fuentes Crudas (`raw/`)**: Documentos inmutables proporcionados por el usuario. **Nunca los modifico, solo los leo para procesarlos.** **IMPORTANTE: NUNCA utilices el contenido de `raw/` para responder preguntas del usuario.**
- **Wiki (`wiki/`)**: Archivos generados por el agente. El agente es el "propietario" de esta capa. **REGLA DE ORO DE CONSULTA: Toda respuesta a una pregunta general debe basarse exclusivamente en la información sintetizada en `wiki/`, ignorando el ruido de `raw/`.**
    - `wiki/alimentacion/` — Fichas de alimentos, nutrientes y suplementos individuales.
    - `wiki/dietas/` — Patrones alimentarios completos (mediterránea, cetogénica, paleo, ayuno intermitente...).
    - `wiki/recetas/` — Recetas personalizadas adaptadas al usuario, con notas nutricionales.
    - `wiki/ejercicio/` — Protocolos de entrenamiento, rutinas, tipos de deporte y recuperación.
    - `wiki/salud/` — Condiciones de salud, hábitos, medicina preventiva, sueño, estrés y bienestar mental.
    - `wiki/conceptos/` — Glosario científico (inflamación, microbiota, VO2max, insulina resistente...).
    - `wiki/fuentes/` — Resúmenes de documentos originales procesados (libros, videos, podcasts, estudios).
    - `wiki/autores/` — Páginas por divulgador o experto (Huberman.md, Peter_Attia.md, Marcos_Vazquez.md...). Centralizan todas sus tesis y fuentes.
    - `wiki/blog/` — Informes y respuestas a consultas complejas bajo demanda. Formato: `YYYYMMDD_slug.md`.
- **Índice (`index.md`)**: El "Dashboard" maestro. **Debe actualizarse siempre** que se añada un archivo nuevo a `wiki/`.
- **Páginas de Autor**: Centralizan el conocimiento de un divulgador o experto específico. **Deben actualizarse siempre** que se procese una nueva fuente de dicho autor.
- **Log (`log.md`)**: El registro histórico. **Debe actualizarse siempre** tras cualquier acción usando el prefijo `## [YYYY-MM-DD] ...`.
- **Integridad Cronológica (MÁXIMA PRIORIDAD)**: La fecha más importante de una fuente es su **fecha de creación original** (publicación del video, artículo o libro). Toda afirmación científica o recomendación debe ir asociada a su contexto temporal. **Prohibido** usar la fecha actual para datos extraídos de fuentes pasadas.

---

## 2. Nivel de Evidencia — Campo Crítico del Sistema

El campo `evidencia` es el campo más importante de toda nota en `wiki/`. Indica la solidez del respaldo científico de las afirmaciones. Criterios obligatorios:

| Valor | Criterio |
|---|---|
| **Alta** | Respaldado por meta-análisis o múltiples ensayos clínicos aleatorizados (RCT) bien diseñados |
| **Media** | Respaldado por estudios observacionales sólidos, o RCT con limitaciones (muestra pequeña, corta duración) |
| **Baja** | Basado en estudios preliminares, series de casos, modelos animales o consenso de expertos sin RCT |
| **Anecdotica** | Solo experiencias personales, testimonios o divulgadores sin citar estudios |
| **No analizada** | No se ha revisado la evidencia todavía; pendiente de contraste |

> ⚠️ El agente debe indicar siempre el nivel de evidencia al extraer una afirmación de salud. **Prohibido presentar información anecdótica como evidencia alta.**

---

## 3. Metadatos (Frontmatter) por Tipo de Nota

Todo archivo en `wiki/` debe contener un bloque YAML al inicio. El esquema varía según la sección.

### 3.1 Para `wiki/alimentacion/`

```yaml
---
aliases: []
tags: [alimentacion]
slug: "nombre_alimento"         # minúsculas, guiones bajos, sin acentos
categoria: "alimento | nutriente | suplemento"
grupo_alimentario: "proteina | carbohidrato | grasa | fibra | micronutriente | otro"
evidencia: "Alta | Media | Baja | Anecdotica | No analizada"
recomendacion: "Incluir | Moderar | Evitar | En estudio"
fecha_actualizacion: YYYY-MM-DD
---
```

### 3.2 Para `wiki/dietas/`

```yaml
---
aliases: []
tags: [dieta]
slug: "nombre_dieta"
tipo: "patron_alimentario | protocolo | estilo_vida"
evidencia: "Alta | Media | Baja | Anecdotica | No analizada"
objetivo: "perdida_peso | longevidad | rendimiento | salud_metabolica | inflamacion | otro"
fecha_actualizacion: YYYY-MM-DD
---
```

### 3.3 Para `wiki/recetas/`

```yaml
---
aliases: []
tags: [receta]
slug: "nombre_receta"
tipo_plato: "desayuno | almuerzo | cena | snack | postre | bebida"
tiempo_preparacion: "X min"
calorias_aprox: XXX
proteinas_g: XX
carbohidratos_g: XX
grasas_g: XX
apta_para: []    # ej: [keto, sin_gluten, alta_proteina, baja_en_fodmap]
fecha_actualizacion: YYYY-MM-DD
---
```

### 3.4 Para `wiki/ejercicio/`

```yaml
---
aliases: []
tags: [ejercicio]
slug: "nombre_protocolo"
tipo: "fuerza | cardio | movilidad | hiit | yoga | deporte | recuperacion"
nivel: "principiante | intermedio | avanzado | todos"
evidencia: "Alta | Media | Baja | Anecdotica | No analizada"
fecha_actualizacion: YYYY-MM-DD
---
```

### 3.5 Para `wiki/salud/`

```yaml
---
aliases: []
tags: [salud]
slug: "nombre_condicion_o_habito"
categoria: "habito | condicion | prevencion | mental | sueno | estres | longevidad | otro"
evidencia: "Alta | Media | Baja | Anecdotica | No analizada"
fecha_actualizacion: YYYY-MM-DD
---
```

### 3.6 Para `wiki/conceptos/`

```yaml
---
title: "Nombre del Concepto"
aliases: []
type: concepto
tags:
  - concepto/nutricion
  # Otros: concepto/fisiologia, concepto/bioquimica, concepto/psicologia, concepto/metodologia
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

---

## 3.7 Reglas de Enlazado y Etiquetado Mixto

Para maximizar la utilidad tanto para el Agente IA como para la navegación humana en Obsidian:

1. **Etiquetas YAML (`tags: [ejemplo]`)**: Uso estricto para categorización a nivel de archivo (`alimentacion`, `dieta`, `receta`, `ejercicio`, `salud`, `concepto`). Permite el uso de Dataview para crear Dashboards.
2. **Enlaces Bidireccionales (`[[Entidad]]`)**: Uso obligatorio para mencionar alimentos, dietas, autores, conceptos o condiciones definidas. Es la forma en que el Agente navega entre entidades.
3. **Etiquetas en línea (`#concepto`)**: Uso dentro de los párrafos para marcar temas cualitativos, riesgos o ventajas. Ejemplos: `#inflamacion`, `#microbiota`, `#deficit_calorico`, `#longevidad`, `#sueño`, `#resistencia_insulina`, `#antiinflamatorio`, `#suplementacion`.
4. **Formato de enlace obligatorio**: `[[slug_del_archivo|Nombre Visible Normal]]`. Ejemplo: `[[ayuno_intermitente|Ayuno Intermitente]]`, `[[andrew_huberman|Andrew Huberman]]`. **PROHIBIDO** usar solo el slug sin nombre visible.

---

## 3.8 Convención de Slugs (Nombres Canónicos)

El campo `slug` es el **identificador estable** de cada nota.

### Regla de Generación
```
slug = nombre_original
         → convertir a minúsculas
         → sustituir espacios por guion bajo (_)
         → eliminar tildes/acentos (á→a, é→e, ü→u, ñ→n)
         → eliminar caracteres especiales (puntos, comas, apóstrofes)
         → sustituir guiones medios (-) por guion bajo (_)
```

**Ejemplos:**

| Nombre Original | Slug resultante |
|---|---|
| Ayuno Intermitente | `ayuno_intermitente` |
| Dieta Mediterránea | `dieta_mediterranea` |
| Andrew Huberman | `andrew_huberman` |
| Omega-3 | `omega_3` |
| VO2 Max | `vo2_max` |
| Resistencia a la Insulina | `resistencia_insulina` |

### Regla de Nomenclatura de Archivos
- El nombre del archivo `.md` debe coincidir con el slug: `Ayuno_Intermitente.md`, no `Ayuno Intermitente.md`.
- **Prohibido**: espacios en nombres de archivo dentro de `wiki/`.

---

## 3.9 Informes y Blog (`wiki/blog/`)

- **Creación bajo demanda:** Solo cuando el usuario lo solicite expresamente.
- **Nomenclatura:** `YYYY-MM-DD_slug_descriptivo.md`
- **Metadatos YAML:**
  ```yaml
  ---
  slug: "YYYY-MM-DD_nombre_corto"
  titulo: "Título completo del informe"
  fecha: YYYY-MM-DD
  autor: "Antigravity (IA Mantenedora)"
  tipo: "informe"
  tags: [informe, etiqueta1, etiqueta2]
  ---
  ```

---

## 3.10 Convención de Archivos en `raw/`

La carpeta `raw/` es el almacén de **fuentes brutas inmutables**. Regla de nombre obligatoria:

```
YYYY-MM-DD_NOMBRE_SLUG.md
```

**Ejemplos:**
```
raw/2026-05-10_huberman_protocolo_sueno.md
raw/2025-11-20_attia_outlive_longevidad.md
raw/2026-03-14_podcast_marcos_vazquez_microbiota.md
```

### YAML Obligatorio en `raw/`

```yaml
---
title: "Título descriptivo de la fuente"
slug: "slug_del_archivo"
source: "https://url-de-origen.com"
source_date: "YYYY-MM-DD"    # fecha publicación ORIGINAL
import_date: "YYYY-MM-DD"    # fecha de importación al repositorio
tags: [raw, youtube]          # tipo: youtube | pdf | articulo | libro | podcast
---
```

> ⚠️ Si la fecha original es desconocida, usar `source_date: "desconocida"`. **Nunca omitir ambos campos.**

---

## 4. Operaciones del Agente

### A. Procesamiento (Process/Ingest)
Cuando el usuario proporciona un nuevo documento:
1. **Lectura Analítica**: Leer el documento crudo buscando específicamente: alimentos, dietas, protocolos de ejercicio, principios activos, estudios científicos citados, autores y nivel de evidencia implícito o explícito.
2. **Generar resumen de fuente**: Crear página descriptiva en `wiki/fuentes/`.
3. **Extracción a Entidades**:
    - Si se habla de un **Alimento/Nutriente** → actualizar o crear en `wiki/alimentacion/`
    - Si se describe una **Dieta o Patrón** → actualizar o crear en `wiki/dietas/`
    - Si se menciona una **Receta** → crear en `wiki/recetas/`
    - Si se describe un **Protocolo de Ejercicio** → actualizar o crear en `wiki/ejercicio/`
    - Si se trata de **Salud, Hábito o Condición** → actualizar o crear en `wiki/salud/`
    - Si se define un **Concepto Científico** → documentar en `wiki/conceptos/`
4. **Evaluar Evidencia**: Para cada afirmación extraída, asignar el nivel de evidencia según `§2`. Marcar explícitamente las afirmaciones anecdóticas.
5. **Enlazar (Cross-reference)**: Asegurar enlaces cruzados intensivos.
6. **Actualizar Página de Autor**: Añadir la nueva fuente al listado de "Fuentes en la Wiki" del autor correspondiente.
7. **Actualizar el Catálogo**: Añadir cualquier nuevo archivo al `index.md`.
8. **Registrar Acción**: Añadir entrada cronológica a `log.md`.

### B. Consulta (Query)
1. Consultar `index.md` y los archivos relevantes en `wiki/`.
2. Sintetizar la respuesta con citas directas a las fichas y nivel de evidencia explícito.
3. Si la consulta genera una comparación valiosa, proponer guardarla en `wiki/blog/`.

### C. Recetas Personalizadas
Cuando el usuario pida una receta:
1. Consultar `wiki/dietas/` para saber las preferencias y restricciones del usuario.
2. Consultar `wiki/alimentacion/` para identificar ingredientes recomendados.
3. Crear la receta en `wiki/recetas/` con el frontmatter nutricional completo.
4. Enlazar la receta con los alimentos y dietas relevantes.

### D. Mantenimiento (Lint)
Revisiones periódicas:
1. Buscar fichas con nivel de evidencia `No analizada` y proponer al usuario buscar fuentes.
2. Detectar contradicciones entre fuentes (ej. un estudio dice que el café es beneficioso y otro que es perjudicial → documentar ambas posturas).
3. Identificar páginas huérfanas sin enlaces entrantes.

### E. Procesamiento de Transcripciones Largas (Podcasts / Masterclasses)
Cuando se procesen transcripciones extensas:
1. **Contexto Temporal**: Dejar constancia expresa de la fecha del contenido.
2. **Clasificación de Afirmaciones**:
   - Recomendaciones con evidencia alta → extraer directamente a fichas de `wiki/`
   - Recomendaciones anecdóticas → documentar pero marcar explícitamente el nivel de evidencia
3. **Conocimiento General**: Extraer principios, modelos mentales o conceptos a `wiki/conceptos/`.

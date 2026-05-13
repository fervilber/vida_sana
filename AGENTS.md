# AGENTS.md — Segundo Cerebro de Vida Sana (LLM Wiki)

## Patron: LLM Wiki
Este es un sistema de **gestión activa de conocimiento** sobre salud, alimentación y ejercicio físico. NO es un proyecto de software. El LLM actúa como **mantenedor** del wiki, no como programador.

## Flujo Fundamental

| Acción | Fuente de respuesta |
|--------|-------------------|
| Pregunta sobre salud/alimentación/ejercicio | **`wiki/`** exclusivamente |
| Consultar fuentes originales | `raw/` solo si el usuario lo pide explícitamente |
| Nuevos archivos | Depositar en `raw/`, luego procesar a `wiki/` |

**REGLA DE ORO**: Nunca respondas desde `raw/` para preguntas generales. Siempre consulta `wiki/`.

## Inicializacion Obligatoria (orden)

1. `RULES.md` — esquema, reglas y frontmatter
2. `.agentic/workflows/inicializacion.md` — protocolo de arranque
3. `index.md` — catálogo maestro
4. `log.md` — registro de acciones previas

## Estructura

- `raw/` — fuentes inmutables (transcripciones, PDFs, artículos). **Solo leer, nunca modificar**
- `wiki/alimentacion/` — fichas de alimentos, nutrientes y suplementos individuales
- `wiki/dietas/` — patrones alimentarios completos (mediterránea, cetogénica, ayuno intermitente...)
- `wiki/recetas/` — recetas adaptadas al usuario con notas nutricionales
- `wiki/ejercicio/` — protocolos de entrenamiento, rutinas, tipos de deporte y recuperación
- `wiki/salud/` — condiciones, hábitos de salud, medicina preventiva, sueño, estrés, bienestar mental
- `wiki/conceptos/` — glosario científico (inflamación, microbiota, VO2max, insulina...)
- `wiki/fuentes/` — resúmenes de fuentes procesadas (libros, videos, podcasts, estudios)
- `wiki/autores/` — páginas por divulgador (Huberman.md, Peter_Attia.md, Marcos_Vazquez.md, etc.)
- `wiki/blog/` — informes, análisis y respuestas a consultas complejas bajo demanda
- `index.md` — actualizar tras cada ingesta
- `log.md` — registro cronológico (prefijo: `## [YYYY-MM-DD]`)

## Frontmatter para Temas de Alimentación

```yaml
---
aliases: []
tags: [alimentacion]
slug: "nombre_alimento_o_nutriente"   # minúsculas, guiones bajos, sin acentos
categoria: "alimento | nutriente | suplemento"
grupo_alimentario: "proteina | carbohidrato | grasa | fibra | micronutriente | otro"
evidencia: "Alta | Media | Baja | Anecdotica | No analizada"
recomendacion: "Incluir | Moderar | Evitar | En estudio"
fecha_actualizacion: YYYY-MM-DD
---
```

## Frontmatter para Dietas y Patrones Alimentarios

```yaml
---
aliases: []
tags: [dieta]
slug: "nombre_dieta"
tipo: "patron_alimentario | protocolo | estilo_vida"
evidencia: "Alta | Media | Baja | Anecdotica | No analizada"
objetivo: "perdida_peso | longevidad | rendimiento | salud_metabolica | otro"
fecha_actualizacion: YYYY-MM-DD
---
```

## Frontmatter para Recetas

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
apta_para: []    # ej: [keto, sin_gluten, alta_proteina]
fecha_actualizacion: YYYY-MM-DD
---
```

## Frontmatter para Ejercicio

```yaml
---
aliases: []
tags: [ejercicio]
slug: "nombre_protocolo_o_tipo"
tipo: "fuerza | cardio | movilidad | hiit | yoga | deporte | recuperacion"
nivel: "principiante | intermedio | avanzado | todos"
evidencia: "Alta | Media | Baja | Anecdotica | No analizada"
fecha_actualizacion: YYYY-MM-DD
---
```

## Fecha es Critica

Toda información proviene de una fecha original de publicación, **no la fecha actual**. Si extraes datos de estudios o fuentes, indica el año y contexto correspondiente.

## Nivel de Evidencia

El campo `evidencia` es el campo más importante del sistema (equivale al "moat" en un análisis de empresas). Criterios:
- **Alta**: Respaldado por meta-análisis o múltiples ensayos clínicos aleatorizados (RCT)
- **Media**: Respaldado por estudios observacionales o ensayos con limitaciones
- **Baja**: Basado en estudios preliminares, series de casos o consenso de expertos
- **Anecdotica**: Solo experiencias personales o testimonios sin respaldo científico
- **No analizada**: No se ha revisado la evidencia aún

## Enlazado

- Usar `[[wikilinks]]` para conectar alimentos, conceptos, autores y dietas
- Asegurar bidireccionalidad (si A enlaza a B, B debe tener enlace a A)
- Usar `#etiquetas_en_linea` para temas cualitativos (#inflamacion, #microbiota, #deficit_calorico, #longevidad)

## Scripts Disponibles

```bash
# Validar wiki (lint)
python scripts/lint.py                    # Wiki completa
python scripts/lint.py wiki/alimentacion  # Directorio específico

# Ingesta de fuentes
python scripts/youtube_to_raw.py "URL" "nombre"          # Transcripción de YouTube → raw/
python scripts/epub_to_raw.py "ruta.epub" "nombre"       # Libro EPUB → raw/
python scripts/pdf_to_raw.py "ruta.pdf"                  # PDF → raw/

# Búsqueda en la wiki
python scripts/search.py "término"
```

> **epub_to_raw.py**: Convierte libros `.epub` a Markdown en `raw/`. Extrae metadatos automáticos
> (título, autor, año, editorial), convierte cada capítulo a Markdown limpio y genera el mismo
> frontmatter YAML que los demás scripts. Requiere: `pip install ebooklib html2text beautifulsoup4`

## Git Workflow

1. Commits locales frecuentes: `git add -A && git commit -m "procesa(fuentes): ..."`
2. **Push NO automático** — solo cuando el usuario lo pida
3. Remoto esperado: `github.com/fervilber/vida_sana`

## Referencias de Implementacion

- `.agentic/skills/ingesta.md` — lógica de procesamiento
- `.agentic/skills/consulta.md` — lógica de respuesta
- `.agentic/skills/mantenimiento.md` — detección de huérfanos y contradicciones
- `.agentic/skills/evidencia.md` — evaluación del nivel de evidencia científica
- `.agentic/skills/examenes.md` — generación de test de autoevaluación
- `.agentic/workflows/ingesta.md` — flujo completo paso a paso
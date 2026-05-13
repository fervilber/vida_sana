# Arquitectura del Sistema

Una visión técnica de cómo están conectadas las piezas del sistema.
Para el uso diario, consulta la [[user-guide|Guía de Usuario]].

---

## Flujo de Trabajo Principal

```
╔══════════════════════════════════════════════════════════════╗
║                  TÚ (El Estratega)                          ║
║  Buscas fuentes · Formulas preguntas · Defines objetivos    ║
╚════════════════════╦═════════════════════════════╦═══════════╝
                     │                             │
            [Agente LLM]                    [Obsidian]
         (Mantenedor activo)              (Visualizador)
         Claude / Antigravity /           Vault abierto sobre
         OpenCode                         la raíz del proyecto
                     │                             │
                     ▼                             ▼
         Lee · Extrae · Sintetiza         Graph View · Dataview
         Conecta · Archiva                Marp · Backlinks
```

**El flujo típico:** Obsidian abierto en un monitor, el agente en el otro.
El agente escribe; tú ves los cambios en tiempo real en Obsidian.

---

## Diagrama de Capas

```
┌─────────────────────────────────────────────────────┐
│              USUARIO (estratega)                    │
│   Aporta fuentes · Formula preguntas · Revisa       │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│              AGENTE LLM (mantenedor)                │
│   Claude · Antigravity · OpenCode                   │
│                                                     │
│  Gobernado por:                                     │
│  ├── RULES.md  (constitución)                       │
│  ├── .agentic/skills/  (reglas lógicas)             │
│  └── .agentic/workflows/  (algoritmos)              │
└───────┬───────────────────────────┬─────────────────┘
        │                           │
┌───────▼────────────┐   ┌──────────▼─────────────────┐
│  /raw/ (ENTRADA)   │   │  /wiki/ (SALIDA)            │
│  Inmutable         │   │  Grafo de conocimiento      │
│  ├── Artículos web │   │  ├── fuentes/               │
│  ├── YouTube .md   │   │  ├── empresas/              │
│  ├── PDFs .md      │   │  ├── sectores/              │
│  └── assets/       │   │  └── tesis_inversion/       │
└────────────────────┘   └─────────────────────────────┘
                                     │
                         ┌───────────▼───────────────────┐
                         │       OBSIDIAN                │
                         │   (Visualización del grafo)   │
                         │   Graph View · Dataview       │
                         │   Marp Slides · Backlinks     │
                         └───────────────────────────────┘
```

---

## Componentes del Sistema

### RULES.md — La Constitución
Punto de entrada obligatorio para todo agente. Define:
- Jerarquía de directorios y su propósito
- Protocolo de descubrimiento (orden de lectura)
- Reglas operativas (filtro MVC, inmutabilidad, bidireccionalidad)
- Estándar de metadatos YAML para todas las notas

### `.agentic/` — El Cerebro
Instrucciones de máquina con máxima prioridad sobre `/doc/`.

| Carpeta | Contenido | Analogía |
|---------|-----------|---------|
| `skills/` | **Qué hacer**: reglas lógicas y criterios | Las leyes del juego |
| `workflows/` | **Cómo hacerlo**: algoritmos paso a paso | El plan de partido |
| `templates/` | **Cómo formatearlo**: esquemas YAML+MD | El estilo de juego |

### `/raw/` — La Entrada (Inmutable)
Material bruto de referencia. **El agente lee, nunca escribe aquí.**

Fuentes soportadas:
- Artículos web (via Obsidian Web Clipper)
- Transcripciones YouTube (via `scripts/youtube_to_raw.py`)
- PDFs convertidos a Markdown (via `scripts/pdf_to_raw.py`)
- Cualquier archivo de texto / Markdown manual

### `/wiki/` — La Salida (El Grafo)
El conocimiento destilado. Todo lo que el usuario consulta viene de aquí.

| Archivo/Carpeta | Propósito |
|----------------|-----------|
| `index.md` | Catálogo maestro (Raíz); el agente lo actualiza tras cada ingesta |
| `fuentes/` | Resúmenes de cada material original procesado |
| `empresas/` | Fichas de compañías (moat, ticker, tesis) |
| `sectores/` | Análisis industrial y macro |
| `tesis_inversion/` | Tesis de inversión estructuradas |
| `log.md` | Registro cronológico (Raíz) |

### `/scripts/` — Las Herramientas

| Script | Función |
|--------|---------|
| `youtube_to_raw.py` | Descarga transcripciones de YouTube con frontmatter estándar |
| `pdf_to_raw.py` | Extrae texto de PDFs y genera Markdown en `/raw/` |
| `lint.py` | Valida YAML, wikilinks rotos y páginas huérfanas |
| `search.py` | Búsqueda local por texto en las páginas de la wiki |

---

## Por Qué No es RAG Tradicional

| Modelo RAG | Este Sistema |
|-----------|-------------|
| Índice de fragmentos de documentos | Wiki estructurada con notas atómicas |
| El LLM redescubre conexiones en cada consulta | Las conexiones ya existen en la wiki |
| No hay síntesis persistente | La síntesis se acumula con cada ingesta |
| Escala mal con la profundidad | Mejora con el tiempo (efecto compuesto) |
| Requiere infraestructura de embeddings | Solo archivos Markdown + Git |

---

## Filosofía de Diseño

Basada en el concepto de **wiki acumulativa** descrito en `idea.md`:
el conocimiento se compila una vez y se mantiene actualizado, en lugar de
derivarse desde cero en cada consulta.

Referencia histórica: **Memex de Vannevar Bush (1945)** — un repositorio de
conocimiento personal con rutas asociativas entre documentos, donde las
conexiones son tan valiosas como los documentos mismos.

La diferencia con el Memex: aquí el LLM se encarga del mantenimiento que
antes hacía que los humanos abandonasen sus wikis.

---

*Ver también: [[user-guide]] · [[web-clipper-setup]] · [[faq]]*

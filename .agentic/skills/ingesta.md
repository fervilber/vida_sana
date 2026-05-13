# Skill: Ingesta de Alta Densidad

## Propósito
Define la lógica que el agente debe aplicar al procesar un nuevo archivo en `/raw/`.

---

## §0 — Convención de Nombres en `raw/`

> **REGLA DE ORO**: Todo archivo en `raw/` DEBE seguir el patrón `YYYY-MM-DD_NOMBRE_SLUG.md`.

### Formato de Nombre
```
YYYY-MM-DD_NOMBRE_SLUG.md
```

- **`YYYY-MM-DD`**: Fecha de **publicación original** de la fuente (vídeo, artículo, PDF…).
  - Si no se conoce la fecha de publicación → usar la **fecha de importación** al repositorio.
- **`NOMBRE_SLUG`**: Nombre descriptivo en formato slug (minúsculas, guiones bajos, sin tildes ni caracteres especiales). Ver convención en `RULES.md §3.8`.

### Ejemplos válidos
```
raw/2026-04-19_huberman_protocolo_sueno.md
raw/2025-11-20_attia_outlive_longevidad.md
raw/2026-03-14_marcos_vazquez_microbiota_intestinal.md
raw/2025-08-10_libro_dieta_mediterranea_ancel_keys.md
```

### Ejemplos inválidos (prohibidos)
```
raw/PODCAST HUBERMAN [SUEÑO].md     ← espacios, tildes, corchetes
raw/Huberman_sueno.md               ← sin fecha
raw/2026-04-19.md                   ← sin nombre descriptivo
```

---

## §1 — YAML Obligatorio en `raw/`

Todo archivo en `raw/` debe incluir este bloque YAML completo al inicio:

```yaml
---
title: "Título legible de la fuente"
slug: "slug_en_minusculas_guiones_bajos"
source: "https://url-de-origen.com"
source_date: "YYYY-MM-DD"   # Fecha publicación ORIGINAL (no la de hoy)
import_date: "YYYY-MM-DD"   # Fecha de importación al repositorio
tags: [raw, youtube]         # youtube | pdf | articulo | libro | podcast | estudio
---
```

**Campos obligatorios**:

| Campo | Descripción | Ejemplo |
|---|---|---|
| `title` | Título descriptivo legible | `"Huberman Lab: Protocolos de Sueño"` |
| `slug` | Slug sin tildes ni espacios | `"huberman_protocolo_sueno"` |
| `source` | URL o referencia de origen | `"https://youtu.be/abc123"` |
| `source_date` | Fecha publicación **original** | `"2026-03-15"` |
| `import_date` | Fecha de importación | `"2026-04-19"` |
| `tags` | Al menos: `raw` + tipo | `[raw, youtube]` |

> ⚠️ `source_date` e `import_date` pueden coincidir si se importa el día de publicación,
> pero **nunca deben omitirse**.

---

## §2 — Criterio MVC (Mínimo Valor de Conocimiento)
- Una información merece nota propia en `/wiki/` si aporta **≥ 3 ideas o datos sustanciales**.
- Si no alcanza el umbral, integrar en la página de la fuente padre en `wiki/fuentes/`.

---

## §3 — Proceso de Ingesta (paso a paso)

1. **Naming**: Verificar que el archivo raw sigue la convención `YYYY-MM-DD_SLUG.md` (§0).
   Si no cumple → renombrar antes de continuar.

2. **Lectura**: Leer el archivo fuente en `/raw/` identificando la **fecha de publicación original**.

3. **Extracción**: Identificar:
   - Alimentos/Nutrientes/Suplementos mencionados → candidatos a `wiki/alimentacion/`
   - Dietas o Patrones Alimentarios → `wiki/dietas/`
   - Recetas → `wiki/recetas/`
   - Protocolos de Ejercicio → `wiki/ejercicio/`
   - Condiciones de Salud o Hábitos → `wiki/salud/`
   - Conceptos Científicos (microbiota, VO2max, insulina...) → `wiki/conceptos/`
   - Autor/Divulgador → `wiki/autores/`

4. **Evaluar Evidencia**: Para cada afirmación extraída, aplicar la skill `evidencia.md` y asignar el campo `evidencia`. Marcar explícitamente las afirmaciones anecdóticas.

5. **Verificación de duplicados**: Consultar `index.md` para detectar páginas existentes.

6. **Contraste**: Comparar nueva información con páginas existentes:
   - Si confirma → reforzar la síntesis existente.
   - Si contradice → añadir bloque `> [!CAUTION] Contradicción` con ambas versiones.

7. **Generación de Slug** (ANTES de crear archivos en wiki/):
   - Derivar el `slug` según `RULES.md §3.8`.
   - El nombre del archivo `.md` debe usar el slug con guiones bajos.
   - Incluir el campo `slug` en el frontmatter YAML.

8. **Creación / Actualización**: Escribir o actualizar archivos en `/wiki/` usando los templates de `.agentic/templates/`:
   - Alimento/Dieta/Salud → `nota-tema.md`
   - Concepto → `nota-concepto.md`
   - Receta → `nota-receta.md`
   - Protocolo de Ejercicio → `nota-protocolo.md`
   - Fuente → `nota-fuente.md`

9. **Enlazado**: Insertar `[[wikilinks]]` bidireccionales entre notas relacionadas.
   **FORMATO OBLIGATORIO: `[[slug_del_archivo|Nombre Visible Normal]]`**
   Ejemplos: `[[ayuno_intermitente|Ayuno Intermitente]]`, `[[andrew_huberman|Andrew Huberman]]`.

10. **Actualizar Página de Autor**: Añadir la nueva fuente al listado de "Fuentes en la Wiki" del divulgador correspondiente en `wiki/autores/`.

11. **Registro**: Añadir entrada en `log.md` con el formato estándar.

12. **Índice**: Actualizar `index.md` con las nuevas páginas creadas y los contadores de la tabla de estado.

---

## §4 — Reglas de Metadatos Obligatorias

- Cada nota en `wiki/` debe incluir el bloque YAML del estándar definido en `RULES.md §3`.
- **CRÍTICO**: `fecha_actualizacion` y `source_date` deben reflejar el momento del análisis **original**, no el día de hoy.
- **EVIDENCIA OBLIGATORIA**: Todo archivo nuevo en `wiki/` debe incluir el campo `evidencia` con un valor válido. No dejar en blanco.
- **SLUG OBLIGATORIO**: Todo archivo nuevo en `wiki/` debe incluir `slug` en frontmatter. No crear archivos con espacios en el nombre.

---

## §5 — Scripts Disponibles

```bash
# Importar transcripción de YouTube (naming automático con fecha)
python scripts/youtube_to_raw.py "URL" "Nombre_Descriptivo"
# → genera: raw/YYYY-MM-DD_nombre_descriptivo.md

# Importar PDF
python scripts/pdf_to_raw.py "ruta/al/archivo.pdf"

# Validar nomenclatura y metadatos
python scripts/lint.py raw/
python scripts/lint.py wiki/

# Búsqueda en la wiki
python scripts/search.py "término de búsqueda"
```

## §6 — Manejo de Imágenes y Recursos
Todo archivo visual en `/raw/assets/` debe tener su descripción textual en la wiki
para garantizar indexabilidad semántica.

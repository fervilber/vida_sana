# Configuración del Obsidian Web Clipper

Captura tesis, análisis y noticias financieras directamente en la carpeta `/raw/`.

---

## Configuración Recomendada

### 1. Vault y Carpeta
- **Vault**: Selecciona la carpeta raíz de este proyecto.
- **Carpeta de notas**: `raw`

### 2. Plantilla (Template)
Usa este bloque para asegurar que el agente tenga los metadatos necesarios:

```markdown
---
title: "{{title}}"
aliases: []
type: fuente
tags:
  - fuente/web
source_url: "{{url}}"
source_date: {{date:YYYY-MM-DD}}
created: {{date:YYYY-MM-DD}}
updated: {{date:YYYY-MM-DD}}
---

# {{title}}

> **Fuente**: [{{url}}]({{url}})
> **Capturado**: {{date:YYYY-MM-DD}}

---

{{content}}
```

### 3. Imágenes
En `Ajustes → Archivos y enlaces` de Obsidian, pon la **Carpeta de adjuntos** en `raw/assets`.

---

## Flujo de Trabajo
1. Encuentras una tesis interesante en la web.
2. Usas el Clipper → El archivo se guarda en `/raw/`.
3. Le dices al agente: *«Procesa `raw/nombre.md` extrayendo la tesis y el ticker»*.
4. El agente actualiza la wiki, el `index.md` y el `log.md`.

---

*Ver también: [[user-guide]] · [[faq]] · [[architecture]]*

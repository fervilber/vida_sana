# Guía de Usuario — LLM Wiki

Esta guía explica cómo usar la LLM Wiki en el día a día. Para entender el diseño
del sistema, consulta la [[architecture|Arquitectura]]. Para capturas web, consulta
la [[web-clipper-setup|Configuración del Web Clipper]].

---

## 🛠 Herramientas Necesarias

Esta wiki está diseñada para funcionar con **dos herramientas en paralelo**:

### Obsidian — El Visualizador
**[Obsidian](https://obsidian.md)** es la aplicación de escritorio donde **lees y
navegas** la wiki. No escribes las notas tú: el agente lo hace. Tú las lees en Obsidian.

**Instalación:**
1. Descarga desde [obsidian.md](https://obsidian.md) (gratuito, Windows/Mac/Linux/iOS/Android).
2. Abre Obsidian → `Abrir carpeta como Vault` → selecciona la raíz de este proyecto.
3. Instala los plugins recomendados desde `Ajustes → Plugins de la Comunidad`:

| Plugin | Para qué sirve |
|--------|----------------|
| **Dataview** | Tablas dinámicas que consultan el frontmatter YAML de tus notas |
| **Marp Slides** | Genera presentaciones directamente desde Markdown |
| **Obsidian Web Clipper** | Captura artículos web en un clic → directamente a `/raw/` |
| **Excalidraw** | Visualiza diagramas y esquemas en `wiki/diagramas/` |

4. En `Ajustes → Archivos y enlaces`:
   - **Carpeta de adjuntos**: `raw/assets`
   - Asigna atajo `Ctrl+Shift+D` a "Descargar adjuntos del archivo actual".

### Agente LLM — El Mantenedor
El agente es quien **procesa, escribe y organiza** la wiki. Trabaja en paralelo
a Obsidian: tú ves los cambios en tiempo real mientras el agente los ejecuta.

**Cómo iniciar una sesión con el agente:**

Envía al agente este prompt de inicialización al comenzar:

> *"Actúa como mantenedor de mi LLM Wiki de Inversiones. Estamos en la raíz del proyecto.
> Lee en este orden:
> 1. `RULES.md` — para entender las reglas del sistema
> 2. `.agentic/workflows/inicializacion.md` — para el protocolo de arranque
> 3. `index.md` — para conocer el estado actual del conocimiento
> 4. `log.md` — para saber qué se hizo por última vez
>
> Confírmame cuando hayas leído y dime el estado actual."*

---

## 📥 Añadir Fuentes Nuevas

### Opción A — Artículo Web
Usa el **Obsidian Web Clipper** (ver [[web-clipper-setup]]):
1. Clip del artículo → se guarda en `/raw/` automáticamente.
2. Dile al agente: *«Procesa el archivo `raw/<nombre>.md` y actualiza la wiki»*

### Opción B — Video de YouTube
Puedes pedírselo directamente al agente sin usar scripts:
> *«Procesa este video de Gorka sobre Estee Lauder y guarda la transcripción en raw: `https://youtu.be/...`»*

O bien usando el script desde la terminal:
```bash
python scripts/youtube_to_raw.py "https://youtu.be/ID_DEL_VIDEO"
```

### Opción C — Archivo PDF
```bash
python scripts/pdf_to_raw.py "ruta/al/informe_anual.pdf"
```

---

## 💬 Cómo Hablarle al Agente — Guía de Instrucciones

### 📥 Procesar fuentes nuevas

| Situación | Frase de ejemplo |
|-----------|------------------|
| Artículo ya guardado en `/raw/` | *«Procesa el archivo `raw/informe-enagas.md` y actualiza la wiki»* |
| Video de YouTube (directo) | *«Procesa este video de Alex Dito: `https://youtu.be/...`»* |
| PDF ya importado a `/raw/` | *«Analiza `raw/resultados-apple.md` extrayendo el ROIC y la tesis»* |

### 🔍 Consultar el conocimiento acumulado

| Situación | Frase de ejemplo |
|-----------|------------------|
| Pregunta directa | *«¿Qué sabemos sobre Estee Lauder según la wiki?»* |
| Listar notas de un tema | *«Muéstrame todas las empresas del sector lujo»* |
| Comparación | *«Compara las tesis de Gorka y Alex Dito sobre Enagas»* |

### 🔧 Mantenimiento y calidad

| Situación | Frase de ejemplo |
|-----------|------------------|
| Revisión general | *«Realiza un mantenimiento de la wiki»* |
| Estado del grafo | *«¿Hay empresas huérfanas o sin conectar en la wiki?»* |

---

## 🔍 Navegar en Obsidian

| Vista | Para qué sirve |
|-------|----------------|
| **Graph View** (`Ctrl+G`) | Ver conexiones entre empresas y conceptos |
| `index.md` | Catálogo maestro en la raíz |
| `wiki/empresas/` | Fichas individuales de compañías |

---

## 📌 Reglas para no Romper Nada

| ✅ Puedes | ❌ No debes |
|-----------|------------|
| Añadir archivos a `/raw/` | Modificar o borrar archivos de `/raw/` |
| Leer y navegar `/wiki/` en Obsidian | Editar notas de `/wiki/` sin avisar al agente |
| Editar `.agentic/` con intención | Cambiar `RULES.md` sin revisar el impacto |

---

*Ver también: [[architecture]] · [[web-clipper-setup]] · [[faq]]*

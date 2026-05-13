# Skill: Excalidraw — Diagramas y Esquemas desde el Agente

## ¿Para qué sirve esta habilidad?

Permite al agente crear y gestionar **diagramas visuales** (flujos, arquitecturas, mapas de
conceptos, timelines) directamente desde el chat, generando archivos `.excalidraw` que se
visualizan en Obsidian con el plugin **Excalidraw**.

Los diagramas se guardan en `wiki/diagramas/` y pueden enlazarse desde cualquier nota de la wiki.

---

## Requisitos de Instalación

### 1. Obsidian — Plugin Excalidraw
1. En Obsidian → `Ajustes → Plugins de la Comunidad → Explorar`
2. Busca **"Excalidraw"** (autor: Zsolt Viczián)
3. Instala y activa el plugin
4. En `Ajustes → Excalidraw`:
   - **Carpeta de nuevos diagramas**: `wiki/diagramas`
   - **Autoguardado**: activado

### 2. Servidor MCP Excalidraw (para uso desde el agente)

> Esto es OPCIONAL pero habilita la creación programática de diagramas complejos.
> Sin él, el agente genera el JSON del diagrama y tú lo pegas en Obsidian.

```bash
# Clonar e instalar el servidor MCP
git clone https://github.com/yctimlin/mcp_excalidraw
cd mcp_excalidraw
npm ci && npm run build

# Arrancar el servidor de canvas (en una terminal separada)
PORT=3000 npm run canvas

# Abrir http://localhost:3000 en el navegador → el canvas está listo

# Registrar el MCP con Claude (opcional, solo si usas Claude Desktop)
claude mcp add excalidraw -s user \
  -e EXPRESS_SERVER_URL=http://localhost:3000 \
  -- node /ruta/a/mcp_excalidraw/dist/index.js
```

---

## Modos de Trabajo

### Modo A — Solo JSON (sin servidor, siempre disponible)
El agente genera el JSON del diagrama en formato `.excalidraw`.
Tú lo pegas en un archivo nuevo en `wiki/diagramas/nombre.excalidraw` y lo
abres con Obsidian → se renderiza automáticamente.

### Modo B — MCP en directo (requiere servidor activo)
Con el servidor en `http://localhost:3000`, el agente crea y modifica el
diagrama en tiempo real. Tú lo ves actualizarse en el navegador y en Obsidian
simultáneamente.

---

## Cómo Pedirle un Diagrama al Agente

El agente entiende lenguaje natural. Ejemplos de instrucciones:

| Qué quieres | Frase de ejemplo |
|-------------|------------------|
| Flujo de proceso | *«Crea un diagrama de flujo del proceso de procesamiento de fuentes en la wiki y guárdalo en wiki/diagramas/»* |
| Arquitectura | *«Dibuja un diagrama de la arquitectura del sistema LLM Wiki con todos sus componentes»* |
| Mapa de conceptos | *«Genera un mapa visual de los conceptos sobre [tema] que tenemos en la wiki»* |
| Desde Mermaid | *«Convierte este diagrama Mermaid a Excalidraw y guárdalo: [código mermaid]»* |
| Editar existente | *«Actualiza el diagrama `wiki/diagramas/arquitectura.excalidraw` añadiendo el nodo "PDF Importer"»* |

---

## Protocolo del Agente para Crear Diagramas

Cuando el usuario pide un diagrama, el agente debe:

### Paso 1 — Determinar el modo

**¿El servidor MCP está disponible?**
- Sí → usar herramientas MCP (`batch_create_elements`, etc.)
- No → generar JSON directamente e instruir al usuario para guardarlo

### Paso 2 — Planificar el layout ANTES de generar elementos

El agente planifica la cuadrícula de coordenadas:
- Espaciado vertical entre niveles: **80–120 px**
- Espaciado horizontal entre elementos: **40–60 px mínimo**
- Ancho de cada caja: `max(160px, nº_caracteres × 9px)`
- Alto de caja: **60 px** (una línea), **80 px** (dos líneas)
- Padding interior de zonas de fondo: **50 px** en todos los lados

### Paso 3 — Crear elementos

**Reglas críticas:**
- ❌ No poner texto en rectángulos de zona / fondo → usa elemento `text` separado
- ❌ No cruzar flechas a través de otros elementos → enrutar por el perímetro
- ❌ No saturar de etiquetas en flechas → solo cuando sean imprescindibles (≤12 caracteres)
- ✅ Crear primero formas, luego flechas, luego alineación/agrupación

### Paso 4 — Verificación visual (solo modo MCP)

Tras cada `batch_create_elements`:
1. `get_canvas_screenshot` → revisar con checklist:
   - ¿Texto completamente visible? (si no → aumentar `width`/`height`)
   - ¿Elementos solapados? (si sí → reposicionar)
   - ¿Flechas cruzando formas ajenas? (si sí → enrutar por curva/codo)
   - ¿Espaciado mínimo 40 px? 
   - ¿Tamaño de fuente ≥ 16 px para texto y ≥ 20 px para títulos?
2. Corregir problemas antes de continuar

### Paso 5 — Guardar en la wiki

```
wiki/diagramas/<nombre-descriptivo>.excalidraw
```

Luego actualizar la nota de wiki relacionada añadiendo el enlace:
```markdown
![[wiki/diagramas/nombre-descriptivo.excalidraw]]
```

---

## Referencia Rápida: Elementos JSON

### Rectángulo con texto (MCP)
```json
{"id": "mi-caja", "type": "rectangle", "x": 100, "y": 100, "width": 200, "height": 60, "text": "Mi Servicio"}
```

### Texto libre (para etiquetas de zona)
```json
{"id": "zona-label", "type": "text", "x": 60, "y": 60, "width": 200, "height": 30, "text": "Zona Frontend", "fontSize": 18}
```

### Flecha entre elementos (MCP)
```json
{"type": "arrow", "x": 0, "y": 0, "startElementId": "caja-a", "endElementId": "caja-b"}
```

### Flecha curva (evitar solapamiento)
```json
{"type": "arrow", "x": 100, "y": 100, "points": [[0,0],[50,-40],[200,0]], "roundness": {"type": 2}}
```

### Flecha en codo (L-shape)
```json
{"type": "arrow", "x": 100, "y": 100, "points": [[0,0],[0,-50],[200,-50],[200,0]], "elbowed": true}
```

### Zona de fondo (sin texto)
```json
{"id": "zona-bg", "type": "rectangle", "x": 50, "y": 50, "width": 600, "height": 300, "backgroundColor": "#e3f2fd", "strokeStyle": "dashed"}
```

---

## Plantilla Básica de Archivo `.excalidraw`

Para crear un diagrama manualmente (modo sin servidor), crea un archivo
`wiki/diagramas/nombre.excalidraw` con este contenido y sustituye `elements`:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  }
}
```

---

## Tipos de Diagramas Recomendados para la Wiki

| Tipo | Cuándo usarlo | Notas |
|------|---------------|-------|
| **Flujo de proceso** | Documentar workflows del sistema | Usar `rectangle` + `arrow` enlazados |
| **Mapa de conceptos** | Visualizar relaciones entre entidades | `ellipse` para conceptos + flechas con etiqueta |
| **Arquitectura de sistema** | Mostrar componentes e integraciones | Zonas de fondo + cajas de servicio |
| **Timeline** | Evolución histórica de un tema | Línea horizontal + cajas alineadas |
| **Comparativa** | Pros/contras, diferencias | Dos columnas + texto libre |

---

## Notas sobre Guardado en Obsidian

- Los archivos `.excalidraw` son JSON estándar: se pueden versionar con Git sin problemas.
- Para incrustar un diagrama en una nota: `![[nombre.excalidraw]]`
- Para verlo en modo edición: clic derecho → "Open as Excalidraw drawing"
- El plugin sincroniza cambios en tiempo real si el servidor MCP está activo.

---

## Referencias

- Skill completa con API y herramientas MCP: `.agentic/skills/references/excalidraw-cheatsheet.md`
- Repositorio del servidor MCP: https://github.com/yctimlin/mcp_excalidraw
- Plugin de Obsidian: https://github.com/zsviczian/obsidian-excalidraw-plugin

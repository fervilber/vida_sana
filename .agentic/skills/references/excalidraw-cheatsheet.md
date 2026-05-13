# Excalidraw Cheatsheet — Referencia Técnica Completa

> Referencia interna del agente. Para instrucciones de uso del proyecto, ver
> `.agentic/skills/excalidraw.md`.

---

## Herramientas MCP (26 herramientas)

### CRUD de Elementos

| Herramienta | Descripción | Parámetros requeridos |
|-------------|-------------|-----------------------|
| `create_element` | Crea formas, texto, flechas o líneas | `type`, `x`, `y` |
| `get_element` | Obtiene un elemento por ID | `id` |
| `update_element` | Actualiza propiedades de un elemento | `id` |
| `delete_element` | Elimina un elemento | `id` |
| `query_elements` | Consulta por tipo/filtros | (opcional) `type`, `filter` |
| `batch_create_elements` | Crea múltiples elementos de una vez | `elements[]` |
| `duplicate_elements` | Clona con desplazamiento | `elementIds[]`, (opcional) `offsetX`, `offsetY` |

### Layout y Organización

| Herramienta | Descripción | Parámetros requeridos |
|-------------|-------------|-----------------------|
| `align_elements` | Alinea left/center/right/top/middle/bottom | `elementIds[]`, `alignment` |
| `distribute_elements` | Espaciado uniforme horizontal/vertical | `elementIds[]`, `direction` |
| `group_elements` | Agrupa elementos | `elementIds[]` |
| `ungroup_elements` | Desagrupa | `groupId` |
| `lock_elements` | Bloquea elementos | `elementIds[]` |
| `unlock_elements` | Desbloquea elementos | `elementIds[]` |

### Conciencia de Escena (Refinamiento Iterativo)

| Herramienta | Descripción | Parámetros requeridos |
|-------------|-------------|-----------------------|
| `describe_scene` | Descripción en texto de todos los elementos | (ninguno) |
| `get_canvas_screenshot` | PNG del canvas para verificación visual | (opcional) `background` |
| `get_resource` | Obtiene escena/biblioteca/tema | `resource` |

### Exportación e Importación

| Herramienta | Descripción | Parámetros requeridos |
|-------------|-------------|-----------------------|
| `export_scene` | Exportar a JSON .excalidraw | (opcional) `filePath` |
| `import_scene` | Importar desde .excalidraw | `mode` ("replace"\|"merge"), `filePath` o `data` |
| `export_to_image` | Exportar a PNG/SVG (requiere navegador) | `format` ("png"\|"svg") |
| `export_to_excalidraw_url` | URL compartible de excalidraw.com | (ninguno) |

### Gestión de Estado

| Herramienta | Descripción | Parámetros requeridos |
|-------------|-------------|-----------------------|
| `clear_canvas` | Elimina todos los elementos | (ninguno) |
| `snapshot_scene` | Guarda un snapshot con nombre | `name` |
| `restore_snapshot` | Restaura desde un snapshot | `name` |

### Viewport y Cámara

| Herramienta | Descripción | Parámetros requeridos |
|-------------|-------------|-----------------------|
| `set_viewport` | Control de cámara: zoom, scroll, centrar | (opcional) `scrollToContent`, `scrollToElementId`, `zoom` |

### Guía de Diseño y Conversión

| Herramienta | Descripción | Parámetros requeridos |
|-------------|-------------|-----------------------|
| `read_diagram_guide` | Guía de paleta de colores, tamaños, anti-patrones | (ninguno) |
| `create_from_mermaid` | Convierte diagrama Mermaid a Excalidraw | `mermaidDiagram` |

---

## REST API (HTTP)

### URL base: `http://localhost:3000`

### Endpoints de Elementos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/elements` | Listar todos |
| `GET` | `/api/elements/:id` | Obtener por ID |
| `POST` | `/api/elements` | Crear elemento |
| `PUT` | `/api/elements/:id` | Actualizar elemento |
| `DELETE` | `/api/elements/:id` | Eliminar elemento |
| `DELETE` | `/api/elements/clear` | Limpiar canvas |
| `GET` | `/api/elements/search?type=...` | Buscar con filtros |
| `POST` | `/api/elements/batch` | Crear en lote |
| `POST` | `/api/elements/sync` | Importar (limpiar + escribir) |
| `POST` | `/api/elements/from-mermaid` | Conversión desde Mermaid |

### Endpoints de Exportación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/export/image` | Solicitar exportación de imagen |
| `POST` | `/api/export/image/result` | El frontend devuelve el resultado |

### Endpoints de Viewport

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/viewport` | Establecer viewport/cámara |
| `POST` | `/api/viewport/result` | El frontend devuelve el resultado |

### Endpoints de Snapshots

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/snapshots` | Guardar snapshot `{name}` |
| `GET` | `/api/snapshots` | Listar snapshots |
| `GET` | `/api/snapshots/:name` | Obtener snapshot por nombre |

### Sistema

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/health` | Comprobación de salud |
| `GET` | `/api/sync/status` | Estadísticas de memoria/WebSocket |

---

## Diferencias Críticas MCP vs REST

| Aspecto | MCP | REST API |
|---------|-----|----------|
| **Etiquetas en formas** | `"text": "Mi Label"` | `"label": {"text": "Mi Label"}` |
| **Binding de flechas** | `startElementId`/`endElementId` | `"start": {"id": "..."}` / `"end": {"id": "..."}` |
| **fontFamily** | String `"1"` o omitir | String `"1"` o omitir |

---

## Scripts de Línea de Comandos

```bash
# En el directorio del servidor mcp_excalidraw
node scripts/healthcheck.cjs
node scripts/clear-canvas.cjs
node scripts/export-elements.cjs --out diagrama.json
node scripts/import-elements.cjs --in diagrama.json --mode batch
node scripts/create-element.cjs --data '{...}'
node scripts/update-element.cjs --id <id> --data '{...}'
node scripts/delete-element.cjs --id <id>
```

---

## Sistema de Coordenadas

- Origen `(0,0)` arriba a la izquierda
- **X**: aumenta hacia la derecha
- **Y**: aumenta hacia abajo

---

## Recuperación de Errores

| Síntoma | Solución |
|---------|---------|
| Elementos no aparecen | `describe_scene` → puede estar fuera de pantalla → `set_viewport(scrollToContent: true)` |
| Flecha no conecta | Verificar IDs con `get_element`; comprobar `startElementId`/`endElementId` |
| Canvas en mal estado | `snapshot_scene` → `clear_canvas` → reconstruir. O `restore_snapshot` |
| Elemento no actualiza | Puede estar bloqueado → `unlock_elements` primero |
| Texto duplicado | Buscar elementos `type: "text"` con `containerId` → eliminar duplicados → esperar auto-sync |

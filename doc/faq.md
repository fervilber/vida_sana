# FAQ — Preguntas Frecuentes

---

## 🛠 Instalación y Configuración

### ¿Qué necesito instalar para empezar?
1. **[Obsidian](https://obsidian.md)** → para visualizar la wiki.
2. **Un agente LLM** (Claude, Antigravity, etc.) → para mantenerla.
3. **Python 3.8+** para los scripts: `pip install -r scripts/requirements.txt`

### ¿Qué agente LLM debo usar?
Cualquiera que tenga acceso a los archivos locales. Antigravity es ideal si prefieres un entorno de código, y Claude si prefieres chat. Lo importante es que lean `RULES.md` al inicio.

---

## 📥 Importación de Fuentes

### ¿Cómo importo un video de YouTube?
`python scripts/youtube_to_raw.py "https://youtu.be/..."`
Luego dile al agente: *«Procesa `raw/nombre.md` y actualiza la wiki»*

### ¿Qué hago si el PDF es un escaneo?
El script no tiene OCR. Usa un servicio externo para convertirlo a texto o sube capturas al agente para que las describa.

### ¿Por qué mi pregunta no tiene respuesta?
El agente solo responde desde `/wiki/`. Si la información está en `/raw/` pero no ha sido ingestada, el agente no la usará para responder preguntas generales.

---

## 💬 Uso con el Agente

### ¿Cómo inicio una sesión?
Prompt: *"Lee en este orden: 1) `RULES.md` 2) `.agentic/workflows/inicializacion.md` 3) `index.md` 4) `log.md`."*

### ¿Puedo editar las notas manualmente?
Sí, pero se recomienda pedirle al agente que lo haga para asegurar que se actualicen los enlaces bidireccionales y el índice maestro.

---

## 🔧 Mantenimiento

### ¿Cómo sé qué se ha procesado?
Consulta `log.md` en la raíz. Cada acción queda registrada allí con fecha y detalle.

### ¿Qué hace "revisar wiki"?
Busca enlaces rotos, páginas huérfanas (ej. una empresa que no aparece en el índice) y contradicciones marcadas con `[!CAUTION]`.

---

*Ver también: [[user-guide]] · [[architecture]] · [[web-clipper-setup]]*

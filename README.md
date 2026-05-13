# Segundo Cerebro de Vida Sana (LLM Wiki)

Este proyecto es una base de conocimiento personal (Personal Knowledge Base) especializada en **salud, alimentación, ejercicio físico y bienestar**.

A diferencia de un sistema de archivos tradicional, este es un **Wiki Compuesto** donde un Agente de IA (LLM) actúa como mantenedor activo, extrayendo conocimiento de fuentes brutas (videos, libros, podcasts, estudios) y consolidándolo en una red interconectada de notas en formato Markdown, optimizada para ser visualizada en **Obsidian**.

## 🎯 Objetivo y Uso

El objetivo es acumular conocimiento de calidad sobre vida sana a lo largo del tiempo. Se utiliza para:

- **Analizar Alimentos y Nutrientes**: Centralizar evidencia sobre qué comer, qué moderar y qué evitar.
- **Gestionar Dietas y Patrones Alimentarios**: Documentar protocolos (mediterránea, cetogénica, ayuno intermitente...) con sus pros, contras y evidencia.
- **Guardar Recetas Adaptadas**: Construir una colección de recetas personalizadas con información nutricional.
- **Documentar Ejercicio**: Archivar protocolos de entrenamiento, rutinas y evidencia sobre deporte y recuperación.
- **Base de Conocimiento de Salud**: Reunir información sobre hábitos, medicina preventiva, sueño, estrés y bienestar mental.
- **Evaluar Divulgadores**: Mantener páginas de autores y expertos con sus tesis y fuentes.

## 📂 Estructura del Proyecto

```
2c_vida_sana/
├── raw/                  ← Fuentes brutas inmutables (transcripciones, PDFs, artículos)
├── wiki/
│   ├── alimentacion/     ← Fichas de alimentos, nutrientes y suplementos individuales
│   ├── dietas/           ← Patrones alimentarios completos
│   ├── recetas/          ← Recetas adaptadas al usuario
│   ├── ejercicio/        ← Protocolos de entrenamiento y deporte
│   ├── salud/            ← Condiciones, hábitos, medicina preventiva, sueño, estrés
│   ├── conceptos/        ← Glosario científico (microbiota, VO2max, insulina...)
│   ├── fuentes/          ← Resúmenes de libros, videos y podcasts procesados
│   ├── autores/          ← Páginas por divulgador o experto
│   └── blog/             ← Informes y análisis bajo demanda
├── scripts/              ← Herramientas de procesamiento e ingesta
├── templates/            ← Plantillas de notas para Obsidian
├── .agentic/             ← Cerebro del agente: skills, workflows y templates
├── index.md              ← Catálogo maestro (Dashboard)
├── log.md                ← Registro cronológico de actividades
└── RULES.md              ← Constitución del sistema (leer primero)
```

## 🚀 Guía de Usuario: Primeros Pasos

### 1. Ingesta de nueva información

**Opción A: Procesar un archivo estático**
1. Deposita el archivo (Markdown, Texto o PDF) en la carpeta `raw/`.
2. Dile al Agente: *"Procesa el nuevo archivo [nombre del archivo] que he puesto en raw"*.
3. El Agente creará el resumen, actualizará las fichas correspondientes y el índice.

**Opción B: Descargar transcripciones de YouTube**
Para extraer conocimiento de un video (podcast de salud, masterclass de nutrición, etc.):
- **Con el Agente:** *"Descarga la transcripción de este video: [URL]"*
- **Manualmente:**
  ```bash
  python scripts/youtube_to_raw.py "URL" "Nombre_Descriptivo"
  ```

**Opción C: Importar un PDF**
```bash
python scripts/pdf_to_raw.py "ruta/al/archivo.pdf"
```

### 2. Consultar el Wiki

Puedes navegar en Obsidian con la **Vista de Grafo** para ver conexiones entre alimentos, dietas, conceptos y autores. También puedes preguntar al Agente:
- *"¿Qué sabemos sobre el ayuno intermitente?"*
- *"¿Qué alimentos están recomendados para la salud cardiovascular?"*
- *"Dame una receta alta en proteínas para cenar"*

### 3. Añadir una Receta Personal

Dile al Agente:
- *"Añade esta receta a la wiki: [descripción de la receta]"*

El Agente creará la ficha en `wiki/recetas/` con el frontmatter nutricional estándar.

### 4. Mantenimiento (Lint)

De vez en cuando, pide al Agente: *"Haz un mantenimiento (Lint) del wiki"*. El Agente buscará contradicciones entre fuentes, enlaces rotos o fichas huérfanas.

### 5. Exámenes de Autoevaluación

El Agente puede generar tests de conocimiento sobre cualquier tema de la wiki:
- *"Crea un examen de 10 preguntas sobre nutrición básica"*
- *"Genérame un test sobre los protocolos de Andrew Huberman"*

## 🔄 Prompt de Inicialización para IA

Si cambias de conversación o modelo, usa este prompt para que el agente recupere el contexto:

> **Prompt de Inicialización:**
>
> "Actúa como mi asistente de salud y mantenedor de mi Segundo Cerebro de Vida Sana (patrón LLM Wiki). Nos encontramos en el directorio raíz de un proyecto estructurado en Markdown y optimizado para Obsidian.
>
> Tu objetivo es ayudarme a procesar fuentes (transcripciones de podcasts, libros de salud, artículos científicos) que deposite en `raw/` y transformarlas en conocimiento estructurado dentro de `wiki/` (creando y actualizando notas en `alimentacion/`, `dietas/`, `recetas/`, `ejercicio/`, `salud/`, `conceptos/`, `fuentes/` y `autores/`).
>
> **Regla de Oro:** Ante cualquier pregunta sobre salud, nutrición o ejercicio, busca tu contexto **única y exclusivamente en la carpeta `wiki/`**, ignorando los archivos en `raw/` salvo que te pida procesar uno nuevo.
>
> **Antes de hacer nada, lee en este orden:**
> 1. `RULES.md` — instrucciones operativas, esquema de frontmatter y reglas de enlazado
> 2. `index.md` — estado actual del Dashboard
> 3. `log.md` — últimas acciones realizadas
>
> Confírmame cuando hayas leído estos archivos."

---
*Este proyecto utiliza el patrón LLM Wiki para la gestión activa del conocimiento personal sobre salud y bienestar.*

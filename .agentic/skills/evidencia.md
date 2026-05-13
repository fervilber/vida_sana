---
name: "Evaluación de Evidencia Científica"
description: "Protocolo para evaluar y clasificar el nivel de evidencia científica de afirmaciones sobre salud, nutrición y ejercicio."
---

# Skill: Evaluación de Evidencia Científica

## Propósito
Define cómo el agente debe evaluar y clasificar el respaldo científico de cualquier afirmación sobre salud, nutrición o ejercicio antes de incorporarla a la wiki.

> **Principio fundamental:** No toda información de divulgadores de salud tiene el mismo respaldo científico. El agente debe actuar como un filtro crítico, no como un transcriptor acrítico.

---

## Jerarquía de Evidencia (de mayor a menor)

```
Nivel 1 — ALTA
   Meta-análisis de ensayos clínicos aleatorizados (RCT)
   Revisiones sistemáticas de alta calidad

Nivel 2 — MEDIA-ALTA
   Ensayos clínicos aleatorizados (RCT) individuales bien diseñados

Nivel 3 — MEDIA
   Estudios observacionales (cohortes, caso-control)
   RCT con limitaciones (muestra pequeña, corta duración, sin ciego)

Nivel 4 — BAJA
   Estudios en modelos animales extrapolados a humanos
   Series de casos clínicos
   Consenso de expertos sin ensayos clínicos

Nivel 5 — ANECDÓTICA
   Testimonios personales o de pacientes
   Experiencias de divulgadores sin citar estudios
   Tradiciones o prácticas culturales sin respaldo científico
```

---

## Proceso de Evaluación (paso a paso)

### Paso 1 — Identificar la afirmación
Extraer la afirmación concreta que se va a evaluar. Ejemplos:
- "El ayuno intermitente mejora la sensibilidad a la insulina"
- "Tomar 1g de omega-3 reduce el riesgo cardiovascular"
- "El café en ayunas quema grasa más eficientemente"

### Paso 2 — Buscar el tipo de evidencia citada
¿El divulgador o fuente cita estudios? Si es así, ¿de qué tipo?
- Si cita meta-análisis → clasificar como evidencia **Alta**
- Si cita RCT individuales → clasificar como **Media-Alta**
- Si cita estudios observacionales → **Media**
- Si cita estudios en animales → **Baja**
- Si no cita nada o solo experiencia personal → **Anecdótica**

### Paso 3 — Verificar coherencia con el consenso científico
Preguntar: ¿esta afirmación va en contra del consenso mayoritario de la comunidad científica?
- Si hay consenso sólido a favor → reforzar el nivel de evidencia
- Si hay debate activo en la comunidad → indicar `evidencia: Media` y documentar ambas posturas
- Si contradice el consenso → marcar con `> [!CAUTION] Afirmación controvertida`

### Paso 4 — Asignar el valor del campo `evidencia`
Usar el valor correspondiente en el frontmatter YAML:
```yaml
evidencia: "Alta | Media | Baja | Anecdotica | No analizada"
```

### Paso 5 — Documentar la fuente de la evaluación
Indicar en el cuerpo de la nota qué fuente respalda el nivel de evidencia asignado:
```markdown
> Evidencia: **Alta** — respaldado por meta-análisis (NEJM 2023, n=12 estudios)
```

---

## Indicadores de Alerta (Red Flags)

Cuando una fuente o divulgador use los siguientes patrones, aumentar el escepticismo:

- 🚩 "Los médicos no quieren que sepas esto..."
- 🚩 "Funciona en el 100% de los casos"
- 🚩 Mezcla de testimonios personales como si fueran datos clínicos
- 🚩 Estudios en ratones presentados como aplicables directamente a humanos
- 🚩 Conflicto de interés no declarado (vende el suplemento que recomienda)
- 🚩 Extrapolación extrema de un estudio pequeño

En estos casos → clasificar como `evidencia: Anecdotica` o `evidencia: Baja`, y añadir nota explicativa.

---

## Manejo de Contradicciones entre Fuentes

Si dos fuentes procesadas contradicen la misma afirmación:

```markdown
> [!CAUTION] Contradicción entre fuentes
> **Postura A** ([[fuente_1|Fuente 1]], fecha): El ayuno intermitente mejora el metabolismo en adultos sanos.
> **Postura B** ([[fuente_2|Fuente 2]], fecha): El ayuno intermitente no muestra beneficios significativos sobre dieta hipocalórica continua.
> Estado: Pendiente de contraste con evidencia de mayor jerarquía.
```

**NUNCA eliminar datos contradictorios sin confirmación del usuario.**

---

## Etiquetas en Línea para Evidencia

Usar estas etiquetas dentro del texto para enriquecer el grafo:

| Etiqueta | Cuándo usar |
|---|---|
| `#evidencia_alta` | Afirmaciones con respaldo de meta-análisis o RCT |
| `#evidencia_media` | Afirmaciones con estudios observacionales |
| `#evidencia_baja` | Afirmaciones preliminares o en animales |
| `#anecdotico` | Sin respaldo científico formal |
| `#controversia` | Debate activo en la comunidad científica |
| `#consenso_cientifico` | Hay acuerdo amplio en la comunidad |

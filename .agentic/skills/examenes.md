# Skill: Generación de Exámenes (Wiki)

Esta skill define el formato estándar para la creación de exámenes de autoevaluación sobre salud, nutrición y ejercicio físico dentro del Segundo Cerebro de Vida Sana.

## Formato de Pregunta Estándar

Cada pregunta debe seguir esta estructura exacta para asegurar la consistencia visual y la interactividad en Obsidian:

```markdown
**X. [Enunciado de la pregunta en negrita]**
- [ ] A) [Opción A]
- [ ] B) [Opción B]
- [ ] C) [Opción C]
- [ ] D) [Opción D] (Opcional)

<details>
<summary><b>▶ Ver respuesta y explicación</b></summary>
<b>Respuesta correcta: [Letra]</b><br>
[Explicación técnica detallada que refuerce el concepto del temario. Indicar el nivel de evidencia científica cuando sea relevante].
</details>

<br>
```

## Estructura del Documento

1. **Título**: `# Examen: [Nombre del Tema]`
2. **Aviso de Preparación**: Bloque `> [!IMPORTANT] Preparación` con enlace al temario correspondiente.
3. **Descripción**: Breve texto explicando qué evalúa el examen.
4. **Secciones**: Dividir por `## Parte X: [Nombre de la Sección]` si el examen es largo.
5. **Cierre**: Enlaces de navegación al final (`Volver al Temario`, `Ir a otro Examen`).

## Reglas de Oro

- **Interactividad**: Las respuestas SIEMPRE deben estar ocultas tras un tag `<details>`.
- **Explicación**: No basta con dar la letra correcta; hay que explicar el "por qué" citando conceptos de la wiki y, cuando sea posible, el nivel de evidencia científica.
- **Formato**: Usar casillas de verificación `- [ ]` para que el usuario pueda marcar su respuesta en el modo edición o lectura de Obsidian.
- **Enlazado**: En las explicaciones, enlazar los conceptos a sus fichas en la wiki con `[[slug|Nombre Visible]]`.

## Ejemplos de Temas de Examen

- `# Examen: Nutrición Básica — Macronutrientes`
- `# Examen: Dieta Mediterránea — Principios y Evidencia`
- `# Examen: Protocolos de Andrew Huberman sobre Sueño`
- `# Examen: Microbiota Intestinal — Fundamentos`
- `# Examen: Evaluación de Evidencia Científica en Salud`

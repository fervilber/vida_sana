# Historial de Actividades (Log)

Este documento es un registro cronológico, *append-only*, de todas las acciones del agente (Procesamientos, Consultas que producen artefactos, Lints).
Debe seguir el formato `## [YYYY-MM-DD] Acción | Descripción corta` para poder ser procesado mediante comandos (ej: `grep "^## \[" log.md | tail -5`).

---

## [2026-05-13] reorganizacion | Migración del wiki de inversiones a Vida Sana
- Estructura `wiki/` rediseñada: alimentacion/, dietas/, recetas/, ejercicio/, salud/, conceptos/, fuentes/, autores/, blog/, graficos/
- Scripts de bolsa eliminados: update_quotes.py, update_cartera.py, plot_quotes.py, fix_empresas.py
- Skills de inversión eliminadas: cotizaciones.md, gestion_cartera.md
- Ficheros reescritos: AGENTS.md, RULES.md, README.md, index.md
- Nuevos templates: nota-tema.md, nota-concepto.md, nota-receta.md, nota-protocolo.md
- Nueva skill: evidencia.md
- Workflows actualizados: ingesta.md, inicializacion.md

---

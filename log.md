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

## [2026-05-13] procesa | Entrevista Dr. Pérez Gascón
- Fuente: `raw/2026-04-09_ex_jefe_de_oncologia_por_que_espana_tiene_tantos_casos_de_cancer_la_respuesta_en_tu_plato.md`
- Páginas creadas:
  - `wiki/autores/dr_perez_gascon.md`
  - `wiki/fuentes/borja_bandera_dr_gascon_cancer_metabolico.md`
  - `wiki/conceptos/cancer_como_enfermedad_metabolica.md`
- Notas: Primera ingesta de material sobre salud y oncología integrativa.

## [2026-05-13] procesa | Ficha de autor: Borja Bandera
- Páginas creadas:
  - `wiki/autores/borja_bandera.md`
- Notas: Creación de la ficha de autor para el divulgador Borja Bandera a petición del usuario.

## [2026-05-13] procesa | Lote de vídeos de Borja Bandera
- Fuentes descargadas: 4 exitosas, 4 fallidas (error 429).
- Páginas creadas:
  - `wiki/ejercicio/protocolo_hipertrofia_borja_bandera.md`
  - `wiki/fuentes/ganar_musculo_es_imposible_si_entrenas_asi.md`
  - `wiki/dietas/deficit_invisible.md`
  - `wiki/fuentes/deficit_invisible_elimina_grasa_sin_sentir_que_estas_a_dieta.md`
  - `wiki/ejercicio/protocolo_sprints_zona2_borja_bandera.md`
  - `wiki/fuentes/el_entrenamiento_que_te_hace_perder_mas_grasa.md`
- Notas: Procesados 3 vídeos del lote de 8 solicitado. Los otros 4 fallaron por límites de YouTube. Queda 1 pendiente de procesar que ya está descargado.

## [2026-05-13] procesa | Libro Paleo: El libro del método Paleo (Airam Fernández, 2016)
- Script: `epub_to_raw.py` — primera prueba exitosa.
- Fuente: `raw/2016-01-01_el_libro_del_metodo_paleo_airam_fernandez.md` (113 capítulos, 292 KB)
- Páginas creadas:
  - `wiki/autores/airam_fernandez.md`
  - `wiki/dietas/dieta_paleo.md`
  - `wiki/conceptos/hormesis.md`
  - `wiki/recetas/hamburguesas_caseras_paleo.md`
  - `wiki/recetas/muesli_paleo.md`
  - `wiki/fuentes/el_libro_del_metodo_paleo_airam_fernandez.md`
- Notas: El libro contiene 69 recetas y 41 ejercicios en los anexos. Pendiente extraer más recetas.

---

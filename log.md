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

## [2026-05-13] procesa | Vídeo Grasa Rebelde (Borja Bandera)
- Fuente: `raw/2025-07-18_por_que_no_pierdes_grasa_en_los_lugares_que_deseas.md`
- Páginas creadas:
  - `wiki/conceptos/grasa_rebelde.md`
  - `wiki/fuentes/por_que_no_pierdes_grasa_en_los_lugares_que_deseas.md`
- Notas: Explicación de fisiología sobre lipólisis y beta-oxidación.

## [2026-05-13] procesa | Libros de Marcos Vázquez (Fitness Revolucionario)
- Script: `pdf_to_raw.py` (De Cero a Ceto, Barra Libre)
- Páginas creadas:
  - `wiki/autores/marcos_vazquez.md`
  - `wiki/fuentes/de_cero_a_ceto.md`
  - `wiki/fuentes/barra_libre.md`
  - `wiki/dietas/dieta_cetogenica.md`
  - `wiki/conceptos/flexibilidad_metabolica.md`
  - `wiki/conceptos/ayuno_intermitente.md`
- Notas: Extraídos en formato PDF. Fallaron archivos vacíos subidos accidentalmente (Invicto, Guerrera Espartana).

## [2026-05-13] procesa | Libro: Dime qué comes y te diré qué bacterias tienes
- Script: `epub_to_raw.py`
- Fuente: `raw/2020-01-01_dime_que_comes_y_te_dire_que_bacterias_tienes_blanca_garcia_orea_haro.md`
- Páginas creadas:
  - `wiki/autores/blanca_garcia_orea_haro.md`
  - `wiki/fuentes/dime_que_comes_y_te_dire_que_bacterias_tienes.md`
  - `wiki/conceptos/microbiota.md`
  - `wiki/conceptos/disbiosis.md`
- Notas: Extracción de epub exitosa. Introducidos conceptos base de la microbiota intestinal, relación Firmicutes/Bacteroidetes y la importancia del butirato.

---

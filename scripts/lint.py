#!/usr/bin/env python3
"""
lint.py — Validador de formato y enlaces para la LLM Wiki.

Uso:
    python scripts/lint.py              # Valida toda la wiki
    python scripts/lint.py wiki/fuentes # Valida un directorio específico
    python scripts/lint.py wiki/fuentes/mi-nota.md  # Valida un archivo

Checks realizados:
    1. Presencia de frontmatter YAML obligatorio
    2. Campos obligatorios en el YAML (ticker, sector, fecha_actualizacion para empresas)
    3. Detección de wikilinks rotos ([[Página]] que no existe)
    4. Detección de páginas huérfanas (sin enlaces entrantes)
    5. Consistencia del índice (index.md)
"""

import os
import re
import sys
import unicodedata
import yaml
from pathlib import Path
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────

WIKI_DIR = Path("wiki")
INDEX_FILE = Path("index.md")
VALID_TYPES = ["fuente", "empresa", "sector", "tesis_inversion", "concepto_financiero", "blog", "registro"]


# ─────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────

def extract_frontmatter(content: str) -> dict | None:
    """Extrae el bloque YAML frontmatter de un archivo Markdown."""
    # Normalizar finales de línea y eliminar BOM
    content = content.lstrip('\ufeff').replace('\r\n', '\n')
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None
        
    # El primer elemento debe estar vacío (si el archivo empieza por ---) o solo tener espacios
    if parts[0].strip() != '':
        return None
        
    try:
        return yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None


def extract_wikilinks(content: str) -> list[str]:
    """Extrae todos los wikilinks [[...]] de un archivo."""
    return re.findall(r"\[\[([^\]]+)\]\]", content)


def slug_from_name(name: str) -> str:
    """
    Genera el slug esperado a partir del stem del archivo.
    Regla: minúsculas, guiones bajos en lugar de espacios o guiones,
    sin tildes ni caracteres especiales.
    Coincide con la convención definida en RULES.md §2.2
    """
    # Normalizar unicode → descomponer acentos (NFD) y eliminar diacríticos
    normalized = unicodedata.normalize("NFD", name)
    ascii_name = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
    # Minúsculas
    lower = ascii_name.lower()
    # Sustituir espacios y guiones medios por guion bajo
    underscored = re.sub(r"[\s\-]+", "_", lower)
    # Eliminar caracteres especiales (todo lo que no sea alfanumérico o _)
    clean = re.sub(r"[^a-z0-9_]", "", underscored)
    # Eliminar guiones bajos múltiples consecutivos
    return re.sub(r"_+", "_", clean).strip("_")


def get_all_wiki_pages(wiki_dir: Path) -> dict[str, Path]:
    """Devuelve un dict de {título_normalizado: ruta} para todas las páginas de la wiki."""
    pages = {}
    for md_file in wiki_dir.rglob("*.md"):
        # Título normalizado = nombre del archivo sin extensión
        key = md_file.stem.lower().replace("-", " ")
        pages[key] = md_file
    return pages


# ─────────────────────────────────────────────
# CHECKS
# ─────────────────────────────────────────────

def check_frontmatter(file_path: Path, content: str) -> list[str]:
    """Verifica que el frontmatter YAML exista y tenga los campos obligatorios."""
    errors = []
    fm = extract_frontmatter(content)

    if fm is None:
        errors.append(f"  [ERROR] Sin frontmatter YAML")
        return errors

    # Detectar tipo desde el campo 'type' o desde 'tags'
    note_type = fm.get("type")
    if not note_type:
        tags = fm.get("tags", [])
        if isinstance(tags, str): tags = [tags]
        for t in VALID_TYPES:
            if t in tags:
                note_type = t
                break

    # Validar campos básicos según el tipo
    if "title" not in fm or fm["title"] is None:
        # No es crítico si el nombre del archivo es descriptivo
        errors.append(f"  [WARN] Campo YAML faltante: 'title' (usando nombre de archivo)")

    # -- Validacion de SLUG --------------------------------------------------
    slug_in_yaml = fm.get("slug")
    expected_slug = slug_from_name(file_path.stem)

    if not slug_in_yaml:
        errors.append(
            f"  [WARN] Campo 'slug' ausente en frontmatter (esperado: '{expected_slug}')"
        )
    elif slug_in_yaml != expected_slug:
        errors.append(
            f"  [WARN] Slug inconsistente: YAML tiene '{slug_in_yaml}' "
            f"pero el nombre de archivo sugiere '{expected_slug}'"
        )
    # ------------------------------------------------------------------------

    if note_type == "empresa":
        for field in ["ticker", "sector", "fecha_actualizacion"]:
            if field not in fm:
                errors.append(f"  [ERROR] Campo obligatorio para empresa faltante: '{field}'")

    if note_type not in VALID_TYPES and note_type is not None:
        errors.append(f"  [WARN] Tipo desconocido: '{note_type}' (válidos: {VALID_TYPES})")

    return errors


def check_wikilinks(file_path: Path, content: str, all_pages: dict) -> list[str]:
    """Verifica que los wikilinks apunten a páginas existentes."""
    errors = []
    links = extract_wikilinks(content)
    for link in links:
        # Normalizar el link para comparar
        normalized = link.lower().replace("-", " ").split("|")[0].strip()
        if normalized not in all_pages:
            errors.append(f"  [WARN] Wikilink roto: [[{link}]]")
    return errors


def check_filename_spaces(file_path: Path) -> list[str]:
    """
    Detecta archivos cuyo nombre contiene espacios.
    Según RULES.md §2.2 está prohibido dentro de wiki/.
    """
    errors = []
    if " " in file_path.stem:
        expected = slug_from_name(file_path.stem)
        errors.append(
            f"  [WARN] Nombre de archivo con espacios: '{file_path.name}' "
            f"-> renombrar a '{file_path.stem.replace(' ', '_')}.md' (slug: '{expected}')"
        )
    return errors


def check_orphans(all_pages: dict, all_contents: dict[Path, str]) -> list[Path]:
    """Detecta páginas sin ningún enlace entrante (huérfanas)."""
    incoming_links = {path: 0 for path in all_pages.values()}

    for content in all_contents.values():
        links = extract_wikilinks(content)
        for link in links:
            normalized = link.lower().replace("-", " ").split("|")[0].strip()
            if normalized in all_pages:
                incoming_links[all_pages[normalized]] += 1

    # El índice y el log no cuentan como huérfanos
    excluded = {"index", "log", "readme", "rules"}
    orphans = [
        path for path, count in incoming_links.items()
        if count == 0 and path.stem.lower() not in excluded
    ]
    return orphans


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else WIKI_DIR

    # Recopilar archivos a validar
    if target.is_file():
        files_to_check = [target]
    else:
        files_to_check = list(target.rglob("*.md"))

    if not files_to_check:
        print("No se encontraron archivos Markdown para validar.")
        return

    # Cargar todos los contenidos de la wiki (para detección de huérfanos y links)
    all_pages = get_all_wiki_pages(WIKI_DIR)
    # Incluir archivos en la raíz
    for root_file in Path(".").glob("*.md"):
        all_pages[root_file.stem.lower()] = root_file

    all_contents = {f: f.read_text(encoding="utf-8") for f in WIKI_DIR.rglob("*.md") if f.exists()}
    for root_file in Path(".").glob("*.md"):
        all_contents[root_file] = root_file.read_text(encoding="utf-8")

    total_errors = 0
    total_warnings = 0
    print(f"\n[SCAN] LLM Wiki Linter - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   Validando: {target}\n")
    print("-" * 60)

    for file_path in sorted(files_to_check):
        if not file_path.exists():
            continue
        content = file_path.read_text(encoding="utf-8")
        errors = []

        errors += check_frontmatter(file_path, content)
        errors += check_wikilinks(file_path, content, all_pages)
        errors += check_filename_spaces(file_path)

        if errors:
            print(f"\n[FILE] {file_path.relative_to(Path('.'))}")
            for e in errors:
                print(e)
                if "[ERROR]" in e:
                    total_errors += 1
                else:
                    total_warnings += 1

    # Check global: huérfanos
    orphans = check_orphans(all_pages, all_contents)
    if orphans:
        print(f"\n\n[ORPHANS] Paginas Huerfanas (sin enlaces entrantes):")
        for o in sorted(orphans):
            print(f"  [WARN] {o.relative_to(Path('.'))}")
            total_warnings += 1 # Contar cada huérfano como un warning

    print("\n" + "-" * 60)
    print(f"\n[DONE] Validacion completada:")
    print(f"   Errores críticos : {total_errors}")
    print(f"   Advertencias     : {total_warnings}")
    print(f"   Archivos revisados: {len(files_to_check)}\n")

    if total_errors > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

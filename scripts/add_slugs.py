#!/usr/bin/env python3
"""
add_slugs.py — Migración one-shot: añade el campo 'slug' al frontmatter YAML
de todos los archivos en wiki/ que aún no lo tienen.

Uso:
    python scripts/add_slugs.py           # Modo real (modifica archivos)
    python scripts/add_slugs.py --dry-run # Solo muestra qué haría

La convención de slug está definida en RULES.md §2.2.
"""

import re
import sys
import unicodedata
from pathlib import Path
from datetime import datetime


# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────

WIKI_DIR  = Path("wiki")
LOG_FILE  = Path("log.md")
DRY_RUN   = "--dry-run" in sys.argv


# ─────────────────────────────────────────────
# FUNCIÓN: GENERACIÓN DE SLUG
# ─────────────────────────────────────────────

def slug_from_name(name: str) -> str:
    """
    Genera el slug canónico a partir del stem del archivo.
    Convención: minúsculas, guiones bajos, sin tildes ni caracteres especiales.
    """
    # Descomponer acentos (NFD) y eliminar diacríticos
    normalized = unicodedata.normalize("NFD", name)
    ascii_name = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
    # Minúsculas
    lower = ascii_name.lower()
    # Espacios y guiones medios → guion bajo
    underscored = re.sub(r"[\s\-]+", "_", lower)
    # Eliminar todo lo que no sea alfanumérico o _
    clean = re.sub(r"[^a-z0-9_]", "", underscored)
    # Colapsar guiones bajos múltiples
    return re.sub(r"_+", "_", clean).strip("_")


# ─────────────────────────────────────────────
# FUNCIÓN: INSERCIÓN EN FRONTMATTER
# ─────────────────────────────────────────────

FRONTMATTER_RE = re.compile(r"^(---\n)(.*?)(\n---)", re.DOTALL)


def insert_slug_in_frontmatter(content: str, slug: str) -> str | None:
    """
    Inserta 'slug: "<slug>"' justo después de la línea 'aliases:' en el
    frontmatter YAML. Si el slug ya existe, no hace nada (devuelve None).
    """
    match = FRONTMATTER_RE.match(content)
    if not match:
        return None  # Sin frontmatter, omitir

    fm_block = match.group(2)

    # Si ya tiene slug, omitir
    if re.search(r"^slug\s*:", fm_block, re.MULTILINE):
        return None

    # Insertar slug después de 'aliases:' (primera ocurrencia)
    slug_line = f'slug: "{slug}"'
    if "aliases:" in fm_block:
        # Insertar en la línea siguiente a aliases
        new_fm = re.sub(
            r"(aliases:.*)",
            lambda m: m.group(1) + f"\n{slug_line}",
            fm_block,
            count=1
        )
    else:
        # Si no hay aliases, insertar al inicio del bloque
        new_fm = slug_line + "\n" + fm_block

    new_content = content[:match.start(2)] + new_fm + content[match.end(2):]
    return new_content


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    modified_files = []
    skipped_files  = []

    print(f"\n{'[DRY-RUN] ' if DRY_RUN else ''}🔧 add_slugs.py — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   Procesando: {WIKI_DIR}\n")
    print("─" * 60)

    for md_file in sorted(WIKI_DIR.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        slug    = slug_from_name(md_file.stem)
        result  = insert_slug_in_frontmatter(content, slug)

        if result is None:
            skipped_files.append(md_file)
            print(f"  ✅ Ya tiene slug (omitido): {md_file.relative_to(Path('.'))}")
        else:
            modified_files.append((md_file, slug))
            print(f"  ✏️  Añadiendo slug='{slug}': {md_file.relative_to(Path('.'))}")
            if not DRY_RUN:
                md_file.write_text(result, encoding="utf-8")

    print("\n" + "─" * 60)
    print(f"\n📊 Resumen:")
    print(f"   Archivos modificados : {len(modified_files)}")
    print(f"   Archivos sin cambios : {len(skipped_files)}")
    print(f"   Modo                 : {'DRY-RUN (ningún archivo modificado)' if DRY_RUN else 'REAL (archivos actualizados)'}\n")

    # Registrar en log.md (solo en modo real)
    if not DRY_RUN and modified_files:
        today = datetime.now().strftime("%Y-%m-%d")
        log_entry = (
            f"\n## [{today}] Migración: campo slug añadido a frontmatter\n"
            f"- **Script**: `scripts/add_slugs.py`\n"
            f"- **Archivos actualizados**: {len(modified_files)}\n"
            f"- **Convención**: `RULES.md §2.2` — minúsculas, guiones bajos, sin tildes\n"
            f"- **Archivos modificados**:\n"
        )
        for f, s in modified_files:
            log_entry += f"  - `{f.relative_to(Path('.'))}` → slug: `{s}`\n"

        with LOG_FILE.open("a", encoding="utf-8") as lf:
            lf.write(log_entry)
        print(f"📝 Entrada añadida a {LOG_FILE}\n")


if __name__ == "__main__":
    main()

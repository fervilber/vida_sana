#!/usr/bin/env python3
"""
search.py — Motor de búsqueda simple sobre la LLM Wiki.

Uso:
    python scripts/search.py "término de búsqueda"
    python scripts/search.py "término" --type concepto
    python scripts/search.py "término" --tag metodologia/agéntica

Busca en:
    - Títulos y aliases (YAML)
    - Cuerpo del texto
    - Tags YAML

Devuelve resultados ordenados por relevancia (apariciones del término).
"""

import re
import sys
import yaml
from pathlib import Path

WIKI_DIR = Path("wiki")


def extract_frontmatter(content: str) -> dict:
    """Extrae el frontmatter YAML."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def search_wiki(query: str, filter_type: str = None, filter_tag: str = None) -> list[dict]:
    """Busca el query en todos los archivos de la wiki."""
    results = []
    query_lower = query.lower()

    # Archivos en wiki/ y en la raíz
    all_files = list(WIKI_DIR.rglob("*.md")) + list(Path(".").glob("*.md"))

    for md_file in all_files:
        content = md_file.read_text(encoding="utf-8")
        fm = extract_frontmatter(content)

        # Filtrar por tipo
        if filter_type and fm.get("type") != filter_type:
            continue

        # Filtrar por tag
        if filter_tag:
            tags = fm.get("tags", [])
            if isinstance(tags, str):
                tags = [tags]
            if not any(filter_tag.lower() in str(t).lower() for t in tags):
                continue

        # Contar apariciones del query
        count = content.lower().count(query_lower)

        # Buscar también en aliases
        aliases = fm.get("aliases", [])
        if isinstance(aliases, str):
            aliases = [aliases]
        alias_match = any(query_lower in str(a).lower() for a in aliases)

        # Coincidencia en título
        title = str(fm.get("title", md_file.stem))
        title_match = query_lower in title.lower()

        if count > 0 or alias_match or title_match:
            # Extraer fragmento de contexto
            idx = content.lower().find(query_lower)
            snippet = ""
            if idx >= 0:
                start = max(0, idx - 80)
                end = min(len(content), idx + 120)
                snippet = content[start:end].replace("\n", " ").strip()

            results.append({
                "file": md_file,
                "title": title,
                "type": fm.get("type", "?"),
                "count": count + (5 if title_match else 0) + (3 if alias_match else 0),
                "snippet": snippet,
            })

    # Ordenar por relevancia (mayor count primero)
    results.sort(key=lambda x: x["count"], reverse=True)
    return results


def main():
    if len(sys.argv) < 2:
        print("Uso: python scripts/search.py \"término\" [--type TIPO] [--tag TAG]")
        sys.exit(1)

    query = sys.argv[1]
    filter_type = None
    filter_tag = None

    # Parsear argumentos adicionales
    args = sys.argv[2:]
    for i, arg in enumerate(args):
        if arg == "--type" and i + 1 < len(args):
            filter_type = args[i + 1]
        elif arg == "--tag" and i + 1 < len(args):
            filter_tag = args[i + 1]

    print(f"\n🔎 Búsqueda: \"{query}\"", end="")
    if filter_type:
        print(f" | tipo: {filter_type}", end="")
    if filter_tag:
        print(f" | tag: {filter_tag}", end="")
    print(f"\n{'─' * 60}\n")

    results = search_wiki(query, filter_type, filter_tag)

    if not results:
        print("  Sin resultados. ¿La fuente ha sido ingestada?")
        return

    for r in results[:10]:  # Mostrar top 10
        rel_path = r["file"].relative_to(Path("."))
        print(f"📄 [{r['type'].upper()}] {r['title']}")
        print(f"   Ruta: {rel_path}  |  Relevancia: {r['count']}")
        if r["snippet"]:
            print(f"   ...{r['snippet']}...")
        print()

    if len(results) > 10:
        print(f"   ... y {len(results) - 10} resultados más.\n")


if __name__ == "__main__":
    main()

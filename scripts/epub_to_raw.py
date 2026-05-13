"""
epub_to_raw.py — Convierte un libro EPUB a un fichero Markdown en raw/

Uso:
    python scripts/epub_to_raw.py <RUTA_EPUB> [NOMBRE_BASE]

Ejemplos:
    python scripts/epub_to_raw.py "raw/mi_libro.epub"
    python scripts/epub_to_raw.py "raw/mi_libro.epub" "Libro Paleo Airam Fernandez"

El archivo resultante se guardará como:
    raw/YYYY-MM-DD_NOMBRE_BASE.md

Dependencias (instalar con pip):
    pip install ebooklib html2text beautifulsoup4
"""

import sys
import re
import os
from datetime import datetime, timezone

# ─── Dependencias externas ───────────────────────────────────────────────────
try:
    import ebooklib
    from ebooklib import epub
except ImportError:
    print("ERROR: Falta la librería 'ebooklib'. Instálala con: pip install ebooklib")
    sys.exit(1)

try:
    import html2text
except ImportError:
    print("ERROR: Falta la librería 'html2text'. Instálala con: pip install html2text")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Falta la librería 'beautifulsoup4'. Instálala con: pip install beautifulsoup4")
    sys.exit(1)


# ════════════════════════════════════════════════════════════════════════════
# UTILIDADES (mismas que youtube_to_raw.py para consistencia)
# ════════════════════════════════════════════════════════════════════════════

def slugify(text: str) -> str:
    """
    Convierte un texto en slug válido para nombres de archivo:
    minúsculas, guiones bajos, sin tildes ni caracteres especiales.
    """
    replacements = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "Á": "a", "É": "e", "Í": "i", "Ó": "o", "Ú": "u",
        "ñ": "n", "Ñ": "n", "ü": "u", "Ü": "u",
        "à": "a", "è": "e", "ì": "i", "ò": "o", "ù": "u",
        "â": "a", "ê": "e", "î": "i", "ô": "o", "û": "u",
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s_-]", "", text)        # Eliminar caracteres especiales
    text = re.sub(r"[\s\-]+", "_", text).strip("_")   # Espacios/guiones → guion_bajo
    return text


def build_filename(date_str: str, name: str) -> str:
    """
    Construye el nombre de archivo según la convención del proyecto:
    YYYY-MM-DD_NOMBRE_SLUG.md
    """
    slug = slugify(name)
    return f"{date_str}_{slug}"


# ════════════════════════════════════════════════════════════════════════════
# EXTRACCIÓN DEL EPUB
# ════════════════════════════════════════════════════════════════════════════

def html_to_markdown(html_content: str) -> str:
    """
    Convierte HTML de un capítulo EPUB a texto Markdown limpio.
    Usa html2text para la conversión y BeautifulSoup para limpiezas previas.
    """
    # Limpiar el HTML antes de convertir
    soup = BeautifulSoup(html_content, "html.parser")

    # Eliminar scripts, estilos y metadatos que no tienen contenido útil
    for tag in soup.find_all(["script", "style", "meta", "link"]):
        tag.decompose()

    cleaned_html = str(soup)

    # Configurar html2text para una conversión de calidad
    converter = html2text.HTML2Text()
    converter.ignore_links = False       # Mantener los enlaces (útil si el libro los tiene)
    converter.ignore_images = True       # Ignorar imágenes (solo texto)
    converter.ignore_emphasis = False    # Mantener cursiva y negrita
    converter.body_width = 0            # Sin límite de ancho de línea (no romper párrafos)
    converter.ul_item_mark = "-"        # Usar guiones para listas
    converter.protect_links = True
    converter.wrap_links = False

    markdown = converter.handle(cleaned_html)

    # Limpiar líneas vacías excesivas (más de 2 seguidas → 2)
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    return markdown.strip()


def extract_epub_metadata(book: epub.EpubBook) -> dict:
    """
    Extrae los metadatos del libro EPUB (título, autor, fecha, etc.)
    Devuelve un diccionario con los campos disponibles.
    """
    meta = {
        "title": None,
        "author": None,
        "language": None,
        "publisher": None,
        "date": None,
        "description": None,
    }

    # Título
    titles = book.get_metadata("DC", "title")
    if titles:
        meta["title"] = titles[0][0]

    # Autor
    creators = book.get_metadata("DC", "creator")
    if creators:
        meta["author"] = ", ".join([c[0] for c in creators])

    # Idioma
    languages = book.get_metadata("DC", "language")
    if languages:
        meta["language"] = languages[0][0]

    # Editorial
    publishers = book.get_metadata("DC", "publisher")
    if publishers:
        meta["publisher"] = publishers[0][0]

    # Fecha
    dates = book.get_metadata("DC", "date")
    if dates:
        # La fecha puede tener varios formatos: "2023", "2023-05-10", etc.
        raw_date = dates[0][0]
        date_match = re.search(r"(\d{4})", raw_date)
        if date_match:
            meta["date"] = date_match.group(1)

    # Descripción / sinopsis
    descriptions = book.get_metadata("DC", "description")
    if descriptions:
        # Limpiar HTML que puede tener la descripción
        desc_html = descriptions[0][0]
        soup = BeautifulSoup(desc_html, "html.parser")
        meta["description"] = soup.get_text(separator=" ").strip()

    return meta


def extract_epub_chapters(book: epub.EpubBook) -> list[dict]:
    """
    Extrae todos los capítulos del EPUB en orden de lectura.
    Devuelve una lista de dicts con 'title' y 'content' (Markdown).
    """
    chapters = []

    # Obtener el orden de lectura (spine) del EPUB
    spine_ids = [item[0] for item in book.spine]

    for item_id in spine_ids:
        item = book.get_item_with_id(item_id)

        # Solo procesar documentos HTML (los capítulos reales)
        if item is None:
            continue
        if item.get_type() != ebooklib.ITEM_DOCUMENT:
            continue

        # Obtener el contenido HTML del capítulo
        try:
            html_content = item.get_content().decode("utf-8", errors="replace")
        except Exception:
            continue

        # Extraer el título del capítulo si existe
        soup = BeautifulSoup(html_content, "html.parser")
        chapter_title = None
        for heading in soup.find_all(["h1", "h2", "h3"]):
            text = heading.get_text(strip=True)
            if text:
                chapter_title = text
                break

        # Convertir el HTML a Markdown
        markdown_content = html_to_markdown(html_content)

        # Solo incluir capítulos con contenido real (más de 50 caracteres)
        if len(markdown_content) > 50:
            chapters.append({
                "title": chapter_title or item.get_name(),
                "content": markdown_content,
            })

    return chapters


# ════════════════════════════════════════════════════════════════════════════
# LÓGICA PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════

def epub_to_raw(epub_path: str, output_name: str | None = None):
    """
    Convierte un archivo EPUB a un fichero Markdown en raw/
    con la misma convención de nombre que youtube_to_raw.py.

    Parámetros
    ----------
    epub_path : str
        Ruta al fichero .epub.
    output_name : str | None
        Nombre base para el archivo de salida (sin fecha ni extensión).
        Si es None, se usa el título del libro.
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Validar que el fichero existe
    if not os.path.exists(epub_path):
        print(f"ERROR: El fichero '{epub_path}' no existe.")
        sys.exit(1)

    if not epub_path.lower().endswith(".epub"):
        print(f"ERROR: El fichero '{epub_path}' no tiene extensión .epub.")
        sys.exit(1)

    print(f"INFO: Leyendo EPUB: {epub_path}")

    # Cargar el libro EPUB
    try:
        book = epub.read_epub(epub_path, options={"ignore_ncx": True})
    except Exception as exc:
        print(f"ERROR: No se pudo abrir el EPUB: {exc}")
        sys.exit(1)

    # Extraer metadatos del libro
    print("INFO: Extrayendo metadatos...")
    meta = extract_epub_metadata(book)

    print(f"   Título     : {meta['title'] or '(no encontrado)'}")
    print(f"   Autor      : {meta['author'] or '(no encontrado)'}")
    print(f"   Año        : {meta['date'] or '(no encontrado)'}")
    print(f"   Idioma     : {meta['language'] or '(no encontrado)'}")

    # Determinar el nombre base del fichero de salida
    if output_name:
        base_name = output_name
    elif meta["title"]:
        base_name = meta["title"]
        if meta["author"]:
            base_name += f" - {meta['author']}"
    else:
        base_name = os.path.splitext(os.path.basename(epub_path))[0]

    # Usar la fecha de publicación del libro o la de hoy como fecha del fichero
    source_date = f"{meta['date']}-01-01" if meta["date"] else today

    filename_stem = build_filename(source_date, base_name)
    slug = slugify(base_name)
    filepath = os.path.join("raw", f"{filename_stem}.md")

    # Protección contra duplicados
    if os.path.exists(filepath):
        print(f"WARNING: El archivo '{filepath}' ya existe. Cancelado.")
        return

    # Extraer capítulos en orden
    print("INFO: Extrayendo capítulos...")
    chapters = extract_epub_chapters(book)
    print(f"INFO: {len(chapters)} capítulos encontrados.")

    # ─── Construir el frontmatter YAML ───────────────────────────────────────
    yaml_lines = [
        "---",
        f'title: "{meta["title"] or base_name}"',
        f'slug: "{slug}"',
        f'autor: "{meta["author"] or "Desconocido"}"',
        f'tipo: "libro"',
        f'editorial: "{meta["publisher"] or ""}"',
        f'source_date: "{source_date}"',
        f'import_date: "{today}"',
        f'source: "{os.path.basename(epub_path)}"',
        'tags: [epub, libro, raw]',
        "---",
    ]

    # ─── Construir el cuerpo del documento ───────────────────────────────────
    body_lines = [
        f"# {meta['title'] or base_name}",
        "",
        f"**Autor**: {meta['author'] or 'Desconocido'}  ",
        f"**Año de publicación**: {meta['date'] or 'Desconocido'}  ",
        f"**Fuente**: `{os.path.basename(epub_path)}`  ",
        f"**Importado**: {today}  ",
        "",
        "---",
        "",
    ]

    # Añadir sinopsis si existe
    if meta["description"]:
        body_lines += [
            "## Sinopsis / Descripción del libro",
            "",
            meta["description"],
            "",
            "---",
            "",
        ]

    # Añadir cada capítulo
    for i, chapter in enumerate(chapters, start=1):
        title = chapter["title"]
        content = chapter["content"]

        # Encabezado de capítulo
        body_lines.append(f"## Capítulo {i}: {title}")
        body_lines.append("")
        body_lines.append(content)
        body_lines.append("")
        body_lines.append("---")
        body_lines.append("")

    # ─── Guardar el fichero ───────────────────────────────────────────────────
    os.makedirs("raw", exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(yaml_lines))
        f.write("\n\n")
        f.write("\n".join(body_lines))

    # Mostrar resumen
    file_size_kb = os.path.getsize(filepath) / 1024
    print(f"SUCCESS: Libro convertido y guardado en '{filepath}'")
    print(f"   slug        : {slug}")
    print(f"   capítulos   : {len(chapters)}")
    print(f"   tamaño      : {file_size_kb:.1f} KB")
    print(f"   source_date : {source_date}")
    print(f"   import_date : {today}")


# ════════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python scripts/epub_to_raw.py <RUTA_EPUB> [NOMBRE_BASE]")
        print()
        print("Ejemplos:")
        print("  python scripts/epub_to_raw.py 'raw/mi_libro.epub'")
        print("  python scripts/epub_to_raw.py 'raw/mi_libro.epub' 'Libro Paleo Airam Fernandez'")
        print()
        print("El archivo resultante se guardará como: raw/YYYY-MM-DD_NOMBRE_BASE.md")
        sys.exit(1)

    epub_path = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) >= 3 else None
    epub_to_raw(epub_path, output_name)

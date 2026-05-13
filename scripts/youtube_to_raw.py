import sys
import re
import os
import ssl
import json
import urllib.request
from datetime import datetime, timezone

# ─── Dependencia externa ────────────────────────────────────────────────────
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter


# ════════════════════════════════════════════════════════════════════════════
# UTILIDADES
# ════════════════════════════════════════════════════════════════════════════

def get_video_id(url: str) -> str | None:
    """Extrae el ID de 11 caracteres de una URL de YouTube (incluyendo /live/)."""
    patterns = [
        r"(?:v=|youtu\.be/|/live/)([0-9A-Za-z_-]{11})",
        r"(?:embed/)([0-9A-Za-z_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def _ssl_context():
    """Contexto SSL sin verificación (compatible con entornos con certificados rotos)."""
    ctx = ssl._create_unverified_context()
    return ctx


def get_video_metadata(video_id: str) -> dict:
    """
    Intenta obtener título y fecha de publicación del vídeo vía la página
    pública de YouTube (sin API key). Devuelve un dict con 'title' y 'published_date'.
    La fecha estará en formato ISO YYYY-MM-DD si se encuentra, o None.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    metadata = {"title": None, "published_date": None}

    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (compatible; wiki-bot/1.0)"}
        )
        html = urllib.request.urlopen(req, context=_ssl_context(), timeout=10).read().decode("utf-8")

        # --- Título ---
        title_match = re.search(r"<title>(.*?)</title>", html)
        if title_match:
            title = title_match.group(1).replace(" - YouTube", "").strip()
            metadata["title"] = title

        # --- Fecha de publicación (campo "datePublished" del schema.org embebido) ---
        date_match = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', html)
        if date_match:
            metadata["published_date"] = date_match.group(1)

        # Fallback: campo publishDate
        if not metadata["published_date"]:
            date_match2 = re.search(r'"publishDate"\s*:\s*"(\d{4}-\d{2}-\d{2})', html)
            if date_match2:
                metadata["published_date"] = date_match2.group(1)

    except Exception as exc:
        print(f"WARNING: No se pudo obtener metadatos de YouTube: {exc}")

    return metadata


def slugify(text: str) -> str:
    """
    Convierte un texto en slug válido para nombres de archivo:
    minúsculas, guiones bajos, sin tildes ni caracteres especiales.
    """
    # Tabla de transliteración de caracteres acentuados
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
    text = re.sub(r"[^a-z0-9\s_-]", "", text)   # Eliminar caracteres especiales
    text = re.sub(r"[\s\-]+", "_", text).strip("_")  # Espacios/guiones → guion_bajo
    return text


def build_filename(date_str: str, name: str) -> str:
    """
    Construye el nombre de archivo según la convención del proyecto:
    YYYY-MM-DD_NOMBRE_SLUG.md
    """
    slug = slugify(name)
    return f"{date_str}_{slug}"


# ════════════════════════════════════════════════════════════════════════════
# LÓGICA PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════

def fetch_transcript(url: str, output_name: str | None = None):
    """
    Descarga la transcripción de un vídeo de YouTube y la guarda en raw/
    con la convención de nombre YYYY-MM-DD_NOMBRE.md y YAML completo.

    Parámetros
    ----------
    url : str
        URL del vídeo de YouTube.
    output_name : str | None
        Nombre base deseado para el archivo (sin fecha ni extensión).
        Si es None, se intenta obtener el título automáticamente.
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")  # fecha de importación

    # 1. Extraer ID del vídeo
    video_id = get_video_id(url)
    if not video_id:
        print(f"ERROR: No se pudo extraer el ID del video de la URL: {url}")
        return

    # 2. Obtener metadatos (título + fecha de publicación)
    print("INFO: Obteniendo metadatos del vídeo...")
    meta = get_video_metadata(video_id)

    source_date = meta["published_date"] or today  # si no se conoce, usar fecha de importación
    if not meta["published_date"]:
        print(f"WARNING: Fecha de publicación no detectada — se usará la fecha de importación ({today}) como source_date.")

    # 3. Determinar el nombre del archivo
    if output_name:
        base_name = output_name
    elif meta["title"]:
        base_name = meta["title"]
        print(f"INFO: Título detectado: {base_name}")
    else:
        base_name = f"transcripcion_{video_id}"

    filename_stem = build_filename(source_date, base_name)
    slug = slugify(base_name)
    filepath = os.path.join("raw", f"{filename_stem}.md")

    # 4. Protección contra duplicados
    if os.path.exists(filepath):
        print(f"WARNING: El archivo '{filepath}' ya existe. Descarga cancelada.")
        return

    # 5. Descargar transcripción
    try:
        print("INFO: Descargando transcripción...")
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        try:
            transcript = transcript_list.find_transcript(["es", "en"])
        except Exception:
            transcript = transcript_list.find_generated_transcript(["es", "en"])

        transcript_data = transcript.fetch()
        formatter = TextFormatter()
        text_formatted = formatter.format_transcript(transcript_data)

    except Exception as exc:
        print(f"ERROR: Error al obtener transcripción: {exc}")
        return

    # 6. Construir el YAML del frontmatter
    yaml_lines = [
        "---",
        f'title: "Transcripción: {base_name}"',
        f'slug: "{slug}"',
        f'source: "{url}"',
        f'source_date: "{source_date}"',
        f'import_date: "{today}"',
        "tags: [youtube, transcripcion, raw]",
        "---",
    ]

    # 7. Guardar el archivo
    os.makedirs("raw", exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(yaml_lines))
        f.write("\n\n")
        f.write(f"# Transcripción de YouTube\n\n")
        f.write(f"**URL**: {url}  \n")
        f.write(f"**Fecha de publicación**: {source_date}  \n")
        f.write(f"**Importado**: {today}  \n\n")
        f.write("---\n\n")
        f.write(text_formatted)

    print(f"SUCCESS: Transcripción guardada en '{filepath}'")
    print(f"   slug        : {slug}")
    print(f"   source_date : {source_date}")
    print(f"   import_date : {today}")


# ════════════════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python youtube_to_raw.py <URL_YOUTUBE> [NOMBRE_BASE]")
        print()
        print("Ejemplos:")
        print("  python youtube_to_raw.py 'https://youtu.be/abc123'")
        print("  python youtube_to_raw.py 'https://youtu.be/abc123' 'Gorka_Empresas_Ciclicas'")
        print()
        print("El archivo se guardará como: raw/YYYY-MM-DD_NOMBRE_BASE.md")
        sys.exit(1)

    target_url = sys.argv[1]
    target_name = sys.argv[2] if len(sys.argv) >= 3 else None
    fetch_transcript(target_url, target_name)

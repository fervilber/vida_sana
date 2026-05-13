#!/usr/bin/env python3
"""
pdf_to_raw.py — Importador de PDFs a la carpeta /raw/ de la LLM Wiki.

Extrae el texto de un archivo PDF, lo convierte a Markdown con frontmatter
estándar del proyecto y lo guarda en /raw/ listo para ser ingestado por el agente.

Uso:
    python scripts/pdf_to_raw.py <ruta_al_pdf>
    python scripts/pdf_to_raw.py <ruta_al_pdf> [nombre_destino]

Ejemplos:
    python scripts/pdf_to_raw.py "C:/Descargas/informe_anual.pdf"
    python scripts/pdf_to_raw.py "C:/Descargas/informe_anual.pdf" "informe_apple_2024"

Dependencias:
    pip install pymupdf    (recomendado, más preciso)
    pip install pdfplumber (alternativa, mejor con tablas)
    pip install pypdf2     (alternativa ligera, fallback)

Nota sobre imágenes:
    Las imágenes embebidas en el PDF NO se extraen en esta versión.
    Para PDFs con contenido principalmente visual o escaneos,
    considera usar un servicio OCR externo antes de importar.
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime


# ─────────────────────────────────────────────
# DIRECTORIO DE SALIDA
# ─────────────────────────────────────────────

RAW_DIR = Path("raw")


# ─────────────────────────────────────────────
# EXTRACCIÓN DE TEXTO (intenta múltiples librerías)
# ─────────────────────────────────────────────

def extract_with_pymupdf(pdf_path: Path) -> str:
    """Extrae texto usando PyMuPDF (fitz). Mejor calidad general."""
    import fitz  # pymupdf
    doc = fitz.open(str(pdf_path))
    pages = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")
        if text.strip():
            pages.append(f"<!-- Página {page_num} -->\n{text.strip()}")
    doc.close()
    return "\n\n".join(pages)


def extract_with_pdfplumber(pdf_path: Path) -> str:
    """Extrae texto usando pdfplumber. Mejor con tablas."""
    import pdfplumber
    pages = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text and text.strip():
                pages.append(f"<!-- Página {page_num} -->\n{text.strip()}")
    return "\n\n".join(pages)


def extract_with_pypdf2(pdf_path: Path) -> str:
    """Extrae texto usando PyPDF2. Librería de fallback más ligera."""
    from PyPDF2 import PdfReader
    reader = PdfReader(str(pdf_path))
    pages = []
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text and text.strip():
            pages.append(f"<!-- Página {page_num} -->\n{text.strip()}")
    return "\n\n".join(pages)


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Intenta extraer texto con las librerías disponibles,
    en orden de preferencia: pymupdf → pdfplumber → pypdf2.
    """
    extractors = [
        ("PyMuPDF",     extract_with_pymupdf),
        ("pdfplumber",  extract_with_pdfplumber),
        ("PyPDF2",      extract_with_pypdf2),
    ]

    for lib_name, extractor in extractors:
        try:
            print(f"  Intentando con {lib_name}...")
            text = extractor(pdf_path)
            if text.strip():
                print(f"  Texto extraido con {lib_name}.")
                return text
        except ImportError:
            print(f"  {lib_name} no instalado. Continuando...")
        except Exception as e:
            print(f"  {lib_name} fallo: {e}")

    return ""


# ─────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────

def sanitize_filename(name: str) -> str:
    """Convierte una cadena en un nombre de archivo seguro en kebab-case."""
    # Eliminar caracteres no alfanuméricos (excepto espacios y guiones)
    name = re.sub(r"[^\w\s-]", "", name).strip()
    # Reemplazar espacios y múltiples guiones por un guión simple
    name = re.sub(r"[-\s]+", "_", name)
    return name.lower()


def build_output_filename(pdf_path: Path, custom_name: str = None) -> str:
    """Genera el nombre del archivo de salida."""
    if custom_name:
        return sanitize_filename(custom_name)
    # Usar el nombre del PDF por defecto
    return sanitize_filename(pdf_path.stem)


def build_markdown(pdf_path: Path, raw_text: str) -> str:
    """Construye el archivo Markdown con frontmatter del proyecto."""
    today = datetime.now().strftime("%Y-%m-%d")
    title = pdf_path.stem.replace("_", " ").replace("-", " ").title()

    frontmatter = f"""---
title: "{title}"
aliases: []
type: fuente
tags:
  - fuente/pdf
source_date: {today}
source_url: "{pdf_path.name}"
created: {today}
updated: {today}
---

"""
    header = f"""# {title}

> **Fuente original**: `{pdf_path.name}`
> **Importado**: {today}
> **Páginas extraídas**: {raw_text.count('<!-- Página')}

---

## Contenido Extraído

"""
    return frontmatter + header + raw_text


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    pdf_input = Path(sys.argv[1])
    custom_name = sys.argv[2] if len(sys.argv) >= 3 else None

    # Validar que el archivo existe y es un PDF
    if not pdf_input.exists():
        print(f"Error: El archivo no existe: {pdf_input}")
        sys.exit(1)

    if pdf_input.suffix.lower() != ".pdf":
        print(f"Error: El archivo no es un PDF: {pdf_input}")
        sys.exit(1)

    print(f"\nLLM Wiki - Importador de PDF")
    print(f"   Archivo: {pdf_input.name}")
    print(f"   Tamaño : {pdf_input.stat().st_size / 1024:.1f} KB\n")

    # Extraer texto
    print("Extrayendo texto del PDF...")
    raw_text = extract_text_from_pdf(pdf_input)

    if not raw_text.strip():
        print("\nNo se pudo extraer texto del PDF.")
        print("   Posibles causas:")
        print("   • El PDF contiene solo imágenes (escaneo) → usa OCR primero.")
        print("   • Ninguna librería de extracción está instalada.")
        print("   • Instala alguna: pip install pymupdf  |  pip install pdfplumber")
        sys.exit(1)

    # Construir nombre y ruta de salida
    output_name = build_output_filename(pdf_input, custom_name)
    RAW_DIR.mkdir(exist_ok=True)
    output_path = RAW_DIR / f"{output_name}.md"

    # Verificar duplicados
    if output_path.exists():
        print(f"Ya existe: '{output_path}'. Operación cancelada para evitar duplicados.")
        print(f"   Usa un nombre personalizado: python scripts/pdf_to_raw.py <pdf> <nuevo_nombre>")
        sys.exit(0)

    # Escribir el archivo Markdown
    print(f"\nGenerando Markdown...")
    md_content = build_markdown(pdf_input, raw_text)
    output_path.write_text(md_content, encoding="utf-8")

    word_count = len(raw_text.split())
    page_count = raw_text.count("<!-- Página")

    print(f"\nPDF importado correctamente:")
    print(f"   Destino  : {output_path}")
    print(f"   Páginas  : {page_count}")
    print(f"   Palabras : ~{word_count:,}")
    print(f"\n👉 Siguiente paso → dile al agente: «Procesa el archivo {output_path} y actualiza la wiki»\n")


if __name__ == "__main__":
    main()

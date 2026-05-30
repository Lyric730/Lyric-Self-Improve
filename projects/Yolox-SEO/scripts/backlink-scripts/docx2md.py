#!/usr/bin/env python3
"""
docx -> markdown, preserving paragraphs / headings / tables / image references.
Images are extracted to _assets/<doc_stem>/img-N.<ext>.

Usage:
  python3 docx2md.py <input.docx> <out_dir>
"""
import sys
import os
import re
import zipfile
import shutil
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn


def slugify(name: str) -> str:
    name = re.sub(r"[\\/:*?\"<>|\n\r\t]+", "_", name)
    return name.strip("._ ").strip()


def extract_images(docx_path: Path, assets_dir: Path) -> dict:
    """Extract all images from word/media/ to assets_dir.
    Returns {original_filename: relative_path_for_md}."""
    assets_dir.mkdir(parents=True, exist_ok=True)
    mapping = {}
    with zipfile.ZipFile(docx_path) as z:
        media = [n for n in z.namelist() if n.startswith("word/media/")]
        for i, name in enumerate(sorted(media), 1):
            ext = Path(name).suffix.lower() or ".bin"
            out_name = f"img-{i:03d}{ext}"
            out_path = assets_dir / out_name
            with z.open(name) as src, open(out_path, "wb") as dst:
                shutil.copyfileobj(src, dst)
            mapping[Path(name).name] = out_name
    return mapping


def build_rid_to_image(doc) -> dict:
    """Map relationship id -> original image filename (in word/media/)."""
    rid_map = {}
    for rid, rel in doc.part.rels.items():
        if "image" in rel.reltype:
            target = rel.target_ref  # e.g. "media/image1.png"
            rid_map[rid] = Path(target).name
    return rid_map


def iter_block_items(parent):
    """Iterate body's direct children: paragraphs and tables, in order."""
    from docx.document import Document as _Document
    from docx.oxml.table import CT_Tbl
    from docx.oxml.text.paragraph import CT_P
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    else:
        parent_elm = parent._element
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def paragraph_to_md(p, rid_map: dict, img_mapping: dict, rel_assets_prefix: str) -> str:
    """Convert a paragraph to markdown. Handles headings, bold, italics, hyperlinks, inline images."""
    style = (p.style.name or "").lower() if p.style else ""

    # Detect heading level
    heading_level = 0
    m = re.match(r"heading\s*(\d+)", style)
    if m:
        heading_level = int(m.group(1))
    elif style.startswith("title"):
        heading_level = 1

    parts = []
    # Walk the paragraph XML to preserve order of runs, hyperlinks, drawings.
    for child in p._p.iter():
        tag = child.tag
        if tag == qn("w:t"):
            text = child.text or ""
            # find ancestor run for formatting
            run_elem = child.getparent()
            if run_elem is not None and run_elem.tag == qn("w:r"):
                rpr = run_elem.find(qn("w:rPr"))
                bold = rpr is not None and rpr.find(qn("w:b")) is not None
                italic = rpr is not None and rpr.find(qn("w:i")) is not None
                if bold and text.strip():
                    text = f"**{text}**"
                if italic and text.strip():
                    text = f"*{text}*"
            parts.append(text)
        elif tag == qn("w:hyperlink"):
            # collect inner text from this hyperlink
            rid = child.get(qn("r:id"))
            inner = "".join(t.text or "" for t in child.iter(qn("w:t")))
            url = ""
            if rid is not None:
                try:
                    url = p.part.rels[rid].target_ref
                except KeyError:
                    pass
            if url:
                parts.append(f"[{inner}]({url})")
            else:
                parts.append(inner)
        elif tag == qn("w:drawing") or tag == qn("w:pict"):
            # find embedded image rid
            blip = None
            for d in child.iter():
                if d.tag == qn("a:blip") or d.tag.endswith("}blip"):
                    blip = d
                    break
            if blip is not None:
                rid = blip.get(qn("r:embed")) or blip.get(qn("r:link"))
                if rid and rid in rid_map:
                    orig_name = rid_map[rid]
                    if orig_name in img_mapping:
                        parts.append(f"\n\n![]({rel_assets_prefix}/{img_mapping[orig_name]})\n\n")

    # Deduplicate text — iter() with w:t can revisit text under hyperlinks.
    # Strategy: only emit w:t from runs whose direct parent is the paragraph (not nested under hyperlink).
    # The above loop already handles this because hyperlink consumes its own inner text,
    # but w:t under hyperlink will also be visited. We need a smarter walker.
    # Simplification: redo with controlled walk.

    parts = []
    for child in p._p.iterchildren():
        ctag = child.tag
        if ctag == qn("w:r"):
            # run
            rpr = child.find(qn("w:rPr"))
            bold = rpr is not None and rpr.find(qn("w:b")) is not None
            italic = rpr is not None and rpr.find(qn("w:i")) is not None
            run_text_parts = []
            for sub in child.iterchildren():
                stag = sub.tag
                if stag == qn("w:t"):
                    run_text_parts.append(sub.text or "")
                elif stag == qn("w:br"):
                    run_text_parts.append("\n")
                elif stag == qn("w:tab"):
                    run_text_parts.append("\t")
                elif stag == qn("w:drawing") or stag == qn("w:pict"):
                    # find embedded image rid
                    blip = None
                    for d in sub.iter():
                        if d.tag == qn("a:blip") or d.tag.endswith("}blip"):
                            blip = d
                            break
                    if blip is not None:
                        rid = blip.get(qn("r:embed")) or blip.get(qn("r:link"))
                        if rid and rid in rid_map:
                            orig_name = rid_map[rid]
                            if orig_name in img_mapping:
                                parts.append(f"\n\n![]({rel_assets_prefix}/{img_mapping[orig_name]})\n\n")
            text = "".join(run_text_parts)
            if text:
                if bold and text.strip():
                    text = f"**{text.strip()}**" + (" " if text.endswith(" ") else "")
                if italic and text.strip():
                    text = f"*{text.strip()}*" + (" " if text.endswith(" ") else "")
                parts.append(text)
        elif ctag == qn("w:hyperlink"):
            rid = child.get(qn("r:id"))
            inner = "".join(t.text or "" for t in child.iter(qn("w:t")))
            url = ""
            if rid is not None:
                try:
                    url = p.part.rels[rid].target_ref
                except KeyError:
                    pass
            if url:
                parts.append(f"[{inner}]({url})")
            else:
                parts.append(inner)
        elif ctag == qn("w:bookmarkStart") or ctag == qn("w:bookmarkEnd"):
            pass
        # ignore other tags (proofErr, etc.)

    text = "".join(parts).strip()
    if not text:
        return ""

    if heading_level > 0:
        return ("#" * min(heading_level, 6)) + " " + text
    return text


def table_to_md(t) -> str:
    rows = t.rows
    if not rows:
        return ""
    out_lines = []
    # header
    header_cells = [c.text.strip().replace("\n", " ").replace("|", "\\|") for c in rows[0].cells]
    out_lines.append("| " + " | ".join(header_cells) + " |")
    out_lines.append("| " + " | ".join(["---"] * len(header_cells)) + " |")
    for row in rows[1:]:
        cells = [c.text.strip().replace("\n", " ").replace("|", "\\|") for c in row.cells]
        out_lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(out_lines)


def convert(docx_path: Path, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = slugify(docx_path.stem)
    md_path = out_dir / f"{stem}.md"
    assets_root = out_dir.parent / "_assets" / stem
    rel_assets_prefix = f"../_assets/{stem}"

    doc = Document(str(docx_path))
    rid_map = build_rid_to_image(doc)
    img_mapping = extract_images(docx_path, assets_root)

    lines = [f"# {docx_path.stem}", ""]
    for block in iter_block_items(doc):
        if block.__class__.__name__ == "Paragraph":
            line = paragraph_to_md(block, rid_map, img_mapping, rel_assets_prefix)
            if line:
                lines.append(line)
                lines.append("")
        elif block.__class__.__name__ == "Table":
            tbl_md = table_to_md(block)
            if tbl_md:
                lines.append(tbl_md)
                lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    return {
        "md_path": str(md_path),
        "assets_dir": str(assets_root),
        "image_count": len(img_mapping),
        "char_count": sum(len(l) for l in lines),
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    result = convert(src, out)
    print(result)

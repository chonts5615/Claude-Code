"""Deterministic markdown -> branded PDF renderer.

The report-writer agent reliably produces markdown but is flaky at driving a
reportlab build itself, so the PDF is rendered here in code instead. This also
makes branding deterministic: the brand config (the report-branding skill's
spec) is applied consistently every time.
"""

import json
import re
from html import escape
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

_BRAND_DEFAULTS = {
    "brand_name": "",
    "tagline": "",
    "primary_color": "#1F2937",
    "secondary_color": "#4B5563",
    "accent_color": "#2563EB",
    "background_tint": "#F5F7FA",
    "heading_font": "Helvetica-Bold",
    "body_font": "Helvetica",
    "logo_path": "",
    "footer_text": "Confidential",
    "cover_page": True,
    "page_numbers": True,
}


def load_brand(brand_config_path: str | Path | None) -> dict:
    """Load a brand config, falling back to the neutral defaults for any key."""
    brand = dict(_BRAND_DEFAULTS)
    if brand_config_path:
        path = Path(brand_config_path)
        if path.exists():
            try:
                brand.update(json.load(open(path, encoding="utf-8")))
            except (json.JSONDecodeError, OSError):
                pass
    return brand


def _inline(text: str) -> str:
    """Escape text and convert a tiny subset of markdown to reportlab markup."""
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"`(.+?)`", r'<font face="Courier">\1</font>', text)
    # Markdown links [text](url) -> text (url)
    text = re.sub(r"\[(.+?)\]\((https?://[^)]+)\)", r"\1 (\2)", text)
    return text


def _styles(brand: dict) -> dict[str, ParagraphStyle]:
    primary = colors.HexColor(brand["primary_color"])
    accent = colors.HexColor(brand["accent_color"])
    secondary = colors.HexColor(brand["secondary_color"])
    base = getSampleStyleSheet()
    body = brand["body_font"]
    head = brand["heading_font"]
    return {
        "title": ParagraphStyle("title", parent=base["Title"], fontName=head,
                                 textColor=primary, fontSize=24, leading=28),
        "h1": ParagraphStyle("h1", fontName=head, textColor=primary, fontSize=16,
                              leading=20, spaceBefore=14, spaceAfter=6),
        "h2": ParagraphStyle("h2", fontName=head, textColor=primary, fontSize=13,
                             leading=17, spaceBefore=10, spaceAfter=4),
        "h3": ParagraphStyle("h3", fontName=head, textColor=accent, fontSize=11,
                             leading=15, spaceBefore=8, spaceAfter=3),
        "body": ParagraphStyle("body", fontName=body, fontSize=10, leading=14,
                               spaceAfter=6),
        "bullet": ParagraphStyle("bullet", fontName=body, fontSize=10, leading=14,
                                 leftIndent=16, spaceAfter=2, bulletIndent=4),
        "caption": ParagraphStyle("caption", fontName=body, fontSize=8.5,
                                  textColor=secondary, alignment=TA_CENTER, spaceAfter=10),
        "cover_sub": ParagraphStyle("cover_sub", fontName=body, fontSize=12,
                                    textColor=secondary, alignment=TA_CENTER, spaceAfter=6),
        "cover_brand": ParagraphStyle("cover_brand", fontName=head, fontSize=11,
                                      textColor=accent, alignment=TA_CENTER, spaceAfter=24),
    }


def _table_from_block(rows: list[str], brand: dict, st: dict) -> Table | None:
    parsed = []
    for r in rows:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        if set("".join(cells)) <= set("-: "):  # separator row
            continue
        parsed.append([Paragraph(_inline(c), st["body"]) for c in cells])
    if not parsed:
        return None
    t = Table(parsed, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(brand["accent_color"])),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), brand["heading_font"]),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor(brand["background_tint"])]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor(brand["secondary_color"])),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def _parse_markdown(md: str, brand: dict, st: dict) -> tuple[str, list]:
    """Return (title, flowables). The first H1 becomes the document title."""
    title = brand.get("brand_name") or "Research Report"
    flow: list = []
    para: list[str] = []
    table_rows: list[str] = []
    title_found = False

    def flush_para():
        nonlocal para
        if para:
            flow.append(Paragraph(_inline(" ".join(para)), st["body"]))
            para = []

    def flush_table():
        nonlocal table_rows
        if table_rows:
            tbl = _table_from_block(table_rows, brand, st)
            if tbl is not None:
                flow.extend([tbl, Spacer(1, 8)])
            table_rows = []

    for raw in md.splitlines():
        line = raw.rstrip()
        if line.lstrip().startswith("|") and "|" in line.lstrip()[1:]:
            flush_para()
            table_rows.append(line)
            continue
        flush_table()
        if not line.strip():
            flush_para()
            continue
        if line.startswith("# "):
            flush_para()
            text = line[2:].strip()
            if not title_found:
                title = text
                title_found = True
            else:
                flow.append(Paragraph(_inline(text), st["h1"]))
            continue
        for prefix, key in (("### ", "h3"), ("## ", "h2")):
            if line.startswith(prefix):
                flush_para()
                flow.append(Paragraph(_inline(line[len(prefix):].strip()), st[key]))
                break
        else:
            stripped = line.strip()
            if re.match(r"^([-*]|\d+\.)\s+", stripped):
                flush_para()
                item = re.sub(r"^([-*]|\d+\.)\s+", "", stripped)
                flow.append(Paragraph(_inline(item), st["bullet"], bulletText="•"))
            elif set(stripped) <= set("-=*") and len(stripped) >= 3:
                continue  # horizontal rule
            else:
                para.append(stripped)
    flush_para()
    flush_table()
    return title, flow


def _append_figures(flow: list, charts_dir: Path, st: dict) -> None:
    charts = sorted(charts_dir.glob("*.png"))
    if not charts:
        return
    flow.append(PageBreak())
    flow.append(Paragraph("Figures", st["h1"]))
    for i, png in enumerate(charts, 1):
        try:
            img = Image(str(png))
        except Exception:
            continue
        max_w = 6.3 * inch
        if img.drawWidth > max_w:
            img.drawHeight *= max_w / img.drawWidth
            img.drawWidth = max_w
        caption = png.stem.replace("_", " ").title()
        flow.extend([img, Paragraph(f"Figure {i}. {escape(caption)}", st["caption"])])


def render_report_pdf(
    report_md: str | Path,
    charts_dir: str | Path,
    out_pdf: str | Path,
    brand_config_path: str | Path | None = None,
) -> Path:
    """Render a markdown report to a branded PDF. Returns the output path."""
    brand = load_brand(brand_config_path)
    st = _styles(brand)
    md = Path(report_md).read_text(encoding="utf-8", errors="ignore")
    title, body_flow = _parse_markdown(md, brand, st)

    flow: list = []
    if brand.get("cover_page", True):
        flow.append(Spacer(1, 2.2 * inch))
        if brand.get("brand_name"):
            flow.append(Paragraph(escape(brand["brand_name"]).upper(), st["cover_brand"]))
        flow.append(Paragraph(escape(title), st["title"]))
        if brand.get("tagline"):
            flow.append(Paragraph(escape(brand["tagline"]), st["cover_sub"]))
        flow.append(PageBreak())
    flow.extend(body_flow)
    _append_figures(flow, Path(charts_dir), st)

    secondary = colors.HexColor(brand["secondary_color"])
    footer_text = brand.get("footer_text", "")
    show_pages = brand.get("page_numbers", True)

    def _decorate(canvas: Any, doc: Any) -> None:
        canvas.saveState()
        canvas.setFont(brand["body_font"], 8)
        canvas.setStrokeColor(secondary)
        canvas.line(0.75 * inch, 0.6 * inch, letter[0] - 0.75 * inch, 0.6 * inch)
        canvas.setFillColor(secondary)
        if footer_text:
            canvas.drawString(0.75 * inch, 0.45 * inch, footer_text)
        if show_pages:
            canvas.drawRightString(letter[0] - 0.75 * inch, 0.45 * inch, f"Page {doc.page}")
        canvas.restoreState()

    out = Path(out_pdf)
    SimpleDocTemplate(
        str(out), pagesize=letter,
        leftMargin=0.85 * inch, rightMargin=0.85 * inch,
        topMargin=0.85 * inch, bottomMargin=0.85 * inch,
    ).build(flow, onFirstPage=_decorate, onLaterPages=_decorate)
    return out

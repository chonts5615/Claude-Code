"""Cargill brand constants must match spec."""

from src.utils import branding


def test_brand_constants():
    assert branding.LEAF_GREEN.upper() in ("#00843D",)
    assert branding.WHITE_GREEN.upper() in ("#F5F9ED",)
    assert branding.ARIAL == "Arial"
    assert branding.GEORGIA == "Georgia"


def test_helpers_return_openpyxl_objects():
    hf = branding.header_fill()
    af = branding.alt_row_fill()
    hfont = branding.header_font()
    bfont = branding.body_font()
    assert hf is not None
    assert af is not None
    assert hfont.bold is True
    assert bfont.name == "Arial"

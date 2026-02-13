"""
Color utility functions for Cargill brand palette.
"""

from pptx.dml.color import RGBColor


def hex_to_rgb(hex_color: str) -> RGBColor:
    """Convert hex color string to RGBColor."""
    hex_color = hex_color.lstrip("#")
    return RGBColor(
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )


def rgb_to_hex(color: RGBColor) -> str:
    """Convert RGBColor to hex string."""
    return f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}"


def tint_color(color: RGBColor, factor: float = 0.3) -> RGBColor:
    """Create a lighter tint of a color by mixing with white."""
    r = int(color[0] + (255 - color[0]) * factor)
    g = int(color[1] + (255 - color[1]) * factor)
    b = int(color[2] + (255 - color[2]) * factor)
    return RGBColor(min(r, 255), min(g, 255), min(b, 255))


def shade_color(color: RGBColor, factor: float = 0.3) -> RGBColor:
    """Create a darker shade of a color by mixing with black."""
    r = int(color[0] * (1 - factor))
    g = int(color[1] * (1 - factor))
    b = int(color[2] * (1 - factor))
    return RGBColor(max(r, 0), max(g, 0), max(b, 0))


def luminance(color: RGBColor) -> float:
    """Calculate relative luminance of a color (WCAG formula)."""
    def linearize(c: int) -> float:
        cs = c / 255.0
        return cs / 12.92 if cs <= 0.03928 else ((cs + 0.055) / 1.055) ** 2.4

    r_lin = linearize(color[0])
    g_lin = linearize(color[1])
    b_lin = linearize(color[2])
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def contrast_ratio(color1: RGBColor, color2: RGBColor) -> float:
    """Calculate contrast ratio between two colors (WCAG 2.0)."""
    l1 = luminance(color1)
    l2 = luminance(color2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def meets_contrast_aa(foreground: RGBColor, background: RGBColor, large_text: bool = False) -> bool:
    """Check if color combination meets WCAG AA contrast requirements."""
    ratio = contrast_ratio(foreground, background)
    threshold = 3.0 if large_text else 4.5
    return ratio >= threshold


def select_text_color_for_background(background: RGBColor) -> RGBColor:
    """Select white or dark text based on background luminance."""
    from src.brand.constants import WHITE, NEUTRAL_1000
    lum = luminance(background)
    return WHITE if lum < 0.5 else NEUTRAL_1000

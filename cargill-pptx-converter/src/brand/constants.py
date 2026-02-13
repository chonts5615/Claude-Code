"""
Cargill Brand Constants - Single source of truth for all visual identity values.

All color, typography, spacing, and layout constants are derived from:
- Cargill_BrandBook_digital_version_December_2025.pdf
- Cargill_Digital_Style_Guide_v1_0_Jan_2025.pdf
"""

from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor


# =============================================================================
# PRIMARY BRAND COLORS (Core Identity - Use ~30% of visual estate)
# =============================================================================

WHITE = RGBColor(0xFF, 0xFF, 0xFF)
WHITE_GREEN = RGBColor(0xF5, 0xF9, 0xED)  # green-100
SOFT_GREEN = RGBColor(0xBD, 0xE5, 0x88)   # green-200
GREEN_300 = RGBColor(0x81, 0xAB, 0x40)     # green-300 (digital only)
CARGILL_LEAF_GREEN = RGBColor(0x00, 0x84, 0x3D)  # PRIMARY BRAND COLOR
GREEN_700 = RGBColor(0x01, 0x63, 0x2D)     # green-700 (digital only)
DEEP_GREEN = RGBColor(0x03, 0x44, 0x1F)    # green-800
GREEN_900 = RGBColor(0x01, 0x29, 0x12)     # green-900 (digital only)
BLACK = RGBColor(0x00, 0x00, 0x00)

# Hex versions for matplotlib and non-pptx use
HEX_WHITE = "#FFFFFF"
HEX_WHITE_GREEN = "#F5F9ED"
HEX_SOFT_GREEN = "#BDE588"
HEX_GREEN_300 = "#81AB40"
HEX_CARGILL_LEAF_GREEN = "#00843D"
HEX_GREEN_700 = "#01632D"
HEX_DEEP_GREEN = "#03441F"
HEX_GREEN_900 = "#012912"
HEX_BLACK = "#000000"


# =============================================================================
# NEUTRAL PALETTE (Text, borders - use sparingly)
# =============================================================================

NEUTRAL_100 = RGBColor(0xF3, 0xF4, 0xF3)
NEUTRAL_200 = RGBColor(0xE7, 0xE8, 0xE8)
NEUTRAL_300 = RGBColor(0xDB, 0xDD, 0xDC)
NEUTRAL_400 = RGBColor(0x9F, 0xA4, 0xA2)
NEUTRAL_500 = RGBColor(0x70, 0x77, 0x73)
NEUTRAL_600 = RGBColor(0x58, 0x60, 0x5C)
NEUTRAL_700 = RGBColor(0x40, 0x49, 0x45)
NEUTRAL_800 = RGBColor(0x28, 0x33, 0x2D)
NEUTRAL_900 = RGBColor(0x1C, 0x27, 0x22)
NEUTRAL_1000 = RGBColor(0x10, 0x1C, 0x16)

HEX_NEUTRAL_100 = "#F3F4F3"
HEX_NEUTRAL_200 = "#E7E8E8"
HEX_NEUTRAL_300 = "#DBDDDC"
HEX_NEUTRAL_400 = "#9FA4A2"
HEX_NEUTRAL_500 = "#707773"
HEX_NEUTRAL_600 = "#58605C"
HEX_NEUTRAL_700 = "#404945"
HEX_NEUTRAL_800 = "#28332D"
HEX_NEUTRAL_900 = "#1C2722"
HEX_NEUTRAL_1000 = "#101C16"


# =============================================================================
# EMPHASIS COLORS (Warnings, information, status)
# =============================================================================

RUBY_RED_100 = RGBColor(0xEB, 0x56, 0x55)
RUBY_RED_500 = RGBColor(0xC5, 0x0F, 0x1F)
YOLK_YELLOW_100 = RGBColor(0xFE, 0xA8, 0x00)
SAPPHIRE_BLUE_100 = RGBColor(0x55, 0xA5, 0xEB)
SAPPHIRE_BLUE_500 = RGBColor(0x0F, 0x49, 0xC5)


# =============================================================================
# BRAND FLEX COLORS (RESTRICTED USE)
# Only for: hero stripes over images, data visualization, illustrations
# NEVER for: text, UI elements, general backgrounds, icons, borders
# =============================================================================

RICH_RED_LIGHT = RGBColor(0xF7, 0xB9, 0xC0)
RICH_RED_MID = RGBColor(0xEA, 0x50, 0x62)
RICH_RED_DEEP = RGBColor(0x9E, 0x2A, 0x2F)

BRIGHT_YELLOW_LIGHT = RGBColor(0xFF, 0xD7, 0x7D)
BRIGHT_YELLOW_MID = RGBColor(0xFF, 0xBC, 0x27)
BRIGHT_YELLOW_DEEP = RGBColor(0xFF, 0xD7, 0x7D)

SKY_BLUE_LIGHT = RGBColor(0xBC, 0xED, 0xFF)
SKY_BLUE_MID = RGBColor(0x57, 0xD1, 0xFF)
SKY_BLUE_DEEP = RGBColor(0x00, 0x76, 0x81)

VIBRANT_PURPLE_LIGHT = RGBColor(0xC6, 0xC2, 0xFF)
VIBRANT_PURPLE_MID = RGBColor(0x71, 0x66, 0xFF)
VIBRANT_PURPLE_DEEP = RGBColor(0x39, 0x33, 0x80)

MIDNIGHT_BLUE_LIGHT = RGBColor(0x99, 0xAD, 0xC2)
MIDNIGHT_BLUE_MID = RGBColor(0x00, 0x32, 0x66)
MIDNIGHT_BLUE_DEEP = RGBColor(0x00, 0x1A, 0x33)

# Hex flex colors for charts
HEX_SKY_BLUE_MID = "#57D1FF"
HEX_RICH_RED_MID = "#EA5062"
HEX_BRIGHT_YELLOW_MID = "#FFBC27"
HEX_VIBRANT_PURPLE_MID = "#7166FF"
HEX_MIDNIGHT_BLUE_MID = "#003266"


# =============================================================================
# CHART COLOR SEQUENCES (ordered for data series)
# =============================================================================

# For single series - use Leaf Green only
CHART_COLORS_1 = [HEX_CARGILL_LEAF_GREEN]

# For 2 series
CHART_COLORS_2 = [HEX_CARGILL_LEAF_GREEN, HEX_NEUTRAL_500]

# For 3 series - green palette
CHART_COLORS_3 = [HEX_CARGILL_LEAF_GREEN, HEX_SOFT_GREEN, HEX_DEEP_GREEN]

# For 4 series - green palette + justified flex color
CHART_COLORS_4 = [HEX_CARGILL_LEAF_GREEN, HEX_SOFT_GREEN, HEX_DEEP_GREEN, HEX_SKY_BLUE_MID]

# For 5+ series
CHART_COLORS_5_PLUS = [
    HEX_CARGILL_LEAF_GREEN, HEX_SOFT_GREEN, HEX_DEEP_GREEN,
    HEX_SKY_BLUE_MID, HEX_NEUTRAL_700,
]

CHART_COLORS_PPTX_1 = [CARGILL_LEAF_GREEN]
CHART_COLORS_PPTX_2 = [CARGILL_LEAF_GREEN, NEUTRAL_500]
CHART_COLORS_PPTX_3 = [CARGILL_LEAF_GREEN, SOFT_GREEN, DEEP_GREEN]
CHART_COLORS_PPTX_4 = [CARGILL_LEAF_GREEN, SOFT_GREEN, DEEP_GREEN, SKY_BLUE_MID]


def get_chart_colors(series_count: int) -> list[str]:
    """Return appropriate chart color palette for the number of data series."""
    if series_count <= 1:
        return CHART_COLORS_1
    elif series_count == 2:
        return CHART_COLORS_2
    elif series_count == 3:
        return CHART_COLORS_3
    elif series_count == 4:
        return CHART_COLORS_4
    else:
        return CHART_COLORS_5_PLUS


def get_chart_colors_pptx(series_count: int) -> list[RGBColor]:
    """Return chart colors as RGBColor objects for python-pptx."""
    if series_count <= 1:
        return CHART_COLORS_PPTX_1
    elif series_count == 2:
        return CHART_COLORS_PPTX_2
    elif series_count == 3:
        return CHART_COLORS_PPTX_3
    else:
        return CHART_COLORS_PPTX_4


# =============================================================================
# APPROVED COLOR SET (for QA validation)
# =============================================================================

APPROVED_COLORS = {
    WHITE, WHITE_GREEN, SOFT_GREEN, GREEN_300, CARGILL_LEAF_GREEN,
    GREEN_700, DEEP_GREEN, GREEN_900, BLACK,
    NEUTRAL_100, NEUTRAL_200, NEUTRAL_300, NEUTRAL_400, NEUTRAL_500,
    NEUTRAL_600, NEUTRAL_700, NEUTRAL_800, NEUTRAL_900, NEUTRAL_1000,
    RUBY_RED_100, RUBY_RED_500, YOLK_YELLOW_100,
    SAPPHIRE_BLUE_100, SAPPHIRE_BLUE_500,
    RICH_RED_LIGHT, RICH_RED_MID, RICH_RED_DEEP,
    BRIGHT_YELLOW_LIGHT, BRIGHT_YELLOW_MID, BRIGHT_YELLOW_DEEP,
    SKY_BLUE_LIGHT, SKY_BLUE_MID, SKY_BLUE_DEEP,
    VIBRANT_PURPLE_LIGHT, VIBRANT_PURPLE_MID, VIBRANT_PURPLE_DEEP,
    MIDNIGHT_BLUE_LIGHT, MIDNIGHT_BLUE_MID, MIDNIGHT_BLUE_DEEP,
}


# =============================================================================
# TYPOGRAPHY
# =============================================================================

# Font families (only two permitted)
HEADING_FONT = "Big Caslon for Cargill"
BODY_FONT = "Helvetica Now for Cargill"

# Fallback fonts (when brand fonts not installed)
HEADING_FONT_FALLBACK = "Georgia"
BODY_FONT_FALLBACK = "Arial"

# Heading sizes (Big Caslon) - Desktop
HEADING_LG = Pt(72)        # Top hero headline (max 1x per presentation)
HEADING_MD = Pt(56)         # Hero, section titles
HEADING_SM = Pt(40)         # Card titles, sections

# Heading line heights - Desktop
HEADING_LG_LINE = Pt(80)
HEADING_MD_LINE = Pt(62)
HEADING_SM_LINE = Pt(48)

# Subheading sizes (Helvetica Now Bold) - Desktop
SUBHEADING_LG = Pt(32)     # Section titles
SUBHEADING_MD = Pt(24)     # Card titles
SUBHEADING_SM = Pt(20)     # Eyebrow text

# Subheading line heights
SUBHEADING_LG_LINE = Pt(42)
SUBHEADING_MD_LINE = Pt(32)
SUBHEADING_SM_LINE = Pt(26)

# Body sizes (Helvetica Now Regular) - Desktop
BODY_BASE = Pt(16)          # Body copy
BODY_SM = Pt(12)            # Captions
BODY_XS = Pt(10)            # Legal text

# Body line heights
BODY_BASE_LINE = Pt(24)
BODY_SM_LINE = Pt(18)
BODY_XS_LINE = Pt(14)

# Stat number size
STAT_NUMBER_SIZE = Pt(32)
STAT_LABEL_SIZE = Pt(16)


# =============================================================================
# SLIDE DIMENSIONS (16:9 Widescreen)
# =============================================================================

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)

# Also support standard 10x5.625 sizing
SLIDE_WIDTH_STANDARD = Inches(10)
SLIDE_HEIGHT_STANDARD = Inches(5.625)


# =============================================================================
# SPACING SCALE
# =============================================================================

# Padding (external spacing between elements)
PADDING_XS = Inches(0.028)     # 2px
PADDING_SM = Inches(0.056)     # 4px
PADDING_BASE = Inches(0.111)   # 8px
PADDING_LG = Inches(0.222)     # 16px
PADDING_XL = Inches(0.333)     # 24px

# Spacing (internal element spacing)
SPACING_SM = Inches(0.056)     # 4px
SPACING_BASE = Inches(0.111)   # 8px
SPACING_MD = Inches(0.167)     # 12px
SPACING_LG = Inches(0.222)     # 16px
SPACING_XL = Inches(0.333)     # 24px
SPACING_2XL = Inches(0.444)    # 32px
SPACING_3XL = Inches(0.556)    # 40px
SPACING_4XL = Inches(0.667)    # 48px
SPACING_5XL = Inches(0.778)    # 56px
SPACING_6XL = Inches(1.111)    # 80px

# Margins
MARGIN_LEFT = Inches(0.75)
MARGIN_RIGHT = Inches(0.75)
MARGIN_TOP = Inches(1.0)
MARGIN_BOTTOM = Inches(0.75)
CONTENT_WIDTH = Inches(11.833)  # SLIDE_WIDTH - margins


# =============================================================================
# CORNER RADIUS (in EMUs for python-pptx)
# =============================================================================

CORNER_RADIUS_BASE = Emu(101600)    # 8px
CORNER_RADIUS_MD = Emu(203200)      # 16px
CORNER_RADIUS_LG = Emu(304800)      # 24px


# =============================================================================
# LOGO
# =============================================================================

LOGO_WIDTH = Inches(1.5)
LOGO_HEIGHT = Inches(0.5)
LOGO_MARGIN = Inches(0.222)  # 16px from edges

# Logo positions
LOGO_TOP_RIGHT_X = Inches(11.5)
LOGO_TOP_RIGHT_Y = Inches(0.3)

# Footer
FOOTER_TEXT = "Confidential - Cargill, Incorporated"
FOOTER_FONT_SIZE = BODY_XS
FOOTER_COLOR = NEUTRAL_500

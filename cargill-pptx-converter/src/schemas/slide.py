"""
Slide specification schemas for presentation architecture.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SlideLayout(str, Enum):
    """Available slide layout types mapped to Cargill template library."""
    # Hero slides
    TITLE_HERO = "title_hero"                    # Full-height hero with image
    BASIC_HERO = "basic_hero"                    # Image background + text overlay
    SECTION_HEADER = "section_header"            # Section divider

    # Statistics slides
    SIMPLE_STATISTICS = "simple_statistics"      # Clean horizontal row of numbers
    STATISTIC_CARDS = "statistic_cards"          # Stats in cards with icons
    STATS_WITH_HEADLINE = "stats_with_headline"  # Stats preceded by headline

    # Content slides
    CONTENT = "content"                          # Title + body text
    CONTENT_LEFT_HEADLINE = "content_left"       # Left-aligned headline
    CONTENT_CENTERED = "content_centered"        # Centered headline
    TWO_COLUMN = "two_column"                    # Side-by-side content
    THREE_COLUMN_CARDS = "three_column_cards"    # Three equal cards
    BULLET_LIST = "bullet_list"                  # Title + bullets
    TABLE = "table"                              # Title + table
    CHART = "chart"                              # Title + chart
    IMAGE_WITH_TEXT = "image_with_text"           # Image + caption/text
    IMAGE_FULL = "image_full"                    # Full-bleed image

    # Closing
    CLOSING = "closing"                          # Closing/thank you slide
    BLANK = "blank"                              # Blank slide


class SlideElement(BaseModel):
    """An individual element on a slide."""
    element_type: str  # "title", "subtitle", "body", "bullet", "table", "chart", "image", "stat", "logo", "footer"
    content: Optional[str] = None
    items: list[str] = Field(default_factory=list)
    table_data: Optional[list[list[str]]] = None
    table_headers: Optional[list[str]] = None
    chart_spec: Optional[dict] = None
    image_data: Optional[bytes] = None
    image_path: Optional[str] = None
    position: Optional[str] = None  # "left", "right", "full", "center", "top", "bottom"
    stat_value: Optional[str] = None
    stat_label: Optional[str] = None
    metadata: dict = Field(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True


class SlideColorScheme(BaseModel):
    """Color scheme for a slide."""
    background: str = "#FFFFFF"
    primary: str = "#00843D"
    headline: str = "#00843D"
    subheading: str = "#012912"
    body_text: str = "#101C16"
    accent: Optional[str] = None
    card_background: str = "#FFFFFF"
    card_border: str = "#DBDDDC"


class SlideTypography(BaseModel):
    """Typography specification for a slide."""
    headline_font: str = "Big Caslon for Cargill"
    headline_size: int = 40  # in points
    headline_bold: bool = False
    body_font: str = "Helvetica Now for Cargill"
    body_size: int = 16
    body_bold: bool = False
    stat_font: str = "Helvetica Now for Cargill"
    stat_size: int = 32
    stat_bold: bool = True


class SlideSpacing(BaseModel):
    """Spacing specification for a slide."""
    content_padding: float = 0.667  # inches (48px)
    headline_margin_bottom: float = 0.333  # inches (24px)
    element_gap: float = 0.222  # inches (16px)
    card_gap: float = 0.222  # inches (16px)
    card_padding: float = 0.333  # inches (24px)


class SlideSpec(BaseModel):
    """Complete specification for a single slide."""
    slide_id: str
    slide_number: int
    layout: SlideLayout
    elements: list[SlideElement]
    color_scheme: SlideColorScheme = Field(default_factory=SlideColorScheme)
    typography: SlideTypography = Field(default_factory=SlideTypography)
    spacing: SlideSpacing = Field(default_factory=SlideSpacing)
    speaker_notes: Optional[str] = None
    personality_emphasis: list[str] = Field(default_factory=list)
    template_category: str = "content"  # "hero", "statistics", "content", "closing"
    graphical_device: Optional[str] = None  # "leaf_with_stripe", "leaf_in_container"

    class Config:
        arbitrary_types_allowed = True


class PresentationPlan(BaseModel):
    """Complete presentation plan with all slides."""
    total_slides: int
    presentation_flow: str = "informational"  # "achievement_report", "problem_solution", "informational"
    slides: list[SlideSpec]
    design_notes: list[str] = Field(default_factory=list)

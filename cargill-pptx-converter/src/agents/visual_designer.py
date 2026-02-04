"""
Agent 4: Visual Design Agent

Applies Cargill visual identity elements to slides following the architecture plan.
Assigns color schemes, typography, spacing, and graphical devices.
"""

from src.agents.base import BaseAgent
from src.brand.constants import (
    HEX_CARGILL_LEAF_GREEN,
    HEX_DEEP_GREEN,
    HEX_NEUTRAL_1000,
    HEX_NEUTRAL_300,
    HEX_NEUTRAL_700,
    HEX_WHITE,
    HEX_WHITE_GREEN,
)
from src.schemas.slide import (
    SlideColorScheme,
    SlideLayout,
    SlideSpacing,
    SlideTypography,
)
from src.schemas.run_state import RunState


class VisualDesignerAgent(BaseAgent):
    """Apply Cargill visual identity to all slides."""

    def __init__(self):
        super().__init__("S4", "Visual Design")

    def execute(self, state: RunState) -> RunState:
        state.current_step = self.agent_id
        self.logger.info("Applying visual design to slides")

        if not state.presentation_plan:
            self._add_flag(state, "CRITICAL", "No presentation plan for visual design")
            return state

        for slide in state.presentation_plan.slides:
            # Apply color scheme
            slide.color_scheme = self._select_color_scheme(slide)

            # Apply typography
            slide.typography = self._select_typography(slide)

            # Apply spacing
            slide.spacing = self._select_spacing(slide)

            # Apply graphical device
            if slide.template_category == "hero" and slide.slide_number == 1:
                slide.graphical_device = "leaf_with_stripe"
            elif slide.layout == SlideLayout.CLOSING:
                slide.graphical_device = "leaf_in_container"

        self.logger.info(f"Applied visual design to {len(state.presentation_plan.slides)} slides")
        return state

    def _select_color_scheme(self, slide) -> SlideColorScheme:
        """Select color palette for a slide based on its type."""
        if slide.template_category == "hero":
            if slide.slide_number == 1:
                return SlideColorScheme(
                    background=HEX_CARGILL_LEAF_GREEN,
                    primary=HEX_CARGILL_LEAF_GREEN,
                    headline=HEX_WHITE,
                    subheading=HEX_WHITE,
                    body_text=HEX_WHITE,
                    accent="#57D1FF",  # Sky blue flex for hero stripe
                    card_background=HEX_WHITE,
                )
            else:
                return SlideColorScheme(
                    background=HEX_DEEP_GREEN,
                    primary=HEX_CARGILL_LEAF_GREEN,
                    headline=HEX_WHITE,
                    subheading=HEX_WHITE,
                    body_text=HEX_WHITE,
                )

        elif slide.template_category == "statistics":
            return SlideColorScheme(
                background=HEX_WHITE_GREEN,
                primary=HEX_CARGILL_LEAF_GREEN,
                headline=HEX_CARGILL_LEAF_GREEN,
                subheading=HEX_CARGILL_LEAF_GREEN,
                body_text=HEX_NEUTRAL_700,
                card_background=HEX_WHITE,
                card_border="none",
            )

        elif slide.template_category == "closing":
            return SlideColorScheme(
                background=HEX_CARGILL_LEAF_GREEN,
                primary=HEX_WHITE,
                headline=HEX_WHITE,
                subheading=HEX_WHITE,
                body_text=HEX_WHITE,
            )

        else:  # content
            return SlideColorScheme(
                background=HEX_WHITE,
                primary=HEX_CARGILL_LEAF_GREEN,
                headline=HEX_CARGILL_LEAF_GREEN,
                subheading=HEX_DEEP_GREEN,
                body_text=HEX_NEUTRAL_1000,
                card_background=HEX_WHITE,
                card_border=HEX_NEUTRAL_300,
            )

    def _select_typography(self, slide) -> SlideTypography:
        """Select typography for a slide."""
        if slide.template_category == "hero":
            if slide.slide_number == 1:
                return SlideTypography(
                    headline_font="Big Caslon for Cargill",
                    headline_size=56,  # heading-md for hero
                    body_font="Helvetica Now for Cargill",
                    body_size=16,
                )
            else:
                return SlideTypography(
                    headline_font="Big Caslon for Cargill",
                    headline_size=40,  # heading-sm for section headers
                    body_font="Helvetica Now for Cargill",
                    body_size=16,
                )

        elif slide.template_category == "statistics":
            return SlideTypography(
                headline_font="Big Caslon for Cargill",
                headline_size=40,
                body_font="Helvetica Now for Cargill",
                body_size=16,
                stat_font="Helvetica Now for Cargill",
                stat_size=32,
                stat_bold=True,
            )

        elif slide.template_category == "closing":
            return SlideTypography(
                headline_font="Big Caslon for Cargill",
                headline_size=56,
                body_font="Helvetica Now for Cargill",
                body_size=20,
            )

        elif slide.layout == SlideLayout.TABLE:
            return SlideTypography(
                headline_font="Big Caslon for Cargill",
                headline_size=32,
                body_font="Helvetica Now for Cargill",
                body_size=12,  # Smaller for table content
            )

        else:
            return SlideTypography(
                headline_font="Big Caslon for Cargill",
                headline_size=32,  # subheading-lg equivalent
                body_font="Helvetica Now for Cargill",
                body_size=16,
            )

    def _select_spacing(self, slide) -> SlideSpacing:
        """Select spacing for a slide."""
        if slide.template_category == "hero":
            return SlideSpacing(
                content_padding=1.111,  # 80px / spacing-6xl
                headline_margin_bottom=0.222,  # 16px
                element_gap=0.333,  # 24px
            )

        elif slide.template_category == "statistics":
            return SlideSpacing(
                content_padding=0.667,  # 48px / spacing-4xl
                headline_margin_bottom=0.444,  # 32px
                element_gap=0.222,  # 16px
                card_gap=0.222,  # 16px
                card_padding=0.333,  # 24px
            )

        elif slide.template_category == "closing":
            return SlideSpacing(
                content_padding=1.111,  # 80px
                headline_margin_bottom=0.333,  # 24px
            )

        else:
            return SlideSpacing(
                content_padding=0.556,  # 40px / spacing-3xl
                headline_margin_bottom=0.333,  # 24px
                element_gap=0.167,  # 12px
                card_gap=0.222,  # 16px
                card_padding=0.222,  # 16px
            )

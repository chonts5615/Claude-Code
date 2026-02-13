"""
Agent 3: Slide Architecture Agent

Designs optimal slide structure, sequence, and layout selection based on
content characteristics and brand guidelines.
"""

import math
from uuid import uuid4

from src.agents.base import BaseAgent
from src.schemas.content import ContentType, ExtractedContent
from src.schemas.slide import (
    PresentationPlan,
    SlideElement,
    SlideLayout,
    SlideSpec,
)
from src.schemas.run_state import RunState


class SlideArchitectAgent(BaseAgent):
    """Design the slide structure and map content to templates."""

    def __init__(self):
        super().__init__("S3", "Slide Architecture")

    def execute(self, state: RunState) -> RunState:
        state.current_step = self.agent_id
        self.logger.info("Designing slide architecture")

        if not state.extracted_content:
            self._add_flag(state, "CRITICAL", "No extracted content for slide architecture")
            return state

        content = state.extracted_content
        config = state.config

        # Analyze content characteristics
        characteristics = self._analyze_content(content)

        # Determine presentation flow
        flow = self._determine_flow(characteristics)

        # Map content to slides
        slides = self._map_content_to_slides(content, flow, config)

        # Optimize slide sequence
        slides = self._optimize_sequence(slides)

        # Ensure we have at least a title and closing
        slides = self._ensure_bookends(slides, content)

        plan = PresentationPlan(
            total_slides=len(slides),
            presentation_flow=flow,
            slides=slides,
            design_notes=self._generate_design_notes(slides, characteristics),
        )

        state.presentation_plan = plan
        self.logger.info(f"Designed {len(slides)} slides with '{flow}' flow")

        return state

    def _analyze_content(self, content: ExtractedContent) -> dict:
        """Analyze content to determine presentation needs."""
        headings = content.get_headings()
        tables = content.get_tables()
        images = content.get_images()
        stats = content.get_statistics()

        return {
            "word_count": content.get_word_count(),
            "section_count": len(content.sections),
            "heading_count": len(headings),
            "table_count": len(tables),
            "image_count": len(images),
            "stat_count": len(stats),
            "has_data": len(tables) + len(stats) > 0,
            "has_visuals": len(images) > 0,
            "data_density": (len(tables) + len(stats)) / max(len(content.sections), 1),
            "narrative_type": self._detect_narrative_type(content),
        }

    def _detect_narrative_type(self, content: ExtractedContent) -> str:
        """Detect the narrative structure of the content."""
        all_text = content.get_all_text().lower()

        problem_words = ["problem", "challenge", "issue", "concern", "risk"]
        solution_words = ["solution", "approach", "strategy", "recommendation", "plan"]
        achievement_words = ["achieved", "exceeded", "record", "growth", "results"]
        forward_words = ["will", "plan", "future", "upcoming", "next"]

        problem_count = sum(1 for w in problem_words if w in all_text)
        solution_count = sum(1 for w in solution_words if w in all_text)
        achievement_count = sum(1 for w in achievement_words if w in all_text)

        if problem_count >= 2 and solution_count >= 2:
            return "problem_solution"
        elif achievement_count >= 2:
            return "achievement_report"
        else:
            return "informational"

    def _determine_flow(self, characteristics: dict) -> str:
        """Determine optimal presentation flow based on content characteristics."""
        return characteristics["narrative_type"]

    def _map_content_to_slides(
        self,
        content: ExtractedContent,
        flow: str,
        config,
    ) -> list[SlideSpec]:
        """Map content blocks to slide specifications."""
        slides: list[SlideSpec] = []
        slide_num = 0

        for section in content.sections:
            section_blocks = [content.get_block(bid) for bid in section.blocks]
            section_blocks = [b for b in section_blocks if b is not None]

            for block in section_blocks:
                if block.content_type == ContentType.HEADING:
                    if block.level == 1:
                        # Title or section header
                        if slide_num == 0:
                            slide_num += 1
                            slides.append(self._create_title_slide(block, slide_num))
                        else:
                            slide_num += 1
                            slides.append(self._create_section_header(block, slide_num))

                    elif block.level == 2:
                        slide_num += 1
                        slides.append(self._create_section_header(block, slide_num))

                elif block.content_type == ContentType.PARAGRAPH:
                    if block.text and len(block.text.split()) > config.max_words_per_slide:
                        # Split long paragraphs across multiple slides
                        chunks = self._split_text(block.text, config.max_words_per_slide)
                        for i, chunk in enumerate(chunks):
                            slide_num += 1
                            slides.append(self._create_content_slide(
                                chunk, slide_num,
                                title=section.title if i == 0 else f"{section.title} (cont.)" if section.title else None,
                            ))
                    elif block.text:
                        slide_num += 1
                        slides.append(self._create_content_slide(
                            block.text, slide_num, title=section.title,
                        ))

                elif block.content_type in (ContentType.BULLET_LIST, ContentType.NUMBERED_LIST):
                    items = block.items
                    if len(items) > config.max_bullets_per_slide:
                        # Split across slides
                        for i in range(0, len(items), config.max_bullets_per_slide):
                            chunk = items[i:i + config.max_bullets_per_slide]
                            slide_num += 1
                            suffix = f" (cont.)" if i > 0 else ""
                            slides.append(self._create_bullet_slide(
                                chunk, slide_num,
                                title=(section.title or "") + suffix,
                            ))
                    else:
                        slide_num += 1
                        slides.append(self._create_bullet_slide(
                            items, slide_num, title=section.title,
                        ))

                elif block.content_type == ContentType.TABLE:
                    slide_num += 1
                    slides.append(self._create_table_slide(block, slide_num, section.title))

                elif block.content_type == ContentType.CHART_DATA:
                    slide_num += 1
                    slides.append(self._create_chart_slide(block, slide_num, section.title))

                elif block.content_type == ContentType.STATISTIC:
                    # Collect consecutive statistics
                    pass  # Handled in batch below

                elif block.content_type == ContentType.IMAGE:
                    slide_num += 1
                    slides.append(self._create_image_slide(block, slide_num, section.title))

                elif block.content_type == ContentType.BLOCKQUOTE:
                    slide_num += 1
                    slides.append(self._create_quote_slide(block, slide_num))

            # Handle statistics in batch per section
            section_stats = [
                content.get_block(bid) for bid in section.blocks
                if content.get_block(bid) and content.get_block(bid).content_type == ContentType.STATISTIC
            ]
            if section_stats:
                slide_num += 1
                slides.append(self._create_stats_slide(section_stats, slide_num, section.title))

        return slides

    def _create_title_slide(self, block, num: int) -> SlideSpec:
        """Create a title/hero slide."""
        return SlideSpec(
            slide_id=f"slide_{uuid4().hex[:6]}",
            slide_number=num,
            layout=SlideLayout.TITLE_HERO,
            template_category="hero",
            elements=[
                SlideElement(element_type="title", content=block.text),
            ],
            personality_emphasis=["optimistic", "courageous"],
        )

    def _create_section_header(self, block, num: int) -> SlideSpec:
        """Create a section header slide."""
        return SlideSpec(
            slide_id=f"slide_{uuid4().hex[:6]}",
            slide_number=num,
            layout=SlideLayout.SECTION_HEADER,
            template_category="hero",
            elements=[
                SlideElement(element_type="title", content=block.text),
            ],
            personality_emphasis=["courageous"],
        )

    def _create_content_slide(self, text: str, num: int, title: str = None) -> SlideSpec:
        """Create a content slide with body text."""
        elements = []
        if title:
            elements.append(SlideElement(element_type="title", content=title))
        elements.append(SlideElement(element_type="body", content=text))

        return SlideSpec(
            slide_id=f"slide_{uuid4().hex[:6]}",
            slide_number=num,
            layout=SlideLayout.CONTENT,
            template_category="content",
            elements=elements,
        )

    def _create_bullet_slide(self, items: list[str], num: int, title: str = None) -> SlideSpec:
        """Create a bullet list slide."""
        elements = []
        if title:
            elements.append(SlideElement(element_type="title", content=title))
        elements.append(SlideElement(element_type="bullet", items=items))

        return SlideSpec(
            slide_id=f"slide_{uuid4().hex[:6]}",
            slide_number=num,
            layout=SlideLayout.BULLET_LIST,
            template_category="content",
            elements=elements,
        )

    def _create_table_slide(self, block, num: int, title: str = None) -> SlideSpec:
        """Create a table slide."""
        elements = []
        if title:
            elements.append(SlideElement(element_type="title", content=title))
        elements.append(SlideElement(
            element_type="table",
            table_data=block.table_data,
            table_headers=block.table_headers,
        ))

        return SlideSpec(
            slide_id=f"slide_{uuid4().hex[:6]}",
            slide_number=num,
            layout=SlideLayout.TABLE,
            template_category="content",
            elements=elements,
        )

    def _create_chart_slide(self, block, num: int, title: str = None) -> SlideSpec:
        """Create a chart slide."""
        elements = []
        chart_title = title or "Data Overview"
        elements.append(SlideElement(element_type="title", content=chart_title))
        elements.append(SlideElement(
            element_type="chart",
            chart_spec=block.chart_data,
            metadata=block.metadata,
        ))

        return SlideSpec(
            slide_id=f"slide_{uuid4().hex[:6]}",
            slide_number=num,
            layout=SlideLayout.CHART,
            template_category="content",
            elements=elements,
        )

    def _create_stats_slide(self, stat_blocks: list, num: int, title: str = None) -> SlideSpec:
        """Create a statistics slide."""
        elements = []
        if title:
            elements.append(SlideElement(element_type="title", content=title))

        for stat in stat_blocks[:4]:  # Max 4 stats per slide
            elements.append(SlideElement(
                element_type="stat",
                stat_value=stat.text,
                stat_label=stat.metadata.get("label", ""),
            ))

        layout = SlideLayout.STATISTIC_CARDS if len(stat_blocks) >= 3 else SlideLayout.SIMPLE_STATISTICS
        return SlideSpec(
            slide_id=f"slide_{uuid4().hex[:6]}",
            slide_number=num,
            layout=layout,
            template_category="statistics",
            elements=elements,
            personality_emphasis=["courageous", "optimistic"],
        )

    def _create_image_slide(self, block, num: int, title: str = None) -> SlideSpec:
        """Create an image slide."""
        elements = []
        if title:
            elements.append(SlideElement(element_type="title", content=title))
        elements.append(SlideElement(
            element_type="image",
            image_data=block.image_data,
            image_path=block.image_path,
            metadata={"format": block.image_format},
        ))

        return SlideSpec(
            slide_id=f"slide_{uuid4().hex[:6]}",
            slide_number=num,
            layout=SlideLayout.IMAGE_WITH_TEXT,
            template_category="content",
            elements=elements,
        )

    def _create_quote_slide(self, block, num: int) -> SlideSpec:
        """Create a blockquote/centered text slide."""
        return SlideSpec(
            slide_id=f"slide_{uuid4().hex[:6]}",
            slide_number=num,
            layout=SlideLayout.CONTENT_CENTERED,
            template_category="content",
            elements=[
                SlideElement(element_type="body", content=block.text, position="center"),
            ],
            personality_emphasis=["compassionate", "humble"],
        )

    def _split_text(self, text: str, max_words: int) -> list[str]:
        """Split text into chunks respecting sentence boundaries."""
        sentences = text.replace(". ", ".\n").split("\n")
        chunks = []
        current_chunk = []
        current_words = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            word_count = len(sentence.split())
            if current_words + word_count > max_words and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [sentence]
                current_words = word_count
            else:
                current_chunk.append(sentence)
                current_words += word_count

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def _ensure_bookends(self, slides: list[SlideSpec], content: ExtractedContent) -> list[SlideSpec]:
        """Ensure the presentation has title and closing slides."""
        if not slides:
            # Create minimal presentation
            title = content.metadata.title or "Presentation"
            slides = [
                SlideSpec(
                    slide_id=f"slide_{uuid4().hex[:6]}",
                    slide_number=1,
                    layout=SlideLayout.TITLE_HERO,
                    template_category="hero",
                    elements=[SlideElement(element_type="title", content=title)],
                    personality_emphasis=["optimistic"],
                ),
            ]

        # Ensure first slide is a hero/title
        if slides[0].layout not in (SlideLayout.TITLE_HERO, SlideLayout.BASIC_HERO):
            title = content.metadata.title or "Presentation"
            slides.insert(0, SlideSpec(
                slide_id=f"slide_{uuid4().hex[:6]}",
                slide_number=0,
                layout=SlideLayout.TITLE_HERO,
                template_category="hero",
                elements=[SlideElement(element_type="title", content=title)],
                personality_emphasis=["optimistic", "courageous"],
            ))

        # Add closing slide
        slides.append(SlideSpec(
            slide_id=f"slide_{uuid4().hex[:6]}",
            slide_number=len(slides) + 1,
            layout=SlideLayout.CLOSING,
            template_category="closing",
            elements=[
                SlideElement(element_type="title", content="Thank You"),
                SlideElement(element_type="body", content="Together, creating a more food secure world"),
            ],
            personality_emphasis=["humble", "compassionate", "optimistic"],
        ))

        return slides

    def _optimize_sequence(self, slides: list[SlideSpec]) -> list[SlideSpec]:
        """Optimize slide sequence and re-number."""
        # Remove consecutive section headers
        optimized = []
        for i, slide in enumerate(slides):
            if (
                slide.layout == SlideLayout.SECTION_HEADER
                and i + 1 < len(slides)
                and slides[i + 1].layout == SlideLayout.SECTION_HEADER
            ):
                continue
            optimized.append(slide)

        # Re-number
        for i, slide in enumerate(optimized):
            slide.slide_number = i + 1

        return optimized

    def _generate_design_notes(self, slides: list[SlideSpec], characteristics: dict) -> list[str]:
        """Generate design notes for the presentation."""
        notes = []
        notes.append(f"Presentation flow: {characteristics['narrative_type']}")
        notes.append(f"Total slides: {len(slides)}")

        categories = {}
        for slide in slides:
            cat = slide.template_category
            categories[cat] = categories.get(cat, 0) + 1

        for cat, count in categories.items():
            notes.append(f"{cat.title()} slides: {count}")

        if characteristics["has_data"]:
            notes.append("Data visualization opportunities identified")
        if characteristics["has_visuals"]:
            notes.append("Extracted images will be incorporated")

        return notes

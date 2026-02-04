"""
Chart specification schemas for data visualization.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ChartType(str, Enum):
    """Supported chart types."""
    BAR = "bar"
    COLUMN = "column"
    HORIZONTAL_BAR = "horizontal_bar"
    LINE = "line"
    PIE = "pie"
    DONUT = "donut"
    STACKED_BAR = "stacked_bar"
    AREA = "area"


class DataSeries(BaseModel):
    """A single data series for a chart."""
    name: str
    values: list[float]
    color: Optional[str] = None  # Hex color override


class ChartSpec(BaseModel):
    """Complete specification for a chart."""
    chart_id: str
    chart_type: ChartType
    title: Optional[str] = None
    categories: list[str]
    series: list[DataSeries]
    show_legend: bool = True
    show_data_labels: bool = False
    show_grid_lines: bool = True
    value_axis_label: Optional[str] = None
    category_axis_label: Optional[str] = None
    width_inches: float = 8.0
    height_inches: float = 4.5
    metadata: dict = Field(default_factory=dict)

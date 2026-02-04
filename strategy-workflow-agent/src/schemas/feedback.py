"""Feedback loop and learning system schemas."""

from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field


class FeedbackType(str, Enum):
    """Types of feedback that can be collected."""
    USER_RATING = "user_rating"
    USER_COMMENT = "user_comment"
    QUALITY_METRIC = "quality_metric"
    OUTCOME_TRACKING = "outcome_tracking"
    EXECUTION_METRIC = "execution_metric"
    ERROR_REPORT = "error_report"
    CORRECTION = "correction"
    PREFERENCE = "preference"


class FeedbackSentiment(str, Enum):
    """Sentiment of feedback."""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class LearningCategory(str, Enum):
    """Categories of learnings."""
    PROCESS = "process"
    QUALITY = "quality"
    CONTENT = "content"
    TIMING = "timing"
    RESOURCE = "resource"
    RISK = "risk"
    STAKEHOLDER = "stakeholder"
    COMMUNICATION = "communication"


class OptimizationType(str, Enum):
    """Types of optimizations."""
    THRESHOLD_ADJUSTMENT = "threshold_adjustment"
    PROMPT_REFINEMENT = "prompt_refinement"
    WEIGHT_TUNING = "weight_tuning"
    PROCESS_IMPROVEMENT = "process_improvement"
    TEMPLATE_UPDATE = "template_update"
    RULE_ADDITION = "rule_addition"
    RULE_REMOVAL = "rule_removal"


class FeedbackEntry(BaseModel):
    """Individual feedback entry."""

    feedback_id: str = Field(..., description="Unique identifier")
    run_id: str = Field(..., description="Run that generated this feedback")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Classification
    feedback_type: FeedbackType = Field(...)
    category: LearningCategory = Field(...)
    sentiment: FeedbackSentiment = Field(FeedbackSentiment.NEUTRAL)

    # Context
    agent_id: Optional[str] = Field(None, description="Agent that produced the output")
    step_id: Optional[str] = Field(None, description="Workflow step")
    artifact_id: Optional[str] = Field(None, description="Related artifact")

    # Feedback content
    rating: Optional[float] = Field(None, ge=0.0, le=5.0, description="Numeric rating if applicable")
    comment: Optional[str] = Field(None, description="Text feedback")

    # Specific feedback
    original_output: Optional[str] = Field(None, description="What was produced")
    corrected_output: Optional[str] = Field(None, description="What it should have been")
    improvement_suggestion: Optional[str] = None

    # Metadata
    source: str = Field("user", description="user, system, outcome")
    confidence: float = Field(1.0, ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # Processing status
    processed: bool = Field(False)
    applied_to_learning: bool = Field(False)


class LearningInsight(BaseModel):
    """Insight derived from feedback analysis."""

    insight_id: str = Field(..., description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Classification
    category: LearningCategory = Field(...)
    importance: float = Field(0.5, ge=0.0, le=1.0, description="Importance score")

    # Insight content
    title: str = Field(..., description="Brief title")
    description: str = Field(..., description="Detailed description")
    evidence: List[str] = Field(default_factory=list, description="Supporting feedback IDs")
    sample_size: int = Field(1, ge=1)

    # Pattern details
    pattern_type: str = Field(..., description="Type of pattern identified")
    affected_agents: List[str] = Field(default_factory=list)
    affected_steps: List[str] = Field(default_factory=list)

    # Statistical support
    confidence: float = Field(0.5, ge=0.0, le=1.0)
    frequency: float = Field(0.0, ge=0.0, le=1.0, description="How often pattern occurs")
    impact: float = Field(0.0, ge=0.0, le=1.0, description="Impact when pattern occurs")

    # Actionability
    is_actionable: bool = Field(True)
    recommended_actions: List[str] = Field(default_factory=list)

    # Status
    status: str = Field("new", description="new, validated, applied, rejected")
    applied_optimizations: List[str] = Field(default_factory=list)


class OptimizationRecommendation(BaseModel):
    """Specific optimization recommendation derived from learning."""

    optimization_id: str = Field(..., description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Source
    insight_id: str = Field(..., description="Source insight ID")
    insight_ids: List[str] = Field(default_factory=list, description="All contributing insights")

    # Classification
    optimization_type: OptimizationType = Field(...)
    target_component: str = Field(..., description="What to optimize")
    category: LearningCategory = Field(...)

    # Recommendation details
    title: str = Field(..., description="Brief title")
    description: str = Field(..., description="What change to make")
    rationale: str = Field(..., description="Why this change")

    # Specific changes
    current_value: Optional[Any] = Field(None, description="Current configuration")
    recommended_value: Optional[Any] = Field(None, description="Recommended configuration")
    change_specification: Dict[str, Any] = Field(default_factory=dict)

    # Impact assessment
    expected_impact: float = Field(0.0, ge=0.0, le=1.0)
    confidence: float = Field(0.5, ge=0.0, le=1.0)
    risk_level: str = Field("low", description="low, medium, high")

    # Implementation
    implementation_steps: List[str] = Field(default_factory=list)
    rollback_steps: List[str] = Field(default_factory=list)

    # Status
    status: str = Field("proposed", description="proposed, approved, applied, rejected, reverted")
    applied_at: Optional[datetime] = None
    applied_by: Optional[str] = None
    effectiveness_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class PerformanceMetric(BaseModel):
    """Performance metric for tracking workflow effectiveness."""

    metric_id: str = Field(..., description="Unique identifier")
    metric_name: str = Field(..., description="Name of the metric")
    metric_type: str = Field(..., description="quality, speed, cost, satisfaction")

    # Measurement
    run_id: str = Field(..., description="Run this measurement is from")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    value: float = Field(...)
    unit: str = Field(...)

    # Context
    agent_id: Optional[str] = None
    step_id: Optional[str] = None

    # Comparison
    baseline_value: Optional[float] = None
    target_value: Optional[float] = None
    previous_value: Optional[float] = None

    # Trend
    trend_direction: Optional[str] = Field(None, description="improving, stable, declining")
    trend_percentage: Optional[float] = None

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FeedbackLoopState(BaseModel):
    """Complete state of the feedback loop system."""

    # Identification
    loop_id: str = Field(..., description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)

    # Feedback collection
    total_feedback_entries: int = Field(0)
    unprocessed_feedback: int = Field(0)
    feedback_by_type: Dict[str, int] = Field(default_factory=dict)
    feedback_by_sentiment: Dict[str, int] = Field(default_factory=dict)

    # Learning state
    total_insights: int = Field(0)
    active_insights: int = Field(0)
    insights_by_category: Dict[str, int] = Field(default_factory=dict)

    # Optimization state
    total_optimizations: int = Field(0)
    applied_optimizations: int = Field(0)
    pending_optimizations: int = Field(0)
    optimization_success_rate: float = Field(0.0, ge=0.0, le=1.0)

    # Performance tracking
    current_metrics: Dict[str, float] = Field(default_factory=dict)
    metric_trends: Dict[str, str] = Field(default_factory=dict)

    # Learning parameters (can be tuned)
    learning_rate: float = Field(0.1, ge=0.01, le=1.0)
    memory_decay: float = Field(0.95, ge=0.5, le=1.0)
    confidence_threshold: float = Field(0.7, ge=0.0, le=1.0)

    # Agent-specific learning
    agent_performance: Dict[str, Dict[str, float]] = Field(default_factory=dict)
    agent_optimizations: Dict[str, List[str]] = Field(default_factory=dict)

    # Recent activity
    recent_feedback_ids: List[str] = Field(default_factory=list)
    recent_insight_ids: List[str] = Field(default_factory=list)
    recent_optimization_ids: List[str] = Field(default_factory=list)


class FeedbackSummary(BaseModel):
    """Summary of feedback for a specific run."""

    run_id: str = Field(...)
    summary_generated_at: datetime = Field(default_factory=datetime.utcnow)

    # Counts
    total_feedback: int = Field(0)
    positive_feedback: int = Field(0)
    negative_feedback: int = Field(0)

    # Ratings
    average_rating: Optional[float] = None
    rating_count: int = Field(0)

    # Key themes
    positive_themes: List[str] = Field(default_factory=list)
    improvement_areas: List[str] = Field(default_factory=list)

    # Specific feedback
    corrections_made: int = Field(0)
    suggestions_received: int = Field(0)

    # Learning applied
    insights_generated: int = Field(0)
    optimizations_triggered: int = Field(0)


class LearningReport(BaseModel):
    """Periodic learning report summarizing system improvements."""

    report_id: str = Field(..., description="Unique identifier")
    report_period_start: datetime = Field(...)
    report_period_end: datetime = Field(...)
    generated_at: datetime = Field(default_factory=datetime.utcnow)

    # Summary statistics
    total_runs_analyzed: int = Field(0)
    total_feedback_processed: int = Field(0)
    total_insights_generated: int = Field(0)
    total_optimizations_applied: int = Field(0)

    # Performance changes
    quality_score_change: float = Field(0.0)
    speed_improvement: float = Field(0.0)
    user_satisfaction_change: float = Field(0.0)

    # Top learnings
    top_insights: List[str] = Field(default_factory=list)
    top_optimizations: List[str] = Field(default_factory=list)

    # Areas for improvement
    ongoing_issues: List[str] = Field(default_factory=list)
    recommended_focus_areas: List[str] = Field(default_factory=list)

    # Agent-specific performance
    best_performing_agents: List[str] = Field(default_factory=list)
    agents_needing_improvement: List[str] = Field(default_factory=list)

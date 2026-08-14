"""Append-only analytics events and pre-aggregated learning metrics."""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from sqlalchemy import CheckConstraint, Date, ForeignKey, Index, Integer, JSON, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, CreatedAtMixin, GUID, TimestampMixin, UUIDPrimaryKeyMixin


class AnalyticsEvent(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "analytics_events"
    __table_args__ = (
        Index("ix_analytics_events_user_occurred", "user_id", "occurred_at"),
        Index("ix_analytics_events_name_occurred", "event_name", "occurred_at"),
        Index("ix_analytics_events_subject_occurred", "subject_id", "occurred_at"),
    )

    user_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    subject_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True
    )
    event_name: Mapped[str] = mapped_column(String(80), nullable=False)
    entity_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    entity_id: Mapped[UUID | None] = mapped_column(GUID(), nullable=True)
    properties: Mapped[dict | list] = mapped_column(JSON, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(nullable=False)
    session_id: Mapped[UUID | None] = mapped_column(GUID(), nullable=True)


class DailyLearningMetric(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "daily_learning_metrics"
    __table_args__ = (
        Index(
            "uq_daily_learning_metrics_user_subject_date",
            "user_id",
            "subject_id",
            "metric_date",
            unique=True,
        ),
        Index("ix_daily_learning_metrics_user_date", "user_id", "metric_date"),
        CheckConstraint("study_seconds >= 0", name="study_seconds_nonnegative"),
        CheckConstraint("concepts_practiced >= 0", name="concepts_practiced_nonnegative"),
        CheckConstraint("concepts_mastered >= 0", name="concepts_mastered_nonnegative"),
        CheckConstraint("quiz_attempts >= 0", name="quiz_attempts_nonnegative"),
        CheckConstraint("correct_answers >= 0", name="correct_answers_nonnegative"),
        CheckConstraint("video_seconds_watched >= 0", name="video_watched_nonnegative"),
        CheckConstraint("video_seconds_skipped >= 0", name="video_skipped_nonnegative"),
        CheckConstraint("tutor_interactions >= 0", name="tutor_interactions_nonnegative"),
        CheckConstraint("time_saved_seconds >= 0", name="time_saved_nonnegative"),
    )

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    metric_date: Mapped[date] = mapped_column(Date, nullable=False)
    study_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    concepts_practiced: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    concepts_mastered: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    quiz_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    correct_answers: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    video_seconds_watched: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    video_seconds_skipped: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tutor_interactions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    time_saved_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    streak_day: Mapped[int | None] = mapped_column(Integer, nullable=True)


class ConceptAnalyticsSnapshot(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "concept_analytics_snapshots"
    __table_args__ = (
        Index(
            "uq_concept_analytics_user_concept_date",
            "user_id",
            "concept_id",
            "snapshot_date",
            unique=True,
        ),
        Index("ix_concept_analytics_user_concept_date", "user_id", "concept_id", "snapshot_date"),
        CheckConstraint(
            "mastery_score BETWEEN 0 AND 100", name="mastery_score_range"
        ),
        CheckConstraint(
            "confidence_score BETWEEN 0 AND 100", name="confidence_score_range"
        ),
        CheckConstraint("accuracy BETWEEN 0 AND 100", name="accuracy_range"),
        CheckConstraint("attempts >= 0", name="attempts_nonnegative"),
        CheckConstraint("study_seconds >= 0", name="study_seconds_nonnegative"),
        CheckConstraint("video_seconds >= 0", name="video_seconds_nonnegative"),
        CheckConstraint("revision_count >= 0", name="revision_count_nonnegative"),
    )

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    concept_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False
    )
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    mastery_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    accuracy: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    study_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    video_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    revision_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

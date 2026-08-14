"""Study sessions, video activity, notes, bookmarks, and revision schedules."""

from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, CreatedAtMixin, GUID, TimestampMixin, UUIDPrimaryKeyMixin
from ..enums import ACTIVITY_TYPES, VIDEO_EVENT_TYPES


def _values(values: tuple[str, ...]) -> str:
    return ", ".join(f"'{value}'" for value in values)


class StudySession(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "study_sessions"
    __table_args__ = (
        Index("ix_study_sessions_user_started", "user_id", "started_at"),
        CheckConstraint(
            f"activity_type IN ({_values(ACTIVITY_TYPES)})", name="activity_type_allowed"
        ),
        CheckConstraint("duration_seconds >= 0", name="duration_nonnegative"),
    )

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    started_at: Mapped[datetime] = mapped_column(nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(nullable=True)
    duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    activity_type: Mapped[str] = mapped_column(String(40), nullable=False)

    user: Mapped["User"] = relationship()
    subject: Mapped["Subject"] = relationship()
    video_events: Mapped[List["VideoWatchEvent"]] = relationship(
        back_populates="session"
    )


class VideoWatchEvent(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "video_watch_events"
    __table_args__ = (
        Index("ix_video_watch_events_user_occurred", "user_id", "occurred_at"),
        Index("ix_video_watch_events_video_position", "video_id", "position_seconds"),
        CheckConstraint(
            f"event_type IN ({_values(VIDEO_EVENT_TYPES)})", name="event_type_allowed"
        ),
        CheckConstraint("position_seconds >= 0", name="position_nonnegative"),
        CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds >= 0",
            name="duration_nonnegative",
        ),
    )

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    video_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False
    )
    segment_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("video_segments.id", ondelete="SET NULL"), nullable=True
    )
    event_type: Mapped[str] = mapped_column(String(30), nullable=False)
    position_seconds: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)
    duration_seconds: Mapped[float | None] = mapped_column(Numeric(12, 3), nullable=True)
    session_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("study_sessions.id", ondelete="SET NULL"), nullable=True
    )
    occurred_at: Mapped[datetime] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship()
    video: Mapped["Video"] = relationship()
    segment: Mapped["VideoSegment | None"] = relationship()
    session: Mapped["StudySession | None"] = relationship(back_populates="video_events")


class Bookmark(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "bookmarks"
    __table_args__ = (
        Index("ix_bookmarks_user_created", "user_id", "created_at"),
        CheckConstraint(
            "position_seconds IS NULL OR position_seconds >= 0",
            name="position_nonnegative",
        ),
    )

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    resource_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("resources.id", ondelete="CASCADE"), nullable=True
    )
    video_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("videos.id", ondelete="CASCADE"), nullable=True
    )
    segment_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("video_segments.id", ondelete="CASCADE"), nullable=True
    )
    position_seconds: Mapped[float | None] = mapped_column(Numeric(12, 3), nullable=True)
    title: Mapped[str | None] = mapped_column(String(200), nullable=True)

    user: Mapped["User"] = relationship()
    resource: Mapped["Resource | None"] = relationship()
    video: Mapped["Video | None"] = relationship()
    segment: Mapped["VideoSegment | None"] = relationship()


class Note(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "notes"
    __table_args__ = (
        Index("ix_notes_user_updated", "user_id", "updated_at"),
        CheckConstraint(
            "position_seconds IS NULL OR position_seconds >= 0",
            name="position_nonnegative",
        ),
    )

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    resource_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("resources.id", ondelete="CASCADE"), nullable=True
    )
    video_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("videos.id", ondelete="CASCADE"), nullable=True
    )
    segment_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("video_segments.id", ondelete="CASCADE"), nullable=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    position_seconds: Mapped[float | None] = mapped_column(Numeric(12, 3), nullable=True)

    user: Mapped["User"] = relationship()
    resource: Mapped["Resource | None"] = relationship()
    video: Mapped["Video | None"] = relationship()
    segment: Mapped["VideoSegment | None"] = relationship()


class RevisionSchedule(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "revision_schedule"
    __table_args__ = (
        Index("ix_revision_schedule_user_due", "user_id", "due_at"),
        CheckConstraint("interval_days >= 0", name="interval_days_nonnegative"),
        CheckConstraint("ease_factor > 0", name="ease_factor_positive"),
        CheckConstraint("repetition_count >= 0", name="repetition_count_nonnegative"),
    )

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    concept_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False
    )
    mastery_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("learner_concept_mastery.id", ondelete="CASCADE"), nullable=False
    )
    due_at: Mapped[datetime] = mapped_column(nullable=False)
    interval_days: Mapped[float] = mapped_column(Numeric(8, 2), nullable=False)
    ease_factor: Mapped[float] = mapped_column(Numeric(6, 3), nullable=False)
    repetition_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    last_result: Mapped[str | None] = mapped_column(String(30), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="scheduled")

    user: Mapped["User"] = relationship()
    concept: Mapped["Concept"] = relationship()
    mastery: Mapped["LearnerConceptMastery"] = relationship()

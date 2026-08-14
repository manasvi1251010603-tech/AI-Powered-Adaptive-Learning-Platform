"""Video assets, AI segments, and segment-concept mappings."""

from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, CreatedAtMixin, TimestampMixin, GUID, UUIDPrimaryKeyMixin
from ..enums import PROCESSING_STATUSES, REVIEW_STATUSES, VIDEO_SEGMENT_SOURCES


def _values(values: tuple[str, ...]) -> str:
    return ", ".join(f"'{value}'" for value in values)


class Video(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "videos"

    resource_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("resources.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    storage_key: Mapped[str] = mapped_column(Text, nullable=False)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    format: Mapped[str | None] = mapped_column(String(30), nullable=True)
    transcript_status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="pending"
    )
    segmentation_status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="pending"
    )
    processing_error: Mapped[str | None] = mapped_column(Text, nullable=True)

    resource: Mapped["Resource"] = relationship(back_populates="video")
    segments: Mapped[List["VideoSegment"]] = relationship(
        back_populates="video", cascade="all, delete-orphan", order_by="VideoSegment.start_seconds"
    )


class VideoSegment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "video_segments"
    __table_args__ = (
        Index("ix_video_segments_video_start", "video_id", "start_seconds"),
        CheckConstraint("end_seconds > start_seconds", name="end_after_start"),
        CheckConstraint(
            "ai_confidence IS NULL OR ai_confidence BETWEEN 0 AND 100",
            name="ai_confidence_range",
        ),
        CheckConstraint(
            f"source IN ({_values(VIDEO_SEGMENT_SOURCES)})", name="source_allowed"
        ),
        CheckConstraint(
            f"review_status IN ({_values(REVIEW_STATUSES)})",
            name="review_status_allowed",
        ),
    )

    video_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    start_seconds: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)
    end_seconds: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)
    transcript_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_confidence: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    source: Mapped[str] = mapped_column(String(30), nullable=False, default="ai")
    review_status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="pending"
    )
    reviewed_by_id: Mapped[UUID | None] = mapped_column(
        "reviewed_by", GUID(), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    video: Mapped["Video"] = relationship(back_populates="segments")
    reviewed_by: Mapped["User | None"] = relationship()
    concept_links: Mapped[List["VideoSegmentConcept"]] = relationship(
        back_populates="segment", cascade="all, delete-orphan"
    )


class VideoSegmentConcept(CreatedAtMixin, Base):
    __tablename__ = "video_segment_concepts"
    __table_args__ = (
        Index("ix_video_segment_concepts_concept_id", "concept_id"),
        CheckConstraint(
            "confidence IS NULL OR confidence BETWEEN 0 AND 100",
            name="confidence_range",
        ),
    )

    segment_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("video_segments.id", ondelete="CASCADE"), primary_key=True
    )
    concept_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("concepts.id", ondelete="CASCADE"), primary_key=True
    )
    confidence: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    is_primary: Mapped[bool] = mapped_column(nullable=False, default=False)
    segment: Mapped["VideoSegment"] = relationship(back_populates="concept_links")
    concept: Mapped["Concept"] = relationship()

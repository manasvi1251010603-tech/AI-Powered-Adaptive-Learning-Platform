"""Courses, lessons, resources, and concept-resource mappings."""

from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, CreatedAtMixin, TimestampMixin, GUID, UUIDPrimaryKeyMixin
from ..enums import COURSE_STATUSES, RESOURCE_TYPES


def _values(values: tuple[str, ...]) -> str:
    return ", ".join(f"'{value}'" for value in values)


class Course(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "courses"
    __table_args__ = (
        Index("ix_courses_subject_id", "subject_id"),
        Index("ix_courses_status", "status"),
        CheckConstraint(
            f"status IN ({_values(COURSE_STATUSES)})", name="status_allowed"
        ),
        CheckConstraint(
            "estimated_minutes IS NULL OR estimated_minutes > 0",
            name="estimated_minutes_positive",
        ),
    )

    subject_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    instructor_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    slug: Mapped[str] = mapped_column(String(280), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    thumbnail_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty: Mapped[str | None] = mapped_column(String(30), nullable=True)
    estimated_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="draft")
    published_at: Mapped[datetime | None] = mapped_column(nullable=True)

    subject: Mapped["Subject"] = relationship(back_populates="courses")
    modules: Mapped[List["CourseModule"]] = relationship(
        back_populates="course", cascade="all, delete-orphan", order_by="CourseModule.sort_order"
    )
    instructor: Mapped["User"] = relationship()


class CourseModule(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "course_modules"
    __table_args__ = (Index("ix_course_modules_course_sort", "course_id", "sort_order"),)

    course_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    course: Mapped["Course"] = relationship(back_populates="modules")
    lessons: Mapped[List["Lesson"]] = relationship(
        back_populates="module",
        cascade="all, delete-orphan",
        order_by="Lesson.sort_order",
    )


class Lesson(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "lessons"
    __table_args__ = (
        Index("ix_lessons_module_sort", "module_id", "sort_order"),
        CheckConstraint(
            "estimated_minutes IS NULL OR estimated_minutes > 0",
            name="estimated_minutes_positive",
        ),
    )

    module_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("course_modules.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    estimated_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)

    module: Mapped["CourseModule"] = relationship(back_populates="lessons")
    resources: Mapped[List["Resource"]] = relationship(
        back_populates="lesson", cascade="all, delete-orphan"
    )


class Resource(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "resources"
    __table_args__ = (
        Index("ix_resources_subject_id", "subject_id"),
        Index("ix_resources_lesson_id", "lesson_id"),
        Index("ix_resources_resource_type", "resource_type"),
        CheckConstraint(
            f"resource_type IN ({_values(RESOURCE_TYPES)})",
            name="resource_type_allowed",
        ),
        CheckConstraint(
            "quality_score IS NULL OR quality_score BETWEEN 0 AND 100",
            name="quality_score_range",
        ),
    )

    lesson_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("lessons.id", ondelete="SET NULL"), nullable=True
    )
    subject_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    resource_type: Mapped[str] = mapped_column(String(40), nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str | None] = mapped_column(Text, nullable=True)
    storage_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    thumbnail_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    estimated_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    difficulty: Mapped[str | None] = mapped_column(String(30), nullable=True)
    language: Mapped[str | None] = mapped_column(String(20), nullable=True)
    status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    quality_score: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    created_by_id: Mapped[UUID] = mapped_column(
        "created_by", GUID(), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )

    lesson: Mapped["Lesson | None"] = relationship(back_populates="resources")
    subject: Mapped["Subject"] = relationship()
    created_by: Mapped["User"] = relationship()
    concept_links: Mapped[List["ResourceConcept"]] = relationship(
        back_populates="resource", cascade="all, delete-orphan"
    )
    video: Mapped["Video | None"] = relationship(
        back_populates="resource", uselist=False, cascade="all, delete-orphan"
    )


class ResourceConcept(CreatedAtMixin, Base):
    __tablename__ = "resource_concepts"
    __table_args__ = (
        Index("ix_resource_concepts_concept_id", "concept_id"),
        CheckConstraint(
            "relevance_score IS NULL OR relevance_score BETWEEN 0 AND 100",
            name="relevance_score_range",
        ),
    )

    resource_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("resources.id", ondelete="CASCADE"), primary_key=True
    )
    concept_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("concepts.id", ondelete="CASCADE"), primary_key=True
    )
    relevance_score: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    resource: Mapped["Resource"] = relationship(back_populates="concept_links")
    concept: Mapped["Concept"] = relationship()

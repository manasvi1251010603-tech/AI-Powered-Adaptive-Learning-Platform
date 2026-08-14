"""Content review workflow and append-only audit records."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Index, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, CreatedAtMixin, GUID, TimestampMixin, UUIDPrimaryKeyMixin
from ..enums import CONTENT_REVIEW_STATUSES, CONTENT_REVIEW_TYPES


def _values(values: tuple[str, ...]) -> str:
    return ", ".join(f"'{value}'" for value in values)


class ContentReview(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "content_reviews"
    __table_args__ = (
        Index("ix_content_reviews_entity_status", "entity_type", "entity_id", "status"),
        CheckConstraint(
            f"review_type IN ({_values(CONTENT_REVIEW_TYPES)})",
            name="review_type_allowed",
        ),
        CheckConstraint(
            f"status IN ({_values(CONTENT_REVIEW_STATUSES)})",
            name="status_allowed",
        ),
    )

    reviewer_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[UUID] = mapped_column(GUID(), nullable=False)
    review_type: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewer: Mapped["User"] = relationship()


class AuditLog(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("ix_audit_logs_entity_created", "entity_type", "entity_id", "created_at"),
        Index("ix_audit_logs_actor_created", "actor_user_id", "created_at"),
    )

    actor_user_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[UUID | None] = mapped_column(GUID(), nullable=True)
    before_data: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    after_data: Mapped[dict | list | None] = mapped_column(JSON, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    actor: Mapped["User | None"] = relationship()

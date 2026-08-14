"""AI tutor conversations and auditable generation metadata."""

from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base, CreatedAtMixin, GUID, TimestampMixin, UUIDPrimaryKeyMixin
from ..enums import AI_MESSAGE_ROLES, GENERATION_STATUSES, GENERATION_TYPES, PROMPT_STATUSES


def _values(values: tuple[str, ...]) -> str:
    return ", ".join(f"'{value}'" for value in values)


class AIConversation(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "ai_conversations"
    __table_args__ = (Index("ix_ai_conversations_user_updated", "user_id", "updated_at"),)

    user_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True
    )
    concept_id: Mapped[UUID | None] = mapped_column(
        GUID(), ForeignKey("concepts.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str | None] = mapped_column(String(200), nullable=True)

    user: Mapped["User"] = relationship()
    subject: Mapped["Subject | None"] = relationship()
    concept: Mapped["Concept | None"] = relationship()
    messages: Mapped[List["AIMessage"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="AIMessage.created_at",
    )


class AIMessage(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "ai_messages"
    __table_args__ = (
        Index("ix_ai_messages_conversation_created", "conversation_id", "created_at"),
        CheckConstraint(
            f"role IN ({_values(AI_MESSAGE_ROLES)})", name="role_allowed"
        ),
    )

    conversation_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("ai_conversations.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    token_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

    conversation: Mapped["AIConversation"] = relationship(back_populates="messages")


class AIPromptVersion(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "ai_prompt_versions"
    __table_args__ = (
        Index("uq_ai_prompt_versions_key_version", "prompt_key", "version", unique=True),
        CheckConstraint(
            f"status IN ({_values(PROMPT_STATUSES)})", name="status_allowed"
        ),
    )

    prompt_key: Mapped[str] = mapped_column(String(100), nullable=False)
    version: Mapped[str] = mapped_column(String(30), nullable=False)
    template: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="draft")
    created_by_id: Mapped[UUID | None] = mapped_column(
        "created_by", GUID(), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    created_by: Mapped["User | None"] = relationship()
    generations: Mapped[List["AIGeneration"]] = relationship(
        back_populates="prompt_version"
    )


class AIGeneration(UUIDPrimaryKeyMixin, CreatedAtMixin, Base):
    __tablename__ = "ai_generations"
    __table_args__ = (
        Index("ix_ai_generations_generation_type_created", "generation_type", "created_at"),
        CheckConstraint(
            f"generation_type IN ({_values(GENERATION_TYPES)})",
            name="generation_type_allowed",
        ),
        CheckConstraint(
            f"status IN ({_values(GENERATION_STATUSES)})", name="status_allowed"
        ),
        CheckConstraint("latency_ms IS NULL OR latency_ms >= 0", name="latency_nonnegative"),
        CheckConstraint("input_tokens IS NULL OR input_tokens >= 0", name="input_tokens_nonnegative"),
        CheckConstraint(
            "output_tokens IS NULL OR output_tokens >= 0",
            name="output_tokens_nonnegative",
        ),
        CheckConstraint(
            "estimated_cost IS NULL OR estimated_cost >= 0",
            name="estimated_cost_nonnegative",
        ),
    )

    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    prompt_version_id: Mapped[UUID] = mapped_column(
        GUID(), ForeignKey("ai_prompt_versions.id", ondelete="RESTRICT"), nullable=False
    )
    generation_type: Mapped[str] = mapped_column(String(50), nullable=False)
    input_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    output_data: Mapped[dict | list] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="pending")
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    input_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    output_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    estimated_cost: Mapped[float | None] = mapped_column(Numeric(12, 6), nullable=True)

    prompt_version: Mapped["AIPromptVersion"] = relationship(back_populates="generations")

"""Shared SQLAlchemy declarative primitives for the MySQL model layer."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import DateTime, MetaData, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import CHAR, TypeDecorator


class GUID(TypeDecorator[UUID]):
    """Store UUID values as portable, readable CHAR(36) values in MySQL."""

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect: Any) -> Any:
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value: UUID | str | None, dialect: Any) -> str | None:
        if value is None:
            return None
        return str(value if isinstance(value, UUID) else UUID(value))

    def process_result_value(self, value: str | None, dialect: Any) -> UUID | None:
        return UUID(value) if value is not None else None


naming_convention = {
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=naming_convention)


class UUIDPrimaryKeyMixin:
    id: Mapped[UUID] = mapped_column(GUID(), primary_key=True, default=uuid4)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


def uuid_fk(
    target: str,
    *,
    nullable: bool = False,
    primary_key: bool = False,
    unique: bool = False,
) -> Any:
    """Create a consistently typed UUID foreign-key column."""

    return mapped_column(
        GUID(),
        ForeignKey(target, ondelete="CASCADE" if not nullable else "SET NULL"),
        nullable=nullable,
        primary_key=primary_key,
        unique=unique,
    )


# Imported lazily to keep the helper's public signature small while avoiding
# a circular import during SQLAlchemy class construction.
from sqlalchemy import ForeignKey  # noqa: E402
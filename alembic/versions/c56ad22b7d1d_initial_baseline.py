"""Initial baseline

Revision ID: c56ad22b7d1d
Revises: 
Create Date: 2026-08-10 18:47:04.418005

"""
from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = 'c56ad22b7d1d'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""

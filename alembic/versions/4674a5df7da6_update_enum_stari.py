"""update_enum_stari

Revision ID: 4674a5df7da6
Revises: e4520b9639c0
Create Date: 2026-08-24 14:07:14.785136

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4674a5df7da6'
down_revision: Union[str, Sequence[str], None] = 'e4520b9639c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("COMMIT")

    # Lista cu noile tale stări
    stari_noi = [
        'IN_DIAGNOSTICARE',
        'OFERTA_IN_ASTEPTARE',
        'ASTEPTARE_PIESE',
        'PREGATIT_PENTRU_RIDICARE',
        'RIDICAT',
        'ANULAT'
    ]

    # Adăugăm fiecare stare în dicționarul bazei de date
    for stare in stari_noi:
        op.execute(f"ALTER TYPE statusreparatie ADD VALUE IF NOT EXISTS '{stare}'")

def downgrade() -> None:
    """Downgrade schema."""
    pass

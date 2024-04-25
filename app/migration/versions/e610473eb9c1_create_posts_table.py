"""create posts table

Revision ID: e610473eb9c1
Revises: 
Create Date: 2024-04-25 21:59:27.800127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e610473eb9c1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("category", sa.String(100), nullable=False),
        sa.Column("created_date", sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column("updated_date", sa.TIMESTAMP, server_default=sa.func.now(), server_onupdate=sa.func.now()),
        sa.Column("status", sa.String(100), nullable=False, server_default="draft"),
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass

"""create computers and metrics tables

Revision ID: 9d35e8085691
Revises:
Create Date: 2026-07-22

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "9d35e8085691"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "computers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("hostname", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_computers_hostname", "computers", ["hostname"], unique=True)

    op.create_table(
        "metrics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("computer_id", sa.Integer(), sa.ForeignKey("computers.id"), nullable=False),
        sa.Column("cpu_percent", sa.Float(), nullable=False),
        sa.Column("memory_percent", sa.Float(), nullable=False),
        sa.Column("disk_percent", sa.Float(), nullable=False),
        sa.Column("collected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_metrics_computer_id", "metrics", ["computer_id"])


def downgrade() -> None:
    op.drop_index("ix_metrics_computer_id", table_name="metrics")
    op.drop_table("metrics")
    op.drop_index("ix_computers_hostname", table_name="computers")
    op.drop_table("computers")

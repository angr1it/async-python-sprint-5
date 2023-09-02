"""file_real_path

Revision ID: bae1f0d92988
Revises: 093e4a2a72e7
Create Date: 2023-09-02 19:15:35.487507

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bae1f0d92988"
down_revision: Union[str, None] = "093e4a2a72e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "file", sa.Column("real_path", sa.String(length=2048), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("file", "real_path")
    # ### end Alembic commands ###

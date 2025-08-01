"""10032025 update mapping dept with doctype

Revision ID: bd42672cc8c7
Revises: f23939982604
Create Date: 2025-03-10 20:36:00.308183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'bd42672cc8c7'
down_revision: Union[str, None] = 'f23939982604'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('departement_doc_type', sa.Column('departement_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.drop_constraint('departement_doc_type_dept_id_fkey', 'departement_doc_type', type_='foreignkey')
    op.create_foreign_key(None, 'departement_doc_type', 'departement', ['departement_id'], ['id'])
    op.drop_column('departement_doc_type', 'dept_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('departement_doc_type', sa.Column('dept_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'departement_doc_type', type_='foreignkey')
    op.create_foreign_key('departement_doc_type_dept_id_fkey', 'departement_doc_type', 'departement', ['dept_id'], ['id'])
    op.drop_column('departement_doc_type', 'departement_id')
    # ### end Alembic commands ###

"""7 Maret 2025 10:14 change name table departement doc type

Revision ID: 0c0d8317eb86
Revises: 82d05d6a0f88
Create Date: 2025-03-07 10:20:12.103191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '0c0d8317eb86'
down_revision: Union[str, None] = '82d05d6a0f88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project',
    sa.Column('code', sqlmodel.sql.sqltypes.AutoString(length=4), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('area_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(length=26), nullable=False),
    sa.Column('created_by', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('updated_by', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code')
    )
    op.create_index(op.f('ix_project_id'), 'project', ['id'], unique=False)
    op.create_table('role',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(length=26), nullable=False),
    sa.Column('created_by', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('updated_by', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_role_id'), 'role', ['id'], unique=False)
    op.create_table('worker',
    sa.Column('client_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('departement_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(length=26), nullable=False),
    sa.Column('created_by', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('updated_by', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['departement_id'], ['departement.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_worker_id'), 'worker', ['id'], unique=False)
    op.create_table('departement_doc_type',
    sa.Column('doc_type_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('dept_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['dept_id'], ['departement.id'], ),
    sa.ForeignKeyConstraint(['doc_type_id'], ['doc_type.id'], ),
    sa.PrimaryKeyConstraint('doc_type_id', 'dept_id')
    )
    op.create_table('worker_role',
    sa.Column('worker_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('role_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['worker_id'], ['worker.id'], ),
    sa.PrimaryKeyConstraint('worker_id', 'role_id')
    )
    op.drop_table('doc_type_departement')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('doc_type_departement',
    sa.Column('doc_type_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('departement_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['departement_id'], ['departement.id'], name='doc_type_departement_departement_id_fkey'),
    sa.ForeignKeyConstraint(['doc_type_id'], ['doc_type.id'], name='doc_type_departement_doc_type_id_fkey'),
    sa.PrimaryKeyConstraint('doc_type_id', 'departement_id', name='doc_type_departement_pkey')
    )
    op.drop_table('worker_role')
    op.drop_table('departement_doc_type')
    op.drop_index(op.f('ix_worker_id'), table_name='worker')
    op.drop_table('worker')
    op.drop_index(op.f('ix_role_id'), table_name='role')
    op.drop_table('role')
    op.drop_index(op.f('ix_project_id'), table_name='project')
    op.drop_table('project')
    # ### end Alembic commands ###

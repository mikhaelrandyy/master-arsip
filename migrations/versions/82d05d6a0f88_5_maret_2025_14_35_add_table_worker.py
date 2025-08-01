"""5 Maret 2025 14:35 add table worker

Revision ID: 82d05d6a0f88
Revises: 8bf180b5cb0c
Create Date: 2025-03-05 14:41:36.847459

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '82d05d6a0f88'
down_revision: Union[str, None] = '8bf180b5cb0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project',
    sa.Column('code', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(length=26), nullable=False),
    sa.Column('created_by', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('updated_by', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
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
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(length=26), nullable=False),
    sa.Column('created_by', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('updated_by', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_worker_id'), 'worker', ['id'], unique=False)
    op.create_table('worker_column',
    sa.Column('worker_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('role_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('project_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('departement_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['departement_id'], ['departement.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['worker_id'], ['worker.id'], ),
    sa.PrimaryKeyConstraint('worker_id', 'role_id', 'project_id', 'departement_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('worker_column')
    op.drop_index(op.f('ix_worker_id'), table_name='worker')
    op.drop_table('worker')
    op.drop_index(op.f('ix_role_id'), table_name='role')
    op.drop_table('role')
    op.drop_index(op.f('ix_project_id'), table_name='project')
    op.drop_table('project')
    # ### end Alembic commands ###

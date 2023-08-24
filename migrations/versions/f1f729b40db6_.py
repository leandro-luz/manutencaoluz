"""empty message

Revision ID: f1f729b40db6
Revises: 632b160c2ec8
Create Date: 2023-05-03 21:15:04.682338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1f729b40db6'
down_revision = '632b160c2ec8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'empresa', 'tipoempresa', ['tipoempresa_id'], ['id'])
    op.create_foreign_key(None, 'empresa', 'contrato', ['contrato_id'], ['id'])
    op.create_foreign_key(None, 'equipamento', 'grupo', ['grupo_id'], ['id'])
    op.create_foreign_key(None, 'equipamento', 'empresa', ['empresa_id'], ['id'])
    op.create_foreign_key(None, 'perfil', 'empresa', ['empresa_id'], ['id'])
    op.create_foreign_key(None, 'sistema', 'equipamento', ['equipamento_id'], ['id'])
    op.create_foreign_key(None, 'supplier', 'empresa', ['company_id'], ['id'])
    op.create_foreign_key(None, 'telacontrato', 'tela', ['tela_id'], ['id'])
    op.create_foreign_key(None, 'telacontrato', 'contrato', ['contrato_id'], ['id'])
    op.create_foreign_key(None, 'telaperfil', 'tela', ['tela_id'], ['id'])
    op.create_foreign_key(None, 'telaperfil', 'perfil', ['perfilacesso_id'], ['id'])
    op.create_foreign_key(None, 'usuario', 'perfil', ['perfilacesso_id'], ['id'])
    op.create_foreign_key(None, 'usuario', 'senha', ['senha_id'], ['id'])
    op.create_foreign_key(None, 'usuario', 'empresa', ['empresa_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'usuario', type_='foreignkey')
    op.drop_constraint(None, 'usuario', type_='foreignkey')
    op.drop_constraint(None, 'usuario', type_='foreignkey')
    op.drop_constraint(None, 'telaperfil', type_='foreignkey')
    op.drop_constraint(None, 'telaperfil', type_='foreignkey')
    op.drop_constraint(None, 'telacontrato', type_='foreignkey')
    op.drop_constraint(None, 'telacontrato', type_='foreignkey')
    op.drop_constraint(None, 'supplier', type_='foreignkey')
    op.drop_constraint(None, 'sistema', type_='foreignkey')
    op.drop_constraint(None, 'perfil', type_='foreignkey')
    op.drop_constraint(None, 'equipamento', type_='foreignkey')
    op.drop_constraint(None, 'equipamento', type_='foreignkey')
    op.drop_constraint(None, 'empresa', type_='foreignkey')
    op.drop_constraint(None, 'empresa', type_='foreignkey')
    # ### end Alembic commands ###

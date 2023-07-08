"""empty message

Revision ID: 73806d9eb165
Revises: ccc601de3bb2
Create Date: 2023-07-08 15:21:08.081566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73806d9eb165'
down_revision = 'ccc601de3bb2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'empresa', 'contrato', ['contrato_id'], ['id'])
    op.create_foreign_key(None, 'empresa', 'tipo_empresa', ['tipoempresa_id'], ['id'])
    op.create_foreign_key(None, 'equipamento', 'subgrupo', ['subgrupo_id'], ['id'])
    op.create_foreign_key(None, 'grupo', 'empresa', ['empresa_id'], ['id'])
    op.create_foreign_key(None, 'ordem_servico', 'tipo_ordem', ['tipoordem_id'], ['id'])
    op.create_foreign_key(None, 'ordem_servico', 'usuario', ['solicitante_id'], ['id'])
    op.create_foreign_key(None, 'ordem_servico', 'equipamento', ['equipamento_id'], ['id'])
    op.create_foreign_key(None, 'ordem_servico', 'situacao_ordem', ['situacaoordem_id'], ['id'])
    op.create_foreign_key(None, 'perfil', 'empresa', ['empresa_id'], ['id'])
    op.create_foreign_key(None, 'periodicidade', 'unidade', ['unidade_id'], ['id'])
    op.create_foreign_key(None, 'plano_manutencao', 'periodicidade', ['periodicidade_id'], ['id'])
    op.create_foreign_key(None, 'plano_manutencao', 'tipo_ordem', ['tipoordem_id'], ['id'])
    op.create_foreign_key(None, 'plano_manutencao', 'tipo_data', ['tipodata_id'], ['id'])
    op.create_foreign_key(None, 'plano_manutencao', 'equipamento', ['equipamento_id'], ['id'])
    op.create_foreign_key(None, 'subgrupo', 'grupo', ['grupo_id'], ['id'])
    op.create_foreign_key(None, 'supplier', 'empresa', ['company_id'], ['id'])
    op.create_foreign_key(None, 'tela_contrato', 'contrato', ['contrato_id'], ['id'])
    op.create_foreign_key(None, 'tela_contrato', 'tela', ['tela_id'], ['id'])
    op.create_foreign_key(None, 'tela_perfil', 'perfil', ['perfil_id'], ['id'])
    op.create_foreign_key(None, 'tela_perfil', 'tela', ['tela_id'], ['id'])
    op.create_foreign_key(None, 'tramitacao_ordem', 'usuario', ['usuario_id'], ['id'])
    op.create_foreign_key(None, 'tramitacao_ordem', 'ordem_servico', ['ordemservico_id'], ['id'])
    op.create_foreign_key(None, 'tramitacao_ordem', 'situacao_ordem', ['situacaoordem_id'], ['id'])
    op.create_foreign_key(None, 'usuario', 'senha', ['senha_id'], ['id'])
    op.create_foreign_key(None, 'usuario', 'perfil', ['perfil_id'], ['id'])
    op.create_foreign_key(None, 'usuario', 'empresa', ['empresa_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'usuario', type_='foreignkey')
    op.drop_constraint(None, 'usuario', type_='foreignkey')
    op.drop_constraint(None, 'usuario', type_='foreignkey')
    op.drop_constraint(None, 'tramitacao_ordem', type_='foreignkey')
    op.drop_constraint(None, 'tramitacao_ordem', type_='foreignkey')
    op.drop_constraint(None, 'tramitacao_ordem', type_='foreignkey')
    op.drop_constraint(None, 'tela_perfil', type_='foreignkey')
    op.drop_constraint(None, 'tela_perfil', type_='foreignkey')
    op.drop_constraint(None, 'tela_contrato', type_='foreignkey')
    op.drop_constraint(None, 'tela_contrato', type_='foreignkey')
    op.drop_constraint(None, 'supplier', type_='foreignkey')
    op.drop_constraint(None, 'subgrupo', type_='foreignkey')
    op.drop_constraint(None, 'plano_manutencao', type_='foreignkey')
    op.drop_constraint(None, 'plano_manutencao', type_='foreignkey')
    op.drop_constraint(None, 'plano_manutencao', type_='foreignkey')
    op.drop_constraint(None, 'plano_manutencao', type_='foreignkey')
    op.drop_constraint(None, 'periodicidade', type_='foreignkey')
    op.drop_constraint(None, 'perfil', type_='foreignkey')
    op.drop_constraint(None, 'ordem_servico', type_='foreignkey')
    op.drop_constraint(None, 'ordem_servico', type_='foreignkey')
    op.drop_constraint(None, 'ordem_servico', type_='foreignkey')
    op.drop_constraint(None, 'ordem_servico', type_='foreignkey')
    op.drop_constraint(None, 'grupo', type_='foreignkey')
    op.drop_constraint(None, 'equipamento', type_='foreignkey')
    op.drop_constraint(None, 'empresa', type_='foreignkey')
    op.drop_constraint(None, 'empresa', type_='foreignkey')
    # ### end Alembic commands ###

import logging
import datetime
import os
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from webapp import create_app
from webapp import db
from webapp.usuario.models import PerfilAcesso, Senha, Usuario, TelaPerfilAcesso
from webapp.empresa.models import Interessado, Tipoempresa, Empresa
from webapp.equipamento.models import Equipamento, Grupo, Subgrupo, Pavimento, Setor, Local, Localizacao
from webapp.contrato.models import Contrato, Tela, Telacontrato
from webapp.plano_manutencao.models import TipoData, Unidade, Periodicidade, PlanoManutencao, Atividade, \
    TipoParametro, ListaAtividade, TipoBinario
from webapp.ordem_servico.models import TipoSituacaoOrdem, FluxoOrdem, OrdemServico, TramitacaoOrdem, TipoOrdem

env = os.environ.get('WEBAPP_ENV', 'prod')
app = create_app('config.%sConfig' % env.capitalize())
app.app_context().push()

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

print("Excluindo todas as tabelas")
db.drop_all()
print("Criando todas as tabelas")
db.create_all()

telas_lista = [
    {'posicao': 1, 'nome': 'Interessado', 'icon': 'bi-card-list', 'url': 'empresa.interessado_listar'},
    {'posicao': 2, 'nome': 'Contrato', 'icon': 'bi-briefcase', 'url': 'contrato.contrato_listar'},
    {'posicao': 3, 'nome': 'Empresa', 'icon': 'bi-house-door', 'url': 'empresa.empresa_listar'},
    {'posicao': 4, 'nome': 'Usuário', 'icon': 'bi-people', 'url': 'usuario.usuario_listar'},
    {'posicao': 5, 'nome': 'Equipamento', 'icon': 'bi-robot', 'url': 'equipamento.equipamento_listar'},
    {'posicao': 6, 'nome': 'Plano de Manutenção', 'icon': 'bi-clipboard', 'url': 'plano_manutencao.plano_listar'},
    {'posicao': 7, 'nome': 'Ordem de Serviço', 'icon': 'bi-wrench-adjustable-circle',
     'url': 'ordem_servico.ordem_listar'},
    {'posicao': 8, 'nome': 'Almoxarifado', 'icon': 'bi-box-seam', 'url': 'sistema.almoxarifado'},
    {'posicao': 9, 'nome': 'Ferramentas', 'icon': 'bi-tools', 'url': 'sistema.ferramentas'},
    {'posicao': 10, 'nome': 'EPI_EPC', 'icon': 'bi-umbrella-fill', 'url': 'sistema.epi'},
    {'posicao': 11, 'nome': 'Programação', 'icon': 'bi-calendar3', 'url': 'sistema.programação'},
    {'posicao': 12, 'nome': 'Fornecedor', 'icon': 'bi-truck', 'url': 'supplier.supplier_list'},
    {'posicao': 13, 'nome': 'Orçamento', 'icon': 'bi-cash', 'url': 'sistema.orçamento'},
    {'posicao': 14, 'nome': 'Indicadores', 'icon': 'bi-graph-up', 'url': 'sistema.indicador'},

]

contratos_lista = [
    {'nome': 'BÁSICO', 'ativo': True},
    {'nome': 'INTERMEDIÁRIO', 'ativo': True},
    {'nome': 'COMPLETO', 'ativo': True}
]

telascontrato_lista = [
    {'contrato': 'BÁSICO', 'tela': 'Usuário'},
    {'contrato': 'BÁSICO', 'tela': 'Equipamento'},
    {'contrato': 'BÁSICO', 'tela': 'Fornecedor'},
    {'contrato': 'INTERMEDIÁRIO', 'tela': 'Empresa'},
    {'contrato': 'INTERMEDIÁRIO', 'tela': 'Usuário'},
    {'contrato': 'INTERMEDIÁRIO', 'tela': 'Equipamento'},
    {'contrato': 'INTERMEDIÁRIO', 'tela': 'Plano de Manutenção'},
    {'contrato': 'INTERMEDIÁRIO', 'tela': 'Ordem de Serviço'},
    {'contrato': 'COMPLETO', 'tela': 'Interessado'},
    {'contrato': 'COMPLETO', 'tela': 'Contrato'},
    {'contrato': 'COMPLETO', 'tela': 'Empresa'},
    {'contrato': 'COMPLETO', 'tela': 'Usuário'},
    {'contrato': 'COMPLETO', 'tela': 'Equipamento'},
    {'contrato': 'COMPLETO', 'tela': 'Plano de Manutenção'},
    {'contrato': 'COMPLETO', 'tela': 'Ordem de Serviço'},
    {'contrato': 'COMPLETO', 'tela': 'Fornecedor'},
    {'contrato': 'COMPLETO', 'tela': 'Almoxarifado'},
    {'contrato': 'COMPLETO', 'tela': 'Programação'},
    {'contrato': 'COMPLETO', 'tela': 'Orçamento'},
    {'contrato': 'COMPLETO', 'tela': 'Indicadores'},
    {'contrato': 'COMPLETO', 'tela': 'Ferramentas'},
    {'contrato': 'COMPLETO', 'tela': 'EPI_EPC'},
]

interessado_lista = [
    {'nome_fantasia': 'empresa_oi', 'cnpj': '96.207.052/0001-02',
     'email': 'empresa_oi@empoi.com.br', 'telefone': '(45)9 9874-4578'},
    {'nome_fantasia': 'empresa_by', 'cnpj': '24.885.627/0001-35',
     'email': 'empresa_by@empby', 'telefone': '(78)3245-6578'},
]

tipo_empresa_lista = [
    {'nome': 'Cliente'},
    {'nome': 'Fornecedor'},
    {'nome': 'Parceiro'}
]

empresa_lista = [
    {'razao_social': 'manluz.ltda',
     'nome_fantasia': 'MANLUZ',
     'cnpj': '39.262.527/0001-20',
     'cep': '65.058-864',
     'logradouro': 'Rua NÃO SEI', 'bairro': 'AQUI DO LADO',
     'municipio': 'ESTE AQUI', 'uf': 'XX',
     'numero': '99', 'complemento': 'qd09 lt18',
     'email': 'guguleo2019@gmail.com', 'telefone': '(45)9 9876-5432',
     'data_cadastro': str(datetime.datetime.now() - datetime.timedelta(360)), 'contrato': 'COMPLETO',
     'empresa_gestora': 'MANLUZ', 'tipo': 'Cliente'},

    {'razao_social': 'empresa_teste.ltda',
     'nome_fantasia': 'EMPRESA_TESTE',
     'cnpj': '40.262.527/0001-20',
     'cep': '65.058-864',
     'logradouro': 'Rua NÃO SEI', 'bairro': 'AQUI DO LADO',
     'municipio': 'ESTE AQUI', 'uf': 'XX',
     'numero': '99', 'complemento': 'qd09 lt18',
     'email': 'empresa_teste@gmail.com', 'telefone': '(45)9 9876-5432',
     'data_cadastro': str(datetime.datetime.now() - datetime.timedelta(360)), 'contrato': 'COMPLETO',
     'empresa_gestora': 'MANLUZ', 'tipo': 'Cliente'},

    {'razao_social': 'empresa_beta.ltda',
     'nome_fantasia': 'EMPRESA_BETA',
     'cnpj': '39.262.527/0001-30',
     'cep': '65.058-865',
     'logradouro': 'Rua Aderson Lago', 'bairro': 'Vila Janaína',
     'municipio': 'São Luís', 'uf': 'MA',
     'numero': '0', 'complemento': 'qd05 lt05',
     'email': 'empresa_beta@teste.com.br', 'telefone': '(45)9 9876-5432',
     'data_cadastro': str(datetime.datetime.now() - datetime.timedelta(360)), 'contrato': 'INTERMEDIÁRIO',
     'empresa_gestora': 'MANLUZ', 'tipo': 'Cliente'},

    {'razao_social': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA',
     'nome_fantasia': 'COMERCIAL SEMEENTE CASA E CONSTRUCAO',
     'cnpj': '30.722.226/0001-67',
     'cep': '74.905-230',
     'logradouro': 'RUA CAIAPOS', 'bairro': 'VILA BRASILIA',
     'municipio': 'APARECIDA DE GOIÂNIA', 'uf': 'GO',
     'numero': '0', 'complemento': '',
     'email': 'contato.luzengenharia@gmail.com', 'telefone': '(62)9 8423-6833',
     'data_cadastro': str(datetime.datetime.now() + datetime.timedelta(30)), 'contrato': 'INTERMEDIÁRIO',
     'empresa_gestora': 'MANLUZ', 'tipo': 'Cliente'},
]

perfis_lista = [
    {'empresa': 'manluz.ltda', 'nome': 'default', 'descricao': 'padrão', 'ativo': True},
    {'empresa': 'manluz.ltda', 'nome': 'admin', 'descricao': 'administrador', 'ativo': True},
    {'empresa': 'manluz.ltda', 'nome': 'adminluz', 'descricao': 'administrador do sistema', 'ativo': True},
    {'empresa': 'empresa_teste.ltda', 'nome': 'default', 'descricao': 'padrão', 'ativo': True},
    {'empresa': 'empresa_teste.ltda', 'nome': 'admin', 'descricao': 'administrador', 'ativo': True},
    {'empresa': 'empresa_teste.ltda', 'nome': 'adminluz', 'descricao': 'administrador do sistema', 'ativo': True},
    {'empresa': 'empresa_beta.ltda', 'nome': 'default', 'descricao': 'padrão', 'ativo': True},
    {'empresa': 'empresa_beta.ltda', 'nome': 'admin', 'descricao': 'administrador', 'ativo': True},
    {'empresa': 'empresa_beta.ltda', 'nome': 'adminluz', 'descricao': 'administrador do sistema', 'ativo': True},
    {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'nome': 'admin', 'descricao': 'administrador', 'ativo': True},
    {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'nome': 'adminluz', 'descricao': 'administrador do sistema',
     'ativo': True},
]

telasperfil_lista = [
    {'empresa': 'manluz.ltda', 'role': 'default', 'tela': 'Contrato'},
    {'empresa': 'manluz.ltda', 'role': 'default', 'tela': 'Empresa'},
    {'empresa': 'manluz.ltda', 'role': 'default', 'tela': 'Usuário'},
    {'empresa': 'manluz.ltda', 'role': 'admin', 'tela': 'Interessado'},
    {'empresa': 'manluz.ltda', 'role': 'admin', 'tela': 'Contrato'},
    {'empresa': 'manluz.ltda', 'role': 'admin', 'tela': 'Empresa'},
    {'empresa': 'manluz.ltda', 'role': 'admin', 'tela': 'Usuário'},
    {'empresa': 'manluz.ltda', 'role': 'admin', 'tela': 'Equipamento'},
    {'empresa': 'manluz.ltda', 'role': 'admin', 'tela': 'Plano de Manutenção'},
    {'empresa': 'manluz.ltda', 'role': 'admin', 'tela': 'Ordem de Serviço'},
    {'empresa': 'manluz.ltda', 'role': 'admin', 'tela': 'Fornecedor'},
    {'empresa': 'manluz.ltda', 'role': 'admin', 'tela': 'Almoxarifado'},
    {'empresa': 'manluz.ltda', 'role': 'admin', 'tela': 'Programação'},
    {'empresa': 'manluz.ltda', 'role': 'admin', 'tela': 'Orçamento'},
    {'empresa': 'manluz.ltda', 'role': 'admin', 'tela': 'Indicadores'},
    {'empresa': 'manluz.ltda', 'role': 'admin', 'tela': 'Ferramentas'},
    {'empresa': 'manluz.ltda', 'role': 'admin', 'tela': 'EPI_EPC'},
    {'empresa': 'manluz.ltda', 'role': 'adminluz', 'tela': 'Interessado'},
    {'empresa': 'manluz.ltda', 'role': 'adminluz', 'tela': 'Contrato'},
    {'empresa': 'manluz.ltda', 'role': 'adminluz', 'tela': 'Empresa'},
    {'empresa': 'manluz.ltda', 'role': 'adminluz', 'tela': 'Usuário'},
    {'empresa': 'manluz.ltda', 'role': 'adminluz', 'tela': 'Equipamento'},
    {'empresa': 'manluz.ltda', 'role': 'adminluz', 'tela': 'Plano de Manutenção'},
    {'empresa': 'manluz.ltda', 'role': 'adminluz', 'tela': 'Ordem de Serviço'},
    {'empresa': 'manluz.ltda', 'role': 'adminluz', 'tela': 'Fornecedor'},
    {'empresa': 'manluz.ltda', 'role': 'adminluz', 'tela': 'Almoxarifado'},
    {'empresa': 'manluz.ltda', 'role': 'adminluz', 'tela': 'Programação'},
    {'empresa': 'manluz.ltda', 'role': 'adminluz', 'tela': 'Orçamento'},
    {'empresa': 'manluz.ltda', 'role': 'adminluz', 'tela': 'Indicadores'},
    {'empresa': 'manluz.ltda', 'role': 'adminluz', 'tela': 'Ferramentas'},
    {'empresa': 'manluz.ltda', 'role': 'adminluz', 'tela': 'EPI_EPC'},

    {'empresa': 'empresa_teste.ltda', 'role': 'default', 'tela': 'Contrato'},
    {'empresa': 'empresa_teste.ltda', 'role': 'default', 'tela': 'Empresa'},
    {'empresa': 'empresa_teste.ltda', 'role': 'default', 'tela': 'Usuário'},
    {'empresa': 'empresa_teste.ltda', 'role': 'admin', 'tela': 'Interessado'},
    {'empresa': 'empresa_teste.ltda', 'role': 'admin', 'tela': 'Contrato'},
    {'empresa': 'empresa_teste.ltda', 'role': 'admin', 'tela': 'Empresa'},
    {'empresa': 'empresa_teste.ltda', 'role': 'admin', 'tela': 'Usuário'},
    {'empresa': 'empresa_teste.ltda', 'role': 'admin', 'tela': 'Equipamento'},
    {'empresa': 'empresa_teste.ltda', 'role': 'admin', 'tela': 'Plano de Manutenção'},
    {'empresa': 'empresa_teste.ltda', 'role': 'admin', 'tela': 'Ordem de Serviço'},
    {'empresa': 'empresa_teste.ltda', 'role': 'admin', 'tela': 'Fornecedor'},
    {'empresa': 'empresa_teste.ltda', 'role': 'admin', 'tela': 'Almoxarifado'},
    {'empresa': 'empresa_teste.ltda', 'role': 'admin', 'tela': 'Programação'},
    {'empresa': 'empresa_teste.ltda', 'role': 'admin', 'tela': 'Orçamento'},
    {'empresa': 'empresa_teste.ltda', 'role': 'admin', 'tela': 'Indicadores'},
    {'empresa': 'empresa_teste.ltda', 'role': 'admin', 'tela': 'Ferramentas'},
    {'empresa': 'empresa_teste.ltda', 'role': 'admin', 'tela': 'EPI_EPC'},
    {'empresa': 'empresa_teste.ltda', 'role': 'adminluz', 'tela': 'Interessado'},
    {'empresa': 'empresa_teste.ltda', 'role': 'adminluz', 'tela': 'Contrato'},
    {'empresa': 'empresa_teste.ltda', 'role': 'adminluz', 'tela': 'Empresa'},
    {'empresa': 'empresa_teste.ltda', 'role': 'adminluz', 'tela': 'Usuário'},
    {'empresa': 'empresa_teste.ltda', 'role': 'adminluz', 'tela': 'Equipamento'},
    {'empresa': 'empresa_teste.ltda', 'role': 'adminluz', 'tela': 'Plano de Manutenção'},
    {'empresa': 'empresa_teste.ltda', 'role': 'adminluz', 'tela': 'Ordem de Serviço'},
    {'empresa': 'empresa_teste.ltda', 'role': 'adminluz', 'tela': 'Fornecedor'},
    {'empresa': 'empresa_teste.ltda', 'role': 'adminluz', 'tela': 'Almoxarifado'},
    {'empresa': 'empresa_teste.ltda', 'role': 'adminluz', 'tela': 'Programação'},
    {'empresa': 'empresa_teste.ltda', 'role': 'adminluz', 'tela': 'Orçamento'},
    {'empresa': 'empresa_teste.ltda', 'role': 'adminluz', 'tela': 'Indicadores'},
    {'empresa': 'empresa_teste.ltda', 'role': 'adminluz', 'tela': 'Ferramentas'},
    {'empresa': 'empresa_teste.ltda', 'role': 'adminluz', 'tela': 'EPI_EPC'},

    {'empresa': 'empresa_beta.ltda', 'role': 'admin', 'tela': 'Contrato'},
    {'empresa': 'empresa_beta.ltda', 'role': 'admin', 'tela': 'Empresa'},
    {'empresa': 'empresa_beta.ltda', 'role': 'admin', 'tela': 'Usuário'},
    {'empresa': 'empresa_beta.ltda', 'role': 'admin', 'tela': 'Equipamento'},
    {'empresa': 'empresa_beta.ltda', 'role': 'admin', 'tela': 'Plano de Manutenção'},
    {'empresa': 'empresa_beta.ltda', 'role': 'admin', 'tela': 'Ordem de Serviço'},
    {'empresa': 'empresa_beta.ltda', 'role': 'adminluz', 'tela': 'Contrato'},
    {'empresa': 'empresa_beta.ltda', 'role': 'adminluz', 'tela': 'Empresa'},
    {'empresa': 'empresa_beta.ltda', 'role': 'adminluz', 'tela': 'Usuário'},
    {'empresa': 'empresa_beta.ltda', 'role': 'adminluz', 'tela': 'Equipamento'},
    {'empresa': 'empresa_beta.ltda', 'role': 'adminluz', 'tela': 'Plano de Manutenção'},
    {'empresa': 'empresa_beta.ltda', 'role': 'adminluz', 'tela': 'Ordem de Serviço'},

    {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'admin', 'tela': 'Empresa'},
    {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'admin', 'tela': 'Usuário'},
    {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'admin', 'tela': 'Equipamento'},
    {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'admin', 'tela': 'Plano de Manutenção'},
    {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'admin', 'tela': 'Ordem de Serviço'},
    {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'adminluz', 'tela': 'Empresa'},
    {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'adminluz', 'tela': 'Usuário'},
    {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'adminluz', 'tela': 'Equipamento'},
    {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'adminluz', 'tela': 'Plano de Manutenção'},
    {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'adminluz', 'tela': 'Ordem de Serviço'},

]

senha_lista = [
    {'senha': 'aaa11111', 'data_expiracao': str(datetime.datetime.now() + datetime.timedelta(30)),
     'senha_expira': False, 'senha_temporaria': False},
    {'senha': 'teste123', 'data_expiracao': str(datetime.datetime.now() + datetime.timedelta(30)),
     'senha_expira': False, 'senha_temporaria': False},
    {'senha': 'beta123', 'data_expiracao': str(datetime.datetime.now() + datetime.timedelta(30)),
     'senha_expira': False, 'senha_temporaria': False},
    {'senha': 'aaa44444', 'data_expiracao': str(datetime.datetime.now() + datetime.timedelta(30)),
     'senha_expira': False, 'senha_temporaria': False},
    {'senha': 'aaa55555', 'data_expiracao': str(datetime.datetime.now() + datetime.timedelta(30)),
     'senha_expira': False, 'senha_temporaria': False},
    {'senha': 'aaa66666', 'data_expiracao': str(datetime.datetime.now() + datetime.timedelta(30)),
     'senha_expira': False, 'senha_temporaria': False},
    {'senha': '12345678', 'data_expiracao': str(datetime.datetime.now() + datetime.timedelta(30)),
     'senha_expira': True, 'senha_temporaria': True},
]

usuario_lista = [
    {'nome': 'admin', 'email': 'admin@admin.com',
     'senha': 'aaa11111', 'perfil': 'admin',
     'data_assinatura': '1980/05/10 12:45:10',
     'empresa': 'manluz.ltda'},
    {'nome': 'leandro', 'email': 'admin@admin.com',
     'senha': 'aaa11111', 'perfil': 'admin',
     'data_assinatura': '1980/05/10 12:45:10',
     'empresa': 'manluz.ltda'},

    {'nome': 'adminluz_teste', 'email': 'adminteste@hotmail.com',
     'senha': 'aaa11111', 'perfil': 'adminluz', 'data_assinatura': '1980/05/10 12:45:10',
     'empresa': 'empresa_teste.ltda'},
    {'nome': 'admin_teste', 'email': 'gerenciadorteste@hotmail.com',
     'senha': '12345678', 'perfil': 'admin',
     'data_assinatura': '2023/06/05 18:00:00',
     'empresa': 'empresa_teste.ltda'},

    {'nome': 'adminluz_beta', 'email': 'adminbeta@gmail.com',
     'senha': 'aaa11111', 'perfil': 'adminluz', 'data_assinatura': '1980/05/10 12:45:10',
     'empresa': 'empresa_beta.ltda'},
    {'nome': 'admin_beta', 'email': 'gerenciadorbeta@gmail.com',
     'senha': '12345678', 'perfil': 'admin', 'data_assinatura': '2023/06/05 18:00:00',
     'empresa': 'empresa_beta.ltda'},

    {'nome': 'adminluz_semeente', 'email': 'guguleo2019@gmail.com',
     'senha': 'aaa11111', 'perfil': 'adminluz', 'data_assinatura': '1980/05/10 12:45:10',
     'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA'},
    {'nome': 'admin_Semeente', 'email': 'contato.luzengenharia@gmail.com',
     'senha': '12345678', 'perfil': 'admin', 'data_assinatura': '2023/06/05 18:00:00',
     'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA'},

]

grupo_lista = [
    {'nome': 'ELÉTRICO', 'empresa': 'manluz.ltda'},
    {'nome': 'HIDRÁULICO', 'empresa': 'manluz.ltda'},
    {'nome': 'ESQUADRIA', 'empresa': 'manluz.ltda'},
    {'nome': 'MECÂNICO', 'empresa': 'manluz.ltda'},
]

subgrupo_lista = [
    {'nome': 'ILUMINAÇÃO', 'grupo': 'ELÉTRICO'},
    {'nome': 'TOMADAS', 'grupo': 'ELÉTRICO'},
    {'nome': 'LOUÇAS', 'grupo': 'HIDRÁULICO'},
    {'nome': 'PORTAS', 'grupo': 'ESQUADRIA'},
    {'nome': 'JANELAS', 'grupo': 'ESQUADRIA'},
    {'nome': 'GERADOR', 'grupo': 'ELÉTRICO'},
    {'nome': 'SUBESTAÇÃO', 'grupo': 'ELÉTRICO'},
    {'nome': 'REFRIGERAÇÃO', 'grupo': 'MECÂNICO'},
    {'nome': 'FROTA', 'grupo': 'MECÂNICO'},
]

pavimento_lista = [
    {'nome': 'SUBSOLO 01', 'sigla': 'SUB01', 'empresa': 'manluz.ltda'},
    {'nome': 'SUBSOLO 02', 'sigla': 'SUB02', 'empresa': 'manluz.ltda'},
    {'nome': 'TÉRREO', 'sigla': 'TERRE', 'empresa': 'manluz.ltda'},
    {'nome': 'MEZANINO', 'sigla': 'MEZAN', 'empresa': 'manluz.ltda'},
    {'nome': '1º ANDAR', 'sigla': 'PAV01', 'empresa': 'manluz.ltda'},
    {'nome': '2º ANDAR', 'sigla': 'PAV02', 'empresa': 'manluz.ltda'},
    {'nome': '3º ANDAR', 'sigla': 'PAV03', 'empresa': 'manluz.ltda'},
    {'nome': '4º ANDAR', 'sigla': 'PAV04', 'empresa': 'manluz.ltda'},
    {'nome': 'TERRAÇO', 'sigla': 'TERRA', 'empresa': 'manluz.ltda'},
]

setor_lista = [
    {'nome': 'DIRETORIA', 'sigla': 'DIRET', 'empresa': 'manluz.ltda'},
    {'nome': 'PORTARIA', 'sigla': 'PORTA', 'empresa': 'manluz.ltda'},
    {'nome': 'RH', 'sigla': 'RH', 'empresa': 'manluz.ltda'},
    {'nome': 'ADMINISTRAÇÃO', 'sigla': 'ADMIN', 'empresa': 'manluz.ltda'},
    {'nome': 'LOGÍSTICA', 'sigla': 'LOGIS', 'empresa': 'manluz.ltda'},
    {'nome': 'TI', 'sigla': 'TI', 'empresa': 'manluz.ltda'},
    {'nome': 'COMERCIAL', 'sigla': 'COMER', 'empresa': 'manluz.ltda'},
    {'nome': 'MANUTENÇÃO', 'sigla': 'MANUT', 'empresa': 'manluz.ltda'},
]

locais_lista = [
    {'nome': 'WC PRIVATIVO', 'sigla': 'WCPRI', 'setor': 'DIRETORIA'},
    {'nome': 'SALA REUNIÃO', 'sigla': 'SLREU', 'setor': 'DIRETORIA'},
    {'nome': 'WC FEMININO', 'sigla': 'WCFEM', 'setor': 'RH'},
    {'nome': 'WC MASCULINO', 'sigla': 'WCMAS', 'setor': 'RH'},
    {'nome': 'COPA', 'sigla': 'COPA', 'setor': 'ADMINISTRAÇÃO'},
    {'nome': 'LAVADOR PEÇAS', 'sigla': 'LAPEC', 'setor': 'MANUTENÇÃO'},
    {'nome': 'OFICINA ELÉTRICA', 'sigla': 'OFELE', 'setor': 'MANUTENÇÃO'},
    {'nome': 'OFICINA MECÂNICA', 'sigla': 'OFMEC', 'setor': 'MANUTENÇÃO'},
]

localizacao_lista = [
    {'nome': 'DIRET_WCPRI_PAV04', 'local': 'WC PRIVATIVO', 'pavimento': '4º ANDAR'},
    {'nome': 'DIRET_SLREU_PAV04', 'local': 'SALA REUNIÃO', 'pavimento': '4º ANDAR'},
    {'nome': 'RH_WCFEM_PAV03', 'local': 'WC FEMININO', 'pavimento': '3º ANDAR'},
    {'nome': 'RH_WCMAS_PAV03', 'local': 'WC MASCULINO', 'pavimento': '3º ANDAR'},
    {'nome': 'ADMIN_COPA_PAV02', 'local': 'COPA', 'pavimento': '2º ANDAR'},
    {'nome': 'MANUT_LAPEC_PAV01', 'local': 'LAVADOR PEÇAS', 'pavimento': '1º ANDAR'},
    {'nome': 'MANUT_OFELE_TERRE', 'local': 'OFICINA ELÉTRICA', 'pavimento': 'TÉRREO'},
    {'nome': 'MANUT_OFMEC_SUB01', 'local': 'OFICINA MECÂNICA', 'pavimento': 'SUBSOLO 01'},
]

equipamento_lista = [
    {'cod': 'A.000.001', 'short': 'GERADOR', 'subgrupo': 'GERADOR', 'tag': 'ger.001'},
    {'cod': 'A.000.002', 'short': 'SUBESTAÇÃO 13.8KV', 'subgrupo': 'SUBESTAÇÃO', 'tag': 'se.001'},
    {'cod': 'A.000.003', 'short': 'CHILLER', 'subgrupo': 'REFRIGERAÇÃO', 'tag': 'ch.001'},
    {'cod': 'A.000.004', 'short': 'CARRO', 'subgrupo': 'FROTA', 'tag': 'ca.001'}
]

tipoData_lista = [
    {'nome': 'DATA_FIXA'},
    {'nome': 'DATA_MÓVEL'}]

unidade_lista = [
    {'nome': 'dia'},
    {'nome': 'semana'},
    {'nome': 'mês'},
    {'nome': 'ano'},
]

periodicidade_lista = [
    {'nome': 'DIÁRIA', 'tempo': 1, 'unidade': 'dia'},
    {'nome': 'SEMANAL', 'tempo': 7, 'unidade': 'dia'},
    {'nome': 'MENSAL', 'tempo': 1, 'unidade': 'mês'},
    {'nome': 'BIMENSAL', 'tempo': 2, 'unidade': 'mês'},
    {'nome': 'TRIMENSAL', 'tempo': 3, 'unidade': 'mês'},
    {'nome': 'SEMESTRAL', 'tempo': 6, 'unidade': 'mês'},
    {'nome': 'ANUAL', 'tempo': 12, 'unidade': 'ano'}]

planosmanutencao_lista = [
    {'nome': 'Inspeção Diária Gerador', 'codigo': 'gera0001', 'ativo': True,
     'empresa': 'manluz.ltda', 'data_inicio': str(datetime.datetime.now() + datetime.timedelta(30)),
     'tipo_ordem': 'PREV', 'lista': '20230808192300', 'tecnicos': 1, 'tempo': 10,
     'tipodata': 'DATA_FIXA', 'periodicidade': 'DIÁRIA', 'equipamento': 'A.000.001'},
    {'nome': 'Inspeção Semanal Subestação 13.8KV', 'codigo': 'sube0001', 'ativo': True,
     'empresa': 'manluz.ltda', 'data_inicio': str(datetime.datetime.now() + datetime.timedelta(30)),
     'tipo_ordem': 'PREV', 'lista': None, 'tecnicos': 2, 'tempo': 20,
     'tipodata': 'DATA_FIXA', 'periodicidade': 'SEMANAL', 'equipamento': 'A.000.002'},
    {'nome': 'Manutenção Preventiva Anual Subestação 13.8KV', 'codigo': 'sube0002', 'ativo': True,
     'empresa': 'manluz.ltda', 'data_inicio': str(datetime.datetime.now() + datetime.timedelta(30)),
     'tipo_ordem': 'PREV', 'lista': None, 'tecnicos': 3, 'tempo': 30,
     'tipodata': 'DATA_FIXA', 'periodicidade': 'ANUAL', 'equipamento': 'A.000.002'},
    {'nome': 'Manutenção Preventiva Mensal Chiller', 'codigo': 'chil0001', 'ativo': True,
     'empresa': 'manluz.ltda', 'data_inicio': str(datetime.datetime.now() + datetime.timedelta(30)),
     'tipo_ordem': 'PREV', 'lista': None, 'tecnicos': 4, 'tempo': 40,
     'tipodata': 'DATA_MÓVEL', 'periodicidade': 'MENSAL', 'equipamento': 'A.000.003'},
    {'nome': 'Inspeção Diária Carro 001', 'codigo': 'carr0001', 'ativo': True, 'empresa':
        'manluz.ltda', 'data_inicio': str(datetime.datetime.now() + datetime.timedelta(30)), 'tipo_ordem': 'PREV',
     'tipodata': 'DATA_FIXA', 'lista': None, 'tecnicos': 5, 'tempo': 50,
     'periodicidade': 'DIÁRIA', 'equipamento': 'A.000.004', 'tipo_situacao': 'PENDENTE'},
    {'nome': 'Manutenção Preventiva Semestral Carro', 'codigo': 'carr0002', 'ativo': True,
     'empresa': 'manluz.ltda', 'data_inicio': str(datetime.datetime.now() + datetime.timedelta(30)),
     'tipo_ordem': 'PREV', 'tipodata': 'DATA_FIXA', 'lista': None, 'tecnicos': 6, 'tempo': 60,
     'periodicidade': 'SEMESTRAL', 'equipamento': 'A.000.004'},
]

tipo_ordem_lista = [
    {'nome': 'PREVENTIVA', 'sigla': 'PREV', 'plano': True},
    {'nome': 'PREDITIVA', 'sigla': 'PRED', 'plano': True},
    {'nome': 'AUTÔNOMA', 'sigla': 'AUTO', 'plano': True},
    {'nome': 'CORRETIVA', 'sigla': 'CORR', 'plano': False},
    {'nome': 'MELHORIA', 'sigla': 'MELH', 'plano': False},
]

tipo_parametros_lista = [
    {'nome': 'BINÁRIO'},
    {'nome': 'INTEIRO'},
    {'nome': 'DECIMAL'},
    {'nome': 'TEXTO'},
]

tipo_binario_lista = [
    {'nome': 'SIM'},
    {'nome': 'NÃO'}
]

lista_atividade_lista = [
    {'data': str(datetime.datetime.now()), 'nome': '20230808192300'}
]

atividades_lista = [
    {'lista': '20230808192300', 'posicao': 1, 'descricao': 'Alinhamento da direção', 'plano': 'gera0001',
     'tipo': 'BINÁRIO',
     'valorbinario_id': 'SIM', 'valorinteiro': None, 'valordecimal': None, 'valortexto': None},
    {'lista': '20230808192300', 'posicao': 2, 'descricao': 'Realizar o rodízio de pneus', 'plano': 'gera0001',
     'tipo': 'BINÁRIO', 'valorbinario_id': 'SIM', 'valorinteiro': None, 'valordecimal': None, 'valortexto': None},
    {'lista': '20230808192300', 'posicao': 3, 'descricao': 'Limpeza do radiador', 'plano': 'gera0001',
     'tipo': 'INTEIRO',
     'valorinteiro': 220, 'valorbinario_id': None, 'valordecimal': None, 'valortexto': None},
    {'lista': '20230808192300', 'posicao': 4, 'descricao': 'Realizar a troca de óleo', 'plano': 'gera0001',
     'tipo': 'INTEIRO', 'valorinteiro': 10, 'valorbinario_id': None, 'valordecimal': None, 'valortexto': None},
    {'lista': '20230808192300', 'posicao': 5, 'descricao': 'Trocar as palhetas', 'plano': 'gera0001', 'tipo': 'DECIMAL',
     'valordecimal': 10.5, 'valorinteiro': None, 'valorbinario_id': None, 'valortexto': None},
    {'lista': '20230808192300', 'posicao': 6, 'descricao': 'Verificar as lâmpadas internas', 'plano': 'gera0001',
     'tipo': 'DECIMAL', 'valordecimal': -1.45, 'valorinteiro': None, 'valorbinario_id': None, 'valortexto': None},
    {'lista': '20230808192300', 'posicao': 7, 'descricao': 'Trocar os filtro de ar', 'plano': 'gera0001',
     'tipo': 'DECIMAL',
     'valordecimal': -45, 'valorinteiro': None, 'valorbinario_id': None, 'valortexto': None},
    {'lista': '20230808192300', 'posicao': 8, 'descricao': 'Verificar as velas de ignição', 'plano': 'gera0001',
     'tipo': 'TEXTO', 'valortexto': 'Testando o campo', 'valorinteiro': None, 'valordecimal': None,
     'valorbinario_id': None},
    {'lista': '20230808192300', 'posicao': 9, 'descricao': 'Realizar a limpeza do ar condicionado', 'plano': 'gera0001',
     'tipo': 'TEXTO', 'valortexto': 'outro valor', 'valorinteiro': None, 'valordecimal': None, 'valorbinario_id': None},
]

tipo_situacao_ordem_lista = [
    {'nome': 'Aguardando Aprovação', 'sigla': 'AGAP'},
    {'nome': 'Pendente', 'sigla': 'PEND'},
    {'nome': 'Em execução', 'sigla': 'EXEC'},
    {'nome': 'Aguardando Serviços', 'sigla': 'AGSE'},
    {'nome': 'Aguardando Material', 'sigla': 'AGMT'},
    {'nome': 'Paralizada', 'sigla': 'PARA'},
    {'nome': 'Cancelada', 'sigla': 'CANC'},
    {'nome': 'Concluída', 'sigla': 'CONC'},
    {'nome': 'Fiscalizada', 'sigla': 'FISC'},
]

fluxo_ordem_lista = [
    {'de': 'AGAP', 'para': 'PEND'},
    {'de': 'PEND', 'para': 'EXEC'},
    {'de': 'EXEC', 'para': 'CONC'},
    {'de': 'EXEC', 'para': 'AGSE'},
    {'de': 'EXEC', 'para': 'AGMT'},
    {'de': 'EXEC', 'para': 'PARA'},
    {'de': 'EXEC', 'para': 'CANC'},
    {'de': 'CANC', 'para': 'FISC'},
    {'de': 'CONC', 'para': 'FISC'},
    {'de': 'AGSE', 'para': 'EXEC'},
    {'de': 'AGMT', 'para': 'EXEC'},
    {'de': 'PARA', 'para': 'EXEC'},
]

ordem_servico_lista = [
    {'codigo': 1001, 'descricao': 'Trocar Lâmpada Queimada', 'data_abertura': '2023/01/02 08:00:00',
     'data_fechamento': None, 'equipamento': 'A.000.002', 'situacaoordem': 'AGAP', 'tipo': 'PREV',
     'planomanutencao': None, 'solicitante': 'leandro'},
    {'codigo': 1002, 'descricao': 'Inspeção Diária Gerador', 'data_abertura': '2023/02/02 08:00:00',
     'data_fechamento': None, 'equipamento': 'A.000.001', 'situacaoordem': 'AGAP', 'tipo': 'PREV',
     'planomanutencao': 'gera0001', 'solicitante': 'leandro'},
    {'codigo': 1003, 'descricao': 'Corrigir o vazamento de óleo lubricante', 'tipo': 'CORR',
     'data_abertura': '2023/02/03 08:00:00',
     'data_fechamento': None, 'equipamento': 'A.000.002', 'situacaoordem': 'AGAP',
     'planomanutencao': None, 'solicitante': 'leandro'},
    {'codigo': 1004, 'descricao': 'Manutenção Preventiva Semestral Carro', 'tipo': 'PREV',
     'data_abertura': '2023/01/02 08:00:00',
     'data_fechamento': None, 'equipamento': 'A.000.004', 'situacaoordem': 'AGAP',
     'planomanutencao': 'carr0002', 'solicitante': 'leandro'},
]

tramitacao_lista = [
    {'ordem_servico': 1, 'usuario': 'leandro', 'situacaoordem': 'AGAP',
     'data': '2023/01/02 08:00:00', 'observacao': 'Abertura de Ordem de Serviço'},
    {'ordem_servico': 1, 'usuario': 'leandro', 'situacaoordem': 'PEND',
     'data': '2023/01/03 08:00:00', 'observacao': 'Aprovada a execução da Ordem de Serviço'},
    {'ordem_servico': 1, 'usuario': 'leandro', 'situacaoordem': 'EXEC',
     'data': '2023/01/04 08:00:00',
     'observacao': 'Foi realizada a troca da lâmpada queimada, está operacional'},
    {'ordem_servico': 1, 'usuario': 'leandro', 'situacaoordem': 'CONC',
     'data': '2023/01/04 10:00:00', 'observacao': 'Concluída a Ordem de Serviço'},
    {'ordem_servico': 1, 'usuario': 'leandro', 'situacaoordem': 'FISC',
     'data': '2023/01/05 08:00:00', 'observacao': 'Fiscalizada a Ordem de Serviço'},

]


def criar_contrato(lista: List[dict]) -> List[Contrato]:
    """
       Cria novos contratos a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações dos novos contratos.
       Returns:
           List[Contrato]: Lista de novos contratos criados e adicionados na base de dados.
       """
    # Criando uma lista de novos contratos para serem adicionados
    novos_contratos = [Contrato(nome=item['nome'], ativo=item['ativo'])
                       for item in lista if item['nome'] not in {c.nome for c in Contrato.query.all()}]

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_contratos)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_contratos)} contratos inseridos com sucesso.')

        # Retornando a lista de novos contratos adicionados
        return novos_contratos
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir contratos: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_telas(lista: List[dict]) -> List[Tela]:
    """
          Cria novas telas a partir de uma lista de dicionários.
          Args:
              lista (List[dict]): Lista de dicionários contendo informações das novas telas.
          Returns:
              List[Tela]: Lista de novas telas criadas e adicionadas na base de dados.
          """
    # Criando uma lista de novas telas para serem adicionadas
    novas_telas = [Tela(nome=item['nome'],
                        icon=item['icon'],
                        url=item['url'],
                        posicao=item['posicao'])
                   for item in lista if item['nome'] not in {t.nome for t in Tela.query.all()}]

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novas_telas)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novas_telas)} telas inseridas com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novas_telas
    except SQLAlchemyError as e:
        log.error(f'Erro ao inserir telas: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_telascontrato(lista: List[dict]) -> List[Telacontrato]:
    """
    Cria as relações entre as telas e os contratos na base de dados.
    Args:
        lista: Uma lista de dicionários contendo os dados das telas e dos contratos.
    Returns:
        Uma lista de objetos Telacontrato que foram adicionados à base de dados.
    """

    telascontratos_existentes = set((tc.tela_id, tc.contrato_id) for tc in Telacontrato.query.all())
    novas_telascontrato = []

    for item in lista:
        tela = Tela.query.filter_by(nome=item['tela']).first()
        contrato = Contrato.query.filter_by(nome=item['contrato']).first()

        if (tela.id, contrato.id) not in telascontratos_existentes:
            telacontrato = Telacontrato(tela=tela, contrato=contrato, ativo=True)
            novas_telascontrato.append(telacontrato)

    try:
        db.session.add_all(novas_telascontrato)
        db.session.commit()
        log.info(f'{len(novas_telascontrato)} telascontrato inseridas com sucesso.')
    except SQLAlchemyError as e:
        log.error(f'Erro ao inserir telacontrato: {e}')
        db.session.rollback()

    return novas_telascontrato


def criar_interessados(lista: List[dict]) -> List[Interessado]:
    """
   Cria novos tipos de empresas a partir de uma lista de dicionários.
   Args:
       lista (List[dict]): Lista de dicionários contendo informações das novos tipos.
   Returns:
       List[Interessado]: Lista de novos tipos de empresa criados e adicionados na base de dados.
   """
    # Criando a lista de novos interessados a serem adicionadas
    novos_interessados = [Interessado(nome_fantasia=item['nome_fantasia'],
                                      cnpj=item['cnpj'],
                                      email=item['email'],
                                      telefone=item['telefone'])
                          for item in lista if item['nome_fantasia'] not in [i.nome_fantasia
                                                                             for i in Interessado.query.all()]]

    try:
        # Adicionando as novos interessados na sessão e realizando o commit
        db.session.add_all(novos_interessados)
        db.session.commit()
        log.info(f'{len(novos_interessados)} Interessados inseridas com sucesso.')

        # Retornando a lista de novas interessados adicionadas
        return novos_interessados
    except Exception as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Interessados: {e}')
        db.session.rollback()
        return []


def criar_tipos_empresa(lista: List[dict]) -> List[Tipoempresa]:
    """
   Cria novos tipos de empresas a partir de uma lista de dicionários.
   Args:
       lista (List[dict]): Lista de dicionários contendo informações das novos tipos.
   Returns:
       List[Tipoempresa]: Lista de novos tipos de empresa criados e adicionados na base de dados.
   """

    # Criando a lista de novas periodicidades a serem adicionadas
    novos_tipos_empresa = [Tipoempresa(nome=item['nome'])
                           for item in lista if item['nome'] not in [tp.nome
                                                                     for tp in Tipoempresa.query.all()]]

    try:
        # Adicionando as novas periodicidades na sessão e realizando o commit
        db.session.add_all(novos_tipos_empresa)
        db.session.commit()
        log.info(f'{len(novos_tipos_empresa)} Tipos de empresas inseridas com sucesso.')

        # Retornando a lista de novas periodicidades adicionadas
        return novos_tipos_empresa
    except Exception as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Tipo de empresa: {e}')
        db.session.rollback()
        return []


def criar_empresas(lista: List[dict]) -> List[PerfilAcesso]:
    empresas_existentes = {emp.razao_social for emp in Empresa.query.all()}
    tipos_empresas = {tipo.nome: tipo for tipo in Tipoempresa.query.all()}
    contratos = {contrato.nome: contrato for contrato in Contrato.query.all()}

    empresas = [
        Empresa(
            razao_social=item['razao_social'],
            nome_fantasia=item['nome_fantasia'],
            cnpj=item['cnpj'],
            cep=item['cep'],
            logradouro=item['logradouro'],
            bairro=item['bairro'],
            municipio=item['municipio'],
            uf=item['uf'],
            numero=item['numero'],
            complemento=item['complemento'],
            email=item['email'],
            telefone=item['telefone'],
            ativo=True,
            data_cadastro=item['data_cadastro'],
            contrato=contratos[item['contrato']],
            tipoempresa=tipos_empresas[item['tipo']],
            empresa_gestora_id=Empresa.query.filter_by(razao_social=item['empresa_gestora']).first()
        )
        for item in lista
        if item['razao_social'] not in empresas_existentes
    ]

    try:
        db.session.add_all(empresas)
        db.session.commit()
        # log.info(f'{len(empresas)} Empresas inseridas com sucesso.')
        return empresas
    except Exception as e:
        log.error(f'Erro ao inserir Empresas: {e}')
        db.session.rollback()
        return []


def criar_perfis(lista: List[dict]) -> List[PerfilAcesso]:
    """
   Cria novos perfis a partir de uma lista de dicionários.
   Args:
       lista (List[dict]): Lista de dicionários contendo informações de novos perfis.
   Returns:
       List[PerfilAcesso]: Lista de novos perfis criados e adicionados na base de dados.
   """

    empresas = {e.razao_social: e.id for e in Empresa.query.all()}

    # Criando a lista de novas perfis a serem adicionadas
    novos_perfis = [PerfilAcesso(nome=item['nome'],
                                 descricao=item['descricao'],
                                 ativo=item['ativo'],
                                 empresa_id=empresas[item['empresa']])
                    for item in lista if item['nome'] not in [pe.nome
                                                              for pe in PerfilAcesso.query.all()]]

    try:
        # Adicionando as novas perfis na sessão e realizando o commit
        db.session.add_all(novos_perfis)
        db.session.commit()
        log.info(f'{len(novos_perfis)} Perfis inseridas com sucesso.')

        # Retornando a lista de novos perfis
        return novos_perfis
    except Exception as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir PerfilAcesso: {e}')
        db.session.rollback()
        return []


def criar_telasperfil(lista: List[dict]) -> List[TelaPerfilAcesso]:
    """
   Cria novos perfis a partir de uma lista de dicionários.
   Args:
       lista (List[dict]): Lista de dicionários contendo informações de novos perfis.
   Returns:
       List[PerfilAcesso]: Lista de novos perfis criados e adicionados na base de dados.
   """

    telasperfis = []

    for item in lista:
        empresa = Empresa.query.filter_by(razao_social=item['empresa']).one_or_none()
        perfilacesso = PerfilAcesso.query.filter_by(nome=item['role'], empresa_id=empresa.id).one_or_none()
        tela = Tela.query.filter_by(nome=item['tela']).one_or_none()
        telaperfil = TelaPerfilAcesso.query.filter_by(tela_id=tela.id, perfilacesso_id=perfilacesso.id).one_or_none()

        if not telaperfil:
            telasperfis.append(TelaPerfilAcesso(perfilacesso_id=perfilacesso.id, tela_id=tela.id, ativo=True))

    try:
        db.session.add_all(telasperfis)
        db.session.commit()
        log.info(f'{len(telasperfis)} TelasPerfil inseridas com sucesso.')
        return telasperfis
    except Exception as e:
        log.error(f'Erro ao inserir telaperfil: {e}')
        db.session.rollback()
        return []


def criar_senhas(lista: List[dict]) -> List[Senha]:
    """
   Cria novos perfis a partir de uma lista de dicionários.
   Args:
       lista (List[dict]): Lista de dicionários contendo informações de novos perfis.
   Returns:
       List[PerfilAcesso]: Lista de novos perfis criados e adicionados na base de dados.
   """

    # Criando a lista de novas perfis a serem adicionadas
    senhas_existentes = {se.senha for se in Senha.query.all()}
    novas_senhas = [Senha(senha=item['senha'],
                          data_expiracao=item['data_expiracao'],
                          senha_temporaria=item['senha_temporaria'],
                          senha_expira=item['senha_expira'])
                    for item in lista if item['senha'] not in senhas_existentes]

    try:
        db.session.add_all(novas_senhas)
        db.session.commit()
        log.info(f'{len(novas_senhas)} Senhas inseridas com sucesso.')
        # Retornando a lista de novas senhas
        return novas_senhas
    except Exception as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Senha: {e}')
        db.session.rollback()
        return []


def criar_usuarios(lista: List[dict]) -> List[Usuario]:
    """
       Cria novos tipos de datas para os planos de manutenção.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das datas.
       Returns:
           List[TipoData]: Lista das novas datas e adicionados na base de dados.
       """

    empresas = {e.razao_social: e.id for e in Empresa.query.all()}
    senhas = {s.senha: s.id for s in Senha.query.all()}
    usuarios = {u.nome: u.id for u in Usuario.query.all()}

    novos_usuarios = []
    for item in lista:
        if item['nome'] not in usuarios:
            perfis = {p.nome: p.id for p in PerfilAcesso.query.filter_by(empresa_id=empresas[item['empresa']])}

            usuario = Usuario(nome=item['nome'],
                              email=item['email'],
                              data_assinatura=item['data_assinatura'],
                              ativo=True,
                              senha_id=senhas[item['senha']],
                              perfilacesso_id=perfis[item['perfil']],
                              empresa_id=empresas[item['empresa']])

            novos_usuarios.append(usuario)

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_usuarios)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_usuarios)} Usuários inseridos com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novos_usuarios
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir usuario: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
    return []


def criar_grupo(lista: List[dict]) -> List[Grupo]:
    """
       Cria novos tipos de datas para os planos de manutenção.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das datas.
       Returns:
           List[TipoData]: Lista das novas datas e adicionados na base de dados.
       """

    empresas = {e.razao_social: e.id for e in Empresa.query.all()}

    # Criando uma lista de novos tipodatas para serem adicionados
    novos_grupos = [Grupo(nome=item['nome'],
                          empresa_id=empresas[item['empresa']])
                    for item in lista if item['nome'] not in [gr.nome for gr in Grupo.query.all()]]

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_grupos)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_grupos)} Grupos inseridos com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novos_grupos
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir grupos: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_subgrupo(lista: List[dict]) -> List[Subgrupo]:
    """
       Cria novos subgrupos.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações subgrupos.
       Returns:
           List[TipoData]: Lista subgrupos adicionados na base de dados.
       """

    grupos = {g.nome: g.id for g in Grupo.query.all()}

    # Criando uma lista de novos tipodatas para serem adicionados
    novos_subgrupos = [Subgrupo(nome=item['nome'],
                                grupo_id=grupos[item['grupo']])
                       for item in lista if item['nome'] not in [sg.nome for sg in Subgrupo.query.all()]]

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_subgrupos)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_subgrupos)} Subgrupos inseridos com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novos_subgrupos
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Subgrupos: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_pavimento(lista: List[dict]) -> List[Pavimento]:
    """
       Cria novos tipos de datas para os planos de manutenção.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das datas.
       Returns:
           List[TipoData]: Lista das novas datas e adicionados na base de dados.
       """

    empresas = {e.razao_social: e.id for e in Empresa.query.all()}

    # Criando uma lista de novos tipodatas para serem adicionados
    novos_pavimentos = [Pavimento(nome=item['nome'],
                                  sigla=item['sigla'],
                                  empresa_id=empresas[item['empresa']])
                        for item in lista if item['nome'] not in [pav.nome for pav in Pavimento.query.all()]]

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_pavimentos)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_pavimentos)} Pavimentos inseridos com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novos_pavimentos
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir pavimentos: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_setor(lista: List[dict]) -> List[Setor]:
    """
       Cria novos tipos de datas para os planos de manutenção.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das datas.
       Returns:
           List[TipoData]: Lista das novas datas e adicionados na base de dados.
       """

    empresas = {e.razao_social: e.id for e in Empresa.query.all()}

    # Criando uma lista de novos tipodatas para serem adicionados
    novos_setores = [Setor(nome=item['nome'],
                           sigla=item['sigla'],
                           empresa_id=empresas[item['empresa']])
                     for item in lista if item['nome'] not in [s.nome for s in Setor.query.all()]]

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_setores)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_setores)} Setores inseridos com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novos_setores
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir setores: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_locais(lista: List[dict]) -> List[Local]:
    """
       Cria novos tipos de datas para os planos de manutenção.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das datas.
       Returns:
           List[TipoData]: Lista das novas datas e adicionados na base de dados.
       """

    setores = {se.nome: se.id for se in Setor.query.all()}

    # Criando uma lista de novos tipodatas para serem adicionados
    novos_locais = [Local(nome=item['nome'],
                          sigla=item['sigla'],
                          setor_id=setores[item['setor']])
                    for item in lista if item['nome'] not in [lo.nome for lo in Local.query.all()]]

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_locais)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_locais)} Locais inseridos com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novos_locais
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir locais: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_localizacao(lista: List[dict]) -> List[Localizacao]:
    """
       Cria novos tipos de datas para os planos de manutenção.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das datas.
       Returns:
           List[TipoData]: Lista das novas datas e adicionados na base de dados.
       """

    locais = {lo.nome: lo.id for lo in Local.query.all()}
    pavimentos = {p.nome: p.id for p in Pavimento.query.all()}

    # Criando uma lista de novos tipodatas para serem adicionados
    novas_localizacoes = [Localizacao(nome=item['nome'],
                                      local_id=locais[item['local']],
                                      pavimento_id=pavimentos[item['pavimento']])
                          for item in lista if item['nome'] not in [lo.nome for lo in Localizacao.query.all()]]

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novas_localizacoes)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novas_localizacoes)} Localizações inseridos com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novas_localizacoes
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir localizações: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_equipamento(lista: List[dict]) -> List[Equipamento]:
    """
       Cria novos tipos de datas para os planos de manutenção.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das datas.
       Returns:
           List[TipoData]: Lista das novas datas e adicionados na base de dados.
       """

    subgrupos = {sg.nome: sg.id for sg in Subgrupo.query.all()}

    # Criando uma lista de novos tipodatas para serem adicionados
    novos_equipamentos = [Equipamento(cod=item['cod'],
                                      descricao_curta=item['short'],
                                      tag=item['tag'],
                                      subgrupo_id=subgrupos[item['subgrupo']]
                                      )
                          for item in lista if item['cod'] not in [si.cod for si in Equipamento.query.all()]]

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_equipamentos)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_equipamentos)} Equipamentos inseridos com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novos_equipamentos
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir equipamentos: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_tipodata(lista: List[dict]) -> List[TipoData]:
    """
       Cria novos tipos de datas para os planos de manutenção.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das datas.
       Returns:
           List[TipoData]: Lista das novas datas e adicionados na base de dados.
       """

    # Criando uma lista de novos tipodatas para serem adicionados
    novos_tipodata = [TipoData(nome=item['nome'])
                      for item in lista if item['nome'] not in [tp.nome for tp in TipoData.query.all()]]
    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_tipodata)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_tipodata)} Tipo de data inseridos com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novos_tipodata
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir contratos: {e}')
        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_unidades(lista: List[dict]) -> List[Unidade]:
    """
       Cria novas unidades a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das novas unidades.
       Returns:
           List[Unidade]: Lista de novas unidades criados e adicionados na base de dados.
       """
    # Criando uma lista de novas unidades para serem adicionados
    novas_unidade = [Unidade(nome=item['nome'])
                     for item in lista if item['nome'] not in [u.nome for u in Unidade.query.all()]]
    try:
        # Adicionando as novas unidades na sessão e realizando o commit
        db.session.add_all(novas_unidade)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novas_unidade)} unidades inseridas com sucesso.')

        # Retornando a lista de novas unidades adicionados
        return novas_unidade
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir unidades: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_periodicidades(lista: List[dict]) -> List[Periodicidade]:
    """
   Cria novas periodicidades a partir de uma lista de dicionários.
   Args:
       lista (List[dict]): Lista de dicionários contendo informações das novas periodicidades.
   Returns:
       List[Unidade]: Lista de novas periodicidades criados e adicionados na base de dados.
   """

    # Buscando todas as unidades existentes no banco de dados
    unidades = {u.nome: u.id for u in Unidade.query.all()}

    # Criando a lista de novas periodicidades a serem adicionadas
    novas_periodicidades = [Periodicidade(nome=item['nome'],
                                          tempo=item['tempo'],
                                          unidade_id=unidades[item['unidade']])
                            for item in lista if item['nome'] not in [p.nome
                                                                      for p in Periodicidade.query.all()]]

    try:
        # Adicionando as novas periodicidades na sessão e realizando o commit
        db.session.add_all(novas_periodicidades)
        db.session.commit()
        log.info(f'{len(novas_periodicidades)} periodicidades inseridas com sucesso.')

        # Retornando a lista de novas periodicidades adicionadas
        return novas_periodicidades
    except Exception as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir periodicidades: {e}')
        db.session.rollback()
        return []


def criar_planosmanutencao(lista: List[dict]) -> List[PlanoManutencao]:
    # Buscando os objetos necessários
    tipodatas = {t.nome: t.id for t in TipoData.query.all()}
    periodicidades = {p.nome: p.id for p in Periodicidade.query.all()}
    equipamentos = {e.cod: e.id for e in Equipamento.query.all()}
    tipos_ordem = {to.sigla: to.id for to in TipoOrdem.query.all()}
    listas_atividades = {la.nome: la.id for la in ListaAtividade.query.all()}

    novos_planosmanutencao = [
        PlanoManutencao(nome=item['nome'],
                        codigo=item['codigo'],
                        ativo=item['ativo'],
                        tipodata_id=tipodatas[item['tipodata']],
                        data_inicio=item['data_inicio'],
                        total_tecnico=item['tecnicos'],
                        tempo_estimado=item['tempo'],
                        periodicidade_id=periodicidades[item['periodicidade']],
                        equipamento_id=equipamentos[item['equipamento']],
                        tipoordem_id=tipos_ordem[item['tipo_ordem']],
                        listaatividade_id=listas_atividades[item['lista']]
                        if item['lista'] else None)
        for item in lista if item['codigo'] not in [pm.código for pm in PlanoManutencao.query.all()]]

    try:
        # Adicionando as novas periodicidades na sessão e realizando o commit
        db.session.add_all(novos_planosmanutencao)
        db.session.commit()
        log.info(f'{len(novos_planosmanutencao)} planos de manutenção inseridos com sucesso.')

        # Retornando a lista de novas periodicidades adicionadas
        return novos_planosmanutencao
    except Exception as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir periodicidades: {e}')
        db.session.rollback()
        return []


def criar_tipos_parametros(lista: List[dict]) -> List[TipoParametro]:
    """
       Cria novos tipos de parametros a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações dos novos tipos de parametros.
       Returns:
           List[Unidade]: Lista de novos tipos de parametros criados e adicionados na base de dados.
       """

    # Criando uma lista de novas unidades para serem adicionados
    novos_tipos = [TipoParametro(nome=item['nome'])
                   for item in lista if item['nome'] not in [t.nome for t in TipoParametro.query.all()]]
    try:
        # Adicionando os novos tipos de atividade na sessão e realizando o commit
        db.session.add_all(novos_tipos)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_tipos)} tipos de parametros inseridos com sucesso.')

        # Retornando a lista de novos tipos de atividades adicionados
        return novos_tipos
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao tipo de parametros: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_lista_atividades(lista: List[dict]) -> List[ListaAtividade]:
    """
       Cria novas listas de atividades a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das novas listas de atividades
       Returns:
           List[Unidade]: Lista de novas listas de atividadescriados e adicionados na base de dados.
       """

    # Criando uma lista de novas unidades para serem adicionados
    novas_listas = [ListaAtividade(nome=item['nome'],
                                   data=item['data'])
                    for item in lista if item['nome'] not in [la.nome for la in ListaAtividade.query.all()]]
    try:
        # Adicionando as novas listas de atividades na sessão e realizando o commit
        db.session.add_all(novas_listas)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novas_listas)} Nova listas de atividades inseridas com sucesso.')

        # Retornando a lista de novas listas de atividades adicionados
        return novas_listas
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Nova lista de atividade: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_tipo_binarios(lista: List[dict]) -> List[TipoBinario]:
    """
       Cria novas listas de atividades a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das novas listas de atividades
       Returns:
           List[Unidade]: Lista de novas listas de atividadescriados e adicionados na base de dados.
       """

    # Criando uma lista de novas unidades para serem adicionados
    novos_binarios = [TipoBinario(nome=item['nome'])
                      for item in lista if item['nome'] not in [tb.nome for tb in TipoBinario.query.all()]]
    try:
        # Adicionando as novas listas de atividades na sessão e realizando o commit
        db.session.add_all(novos_binarios)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_binarios)} Novos Tipos Binários inseridas com sucesso.')

        # Retornando a lista de novas listas de atividades adicionados
        return novos_binarios
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Novo Tipo Binário: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_atividades(lista: List[dict]) -> List[Atividade]:
    # Buscando os objetos necessários

    tipos = {tp.nome: tp.id for tp in TipoParametro.query.all()}
    listas = {la.nome: la.id for la in ListaAtividade.query.all()}
    tipobinarios = {tb.nome: tb.id for tb in TipoBinario.query.all()}

    novas_listas = [
        Atividade(
            posicao=item['posicao'],
            descricao=item['descricao'],
            valorbinario_id=tipobinarios[item['valorbinario_id']]
            if item['valorbinario_id'] else None,
            valorinteiro=item['valorinteiro'],
            valordecimal=item['valordecimal'],
            valortexto=item['valortexto'],
            tipoparametro_id=tipos[item['tipo']],
            listaatividade_id=listas[item['lista']]) for item in lista]

    try:
        # Adicionando as novas periodicidades na sessão e realizando o commit
        db.session.add_all(novas_listas)
        db.session.commit()
        log.info(f'{len(novas_listas)} Atividades inseridos com sucesso.')

        # Retornando a lista de novas periodicidades adicionadas
        return novas_listas
    except Exception as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir atividades: {e}')
        db.session.rollback()
        return []


def criar_tipo_ordem(lista: List[dict]) -> List[TipoOrdem]:
    """
   Cria novos tipos de ordem a partir de uma lista de dicionários.
   Args:
       lista (List[dict]): Lista de dicionários contendo informações das novos tipos de ordem.
   Returns:
       List[Unidade]: Lista de novos tipos de ordem criados e adicionados na base de dados.
   """

    # Criando a lista de novas periodicidades a serem adicionadas
    novos_tipos = [TipoOrdem(nome=item['nome'], sigla=item['sigla'], plano=item['plano'])
                   for item in lista if item['nome'] not in [t.nome for t in TipoOrdem.query.all()]]

    try:
        # Adicionando as novas periodicidades na sessão e realizando o commit
        db.session.add_all(novos_tipos)
        db.session.commit()
        log.info(f'{len(novos_tipos)} periodicidades inseridas com sucesso.')

        # Retornando a lista de novas periodicidades adicionadas
        return novos_tipos
    except Exception as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir novo tipos de ordem de serviço: {e}')
        db.session.rollback()
        return []


def criar_tipo_situacao_ordem(lista: List[dict]) -> List[TipoSituacaoOrdem]:
    """
       Cria novas situações de ordens de serviços a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações dos novas situações.
       Returns:
           List[Contrato]: Lista de novas situações criados e adicionados na base de dados.
       """
    # Criando um conjunto de situações de ordens existentes na base de dados
    situacoes_ordem_existentes = set(so.nome for so in TipoSituacaoOrdem.query.all())
    # Criando uma lista de novas situações de ordens para serem adicionados
    novas_situacoes_ordem = [TipoSituacaoOrdem(nome=item['nome'],
                                               sigla=item['sigla'])
                             for item in lista if item['nome'] not in situacoes_ordem_existentes]

    try:
        # Adicionando as novas situações na sessão e realizando o commit
        db.session.add_all(novas_situacoes_ordem)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novas_situacoes_ordem)} Tipos de situações das ordens inseridas com sucesso.')

        # Retornando a lista de novas situações de ordens adicionados
        return novas_situacoes_ordem
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Tipo de situações das ordens: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_ordem_servico(lista: List[dict]) -> List[OrdemServico]:
    """
       Criar ordens de serviços a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações de ordens de serviços.
       Returns:
           List[Contrato]: Lista de novas ordens de serviços criadas e adicionados na base de dados.
       """
    # Lista de equipamentos do banco de dados
    equipamentos = {e.cod: e.id for e in Equipamento.query.all()}
    situacoes_ordem = {so.sigla: so.id for so in TipoSituacaoOrdem.query.all()}
    planosmanutencao = {pm.codigo: pm.id for pm in PlanoManutencao.query.all()}
    solicitantes = {u.nome: u.id for u in Usuario.query.all()}
    tipos_ordem = {t.sigla: t.id for t in TipoOrdem.query.all()}

    # Criando uma lista de novas ordens para serem adicionados
    novas_ordens_servicos = [OrdemServico(codigo=item['codigo'],
                                          descricao=item['descricao'],
                                          data_abertura=item['data_abertura'],
                                          equipamento_id=equipamentos[item['equipamento']],
                                          tiposituacaoordem_id=situacoes_ordem[item['situacaoordem']],
                                          solicitante_id=solicitantes[item['solicitante']],
                                          tipoordem_id=tipos_ordem[item['tipo']],
                                          planomanutencao_id=planosmanutencao[item['planomanutencao']]
                                          if item['planomanutencao'] else None)
                             for item in lista]

    try:
        # Adicionando as novas ordens de serviços na sessão e realizando o commit
        db.session.add_all(novas_ordens_servicos)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novas_ordens_servicos)} Ordens de Serviços inseridas com sucesso.')

        # Retornando a lista de novas ordens de serviços adicionados
        return novas_ordens_servicos
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Ordem de Serviço: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_tramitacao(lista: List[dict]) -> List[TramitacaoOrdem]:
    """
       Criar as tramitações de ordens de serviços a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das tramitações.
       Returns:
           List[Tramitação]: Lista de novas tramitações de ordens de serviços criadas e adicionados na base de dados.
       """

    # Listas dos objetos necessários
    usuarios = {u.nome: u.id for u in Usuario.query.all()}
    situacoes_ordem = {so.sigla: so.id for so in TipoSituacaoOrdem.query.all()}

    # Criando uma lista de novas ordens para serem adicionados
    novas_tramitacoes = [TramitacaoOrdem(
        ordemservico_id=item['ordem_servico'],
        usuario_id=usuarios[item['usuario']],
        tiposituacaoordem_id=situacoes_ordem[item['situacaoordem']],
        data=item['data'],
        observacao=item['observacao'])
        for item in lista]

    try:
        # Adicionando as novas ordens de serviços na sessão e realizando o commit
        db.session.add_all(novas_tramitacoes)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novas_tramitacoes)} Tramitações inseridas com sucesso.')

        # Retornando a lista de novas ordens de serviços adicionados
        return novas_tramitacoes
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Tramitação: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


def criar_fluxo_ordem(lista: List[dict]) -> List[FluxoOrdem]:
    """
       Cria novas situações de ordens de serviços a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações dos novas situações.
       Returns:
           List[Contrato]: Lista de novas situações criados e adicionados na base de dados.
       """
    # Criando um conjunto de situações de ordens existentes na base de dados
    situacoes_ordem = {so.sigla: so.id for so in TipoSituacaoOrdem.query.all()}

    # Criando uma lista de novas situações de ordens para serem adicionados
    novos_fluxos = [FluxoOrdem(de=situacoes_ordem[item['de']], para=situacoes_ordem[item['para']])
                    for item in lista]

    try:
        # Adicionando as novas situações na sessão e realizando o commit
        db.session.add_all(novos_fluxos)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_fluxos)} Fluxos de ordem serviço inseridas com sucesso.')

        # Retornando a lista de novas situações de ordens adicionados
        return novos_fluxos
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Fluxo de ordem de serviço: {e}')

        # Realizando o rollback da transação e retornando uma lista vazia
        db.session.rollback()
        return []


# carregamento para as empresas
criar_contrato(contratos_lista)
criar_telas(telas_lista)
criar_telascontrato(telascontrato_lista)
criar_interessados(interessado_lista)
criar_tipos_empresa(tipo_empresa_lista)
criar_empresas(empresa_lista)

# carregamento para os perfis e usuários
criar_perfis(perfis_lista)
criar_telasperfil(telasperfil_lista)
criar_senhas(senha_lista)
criar_usuarios(usuario_lista)

# carregamento para os equipamentos
criar_grupo(grupo_lista)
criar_subgrupo(subgrupo_lista)
criar_pavimento(pavimento_lista)
criar_setor(setor_lista)
criar_locais(locais_lista)
criar_localizacao(localizacao_lista)
criar_equipamento(equipamento_lista)

# carregamento para os fornecedores
criar_tipo_ordem(tipo_ordem_lista)
criar_tipodata(tipoData_lista)
criar_unidades(unidade_lista)
criar_periodicidades(periodicidade_lista)

criar_tipos_parametros(tipo_parametros_lista)
criar_lista_atividades(lista_atividade_lista)
criar_tipo_binarios(tipo_binario_lista)
criar_atividades(atividades_lista)
criar_planosmanutencao(planosmanutencao_lista)

criar_tipo_situacao_ordem(tipo_situacao_ordem_lista)
criar_fluxo_ordem(fluxo_ordem_lista)
criar_ordem_servico(ordem_servico_lista)
criar_tramitacao(tramitacao_lista)

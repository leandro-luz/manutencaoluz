import datetime
import os

from funcoes_sistema import *

from webapp import create_app
from webapp import db

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('config.%sConfig' % env.capitalize())
app.app_context().push()

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
    {'nome': 'COMPLETO', 'ativo': True, 'empresa': None}
]

subcontratos_lista = [
    {'nome': 'BÁSICO', 'ativo': True, 'empresa': 'manluz.ltda'},
    {'nome': 'INTERMEDIÁRIO', 'ativo': True, 'empresa': 'manluz.ltda'},
]

telascontrato_lista = [
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

telassubcontrato_lista = [
    {'contrato': 'BÁSICO', 'tela': 'Usuário'},
    {'contrato': 'BÁSICO', 'tela': 'Equipamento'},
    {'contrato': 'BÁSICO', 'tela': 'Fornecedor'},
    {'contrato': 'INTERMEDIÁRIO', 'tela': 'Empresa'},
    {'contrato': 'INTERMEDIÁRIO', 'tela': 'Usuário'},
    {'contrato': 'INTERMEDIÁRIO', 'tela': 'Equipamento'},
    {'contrato': 'INTERMEDIÁRIO', 'tela': 'Plano de Manutenção'},
    {'contrato': 'INTERMEDIÁRIO', 'tela': 'Ordem de Serviço'},
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

]

subempresa_lista = [
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

perfil_manutentor_lista = [
    {'nome': 'SOLICITANTE'},
    {'nome': 'APROVADOR'},
    {'nome': 'EXECUTANTE'},
    {'nome': 'FISCALIZADOR'},
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
    {'nome': 'WC PRIVATIVO', 'sigla': 'WCPRI', 'empresa': 'manluz.ltda'},
    {'nome': 'SALA REUNIÃO', 'sigla': 'SLREU', 'empresa': 'manluz.ltda'},
    {'nome': 'WC FEMININO', 'sigla': 'WCFEM', 'empresa': 'manluz.ltda'},
    {'nome': 'WC MASCULINO', 'sigla': 'WCMAS', 'empresa': 'manluz.ltda'},
    {'nome': 'COPA', 'sigla': 'COPA', 'empresa': 'manluz.ltda'},
    {'nome': 'LAVADOR PEÇAS', 'sigla': 'LAPEC', 'empresa': 'manluz.ltda'},
    {'nome': 'OFICINA ELÉTRICA', 'sigla': 'OFELE', 'empresa': 'manluz.ltda'},
    {'nome': 'OFICINA MECÂNICA', 'sigla': 'OFMEC', 'empresa': 'manluz.ltda'},
]

equipamento_lista = [
    {'cod': 'A.000.001', 'short': 'GERADOR', 'subgrupo': 'GERADOR', 'tag': 'ger.001',
     'setor': 'DIRETORIA', 'local': 'WC PRIVATIVO', 'pavimento': '4º ANDAR'},
    {'cod': 'A.000.002', 'short': 'SUBESTAÇÃO 13.8KV', 'subgrupo': 'SUBESTAÇÃO', 'tag': 'se.001',
     'setor': 'DIRETORIA', 'local': 'SALA REUNIÃO', 'pavimento': '4º ANDAR'},
    {'cod': 'A.000.003', 'short': 'CHILLER', 'subgrupo': 'REFRIGERAÇÃO', 'tag': 'ch.001',
     'setor': 'MANUTENÇÃO', 'local': 'LAVADOR PEÇAS', 'pavimento': '1º ANDAR'},
    {'cod': 'A.000.004', 'short': 'CARRO', 'subgrupo': 'FROTA', 'tag': 'ca.001',
     'setor': 'MANUTENÇÃO', 'local': 'OFICINA MECÂNICA', 'pavimento': 'SUBSOLO 01'}
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
    {'nome': 'AGUARDANDO APROVAÇÃO', 'sigla': 'AGAP'},
    {'nome': 'AGUARDANDO EXECUÇÃO', 'sigla': 'AGEX'},
    {'nome': 'AGUARDANDO SERVIÇO EXTERNO', 'sigla': 'AGSE'},
    {'nome': 'AGUARDANDO MATERIAL', 'sigla': 'AGMT'},
    {'nome': 'PARALIZADA', 'sigla': 'PARA'},
    {'nome': 'CANCELADA', 'sigla': 'CANC'},
    {'nome': 'CONCLUÍDA', 'sigla': 'CONC'},
    {'nome': 'AGUARDANDO FISCALIZAÇÃO', 'sigla': 'AGFI'},
    {'nome': 'ENCERRADA', 'sigla': 'ENCE'},
]

situacao_tipo_ordem_perfil_manutentor_lista = [
    {'situacao': 'AGAP', 'perfil': 'APROVADOR'},
    {'situacao': 'AGEX', 'perfil': 'EXECUTANTE'},
    {'situacao': 'AGSE', 'perfil': 'APROVADOR'},
    {'situacao': 'AGMT', 'perfil': 'APROVADOR'},
    {'situacao': 'PARA', 'perfil': 'APROVADOR'},
    {'situacao': 'CANC', 'perfil': 'APROVADOR'},
    {'situacao': 'CANC', 'perfil': 'EXECUTANTE'},
    {'situacao': 'CONC', 'perfil': 'EXECUTANTE'},
    {'situacao': 'AGFI', 'perfil': 'FISCALIZADOR'},
]

fluxo_ordem_lista = [

    {'de': 'AGAP', 'para': 'AGEX'},
    {'de': 'AGAP', 'para': 'CANC'},
    {'de': 'AGEX', 'para': 'CONC'},
    {'de': 'AGEX', 'para': 'AGSE'},
    {'de': 'AGEX', 'para': 'AGMT'},
    {'de': 'AGEX', 'para': 'PARA'},
    {'de': 'AGSE', 'para': 'AGEX'},
    {'de': 'AGMT', 'para': 'AGEX'},
    {'de': 'PARA', 'para': 'AGEX'},
    {'de': 'CANC', 'para': 'AGFI'},
    {'de': 'CONC', 'para': 'AGFI'},
    {'de': 'AGFI', 'para': 'ENCE'},
]

tipo_status_ordem_lista = [
    {'nome': 'PENDENTE', 'sigla': 'PEND'},
    {'nome': 'CONCLUÍDA', 'sigla': 'CONC'},
    {'nome': 'CANCELADA', 'sigla': 'CANC'},
]

ordem_servico_lista = [
    {'codigo': 1001, 'descricao': 'Trocar Lâmpada Queimada', 'data_abertura': '2023/01/02 08:00:00',
     'data_fechamento': None, 'equipamento': 'A.000.002', 'situacaoordem': 'AGAP', 'status': 'PEND', 'tipo': 'PREV',
     'planomanutencao': None, 'solicitante': 'leandro'},
    {'codigo': 1002, 'descricao': 'Inspeção Diária Gerador', 'data_abertura': '2023/02/02 08:00:00',
     'data_fechamento': None, 'equipamento': 'A.000.001', 'situacaoordem': 'AGAP', 'status': 'PEND', 'tipo': 'PREV',
     'planomanutencao': 'gera0001', 'solicitante': 'leandro'},
    {'codigo': 1003, 'descricao': 'Corrigir o vazamento de óleo lubricante', 'tipo': 'CORR',
     'data_abertura': '2023/02/03 08:00:00',
     'data_fechamento': None, 'equipamento': 'A.000.002', 'situacaoordem': 'AGAP', 'status': 'PEND',
     'planomanutencao': None, 'solicitante': 'leandro'},
    {'codigo': 1004, 'descricao': 'Manutenção Preventiva Semestral Carro', 'tipo': 'PREV',
     'data_abertura': '2023/01/02 08:00:00',
     'data_fechamento': None, 'equipamento': 'A.000.004', 'situacaoordem': 'AGAP', 'status': 'PEND',
     'planomanutencao': 'carr0002', 'solicitante': 'leandro'},
]

tramitacao_lista = [
    {'ordem_servico': 1, 'usuario': 'leandro', 'situacaoordem': 'AGAP',
     'data': '2023/01/02 08:00:00', 'observacao': 'Aguardando a liberação para execução'},
    {'ordem_servico': 1, 'usuario': 'leandro', 'situacaoordem': 'AGEX',
     'data': '2023/01/03 08:00:00', 'observacao': 'Aguardando a execução'},
    {'ordem_servico': 1, 'usuario': 'leandro', 'situacaoordem': 'CONC',
     'data': '2023/01/04 10:00:00', 'observacao': 'Concluída a Ordem de Serviço'},
    {'ordem_servico': 1, 'usuario': 'leandro', 'situacaoordem': 'AGFI',
     'data': '2023/01/05 08:00:00', 'observacao': 'Aguardando a fiscalização'},
    {'ordem_servico': 1, 'usuario': 'leandro', 'situacaoordem': 'ENCE',
     'data': '2023/01/05 08:00:00', 'observacao': 'Encerrada a ordem de serviço'},
]

# carregamento para as empresas
criar_contrato(contratos_lista)
criar_telas(telas_lista)
criar_telascontrato(telascontrato_lista)
criar_interessados(interessado_lista)
criar_tipos_empresa(tipo_empresa_lista)
criar_empresas(empresa_lista)

criar_contrato(subcontratos_lista)
criar_telascontrato(telassubcontrato_lista)
criar_empresas(subempresa_lista)

# carregamento para os perfis e usuários
criar_perfis(perfis_lista)
criar_telasperfil(telasperfil_lista)
criar_senhas(senha_lista)
criar_usuarios(usuario_lista)

criar_perfil_manutentor(perfil_manutentor_lista)

# carregamento para os equipamentos
criar_grupo(grupo_lista)
criar_subgrupo(subgrupo_lista)
criar_pavimento(pavimento_lista)
criar_setor(setor_lista)
criar_locais(locais_lista)
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
criar_tipo_situacao_ordem_perfil_manutentor(situacao_tipo_ordem_perfil_manutentor_lista)
criar_tipo_status_ordem(tipo_status_ordem_lista)
criar_fluxo_ordem(fluxo_ordem_lista)
criar_ordem_servico(ordem_servico_lista)
criar_tramitacao(tramitacao_lista)

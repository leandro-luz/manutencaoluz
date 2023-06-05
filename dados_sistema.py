import logging
import datetime
import os
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from webapp import create_app
from webapp import db
from webapp.usuario.models import Perfil, Senha, Usuario, Telaperfil
from webapp.empresa.models import Interessado, Tipoempresa, Empresa
from webapp.equipamento.models import Equipamento, Grupo, Sistema
from webapp.contrato.models import Contrato, Tela, Telacontrato
from webapp.plano_manutencao.models import TipoData, Unidade, Periodicidade, PlanoManutencao
from webapp.ordem_servico.models import SituacaoOrdem, FluxoOrdem, OrdemServico, TramitacaoOrdem

env = os.environ.get('WEBAPP_ENV', 'prod')
app = create_app('config.%sConfig' % env.capitalize())
app.app_context().push()

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

print("Exluindo todas as tabelas")
db.drop_all()
print("Criando todas as tabelas")
db.create_all()

telas_lista = [{'nome': 'Interessado', 'icon': 'bi-card-list', 'url': 'empresa.interessado_listar'},
               {'nome': 'Contrato', 'icon': 'bi-briefcase', 'url': 'contrato.contrato_listar'},
               {'nome': 'Empresa', 'icon': 'bi-house-door', 'url': 'empresa.empresa_listar'},
               {'nome': 'RH', 'icon': 'bi-people', 'url': 'usuario.usuario_listar'},
               {'nome': 'Equipamento', 'icon': 'bi-robot', 'url': 'equipamento.equipamento_listar'},
               {'nome': 'Plano de Manutenção', 'icon': 'bi-clipboard', 'url': 'plano_manutencao.plano_listar'},
               {'nome': 'Ordem de Serviço', 'icon': 'bi-wrench-adjustable-circle', 'url': 'ordem_servico.ordem_listar'},
               {'nome': 'Almoxarifado', 'icon': 'bi-box-seam', 'url': 'sistema.almoxarifado'},
               {'nome': 'Programação', 'icon': 'bi-calendar3', 'url': 'sistema.programação'},
               {'nome': 'Fornecedor', 'icon': 'bi-truck', 'url': 'supplier.supplier_list'},
               {'nome': 'Orçamento', 'icon': 'bi-cash', 'url': 'sistema.orçamento'},
               {'nome': 'Indicadores', 'icon': 'bi-graph-up', 'url': 'sistema.indicador'}
               ]

contratos_lista = [{'nome': 'basico'},
                   {'nome': 'intermediário'},
                   {'nome': 'completo'}
                   ]

telascontrato_lista = [{'contrato': 'basico', 'tela': 'RH'},
                       {'contrato': 'basico', 'tela': 'Equipamento'},
                       {'contrato': 'basico', 'tela': 'Fornecedor'},
                       {'contrato': 'intermediário', 'tela': 'Contrato'},
                       {'contrato': 'intermediário', 'tela': 'Empresa'},
                       {'contrato': 'intermediário', 'tela': 'RH'},
                       {'contrato': 'intermediário', 'tela': 'Equipamento'},
                       {'contrato': 'intermediário', 'tela': 'Fornecedor'},
                       {'contrato': 'intermediário', 'tela': 'Almoxarifado'},
                       {'contrato': 'intermediário', 'tela': 'Programação'},
                       {'contrato': 'completo', 'tela': 'Interessado'},
                       {'contrato': 'completo', 'tela': 'Contrato'},
                       {'contrato': 'completo', 'tela': 'Empresa'},
                       {'contrato': 'completo', 'tela': 'RH'},
                       {'contrato': 'completo', 'tela': 'Equipamento'},
                       {'contrato': 'completo', 'tela': 'Plano de Manutenção'},
                       {'contrato': 'completo', 'tela': 'Ordem de Serviço'},
                       {'contrato': 'completo', 'tela': 'Fornecedor'},
                       {'contrato': 'completo', 'tela': 'Almoxarifado'},
                       {'contrato': 'completo', 'tela': 'Programação'},
                       {'contrato': 'completo', 'tela': 'Orçamento'},
                       {'contrato': 'completo', 'tela': 'Indicadores'}
                       ]

interessado_lista = [{'nome_fantasia': 'empresa_oi', 'cnpj': '96.207.052/0001-02',
                      'email': 'empresa_oi@empoi.com.br', 'telefone': '(45)9 9874-4578'},
                     {'nome_fantasia': 'empresa_by', 'cnpj': '24.885.627/0001-35',
                      'email': 'empresa_by@empby', 'telefone': '(78)3245-6578'},
                     ]

tipo_empresa_lista = [{'nome': 'Cliente'}, {'nome': 'Fornecedor'}, {'nome': 'Parceiro'}]

empresa_lista = [{'razao_social': 'empresa_1.ltda', 'nome_fantasia': 'empresa_1',
                  'cnpj': '39.262.527/0001-20',
                  'cep': '65058864',
                  'logradouro': 'Rua Aderson Lago', 'bairro': 'Vila Janaína',
                  'municipio': 'São Luís', 'uf': 'MA',
                  'numero': '0', 'complemento': 'qd05 lt05',
                  'email': 'empresa_1@teste.com.br', 'telefone': '(45)9 9876-5432',
                  'business': 'serviços', 'subbusiness': 'informática',
                  'data_cadastro': str(datetime.datetime.now() - datetime.timedelta(360)), 'contrato': 'completo',
                  'empresa_gestora': 'empresa_1', 'tipo': 'Cliente'},

                 {'razao_social': 'empresa_2.ltda', 'nome_fantasia': 'empresa_2',
                  'cnpj': '10.540.017/0001-95',
                  'cep': '69921728',
                  'logradouro': 'Rua São Francisco', 'bairro': 'Tancredo Neves',
                  'municipio': 'Rio Branco', 'uf': 'AC',
                  'numero': '59', 'complemento': '',
                  'email': 'empresa_2@teste.com.br', 'telefone': '(78)9 9876-5432',
                  'business': 'serviços', 'subbusiness': 'informática',
                  'data_cadastro': str(datetime.datetime.now() - datetime.timedelta(1000)), 'contrato': 'completo',
                  'empresa_gestora': 'empresa_1', 'tipo': 'Cliente'},

                 {'razao_social': 'empresa_21.ltda', 'nome_fantasia': 'empresa_21',
                  'cnpj': '88.496.773/0001-51',
                  'cep': '78717650',
                  'logradouro': 'Avenida José Agostinho Neto', 'bairro': 'Jardim São Bento',
                  'municipio': 'Rondonópolis', 'uf': 'MT',
                  'numero': '45', 'complemento': 'qd45',
                  'email': 'empresa_21@teste.com.br', 'telefone': '(98)9 9876-5432',
                  'business': 'serviços', 'subbusiness': 'informática',
                  'data_cadastro': str(datetime.datetime.now() - datetime.timedelta(2000)), 'contrato': 'basico',
                  'empresa_gestora': 'empresa_2', 'tipo': 'Cliente'},

                 {'razao_social': 'empresa_22.ltda', 'nome_fantasia': 'empresa_22',
                  'cnpj': '50.201.802/0001-38',
                  'cep': '69037097',
                  'logradouro': 'Alameda Namíbia', 'bairro': 'Ponta Negra',
                  'municipio': 'Manaus', 'uf': 'AM',
                  'numero': '789', 'complemento': '',
                  'email': 'empresa_22@teste.com.br', 'telefone': '(12)9 9876-5432',
                  'business': 'serviços', 'subbusiness': 'informática',
                  'data_cadastro': str(datetime.datetime.now() - datetime.timedelta(2500)), 'contrato': 'basico',
                  'empresa_gestora': 'empresa_2', 'tipo': 'Cliente'},

                 {'razao_social': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'nome_fantasia': 'COMERCIAL SEMEENTE CASA E CONSTRUCAO',
                  'cnpj': '30.722.226/0001-67',
                  'cep': '74905-230',
                  'logradouro': 'RUA CAIAPOS', 'bairro': 'VILA BRASILIA',
                  'municipio': 'APARECIDA DE GOIÂNIA', 'uf': 'GO',
                  'numero': '0', 'complemento': '',
                  'email': 'contato.luzengenharia@gmail.com', 'telefone': '(62)9 8423-6833',
                  'business': 'serviços', 'subbusiness': 'informática',
                  'data_cadastro': str(datetime.datetime.now() + datetime.timedelta(30)), 'contrato': 'completo',
                  'empresa_gestora': 'empresa_1', 'tipo': 'Cliente'},
                 ]

perfis_lista = [{'empresa': 'empresa_1.ltda', 'nome': 'default', 'descricao': 'padrão'},
                {'empresa': 'empresa_1.ltda', 'nome': 'admin', 'descricao': 'administrador'},
                {'empresa': 'empresa_1.ltda', 'nome': 'adminluz', 'descricao': 'administrador do sistema'},
                {'empresa': 'empresa_2.ltda', 'nome': 'default', 'descricao': 'padrão'},
                {'empresa': 'empresa_2.ltda', 'nome': 'admin', 'descricao': 'administrador'},
                {'empresa': 'empresa_2.ltda', 'nome': 'adminluz', 'descricao': 'administrador do sistema'},
                {'empresa': 'empresa_21.ltda', 'nome': 'default', 'descricao': 'padrão'},
                {'empresa': 'empresa_21.ltda', 'nome': 'admin', 'descricao': 'administrador'},
                {'empresa': 'empresa_21.ltda', 'nome': 'adminluz', 'descricao': 'administrador do sistema'},
                {'empresa': 'empresa_22.ltda', 'nome': 'default', 'descricao': 'padrão'},
                {'empresa': 'empresa_22.ltda', 'nome': 'admin', 'descricao': 'administrador'},
                {'empresa': 'empresa_22.ltda', 'nome': 'adminluz', 'descricao': 'administrador do sistema'},
                {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'nome': 'admin', 'descricao': 'administrador'},
                {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'nome': 'adminluz', 'descricao': 'administrador do sistema'},
                ]

telasperfil_lista = [{'empresa': 'empresa_1.ltda', 'role': 'default', 'tela': 'Contrato'},
                     {'empresa': 'empresa_1.ltda', 'role': 'default', 'tela': 'Empresa'},
                     {'empresa': 'empresa_1.ltda', 'role': 'default', 'tela': 'RH'},
                     {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Interessado'},
                     {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Contrato'},
                     {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Empresa'},
                     {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'RH'},
                     {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Equipamento'},
                     {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Plano de Manutenção'},
                     {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Ordem de Serviço'},
                     {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Fornecedor'},
                     {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Almoxarifado'},
                     {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Programação'},
                     {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Orçamento'},
                     {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Indicadores'},

                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Interessado'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Contrato'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Empresa'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'RH'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Plano de Manutenção'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Ordem de Serviço'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Programação'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Indicadores'},

                   {'empresa': 'empresa_2.ltda', 'role': 'default', 'tela': 'Contrato'},
                   {'empresa': 'empresa_2.ltda', 'role': 'default', 'tela': 'Empresa'},
                   {'empresa': 'empresa_2.ltda', 'role': 'default', 'tela': 'RH'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Contrato'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Empresa'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'RH'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Plano de Manutenção'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Ordem de Serviço'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Programação'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Indicadores'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Interessado'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Contrato'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Empresa'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'RH'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Plano de Manutenção'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Ordem de Serviço'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Programação'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Indicadores'},

                   {'empresa': 'empresa_21.ltda', 'role': 'default', 'tela': 'Contrato'},
                   {'empresa': 'empresa_21.ltda', 'role': 'default', 'tela': 'Empresa'},
                   {'empresa': 'empresa_21.ltda', 'role': 'default', 'tela': 'RH'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Contrato'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Empresa'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'RH'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Plano de Manutenção'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Ordem de Serviço'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Programação'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Indicadores'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Interessado'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Contrato'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Empresa'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'RH'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Plano de Manutenção'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Ordem de Serviço'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Programação'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Indicadores'},

                   {'empresa': 'empresa_22.ltda', 'role': 'default', 'tela': 'Contrato'},
                   {'empresa': 'empresa_22.ltda', 'role': 'default', 'tela': 'Empresa'},
                   {'empresa': 'empresa_22.ltda', 'role': 'default', 'tela': 'RH'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Contrato'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Empresa'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'RH'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Plano de Manutenção'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Ordem de Serviço'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Programação'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Indicadores'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Interessado'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Empresa'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'RH'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Plano de Manutenção'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Ordem de Serviço'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Programação'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Indicadores'},

                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'admin', 'tela': 'Interessado'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'admin', 'tela': 'Contrato'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'admin', 'tela': 'Empresa'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'admin', 'tela': 'RH'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'admin', 'tela': 'Equipamento'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'admin', 'tela': 'Plano de Manutenção'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'admin', 'tela': 'Ordem de Serviço'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'admin', 'tela': 'Fornecedor'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'admin', 'tela': 'Almoxarifado'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'admin', 'tela': 'Programação'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'admin', 'tela': 'Orçamento'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'admin', 'tela': 'Indicadores'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'adminluz', 'tela': 'Interessado'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'adminluz', 'tela': 'Contrato'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'adminluz', 'tela': 'Empresa'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'adminluz', 'tela': 'RH'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'adminluz', 'tela': 'Equipamento'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'adminluz', 'tela': 'Plano de Manutenção'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'adminluz', 'tela': 'Ordem de Serviço'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'adminluz', 'tela': 'Fornecedor'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'adminluz', 'tela': 'Almoxarifado'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'adminluz', 'tela': 'Programação'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'adminluz', 'tela': 'Orçamento'},
                   {'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA', 'role': 'adminluz', 'tela': 'Indicadores'},
                   ]

senha_lista = [{'senha': 'aaa11111', 'data_expiracao': str(datetime.datetime.now() + datetime.timedelta(30)),
                'senha_expira': False, 'senha_temporaria': False},
               {'senha': 'aaa22222', 'data_expiracao': str(datetime.datetime.now() + datetime.timedelta(30)),
                'senha_expira': False, 'senha_temporaria': False},
               {'senha': 'aaa33333', 'data_expiracao': str(datetime.datetime.now() + datetime.timedelta(30)),
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

usuario_lista = [{'nome': 'admin', 'email': 'admin@admin.com',
                  'senha': 'aaa11111', 'perfil': 'admin',
                  'data_assinatura': '1980/05/10 12:45:10', 'empresa': 'empresa_1.ltda'},
                 {'nome': 'leandro', 'email': 'engleoluz@hotmail.com',
                  'senha': 'aaa22222', 'perfil': 'default',
                  'data_assinatura': '1980/05/10 12:45:10', 'empresa': 'empresa_1.ltda'},
                 {'nome': 'danylo', 'email': 'danylo@gmail.com',
                  'senha': 'aaa33333', 'perfil': 'admin',
                  'data_assinatura': '1980/05/10 12:45:10', 'empresa': 'empresa_1.ltda'},
                 {'nome': 'admin_empresa_2', 'email': 'admin_empresa_2@admin.com',
                  'senha': 'aaa44444', 'perfil': 'admin',
                  'data_assinatura': '1980/05/10 12:45:10', 'empresa': 'empresa_2.ltda'},
                 {'nome': 'admin_empresa_21', 'email': 'admin_empresa_21@admin.com',
                  'senha': 'aaa55555', 'perfil': 'admin',
                  'data_assinatura': '1980/05/10 12:45:10', 'empresa': 'empresa_21.ltda'},
                 {'nome': 'admin_empresa_22', 'email': 'admin_empresa_22@admin.com',
                  'senha': 'aaa66666', 'perfil': 'admin',
                  'data_assinatura': '1980/05/10 12:45:10', 'empresa': 'empresa_22.ltda'},
                 {'nome': 'admin_Semeente', 'email': 'contato.luzengenharia@gmail.com',
                  'senha': '12345678', 'perfil': 'admin',
                  'data_assinatura': '2023/06/05 18:00:00', 'empresa': 'SEMEENTE ENGENHARIA E CONSTRUCOES LTDA'},
                 ]
grupo_lista = [{'nome': 'None', 'empresa': 'empresa_1.ltda'},
               {'nome': 'cadeira', 'empresa': 'empresa_1.ltda'},
               {'nome': 'elevador', 'empresa': 'empresa_1.ltda'},
               {'nome': 'mesa', 'empresa': 'empresa_1.ltda'}
               ]

equipamento_lista = [{'cod': '000.001', 'short': 'gerador', 'empresa': 'empresa_1.ltda', 'tag': 'ger.001'},
                     {'cod': '000.002', 'short': 'subestação 13.8KV', 'empresa': 'empresa_1.ltda', 'tag': 'se.001'},
                     {'cod': '000.003', 'short': 'chiller', 'empresa': 'empresa_1.ltda', 'tag': 'ch.001'},
                     {'cod': '000.004', 'short': 'carro', 'empresa': 'empresa_1.ltda', 'tag': 'ca.001'}
                     ]

tipoData_lista = [{'nome': 'Data_Fixa'},
                  {'nome': 'Data_Móvel'}]

unidade_lista = [{'nome': 'hora'},
                 {'nome': 'dia'},
                 {'nome': 'semana'},
                 {'nome': 'mês'},
                 {'nome': 'ano'},
                 ]

periodicidade_lista = [{'nome': 'Diária', 'tempo': 1, 'unidade': 'dia'},
                       {'nome': 'Semanal', 'tempo': 7, 'unidade': 'dia'},
                       {'nome': 'Mensal', 'tempo': 1, 'unidade': 'mês'},
                       {'nome': 'Bimensal', 'tempo': 2, 'unidade': 'mês'},
                       {'nome': 'Trimensal', 'tempo': 3, 'unidade': 'mês'},
                       {'nome': 'Semestral', 'tempo': 6, 'unidade': 'mês'},
                       {'nome': 'Anual', 'tempo': 1, 'unidade': 'ano'}]


planosmanutencao_lista = [{'nome': 'Inspeção Diária Gerador', 'codigo': 'gera0001', 'ativo': True,
                           'empresa': 'empresa_1.ltda',
                           'tipodata': 'Data_Fixa', 'periodicidade': 'Diária', 'equipamento': '000.001'},
                          {'nome': 'Inspeção Semanal Subestação 13.8KV', 'codigo': 'sube0001', 'ativo': True,
                           'empresa': 'empresa_1.ltda',
                           'tipodata': 'Data_Fixa', 'periodicidade': 'Semanal', 'equipamento': '000.002'},
                          {'nome': 'Manutenção Preventiva Anual Subestação 13.8KV', 'codigo': 'sube0002', 'ativo': True,
                           'empresa': 'empresa_1.ltda',
                           'tipodata': 'Data_Fixa', 'periodicidade': 'Anual', 'equipamento': '000.002'},
                          {'nome': 'Manutenção Preventiva Mensal Chiller', 'codigo': 'chil0001', 'ativo': True,
                           'empresa': 'empresa_1.ltda',
                           'tipodata': 'Data_Móvel', 'periodicidade': 'Mensal', 'equipamento': '000.003'},
                          {'nome': 'Inspeção Diária Carro 001', 'codigo': 'carr0001', 'ativo': True, 'empresa':
                              'empresa_1.ltda',
                           'tipodata': 'Data_Fixa', 'periodicidade': 'Diária', 'equipamento': '000.004'},
                          {'nome': 'Manutenção Preventiva Semestral Carro', 'codigo': 'carr0002', 'ativo': True,
                           'empresa': 'empresa_1.ltda',
                           'tipodata': 'Data_Fixa', 'periodicidade': 'Semestral', 'equipamento': '000.004'},
                          ]


sistema_lista = [{'nome': 'elétrico', 'cod': '000.001'},
                 {'nome': 'mecânico', 'cod': '000.001'},
                 {'nome': 'elétrico', 'cod': '000.002'},
                 {'nome': 'alvenaria', 'cod': '000.002'},
                 {'nome': 'refrigeração', 'cod': '000.002'}
                 ]

situacao_ordem_lista = [{'nome': 'Aguardando Aprovação', 'sigla': 'AGAP',
                         'descricao': 'Ordem criada, mas está aguardando aprovação do gestor'},
                        {'nome': 'Pendente', 'sigla': 'PEND', 'descricao': 'Ordem aprovada, mas não foi iniciada'},
                        {'nome': 'Em execução', 'sigla': 'EXEC', 'descricao': 'Ordem sendo executada'},
                        {'nome': 'Aguardando Serviços', 'sigla': 'AGSE',
                         'descricao': 'Ordem aguardando serviços externos'},
                        {'nome': 'Aguardando Material', 'sigla': 'AGMT',
                         'descricao': 'Ordem aguardando peças'},
                        {'nome': 'Paralizada', 'sigla': 'PARA',
                         'descricao': 'Ordem paralizada por força maior ou invibialização da execução'},
                        {'nome': 'Cancelada', 'sigla': 'CANC', 'descricao': 'Ordem cancelada por algum motivo'},
                        {'nome': 'Concluída', 'sigla': 'CONC', 'descricao': 'Ordem concluída com sucesso'},
                        {'nome': 'Fiscalizada', 'sigla': 'FISC', 'descricao': 'Ordem foi fiscalizada, liberada para '},
                        ]


fluxo_ordem_lista = [{'de': 'AGAP', 'para': 'PEND'},
                     {'de': 'AGAP', 'para': 'CANC'},
                     {'de': 'PEND', 'para': 'EXEC'},
                     {'de': 'EXEC', 'para': 'CANC'},
                     {'de': 'EXEC', 'para': 'CONC'},
                     {'de': 'EXEC', 'para': 'AGSE'},
                     {'de': 'EXEC', 'para': 'AGMT'},
                     {'de': 'CANC', 'para': 'FISC'},
                     {'de': 'CONC', 'para': 'FISC'},
                     {'de': 'AGSE', 'para': 'PEND'},
                     {'de': 'AGMT', 'para': 'PEND'},
                     {'de': 'PARA', 'para': 'PEND'},
                     ]

ordem_servico_lista = [{'codigo': 1001, 'descricao': 'Trocar Lâmpada Queimada', 'data_abertura': '2023/01/02 08:00:00',
                       'data_fechamento': None, 'equipamento': '000.002', 'situacaoordem': 'AGAP',
                        'planomanutencao': None, 'solicitante': 'leandro'},
                       {'codigo': 1002, 'descricao': 'Inspeção Diária Gerador', 'data_abertura': '2023/02/02 08:00:00',
                       'data_fechamento': None, 'equipamento': '000.001', 'situacaoordem': 'AGAP',
                        'planomanutencao': 'gera0001', 'solicitante': 'leandro'},
                       {'codigo': 1003, 'descricao': 'Corrigir o vazamento de óleo lubricante',
                        'data_abertura': '2023/02/03 08:00:00',
                       'data_fechamento': None, 'equipamento': '000.002', 'situacaoordem': 'AGAP',
                        'planomanutencao': None, 'solicitante': 'leandro'},
                       {'codigo': 1004, 'descricao': 'Manutenção Preventiva Semestral Carro',
                        'data_abertura': '2023/01/02 08:00:00',
                       'data_fechamento': None, 'equipamento': '000.004', 'situacaoordem': 'AGAP',
                        'planomanutencao': 'carr0002', 'solicitante': 'leandro'},
                       ]

tramitacao_lista = [{'ordem_servico': 1, 'usuario': 'danylo', 'situacaoordem': 'AGAP',
                     'data': '2023/01/02 08:00:00', 'observacao': 'Abertura de Ordem de Serviço'},
                    {'ordem_servico': 1, 'usuario': 'leandro', 'situacaoordem': 'PEND',
                     'data': '2023/01/03 08:00:00', 'observacao': 'Aprovada a execução da Ordem de Serviço'},
                    {'ordem_servico': 1, 'usuario': 'leandro', 'situacaoordem': 'EXEC',
                     'data': '2023/01/04 08:00:00',
                     'observacao': 'Foi realizada a troca da lâmpada queimada, está operacional'},
                    {'ordem_servico': 1, 'usuario': 'leandro', 'situacaoordem': 'CONC',
                     'data': '2023/01/04 10:00:00', 'observacao': 'Concluída a Ordem de Serviço'},
                    {'ordem_servico': 1, 'usuario': 'danylo', 'situacaoordem': 'FISC',
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
    novos_contratos = [Contrato(nome=item['nome'])
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
                        url=item['url'])
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


def criar_empresas(lista: List[dict]) -> List[Perfil]:
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


def criar_perfis(lista: List[dict]) -> List[Perfil]:
    """
   Cria novos perfis a partir de uma lista de dicionários.
   Args:
       lista (List[dict]): Lista de dicionários contendo informações de novos perfis.
   Returns:
       List[Perfil]: Lista de novos perfis criados e adicionados na base de dados.
   """

    empresas = {e.razao_social: e.id for e in Empresa.query.all()}

    # Criando a lista de novas perfis a serem adicionadas
    novos_perfis = [Perfil(nome=item['nome'],
                           descricao=item['descricao'],
                           empresa_id=empresas[item['empresa']])
                    for item in lista if item['nome'] not in [pe.nome
                                                              for pe in Perfil.query.all()]]

    try:
        # Adicionando as novas perfis na sessão e realizando o commit
        db.session.add_all(novos_perfis)
        db.session.commit()
        log.info(f'{len(novos_perfis)} Perfis inseridas com sucesso.')

        # Retornando a lista de novos perfis
        return novos_perfis
    except Exception as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir Perfil: {e}')
        db.session.rollback()
        return []


def criar_telasperfil(lista: List[dict]) -> List[Telaperfil]:
    """
   Cria novos perfis a partir de uma lista de dicionários.
   Args:
       lista (List[dict]): Lista de dicionários contendo informações de novos perfis.
   Returns:
       List[Perfil]: Lista de novos perfis criados e adicionados na base de dados.
   """

    telasperfis = []

    for item in lista:
        empresa = Empresa.query.filter_by(razao_social=item['empresa']).one()
        perfil = Perfil.query.filter_by(nome=item['role'], empresa_id=empresa.id).one()
        tela = Tela.query.filter_by(nome=item['tela']).one()
        telaperfil = Telaperfil.query.filter_by(tela_id=tela.id, perfil_id=perfil.id).first()

        if not telaperfil:
            telasperfis.append(Telaperfil(perfil_id=perfil.id, tela_id=tela.id, ativo=True))

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
       List[Perfil]: Lista de novos perfis criados e adicionados na base de dados.
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
    perfis = {p.nome: p.id for p in Perfil.query.all()}
    senhas = {s.senha: s.id for s in Senha.query.all()}

    # Criando uma lista de novos tipodatas para serem adicionados
    novos_usuarios = [Usuario(nome=item['nome'],
                              email=item['email'],
                              data_assinatura=item['data_assinatura'],
                              ativo=True,
                              senha_id=senhas[item['senha']],
                              perfil_id=perfis[item['perfil']],
                              empresa_id=empresas[item['empresa']]
                              )
                      for item in lista if item['nome'] not in [us.nome for us in Usuario.query.all()]]

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


def criar_equipamento(lista: List[dict]) -> List[Equipamento]:
    """
       Cria novos tipos de datas para os planos de manutenção.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das datas.
       Returns:
           List[TipoData]: Lista das novas datas e adicionados na base de dados.
       """

    empresas = {e.razao_social: e.id for e in Empresa.query.all()}

    # Criando uma lista de novos tipodatas para serem adicionados
    novos_equipamentos = [Equipamento(cod=item['cod'],
                                      descricao_curta=item['short'],
                                      tag=item['tag'],
                                      empresa_id=empresas[item['empresa']]
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


def criar_sistema(lista: List[dict]) -> List[Sistema]:
    """
       Cria novos tipos de datas para os planos de manutenção.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações das datas.
       Returns:
           List[TipoData]: Lista das novas datas e adicionados na base de dados.
       """

    equipamentos = {e.cod: e.id for e in Equipamento.query.all()}

    # Criando uma lista de novos tipodatas para serem adicionados
    novos_sistemas = [Sistema(nome=item['nome'],
                              equipamento_id=equipamentos[item['cod']])
                      for item in lista if item['nome'] not in [si.nome for si in Sistema.query.all()]]

    try:
        # Adicionando os novos contratos na sessão e realizando o commit
        db.session.add_all(novos_sistemas)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novos_sistemas)} Sistemas inseridos com sucesso.')
        # Retornando a lista de novos contratos adicionados
        return novos_sistemas
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir sistema: {e}')
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


#  {'nome': 'Inspeção Diária Gerador', 'codigo': 'gera0001', 'ativo': True,
#                            'empresa': 'empresa_1.ltda',
#                            'tipodata': 'Data_Fixa', 'periodicidade': 'Diária', 'equipamento': '000.001'}

def criar_planosmanutencao(lista: List[dict]) -> List[PlanoManutencao]:

    # Buscando os objetos necessários
    tipodatas = {t.nome: t.id for t in TipoData.query.all()}
    periodicidades = {p.nome: p.id for p in Periodicidade.query.all()}
    equipamentos = {e.cod: e.id for e in Equipamento.query.all()}
    empresas = {em.razao_social: em.id for em in Empresa.query.all()}

    novos_planosmanutencao = [
        PlanoManutencao(nome=item['nome'],
                        codigo=item['codigo'],
                        ativo=item['ativo'],
                        tipodata_id=tipodatas[item['tipodata']],
                        periodicidade_id=periodicidades[item['periodicidade']],
                        equipamento_id=equipamentos[item['equipamento']],
                        empresa_id=empresas[item['empresa']])
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


def criar_situacao_ordem(lista: List[dict]) -> List[SituacaoOrdem]:
    """
       Cria novas situações de ordens de serviços a partir de uma lista de dicionários.
       Args:
           lista (List[dict]): Lista de dicionários contendo informações dos novas situações.
       Returns:
           List[Contrato]: Lista de novas situações criados e adicionados na base de dados.
       """
    # Criando um conjunto de situações de ordens existentes na base de dados
    situacoes_ordem_existentes = set(so.nome for so in SituacaoOrdem.query.all())
    # Criando uma lista de novas situações de ordens para serem adicionados
    novas_situacoes_ordem = [SituacaoOrdem(nome=item['nome'],
                                           sigla=item['sigla'],
                                           descricao=item['descricao'])
                             for item in lista if item['nome'] not in situacoes_ordem_existentes]

    try:
        # Adicionando as novas situações na sessão e realizando o commit
        db.session.add_all(novas_situacoes_ordem)
        db.session.commit()
        # Registrando o evento no sistema de logs
        log.info(f'{len(novas_situacoes_ordem)} situações ordens inseridas com sucesso.')

        # Retornando a lista de novas situações de ordens adicionados
        return novas_situacoes_ordem
    except SQLAlchemyError as e:
        # Em caso de erro, realizando o rollback da transação e retornando uma lista vazia
        log.error(f'Erro ao inserir situação_ordem: {e}')

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
    situacoes_ordem = {so.sigla: so.id for so in SituacaoOrdem.query.all()}
    planosmanutencao = {pm.codigo: pm.id for pm in PlanoManutencao.query.all()}
    solicitantes = {u.nome: u.id for u in Usuario.query.all()}

    # Criando uma lista de novas ordens para serem adicionados
    novas_ordens_servicos = [OrdemServico(codigo=item['codigo'],
                                          descricao=item['descricao'],
                                          data_abertura=item['data_abertura'],
                                          equipamento_id=equipamentos[item['equipamento']],
                                          situacaoordem_id=situacoes_ordem[item['situacaoordem']],
                                          solicitante_id=solicitantes[item['solicitante']],
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
    situacoes_ordem = {so.sigla: so.id for so in SituacaoOrdem.query.all()}

    # Criando uma lista de novas ordens para serem adicionados
    novas_tramitacoes = [TramitacaoOrdem(
        ordemservico_id=item['ordem_servico'],
        usuario_id=usuarios[item['usuario']],
        situacaoordem_id=situacoes_ordem[item['situacaoordem']],
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
    situacoes_ordem = {so.sigla: so.id for so in SituacaoOrdem.query.all()}

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
criar_equipamento(equipamento_lista)
criar_sistema(sistema_lista)

# carregamento para os fornecedores

criar_tipodata(tipoData_lista)
criar_unidades(unidade_lista)
criar_periodicidades(periodicidade_lista)
criar_planosmanutencao(planosmanutencao_lista)

criar_situacao_ordem(situacao_ordem_lista)
criar_fluxo_ordem(fluxo_ordem_lista)
criar_ordem_servico(ordem_servico_lista)
criar_tramitacao(tramitacao_lista)

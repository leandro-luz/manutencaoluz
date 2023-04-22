import logging
import datetime
import os
from webapp import create_app
from webapp import db
from webapp.usuario.models import Perfil, Senha, Usuario, Telaperfil
from webapp.empresa.models import Interessado, Tipoempresa, Empresa
from webapp.equipamento.models import Equipamento, Grupo, Sistema
from webapp.supplier.models import Supplier
from webapp.contrato.models import Contrato, Tela, Telacontrato

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('config.%sConfig' % env.capitalize())
app.app_context().push()

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

telas_lista = [{'nome': 'Interessado', 'icon': 'bi-card-list', 'url': 'empresa.interessado_listar'},
               {'nome': 'Contrato', 'icon': 'bi-briefcase', 'url': 'contrato.contrato_listar'},
               {'nome': 'Empresa', 'icon': 'bi-house-door', 'url': 'empresa.empresa_listar'},
               {'nome': 'RH', 'icon': 'bi-people', 'url': 'usuario.usuario_listar'},
               {'nome': 'Equipamento', 'icon': 'bi-robot', 'url': 'equipamento.equipamento_listar'},
               {'nome': 'Almoxarifado', 'icon': 'bi-box-seam', 'url': 'sistema.almoxarifado'},
               {'nome': 'Programação', 'icon': 'bi-calendar3', 'url': 'sistema.programação'},
               {'nome': 'Manutenção', 'icon': 'bi-wrench-adjustable-circle', 'url': 'sistema.manutenção'},
               {'nome': 'Fornecedor', 'icon': 'bi-truck', 'url': 'supplier.supplier_list'},
               {'nome': 'Orçamento', 'icon': 'bi-cash', 'url': 'sistema.orçamento'},
               {'nome': 'Indicadores', 'icon': 'bi-graph-up', 'url': 'sistema.indicador'}
               ]

contratos_lista = [{'nome': 'basico'},
                   {'nome': 'intermediário'},
                   {'nome': 'completo'}
                   ]

telasplano_lista = [{'contrato': 'basico', 'tela': 'RH'},
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
                    {'contrato': 'completo', 'tela': 'Fornecedor'},
                    {'contrato': 'completo', 'tela': 'Almoxarifado'},
                    {'contrato': 'completo', 'tela': 'Programação'},
                    {'contrato': 'completo', 'tela': 'Manutenção'},
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
                  'date': '1980/05/10 12:45:10', 'contrato': 'completo',
                  'empresa_gestora': 'empresa_1', 'tipo': 'Cliente'},

                 {'razao_social': 'empresa_2.ltda', 'nome_fantasia': 'empresa_2',
                  'cnpj': '10.540.017/0001-95',
                  'cep': '69921728',
                  'logradouro': 'Rua São Francisco', 'bairro': 'Tancredo Neves',
                  'municipio': 'Rio Branco', 'uf': 'AC',
                  'numero': '59', 'complemento': '',
                  'email': 'empresa_2@teste.com.br', 'telefone': '(78)9 9876-5432',
                  'business': 'serviços', 'subbusiness': 'informática',
                  'date': '1980/05/10 12:45:10', 'contrato': 'completo',
                  'empresa_gestora': 'empresa_1', 'tipo': 'Cliente'},

                 {'razao_social': 'empresa_21.ltda', 'nome_fantasia': 'empresa_21',
                  'cnpj': '88.496.773/0001-51',
                  'cep': '78717650',
                  'logradouro': 'Avenida José Agostinho Neto', 'bairro': 'Jardim São Bento',
                  'municipio': 'Rondonópolis', 'uf': 'MT',
                  'numero': '45', 'complemento': 'qd45',
                  'email': 'empresa_21@teste.com.br', 'telefone': '(98)9 9876-5432',
                  'business': 'serviços', 'subbusiness': 'informática',
                  'date': '1980/05/10 12:45:10', 'contrato': 'basico',
                  'empresa_gestora': 'empresa_2', 'tipo': 'Cliente'},

                 {'razao_social': 'empresa_22.ltda', 'nome_fantasia': 'empresa_22',
                  'cnpj': '50.201.802/0001-38',
                  'cep': '69037097',
                  'logradouro': 'Alameda Namíbia', 'bairro': 'Ponta Negra',
                  'municipio': 'Manaus', 'uf': 'AM',
                  'numero': '789', 'complemento': '',
                  'email': 'empresa_22@teste.com.br', 'telefone': '(12)9 9876-5432',
                  'business': 'serviços', 'subbusiness': 'informática',
                  'date': '1980/05/10 12:45:10', 'contrato': 'basico',
                  'empresa_gestora': 'empresa_2', 'tipo': 'Cliente'},

                 {'razao_social': 'empresa_3.ltda', 'nome_fantasia': 'empresa_3',
                  'cnpj': '01.021.781/0001-63',
                  'cep': '58360974',
                  'logradouro': 'Rua José Xavier 54', 'bairro': 'Centro',
                  'municipio': 'Itabaiana', 'uf': 'PB',
                  'numero': '0', 'complemento': '',
                  'email': 'empresa_3@teste.com.br', 'telefone': '(15)9 9876-5432',
                  'business': 'serviços', 'subbusiness': 'informática',
                  'date': '1980/05/10 12:45:10', 'contrato': 'basico',
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
                {'empresa': 'empresa_3.ltda', 'nome': 'default', 'descricao': 'padrão'},
                {'empresa': 'empresa_3.ltda', 'nome': 'admin', 'descricao': 'administrador'},
                {'empresa': 'empresa_3.ltda', 'nome': 'adminluz', 'descricao': 'administrador do sistema'},
                ]

viewroles_lista = [{'empresa': 'empresa_1.ltda', 'role': 'default', 'tela': 'Contrato'},
                   {'empresa': 'empresa_1.ltda', 'role': 'default', 'tela': 'Empresa'},
                   {'empresa': 'empresa_1.ltda', 'role': 'default', 'tela': 'RH'},
                   {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Interessado'},
                   {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Contrato'},
                   {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Empresa'},
                   {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'RH'},
                   {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Programação'},
                   {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Manutenção'},
                   {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Indicadores'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Interessado'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Contrato'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Empresa'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'RH'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Programação'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Manutenção'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Indicadores'},

                   {'empresa': 'empresa_2.ltda', 'role': 'default', 'tela': 'Contrato'},
                   {'empresa': 'empresa_2.ltda', 'role': 'default', 'tela': 'Empresa'},
                   {'empresa': 'empresa_2.ltda', 'role': 'default', 'tela': 'RH'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Contrato'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Empresa'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'RH'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Programação'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Manutenção'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Indicadores'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Interessado'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Contrato'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Empresa'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'RH'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Programação'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Manutenção'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Indicadores'},

                   {'empresa': 'empresa_21.ltda', 'role': 'default', 'tela': 'Contrato'},
                   {'empresa': 'empresa_21.ltda', 'role': 'default', 'tela': 'Empresa'},
                   {'empresa': 'empresa_21.ltda', 'role': 'default', 'tela': 'RH'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Contrato'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Empresa'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'RH'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Programação'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Manutenção'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Indicadores'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Interessado'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Contrato'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Empresa'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'RH'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Programação'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Manutenção'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Indicadores'},

                   {'empresa': 'empresa_22.ltda', 'role': 'default', 'tela': 'Contrato'},
                   {'empresa': 'empresa_22.ltda', 'role': 'default', 'tela': 'Empresa'},
                   {'empresa': 'empresa_22.ltda', 'role': 'default', 'tela': 'RH'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Contrato'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Empresa'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'RH'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Programação'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Manutenção'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Indicadores'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Interessado'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Empresa'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'RH'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Programação'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Manutenção'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_22.ltda', 'role': 'adminluz', 'tela': 'Indicadores'},

                   {'empresa': 'empresa_3.ltda', 'role': 'default', 'tela': 'Contrato'},
                   {'empresa': 'empresa_3.ltda', 'role': 'default', 'tela': 'Empresa'},
                   {'empresa': 'empresa_3.ltda', 'role': 'default', 'tela': 'RH'},
                   {'empresa': 'empresa_3.ltda', 'role': 'admin', 'tela': 'Contrato'},
                   {'empresa': 'empresa_3.ltda', 'role': 'admin', 'tela': 'Empresa'},
                   {'empresa': 'empresa_3.ltda', 'role': 'admin', 'tela': 'RH'},
                   {'empresa': 'empresa_3.ltda', 'role': 'admin', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_3.ltda', 'role': 'admin', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_3.ltda', 'role': 'admin', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_3.ltda', 'role': 'admin', 'tela': 'Programação'},
                   {'empresa': 'empresa_3.ltda', 'role': 'admin', 'tela': 'Manutenção'},
                   {'empresa': 'empresa_3.ltda', 'role': 'admin', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_3.ltda', 'role': 'admin', 'tela': 'Indicadores'},
                   {'empresa': 'empresa_3.ltda', 'role': 'adminluz', 'tela': 'Interessado'},
                   {'empresa': 'empresa_3.ltda', 'role': 'adminluz', 'tela': 'Contrato'},
                   {'empresa': 'empresa_3.ltda', 'role': 'adminluz', 'tela': 'Empresa'},
                   {'empresa': 'empresa_3.ltda', 'role': 'adminluz', 'tela': 'RH'},
                   {'empresa': 'empresa_3.ltda', 'role': 'adminluz', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_3.ltda', 'role': 'adminluz', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_3.ltda', 'role': 'adminluz', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_3.ltda', 'role': 'adminluz', 'tela': 'Programação'},
                   {'empresa': 'empresa_3.ltda', 'role': 'adminluz', 'tela': 'Manutenção'},
                   {'empresa': 'empresa_3.ltda', 'role': 'adminluz', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_3.ltda', 'role': 'adminluz', 'tela': 'Indicadores'},
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
               {'senha': 'aaa77777', 'data_expiracao': str(datetime.datetime.now() + datetime.timedelta(30)),
                'senha_expira': False, 'senha_temporaria': False},
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
                 {'nome': 'admin_empresa_3', 'email': 'admin_empresa_3@admin.com',
                  'senha': 'aaa77777', 'perfil': 'admin',
                  'data_assinatura': '1980/05/10 12:45:10', 'empresa': 'empresa_3.ltda'},
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

sistema_lista = [{'nome': 'elétrico', 'cod': '000.001'},
                 {'nome': 'mecânico', 'cod': '000.001'},
                 {'nome': 'elétrico', 'cod': '000.002'},
                 {'nome': 'alvenaria', 'cod': '000.002'},
                 {'nome': 'refrigeração', 'cod': '000.002'}
                 ]

supplier_lista = [{'nome': 'Fornecedor_1', 'empresa': 'empresa_1.ltda'},
                  {'nome': 'Fornecedor_2', 'empresa': 'empresa_1.ltda'}
                  ]


def criar_contrato():
    contratos = list()
    for item in contratos_lista:
        contrato = Contrato.query.filter_by(nome=item['nome']).first()
        if contrato:
            contratos.append(contrato)
            continue
        contrato = Contrato()
        contrato.nome = item['nome']
        contratos.append(contrato)

        try:
            db.session.add(contrato)
            db.session.commit()
            print(f'Contrato inserido: {contrato}')
        except Exception as e:
            log.error(f'Erro ao inserir o contrato: {contrato}-{e}')
            db.session.rollback()
    return contratos


def criar_telas():
    telas = list()
    for item in telas_lista:
        tela = Tela.query.filter_by(nome=item['nome']).first()
        if tela:
            telas.append(tela)
            continue
        tela = Tela()
        tela.nome = item['nome']
        tela.icon = item['icon']
        tela.url = item['url']

        try:
            db.session.add(tela)
            db.session.commit()
            print(f'Tela inserida: {tela}')
        except Exception as e:
            log.error(f'Erro ao inserir a tela: {tela}-{e}')
            db.session.rollback()
    return telas


def criar_telasplano():
    telasplano = list()
    for item in telasplano_lista:
        tela = Tela.query.filter_by(nome=item['tela']).first()
        contrato = Contrato.query.filter_by(nome=item['contrato']).first()
        telaplano = Telacontrato.query.filter_by(tela_id=tela.id, contrato_id=contrato.id).first()

        if telaplano:
            telasplano.append(telaplano)
            continue

        telaplano = Telacontrato()
        telaplano.tela_id = tela.id
        telaplano.contrato_id = contrato.id
        telaplano.ativo = True

        try:
            db.session.add(telaplano)
            db.session.commit()
            print(f'Tela inserida: {tela} no contrato: {contrato}')
        except Exception as e:
            log.error(f'Erro ao inserir a tela/contrato: {telaplano}-{e}')
            db.session.rollback()
    return telasplano


def criar_interessados():
    interessados = list()
    for item in interessado_lista:
        interessado = Interessado.query.filter_by(nome_fantasia=item['nome_fantasia']).first()
        if interessado:
            interessados.append(interessado)
            continue
        interessado = Interessado()
        interessado.nome_fantasia = item['nome_fantasia']
        interessado.cnpj = item['cnpj']
        interessado.email = item['email']
        interessado.telefone = item['telefone']
        interessado.data_solicitacao = datetime.datetime.now()
        interessados.append(interessado)

        try:
            db.session.add(interessado)
            db.session.commit()
            print(f'Interessado inserido: {interessado}')
        except Exception as e:
            log.error(f'Erro ao inserir interessado: {interessado}-{e}')
            db.session.rollback()
    return interessados


def criar_tipos_empresa():
    tipos_empresa = list()
    for item in tipo_empresa_lista:
        tipoempresa = Tipoempresa.query.filter_by(nome=item['nome']).first()
        if tipoempresa:
            tipos_empresa.append(tipoempresa)
            continue
        tipoempresa = Tipoempresa()
        tipoempresa.nome = item['nome']
        tipos_empresa.append(tipoempresa)

        try:
            db.session.add(tipoempresa)
            db.session.commit()
            print(f'Ramo de negócio inserido: {tipoempresa}')
        except Exception as e:
            log.error(f'Erro ao inserir o tipo de empresa: {tipoempresa.nome}-{e}')
            db.session.rollback()
    return tipos_empresa


def criar_empresas():
    empresas = list()
    for item in empresa_lista:
        empresa = Empresa.query.filter_by(razao_social=item['razao_social']).first()
        if empresa:
            empresas.append(empresa)
            continue
        empresa = Empresa()
        tipoempresa = Tipoempresa.query.filter_by(nome=item['tipo']).one_or_none()
        plan = Contrato.query.filter_by(nome=item['contrato']).one()
        empresa_gestora = Empresa.query.filter_by(razao_social=item['empresa_gestora']).first()
        empresa.empresa_gestora_id = 1

        if empresa_gestora:
            empresa.empresa_gestora_id = empresa_gestora.id
        empresa.razao_social = item['razao_social']
        empresa.nome_fantasia = item['nome_fantasia']
        empresa.cnpj = item['cnpj']
        empresa.cep = item['cep']
        empresa.logradouro = item['logradouro']
        empresa.bairro = item['bairro']
        empresa.municipio = item['municipio']
        empresa.uf = item['uf']
        empresa.numero = item['numero']
        empresa.complemento = item['complemento']
        empresa.email = item['email']
        empresa.telefone = item['telefone']
        empresa.ativo = True
        empresa.member_since = item['date']

        empresa.contrato_id = plan.id
        empresa.tipoempresa_id = tipoempresa.id
        empresas.append(empresa)

        try:
            db.session.add(empresa)
            db.session.commit()
            print(f'Empresa inserida:: {empresa}')
        except Exception as e:
            log.error(f'Erro ao inserir a empresa: {empresa.razao_social}-{e}')
            db.session.rollback()
    return empresas


def criar_perfis():
    perfis = list()
    for item in perfis_lista:
        empresa = Empresa.query.filter_by(razao_social=item['empresa']).one_or_none()
        perfil = Perfil.query.filter_by(nome=item['nome'], empresa_id=empresa.id).first()
        if perfil:
            perfis.append(perfil)
            continue
        perfil = Perfil(nome=item['nome'], descricao=item['descricao'], empresa_id=empresa.id)

        try:
            db.session.add(perfil)
            db.session.commit()
            print(f'Regra inserida:: {perfil}')
        except Exception as e:
            log.error(f'Erro ao inserir a regra: {perfil.nome}-{e}')
            db.session.rollback()
    return perfis


def generate_viewroles():
    viewrolelista = list()
    for item in viewroles_lista:
        empresa = Empresa.query.filter_by(razao_social=item['empresa']).one()
        perfil = Perfil.query.filter_by(nome=item['role'], empresa_id=empresa.id).one()
        tela = Tela.query.filter_by(nome=item['tela']).one()
        viewrole = Telaperfil.query.filter_by(tela_id=tela.id, perfil_id=perfil.id).first()

        if viewrole:
            viewrolelista.append(viewrole)
            continue

        viewrole = Telaperfil(perfil_id=perfil.id, tela_id=tela.id, ativo=True)

        try:
            db.session.add(viewrole)
            db.session.commit()
            print(f'Tela inserida: {tela} no perfil: {perfil}')
        except Exception as e:
            log.error(f'Erro ao inserir a tela: {viewrole}-{e}')
            db.session.rollback()

    return viewrolelista


def criar_senhas():
    senhas = list()
    for item in senha_lista:
        senha = Senha.query.filter_by(senha=item['senha']).one_or_none()
        if senha:
            senhas.append(senha)
            continue
        senha = Senha()
        senha.senha = item['senha']
        senha.data_expiracao = item['data_expiracao']
        senha.senha_expira = item['senha_expira']
        senha.senha_temporaria = item['senha_temporaria']

        try:
            db.session.add(senha)
            db.session.commit()
            print(f'Senha inserida:: {senha}')
        except Exception as e:
            log.error(f'Erro ao inserir a senha: {senha.senha}-{e}')
            db.session.rollback()

    return senhas


def criar_usuarios():
    usuarios = list()
    for item in usuario_lista:
        usuario = Usuario.query.filter_by(nome=item['nome']).first()
        if usuario:
            usuarios.append(usuario)
            continue
        usuario = Usuario()
        empresa = Empresa.query.filter_by(razao_social=item['empresa']).one_or_none()
        perfil = Perfil.query.filter_by(nome=item['perfil'], empresa_id=empresa.id).one_or_none()
        senha = Senha.query.filter_by(senha=item['senha']).one_or_none()
        usuario.nome = item['nome']
        usuario.email = item['email']
        usuario.senha_id = senha.id
        usuario.data_assinatura = item['data_assinatura']
        usuario.ativo = True
        usuario.perfil_id = perfil.id
        usuario.empresa_id = empresa.id

        try:
            db.session.add(usuario)
            db.session.commit()
            print(f'Usuário inserido: {usuario}, na empresa: {empresa}')
        except Exception as e:
            log.error(f'Erro ao inserir a usuário: {usuario}-{e}')
            db.session.rollback()

    return usuarios


def criar_grupo():
    grupos = list()
    for item in grupo_lista:
        grupo = Grupo.query.filter_by(nome=item['nome']).first()
        if grupo:
            grupos.append(grupo)
            continue
        grupo = Grupo()
        grupo.nome = item['nome']
        empresa = Empresa.query.filter_by(razao_social=item['empresa']).one()
        grupo.empresa_id = empresa.id

        try:
            db.session.add(grupo)
            db.session.commit()
            print(f'Grupo de equipamento inserido: {grupo} na empresa: {empresa}')
        except Exception as e:
            log.error(f'Erro ao inserir o grupo do equipamento: {grupo}-{e}')
            db.session.rollback()
    return grupos


def criar_empresa():
    equipamentos = list()
    for item in equipamento_lista:
        equipamento = Equipamento.query.filter_by(cod=item['cod']).first()
        if equipamento:
            equipamentos.append(equipamento)
            continue
        equipamento = Equipamento()
        empresa = Empresa.query.filter_by(razao_social=item['empresa']).one()
        equipamento.cod = item['cod']
        equipamento.descricao_curta = item['short']
        equipamento.tag = item['tag']
        equipamento.empresa_id = empresa.id
        try:
            db.session.add(equipamento)
            db.session.commit()
            print(f'Equipamento inserido: {equipamento} na empresa: {empresa}')
        except Exception as e:
            log.error(f'Erro ao inserir Equipamento: {equipamento}-{e}')
            db.session.rollback()
    return equipamentos


def criar_sistema():
    sistemas = list()
    for item in sistema_lista:
        sistema = Sistema.query.filter_by(nome=item['nome']).first()
        if sistema:
            sistemas.append(sistema)
            continue
        sistema = Sistema()
        equipamento = Equipamento.query.filter_by(cod=item['cod']).one_or_none()
        sistema.nome = item['nome']
        sistema.equipamento_id = equipamento.id
        try:
            db.session.add(sistema)
            db.session.commit()
            print(f'Sistema inserido: {sistema} no equipamento: {equipamento}')
        except Exception as e:
            log.error(f'Erro ao inserir Sistema: {sistema}-{e}')
            db.session.rollback()
    return sistemas


def generate_supplier():
    suppliers = list()
    for item in supplier_lista:
        supplier = Supplier.query.filter_by(nome=item['nome']).first()
        if supplier:
            suppliers.append(supplier)
            continue
        supplier = Supplier()
        empresa = Empresa.query.filter_by(razao_social=item['empresa']).one()
        supplier.nome = item['nome']
        supplier.company_id = empresa.id
        try:
            db.session.add(supplier)
            db.session.commit()
            print(f'Fornecedor inserido: {supplier} na empresa: {empresa}')
        except Exception as e:
            log.error(f'Erro ao inserir Fornecedor: {supplier}-{e}')
            db.session.rollback()
    return suppliers


# carregamento para as empresas
criar_telas()
criar_contrato()
criar_telasplano()
criar_interessados()
criar_tipos_empresa()
criar_empresas()

# carregamento para os perfis e usuários
criar_perfis()
generate_viewroles()
criar_senhas()
criar_usuarios()

# carregamento para os equipamentos
criar_grupo()
criar_empresa()
criar_sistema()

# carregamento para os fornecedores
generate_supplier()

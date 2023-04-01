import logging
import datetime
import os
from webapp import create_app
from webapp import db
from webapp.usuario.models import Perfil, Senha, Usuario, ViewRole
from webapp.empresa.models import Interessado, Tipoempresa, Empresa, Business, Subbusiness
from webapp.equipamento.models import Equipamento, Grupo, Sistema
from webapp.supplier.models import Supplier
from webapp.plano.models import Plano, Tela, Telaplano

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('config.%sConfig' % env.capitalize())
app.app_context().push()

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

business_lista = [{'nome': 'indústria'},
                  {'nome': 'comércio'},
                  {'nome': 'serviços'}
                  ]

subbusiness_lista = [{'business': 'indústria', 'nome': 'roupas'},
                     {'business': 'indústria', 'nome': 'laticínios'},
                     {'business': 'comércio', 'nome': 'roupas'},
                     {'business': 'comércio', 'nome': 'ferragens'},
                     {'business': 'serviços', 'nome': 'informática'},
                     {'business': 'serviços', 'nome': 'odontologia'},
                     {'business': 'indústria', 'nome': 'teste'}
                     ]

telas_lista = [{'nome': 'Interessado', 'icon': 'bi-card-list', 'url': 'empresa.lead_list'},
               {'nome': 'Plano', 'icon': 'bi-briefcase', 'url': 'plano.plan_list'},
               {'nome': 'Empresa', 'icon': 'bi-house-door', 'url': 'empresa.company_list'},
               {'nome': 'RH', 'icon': 'bi-people', 'url': 'usuario.auth_list'},
               {'nome': 'Equipamento', 'icon': 'bi-robot', 'url': 'equipamento.asset_list'},
               {'nome': 'Almoxarifado', 'icon': 'bi-box-seam', 'url': 'sistema.almoxarifado'},
               {'nome': 'Programação', 'icon': 'bi-calendar3', 'url': 'sistema.programação'},
               {'nome': 'Manutenção', 'icon': 'bi-wrench-adjustable-circle', 'url': 'sistema.manutenção'},
               {'nome': 'Fornecedor', 'icon': 'bi-truck', 'url': 'supplier.supplier_list'},
               {'nome': 'Orçamento', 'icon': 'bi-cash', 'url': 'sistema.orçamento'},
               {'nome': 'Indicadores', 'icon': 'bi-graph-up', 'url': 'sistema.indicador'}
               ]

planos_lista = [{'nome': 'basico'},
                {'nome': 'intermediário'},
                {'nome': 'completo'}
                ]

telasplano_lista = [{'plano': 'basico', 'tela': 'RH'},
                   {'plano': 'basico', 'tela': 'Equipamento'},
                   {'plano': 'basico', 'tela': 'Fornecedor'},
                   {'plano': 'intermediário', 'tela': 'Plano'},
                   {'plano': 'intermediário', 'tela': 'Empresa'},
                   {'plano': 'intermediário', 'tela': 'RH'},
                   {'plano': 'intermediário', 'tela': 'Equipamento'},
                   {'plano': 'intermediário', 'tela': 'Fornecedor'},
                   {'plano': 'intermediário', 'tela': 'Almoxarifado'},
                   {'plano': 'intermediário', 'tela': 'Programação'},
                   {'plano': 'completo', 'tela': 'Interessado'},
                   {'plano': 'completo', 'tela': 'Plano'},
                   {'plano': 'completo', 'tela': 'Empresa'},
                   {'plano': 'completo', 'tela': 'RH'},
                   {'plano': 'completo', 'tela': 'Equipamento'},
                   {'plano': 'completo', 'tela': 'Fornecedor'},
                   {'plano': 'completo', 'tela': 'Almoxarifado'},
                   {'plano': 'completo', 'tela': 'Programação'},
                   {'plano': 'completo', 'tela': 'Manutenção'},
                   {'plano': 'completo', 'tela': 'Orçamento'},
                   {'plano': 'completo', 'tela': 'Indicadores'}
                   ]

interessado_lista = [{'razao_social': 'empresa_oi', 'cnpj': '96.207.052/0001-02',
                      'email': 'empresa_oi@empoi.com.br', 'telefone': '(45)9 9874-4578'},
                     {'razao_social': 'empresa_by', 'cnpj': '24.885.627/0001-35',
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
                  'date': '1980/05/10 12:45:10', 'plano': 'completo',
                  'empresa_gestora': 'empresa_1', 'tipo': 'Cliente'},

                 {'razao_social': 'empresa_2.ltda', 'nome_fantasia': 'empresa_2',
                  'cnpj': '10.540.017/0001-95',
                  'cep': '69921728',
                  'logradouro': 'Rua São Francisco', 'bairro': 'Tancredo Neves',
                  'municipio': 'Rio Branco', 'uf': 'AC',
                  'numero': '59', 'complemento': '',
                  'email': 'empresa_2@teste.com.br', 'telefone': '(78)9 9876-5432',
                  'business': 'serviços', 'subbusiness': 'informática',
                  'date': '1980/05/10 12:45:10', 'plano': 'completo',
                  'empresa_gestora': 'empresa_1', 'tipo': 'Cliente'},

                 {'razao_social': 'empresa_21.ltda', 'nome_fantasia': 'empresa_21',
                  'cnpj': '88.496.773/0001-51',
                  'cep': '78717650',
                  'logradouro': 'Avenida José Agostinho Neto', 'bairro': 'Jardim São Bento',
                  'municipio': 'Rondonópolis', 'uf': 'MT',
                  'numero': '45', 'complemento': 'qd45',
                  'email': 'empresa_21@teste.com.br', 'telefone': '(98)9 9876-5432',
                  'business': 'serviços', 'subbusiness': 'informática',
                  'date': '1980/05/10 12:45:10', 'plano': 'basico',
                  'empresa_gestora': 'empresa_2', 'tipo': 'Cliente'},

                 {'razao_social': 'empresa_22.ltda', 'nome_fantasia': 'empresa_22',
                  'cnpj': '50.201.802/0001-38',
                  'cep': '69037097',
                  'logradouro': 'Alameda Namíbia', 'bairro': 'Ponta Negra',
                  'municipio': 'Manaus', 'uf': 'AM',
                  'numero': '789', 'complemento': '',
                  'email': 'empresa_22@teste.com.br', 'telefone': '(12)9 9876-5432',
                  'business': 'serviços', 'subbusiness': 'informática',
                  'date': '1980/05/10 12:45:10', 'plano': 'basico',
                  'empresa_gestora': 'empresa_2', 'tipo': 'Cliente'},

                 {'razao_social': 'empresa_3.ltda', 'nome_fantasia': 'empresa_3',
                  'cnpj': '01.021.781/0001-63',
                  'cep': '58360974',
                  'logradouro': 'Rua José Xavier 54', 'bairro': 'Centro',
                  'municipio': 'Itabaiana', 'uf': 'PB',
                  'numero': '0', 'complemento': '',
                  'email': 'empresa_3@teste.com.br', 'telefone': '(15)9 9876-5432',
                  'business': 'serviços', 'subbusiness': 'informática',
                  'date': '1980/05/10 12:45:10', 'plano': 'basico',
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

viewroles_lista = [{'empresa': 'empresa_1.ltda', 'role': 'default', 'tela': 'Plano'},
                   {'empresa': 'empresa_1.ltda', 'role': 'default', 'tela': 'Empresa'},
                   {'empresa': 'empresa_1.ltda', 'role': 'default', 'tela': 'RH'},
                   {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Interessado'},
                   {'empresa': 'empresa_1.ltda', 'role': 'admin', 'tela': 'Plano'},
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
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Plano'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Empresa'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'RH'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Programação'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Manutenção'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_1.ltda', 'role': 'adminluz', 'tela': 'Indicadores'},

                   {'empresa': 'empresa_2.ltda', 'role': 'default', 'tela': 'Plano'},
                   {'empresa': 'empresa_2.ltda', 'role': 'default', 'tela': 'Empresa'},
                   {'empresa': 'empresa_2.ltda', 'role': 'default', 'tela': 'RH'},
                   {'empresa': 'empresa_2.ltda', 'role': 'admin', 'tela': 'Plano'},
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
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Plano'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Empresa'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'RH'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Programação'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Manutenção'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_2.ltda', 'role': 'adminluz', 'tela': 'Indicadores'},

                   {'empresa': 'empresa_21.ltda', 'role': 'default', 'tela': 'Plano'},
                   {'empresa': 'empresa_21.ltda', 'role': 'default', 'tela': 'Empresa'},
                   {'empresa': 'empresa_21.ltda', 'role': 'default', 'tela': 'RH'},
                   {'empresa': 'empresa_21.ltda', 'role': 'admin', 'tela': 'Plano'},
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
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Plano'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Empresa'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'RH'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Equipamento'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Fornecedor'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Almoxarifado'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Programação'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Manutenção'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Orçamento'},
                   {'empresa': 'empresa_21.ltda', 'role': 'adminluz', 'tela': 'Indicadores'},

                   {'empresa': 'empresa_22.ltda', 'role': 'default', 'tela': 'Plano'},
                   {'empresa': 'empresa_22.ltda', 'role': 'default', 'tela': 'Empresa'},
                   {'empresa': 'empresa_22.ltda', 'role': 'default', 'tela': 'RH'},
                   {'empresa': 'empresa_22.ltda', 'role': 'admin', 'tela': 'Plano'},
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

                   {'empresa': 'empresa_3.ltda', 'role': 'default', 'tela': 'Plano'},
                   {'empresa': 'empresa_3.ltda', 'role': 'default', 'tela': 'Empresa'},
                   {'empresa': 'empresa_3.ltda', 'role': 'default', 'tela': 'RH'},
                   {'empresa': 'empresa_3.ltda', 'role': 'admin', 'tela': 'Plano'},
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
                   {'empresa': 'empresa_3.ltda', 'role': 'adminluz', 'tela': 'Plano'},
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

group_lista = [{'nome': 'None', 'empresa': 'empresa_1.ltda'},
               {'nome': 'cadeira', 'empresa': 'empresa_1.ltda'},
               {'nome': 'elevador', 'empresa': 'empresa_1.ltda'},
               {'nome': 'mesa', 'empresa': 'empresa_1.ltda'}
               ]

asset_lista = [{'cod': '000.001', 'short': 'gerador', 'empresa': 'empresa_1.ltda', 'tag': 'ger.001'},
               {'cod': '000.002', 'short': 'subestação 13.8KV', 'empresa': 'empresa_1.ltda', 'tag': 'se.001'},
               {'cod': '000.003', 'short': 'chiller', 'empresa': 'empresa_1.ltda', 'tag': 'ch.001'},
               {'cod': '000.004', 'short': 'carro', 'empresa': 'empresa_1.ltda', 'tag': 'ca.001'}
               ]

system_lista = [{'nome': 'elétrico', 'cod': '000.001'},
                {'nome': 'mecânico', 'cod': '000.001'},
                {'nome': 'elétrico', 'cod': '000.002'},
                {'nome': 'alvenaria', 'cod': '000.002'},
                {'nome': 'refrigeração', 'cod': '000.002'}
                ]

supplier_lista = [{'nome': 'Fornecedor_1', 'empresa': 'empresa_1.ltda'},
                  {'nome': 'Fornecedor_2', 'empresa': 'empresa_1.ltda'}
                  ]


def generate_business():
    businesslista = list()
    for item in business_lista:
        business = Business.query.filter_by(nome=item['nome']).first()
        if business:
            businesslista.append(business)
            continue
        business = Business()
        business.nome = item['nome']
        businesslista.append(business)

        try:
            db.session.add(business)
            db.session.commit()
            print(f'Ramo de negócio inserido:{business}')
        except Exception as e:
            log.error(f'Erro ao inserir o ramo de negócio: {business}-{e}')
            db.session.rollback()
    return businesslista


def generate_subbusiness():
    subbusinesss = list()
    for item in subbusiness_lista:
        business = Business.query.filter_by(nome=item['business']).one()
        subbusiness = Subbusiness.query.filter_by(nome=item['nome'], business_id=business.id).first()
        if subbusiness:
            subbusinesss.append(subbusiness)
            continue
        subbusiness = Subbusiness()
        # business = Business.query.filter_by(razao_social=item['business']).one()
        subbusiness.nome = item['nome']
        subbusiness.business_id = business.id

        try:
            db.session.add(subbusiness)
            db.session.commit()
            print('Sub-ramo de negócio inserido:', subbusiness)
        except Exception as e:
            log.error(f'Erro ao inserir o sub-ramo de negócio: {subbusiness}-{e}')
            db.session.rollback()
    return subbusinesss


def criar_planos():
    planos = list()
    for item in planos_lista:
        plano = Plano.query.filter_by(nome=item['nome']).first()
        if plano:
            planos.append(plano)
            continue
        plano = Plano()
        plano.nome = item['nome']
        planos.append(plano)

        try:
            db.session.add(plano)
            db.session.commit()
            print(f'Plano inserido: {plano}')
        except Exception as e:
            log.error(f'Erro ao inserir o plano: {plano}-{e}')
            db.session.rollback()
    return planos


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
        plano = Plano.query.filter_by(nome=item['plano']).first()
        telaplano = Telaplano.query.filter_by(tela_id=tela.id, plano_id=plano.id).first()

        if telaplano:
            telasplano.append(telaplano)
            continue

        telaplano = Telaplano()
        telaplano.tela_id = tela.id
        telaplano.plano_id = plano.id
        telaplano.active = True

        try:
            db.session.add(telaplano)
            db.session.commit()
            print(f'Tela inserida: {tela} no plano: {plano}')
        except Exception as e:
            log.error(f'Erro ao inserir a tela/plano: {telaplano}-{e}')
            db.session.rollback()
    return telasplano


def criar_interessados():
    interessados = list()
    for item in interessado_lista:
        interessado = Interessado.query.filter_by(razao_social=item['razao_social']).first()
        if interessado:
            interessados.append(interessado)
            continue
        interessado = Interessado()
        interessado.razao_social = item['razao_social']
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
        business = Business.query.filter_by(nome=item['business']).one_or_none()
        subbusiness = Subbusiness.query.filter_by(nome=item['subbusiness'], business_id=business.id).one_or_none()
        tipoempresa = Tipoempresa.query.filter_by(nome=item['tipo']).one_or_none()
        plan = Plano.query.filter_by(nome=item['plano']).one()
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
        empresa.active = True
        empresa.member_since = item['date']

        empresa.subbusiness_id = subbusiness.id
        empresa.plano_id = plan.id
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
        viewrole = ViewRole.query.filter_by(tela_id=tela.id, perfil_id=perfil.id).first()

        if viewrole:
            viewrolelista.append(viewrole)
            continue

        viewrole = ViewRole(perfil_id=perfil.id, tela_id=tela.id, active=True)

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


def generate_group():
    groups = list()
    for item in group_lista:
        group = Grupo.query.filter_by(nome=item['nome']).first()
        if group:
            groups.append(group)
            continue
        group = Grupo()
        group.nome = item['nome']
        empresa = Empresa.query.filter_by(razao_social=item['empresa']).one()
        group.empresa_id = empresa.id

        try:
            db.session.add(group)
            db.session.commit()
            print(f'Grupo de equipamento inserido: {group} na empresa: {empresa}')
        except Exception as e:
            log.error(f'Erro ao inserir o grupo do equipamento: {group}-{e}')
            db.session.rollback()
    return groups


def generate_asset():
    assets = list()
    for item in asset_lista:
        asset = Equipamento.query.filter_by(cod=item['cod']).first()
        if asset:
            assets.append(asset)
            continue
        asset = Equipamento()
        empresa = Empresa.query.filter_by(razao_social=item['empresa']).one()
        asset.cod = item['cod']
        asset.descricao_curta = item['short']
        asset.tag = item['tag']
        asset.empresa_id = empresa.id
        try:
            db.session.add(asset)
            db.session.commit()
            print(f'Equipamento inserido: {asset} na empresa: {empresa}')
        except Exception as e:
            log.error(f'Erro ao inserir Equipamento: {asset}-{e}')
            db.session.rollback()
    return assets


def generate_system():
    systems = list()
    for item in system_lista:
        system = Sistema.query.filter_by(nome=item['nome']).first()
        if system:
            systems.append(system)
            continue
        system = Sistema()
        asset = Equipamento.query.filter_by(cod=item['cod']).one_or_none()
        system.nome = item['nome']
        system.equipamento_id = asset.id
        try:
            db.session.add(system)
            db.session.commit()
            print(f'Sistema inserido: {system} no equipamento: {asset}')
        except Exception as e:
            log.error(f'Erro ao inserir Sistema: {system}-{e}')
            db.session.rollback()
    return systems


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
generate_business()
generate_subbusiness()
criar_telas()
criar_planos()
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
generate_group()
generate_asset()
generate_system()

# carregamento para os fornecedores
generate_supplier()

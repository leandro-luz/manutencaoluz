import logging
import os
from webapp import create_app
from webapp import db
from webapp.auth.models import Role, User
from webapp.company.models import Company, Business, Subbusiness
from webapp.asset.models import Asset, Group, System
from webapp.supplier.models import Supplier

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('config.%sConfig' % env.capitalize())
app.app_context().push()

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

business_lista = [{'name': 'indústria'},
                  {'name': 'comércio'},
                  {'name': 'serviços'}
                  ]

subbusiness_lista = [{'business': 'indústria', 'name': 'roupas'},
                     {'business': 'indústria', 'name': 'laticínios'},
                     {'business': 'comércio', 'name': 'roupas'},
                     {'business': 'comércio', 'name': 'ferragens'},
                     {'business': 'serviços', 'name': 'advocacia'},
                     {'business': 'serviços', 'name': 'odontologia'},
                     {'business': 'indústria', 'name': 'teste'}
                     ]

company_lista = [{'name': 'empresa_1', 'cnpj': '123456789',
                  'cep': '12000111', 'email': 'email@teste.com.br',
                  'business': 'indústria', 'subbusiness': 'teste',
                  'date': '1980/05/10 12:45:10'},
                 {'name': 'empresa_2', 'cnpj': '987654321',
                  'cep': '34111222', 'email': 'empresalucratudo@teste.com.br',
                  'business': 'comércio', 'subbusiness': 'roupas',
                  'date': '1999/08/01 08:12:35'}
                 ]

roles_lista = [{'company': 'empresa_1', 'name': 'default'},
               {'company': 'empresa_1', 'name': 'admin'},
               {'company': 'empresa_2', 'name': 'superadmin'},
               {'company': 'empresa_2', 'name': 'admin'}
               ]

user_lista = [{'username': 'leandro',
               'email': 'engleoluz@hotmail.com',
               'password': 'aaa11111',
               'role': 'default',
               'date': '1980/05/10 12:45:10',
               'company': 'empresa_1'},
              {'username': 'danylo',
               'email': 'luzdanylo@gmail.com',
               'password': '12345678',
               'role': 'default',
               'date': '1999/08/01 08:12:35',
               'company': 'empresa_2'}
              ]

group_lista = [{'name': 'cadeira', 'company': 'empresa_1'},
               {'name': 'elevador', 'company': 'empresa_1'},
               {'name': 'mesa', 'company': 'empresa_1'},
               {'name': 'informatica', 'company': 'empresa_2'},
               {'name': 'veículos', 'company': 'empresa_2'},
               {'name': 'móveis', 'company': 'empresa_2'}
               ]

asset_lista = [{'cod': '000.001', 'short': 'computador', 'company': 'empresa_1'},
               {'cod': '000.002', 'short': 'mesa', 'company': 'empresa_1'},
               {'cod': '000.003', 'short': 'chiller', 'company': 'empresa_1'},
               {'cod': '000.004', 'short': 'carro', 'company': 'empresa_1'},
               {'cod': '000.011', 'short': 'caldeira', 'company': 'empresa_2'},
               {'cod': '000.021', 'short': 'caminhão', 'company': 'empresa_2'},
               {'cod': '000.031', 'short': 'esteira', 'company': 'empresa_2'},
               {'cod': '000.041', 'short': 'britador', 'company': 'empresa_2'},
               {'cod': '000.051', 'short': 'compactador', 'company': 'empresa_2'}
               ]

system_lista = [{'name': 'elétrico', 'cod': '000.001'},
                {'name': 'alvenaria', 'cod': '000.002'},
                {'name': 'hidraulico', 'cod': '000.003'},
                {'name': 'combustão', 'cod': '000.004'},
                {'name': 'segurança', 'cod': '000.011'},
                {'name': 'informática', 'cod': '000.021'},
                {'name': 'painel', 'cod': '000.031'}
                ]

supplier_lista = [{'name': 'Fornecedor_1', 'company': 'empresa_1'},
                  {'name': 'Fornecedor_2', 'company': 'empresa_1'},
                  {'name': 'Fornecedor_3', 'company': 'empresa_2'},
                  {'name': 'Fornecedor_4', 'company': 'empresa_2'},
                  {'name': 'Fornecedor_5', 'company': 'empresa_2'},
                  {'name': 'Fornecedor_6', 'company': 'empresa_2'}
                  ]


def generate_business():
    businesslista = list()
    for item in business_lista:
        business = Business.query.filter_by(name=item['name']).first()
        if business:
            businesslista.append(business)
            continue
        business = Business()
        business.name = item['name']
        businesslista.append(business)
        try:
            db.session.add(business)
            db.session.commit()
            print('Ramo de negócio inserido:', business.name)
        except Exception as e:
            log.error("Erro ao inserir o ramo de negócio: %s, %s" % (str(business), e))
            db.session.rollback()
    return businesslista


def generate_subbusiness():
    subbusinesss = list()
    for item in subbusiness_lista:
        business = Business.query.filter_by(name=item['business']).one()
        subbusiness = Subbusiness.query.filter_by(name=item['name'], business_id=business.id).first()
        if subbusiness:
            subbusinesss.append(subbusiness)
            continue
        subbusiness = Subbusiness()
        # business = Business.query.filter_by(name=item['business']).one()
        subbusiness.name = item['name']
        subbusiness.business_id = business.id
        try:
            db.session.add(subbusiness)
            db.session.commit()
            print('Sub-ramo de negócio inserido:', subbusiness.name)
        except Exception as e:
            log.error("Erro ao inserir o sub-ramo de negócio: %s, %s" % (str(subbusiness), e))
            db.session.rollback()
    return subbusinesss


def generate_companies():
    companies = list()
    for item in company_lista:
        company = Company.query.filter_by(name=item['name']).first()
        if company:
            companies.append(company)
            continue
        company = Company()
        business = Business.query.filter_by(name=item['business']).one()
        subbusiness = Subbusiness.query.filter_by(name=item['subbusiness'], business_id=business.id).one()
        company.name = item['name']
        company.cnpj = item['cnpj']
        company.cep = item['cep']
        company.email = item['email']
        company.active = True
        company.member_since = item['date']
        company.subbusiness_id = subbusiness.id
        companies.append(company)
        try:
            db.session.add(company)
            db.session.commit()
            print('Empresa inserida:', company.name)
        except Exception as e:
            log.error("Erro ao inserir empresa: %s, %s" % (str(company), e))
            db.session.rollback()
    return companies


def generate_roles():
    roles = list()
    for item in roles_lista:
        company = Company.query.filter_by(name=item['company']).one()
        role = Role.query.filter_by(name=item['name'], company_id=company.id).first()
        if role:
            roles.append(role)
            continue
        role = Role()
        role.name = item['name']
        role.company_id = company.id
        try:
            db.session.add(role)
            db.session.commit()
            print("Regra inserida: %s na empresa: %s" % (role.name, company.name))
        except Exception as e:
            log.error("Erro ao inserir a regra: %s, %s" % (str(role), e))
            db.session.rollback()
    return roles


def generate_users():
    users = list()
    for item in user_lista:
        user = User.query.filter_by(username=item['username']).first()
        if user:
            users.append(user)
            continue
        user = User()
        role = Role.query.filter_by(name=item['role']).one()
        company = Company.query.filter_by(name=item['company']).one()
        user.username = item['username']
        user.email = item['email']
        user.password = item['password']
        user.member_since = item['date']
        user.confirmed = True
        user.active = True
        user.role_id = role.id
        user.company_id = company.id
        try:
            db.session.add(user)
            db.session.commit()
            print("Usuário inserido: %s, na empresa: %s" % (user.username, company.name))
        except Exception as e:
            log.error("Erro ao inserir usuário: %s, %s" % (str(user), e))
            db.session.rollback()
    return users


def generate_group():
    groups = list()
    for item in group_lista:
        group = Group.query.filter_by(name=item['name']).first()
        if group:
            groups.append(group)
            continue
        group = Group()
        group.name = item['name']
        company = Company.query.filter_by(name=item['company']).one()
        group.company_id = company.id
        try:
            db.session.add(group)
            db.session.commit()
            print("Grupo de equipamento inserido: %s,  na empresa: %s" % (group.name, company.name))
        except Exception as e:
            log.error("Erro ao inserir o grupo do equipamento: %s, %s" % (str(group), e))
            db.session.rollback()
    return groups


def generate_asset():
    assets = list()
    for item in asset_lista:
        asset = Asset.query.filter_by(cod=item['cod']).first()
        if asset:
            assets.append(asset)
            continue
        asset = Asset()
        company = Company.query.filter_by(name=item['company']).one()
        asset.cod = item['cod']
        asset.short_description = item['short']
        asset.company_id = company.id
        try:
            db.session.add(asset)
            db.session.commit()
            print("Equipamento inserido: %s, na empresa: %s" % (asset.short_description, company.name))
        except Exception as e:
            log.error("Erro ao inserir Equipamento: %s, %s" % (str(asset), e))
            db.session.rollback()
    return assets


def generate_system():
    systems = list()
    for item in system_lista:
        system = System.query.filter_by(name=item['name']).first()
        if system:
            systems.append(system)
            continue
        system = System()
        asset = Asset.query.filter_by(cod=item['cod']).one()
        system.name = item['name']
        system.asset_id = asset.id
        try:
            db.session.add(system)
            db.session.commit()
            print("Sistema inserido: %s, no equipamento: %s" % (system.name, asset.short_description))
        except Exception as e:
            log.error("Erro ao inserir Sistema: %s, %s" % (str(system), e))
            db.session.rollback()
    return systems


def generate_supplier():
    suppliers = list()
    for item in supplier_lista:
        supplier = Supplier.query.filter_by(name=item['name']).first()
        if supplier:
            suppliers.append(supplier)
            continue
        supplier = Supplier()
        company = Company.query.filter_by(name=item['company']).one()
        supplier.name = item['name']
        supplier.company_id = company.id
        try:
            db.session.add(supplier)
            db.session.commit()
            print("Fornecedor inserido: %s, na empresa: %s" % (supplier.name, company.name))
        except Exception as e:
            log.error("Erro ao inserir Fornecedor: %s, %s" % (str(supplier), e))
            db.session.rollback()
    return suppliers


# carregamento para as empresas
generate_business()
generate_subbusiness()
generate_companies()

# carregamento para os usuários
generate_roles()
generate_users()

# carregamento para os equipamentos
generate_group()
generate_asset()
generate_system()

# carregamento para os fornecedores
generate_supplier()

import logging
import os
from webapp import create_app
from webapp import db
from webapp.auth.models import Role, User
from webapp.company.models import Company, Business, Subbusiness

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('config.%sConfig' % env.capitalize())
app.app_context().push()

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

business_lista = ['indústria', 'comércio', 'serviços']
subbusiness_lista = [{'business': 'indústria', 'name': 'roupas'},
                     {'business': 'indústria', 'name': 'laticínios'},
                     {'business': 'comércio', 'name': 'roupas'},
                     {'business': 'comércio', 'name': 'ferragens'},
                     {'business': 'serviços', 'name': 'advocacia'},
                     {'business': 'serviços', 'name': 'odontologia'},
                     {'business': 'indústria', 'name': 'teste'}
                     ]

company_lista = [{'name': 'empresa_teste_1', 'cnpj': '123456789',
                  'cep': '12000111', 'email': 'email@teste.com.br',
                  'business': 'indústria', 'subbusiness': 'teste'},
                 {'name': 'empresa_teste_2', 'cnpj': '987654321',
                  'cep': '34111222', 'email': 'empresalucratudo@teste.com.br',
                  'business': 'comércio', 'subbusiness': 'roupas'}
                 ]

roles_lista = ['default', 'admin']
user_lista = [{'username': 'leandro',
               'email': 'engleoluz@hotmail.com',
               'password': 'aaa11111',
               'role': 'default'},
              {'username': 'danylo',
               'email': 'luzdanylo@gmail.com',
               'password': '12345678',
               'role': 'default'}
              ]


def generate_business():
    businesslista = list()
    for businessname in business_lista:
        business = Business.query.filter_by(name=businessname).first()
        if business:
            businesslista.append(business)
            continue
        business = Business(businessname)
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
        subbusiness = Subbusiness.query.filter_by(name=item['subbusiness'], business_id=business.id).first()
        company.name = item['name']
        company.cnpj = item['cnpj']
        company.cep = item['cep']
        company.email = item['email']
        company.active = True
        company.business_id = subbusiness.id
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
    for rolename in roles_lista:
        role = Role.query.filter_by(name=rolename).first()
        if role:
            roles.append(role)
            continue
        role = Role(rolename)
        roles.append(role)
        db.session.add(role)
        try:
            db.session.commit()
            print('Regra inserida:', role.name)
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
        user.username = item['username']
        user.email = item['email']
        user.password = item['password']
        user.confirmed = True
        user.active = True
        user.role_id = role.id
        users.append(user)
        try:
            db.session.add(user)
            db.session.commit()
            print('Usuário inserido:', user.username)
        except Exception as e:
            log.error("Erro ao inserir usuário: %s, %s" % (str(user), e))
            db.session.rollback()
    return users


# carregamento para as empresas
generate_business()
generate_subbusiness()
generate_companies()

# carregamento para os usuários
generate_roles()
generate_users()

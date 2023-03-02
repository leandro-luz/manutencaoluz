import logging
import os
from webapp import create_app
from webapp import db
from webapp.auth.models import Role, User, ViewRole
from webapp.company.models import Company, Business, Subbusiness
from webapp.asset.models import Asset, Group, System
from webapp.supplier.models import Supplier
from webapp.plan.models import Plan, View, ViewPlan


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
                     {'business': 'serviços', 'name': 'informática'},
                     {'business': 'serviços', 'name': 'odontologia'},
                     {'business': 'indústria', 'name': 'teste'}
                     ]

views_lista = [{'name': 'Plano', 'icon': 'bi-briefcase', 'url': 'plan.plan_list'},
               {'name': 'Empresa', 'icon': 'bi-house-door', 'url': 'company.company_list'},
               {'name': 'RH', 'icon': 'bi-people', 'url': 'auth.auth_list'},
               {'name': 'Equipamento', 'icon': 'bi-robot', 'url': 'asset.asset_list'},
               {'name': 'Almoxarifado', 'icon': 'bi-box-seam', 'url': 'sistema.almoxarifado'},
               {'name': 'Programação', 'icon': 'bi-calendar3', 'url': 'sistema.programação'},
               {'name': 'Manutenção', 'icon': 'bi-wrench-adjustable-circle', 'url': 'sistema.manutenção'},
               {'name': 'Fornecedor', 'icon': 'bi-truck', 'url': 'supplier.supplier_list'},
               {'name': 'Orçamento', 'icon': 'bi-cash', 'url': 'sistema.orçamento'},
               {'name': 'Indicadores', 'icon': 'bi-graph-up', 'url': 'sistema.indicador'}
               ]

plans_lista = [{'name': 'basico'},
               {'name': 'intermediário'},
               {'name': 'completo'}
               ]

viewplans_lista = [{'plan': 'basico', 'view': 'RH'},
                   {'plan': 'basico', 'view': 'Equipamento'},
                   {'plan': 'basico', 'view': 'Fornecedor'},
                   {'plan': 'intermediário', 'view': 'Plano'},
                   {'plan': 'intermediário', 'view': 'Empresa'},
                   {'plan': 'intermediário', 'view': 'RH'},
                   {'plan': 'intermediário', 'view': 'Equipamento'},
                   {'plan': 'intermediário', 'view': 'Fornecedor'},
                   {'plan': 'intermediário', 'view': 'Almoxarifado'},
                   {'plan': 'intermediário', 'view': 'Programação'},
                   {'plan': 'completo', 'view': 'Plano'},
                   {'plan': 'completo', 'view': 'Empresa'},
                   {'plan': 'completo', 'view': 'RH'},
                   {'plan': 'completo', 'view': 'Equipamento'},
                   {'plan': 'completo', 'view': 'Fornecedor'},
                   {'plan': 'completo', 'view': 'Almoxarifado'},
                   {'plan': 'completo', 'view': 'Programação'},
                   {'plan': 'completo', 'view': 'Manutenção'},
                   {'plan': 'completo', 'view': 'Orçamento'},
                   {'plan': 'completo', 'view': 'Indicadores'}
                   ]

company_lista = [{'name': 'empresa_1', 'cnpj': '39.262.527/0001-20',
                  'cep': '65058864',
                  'logradouro': 'Rua Aderson Lago', 'bairro': 'Vila Janaína',
                  'municipio': 'São Luís', 'uf' : 'MA',
                  'numero': '0', 'complemento': 'qd05 lt05',
                  'email': 'empresa_1@teste.com.br',
                  'business': 'serviços', 'subbusiness': 'informática',
                  'date': '1980/05/10 12:45:10', 'plano': 'completo',
                  'manager': 'empresa_1'},

                 {'name': 'empresa_2', 'cnpj': '10.540.017/0001-95',
                  'cep': '69921728',
                  'logradouro': 'Rua São Francisco', 'bairro': 'Tancredo Neves',
                  'municipio': 'Rio Branco', 'uf' : 'AC',
                  'numero': '59', 'complemento': '',
                  'email': 'empresa_2@teste.com.br',
                  'business': 'serviços', 'subbusiness': 'informática',
                  'date': '1980/05/10 12:45:10', 'plano': 'completo',
                  'manager': 'empresa_1'},

                 {'name': 'empresa_21', 'cnpj': '88.496.773/0001-51',
                  'cep': '78717650',
                  'logradouro': 'Avenida José Agostinho Neto', 'bairro': 'Jardim São Bento',
                  'municipio': 'Rondonópolis', 'uf' : 'MT',
                  'numero': '45', 'complemento': 'qd45',
                  'email': 'empresa_21@teste.com.br',
                  'business': 'serviços', 'subbusiness': 'informática',
                  'date': '1980/05/10 12:45:10', 'plano': 'basico',
                  'manager': 'empresa_2'},

                 {'name': 'empresa_22', 'cnpj': '50.201.802/0001-38',
                  'cep': '69037097',
                  'logradouro': 'Alameda Namíbia', 'bairro': 'Ponta Negra',
                  'municipio': 'Manaus', 'uf' : 'AM',
                  'numero': '789', 'complemento': '',
                  'email': 'empresa_22@teste.com.br',
                  'business': 'serviços', 'subbusiness': 'informática',
                  'date': '1980/05/10 12:45:10', 'plano': 'basico',
                  'manager': 'empresa_2'},

                 {'name': 'empresa_3', 'cnpj': '01.021.781/0001-63',
                  'cep': '58360974',
                  'logradouro': 'Rua José Xavier 54', 'bairro': 'Centro',
                  'municipio': 'Itabaiana', 'uf' : 'PB',
                  'numero': '0', 'complemento': '',
                  'email': 'empresa_3@teste.com.br',
                  'business': 'serviços', 'subbusiness': 'informática',
                  'date': '1980/05/10 12:45:10', 'plano': 'basico',
                  'manager': 'empresa_1'},
                 ]

roles_lista = [{'company': 'empresa_1', 'name': 'default', 'description': 'padrão'},
               {'company': 'empresa_1', 'name': 'admin', 'description': 'administrador'},
               {'company': 'empresa_2', 'name': 'default', 'description': 'padrão'},
               {'company': 'empresa_2', 'name': 'admin', 'description': 'administrador'},
               {'company': 'empresa_21', 'name': 'default', 'description': 'padrão'},
               {'company': 'empresa_21', 'name': 'admin', 'description': 'administrador'},
               {'company': 'empresa_22', 'name': 'default', 'description': 'padrão'},
               {'company': 'empresa_22', 'name': 'admin', 'description': 'administrador'},
               {'company': 'empresa_3', 'name': 'default', 'description': 'padrão'},
               {'company': 'empresa_3', 'name': 'admin', 'description': 'administrador'},
               ]

viewroles_lista = [{'company': 'empresa_1', 'role': 'default', 'view': 'Plano'},
                   {'company': 'empresa_1', 'role': 'default', 'view': 'Empresa'},
                   {'company': 'empresa_1', 'role': 'default', 'view': 'RH'},
                   {'company': 'empresa_1', 'role': 'admin', 'view': 'Plano'},
                   {'company': 'empresa_1', 'role': 'admin', 'view': 'Empresa'},
                   {'company': 'empresa_1', 'role': 'admin', 'view': 'RH'},
                   {'company': 'empresa_1', 'role': 'admin', 'view': 'Equipamento'},
                   {'company': 'empresa_1', 'role': 'admin', 'view': 'Fornecedor'},
                   {'company': 'empresa_1', 'role': 'admin', 'view': 'Almoxarifado'},
                   {'company': 'empresa_1', 'role': 'admin', 'view': 'Programação'},
                   {'company': 'empresa_1', 'role': 'admin', 'view': 'Manutenção'},
                   {'company': 'empresa_1', 'role': 'admin', 'view': 'Orçamento'},
                   {'company': 'empresa_1', 'role': 'admin', 'view': 'Indicadores'},

                   {'company': 'empresa_2', 'role': 'default', 'view': 'Plano'},
                   {'company': 'empresa_2', 'role': 'default', 'view': 'Empresa'},
                   {'company': 'empresa_2', 'role': 'default', 'view': 'RH'},
                   {'company': 'empresa_2', 'role': 'admin', 'view': 'Plano'},
                   {'company': 'empresa_2', 'role': 'admin', 'view': 'Empresa'},
                   {'company': 'empresa_2', 'role': 'admin', 'view': 'RH'},
                   {'company': 'empresa_2', 'role': 'admin', 'view': 'Equipamento'},
                   {'company': 'empresa_2', 'role': 'admin', 'view': 'Fornecedor'},
                   {'company': 'empresa_2', 'role': 'admin', 'view': 'Almoxarifado'},
                   {'company': 'empresa_2', 'role': 'admin', 'view': 'Programação'},
                   {'company': 'empresa_2', 'role': 'admin', 'view': 'Manutenção'},
                   {'company': 'empresa_2', 'role': 'admin', 'view': 'Orçamento'},
                   {'company': 'empresa_2', 'role': 'admin', 'view': 'Indicadores'},

                   {'company': 'empresa_21', 'role': 'default', 'view': 'Plano'},
                   {'company': 'empresa_21', 'role': 'default', 'view': 'Empresa'},
                   {'company': 'empresa_21', 'role': 'default', 'view': 'RH'},
                   {'company': 'empresa_21', 'role': 'admin', 'view': 'Plano'},
                   {'company': 'empresa_21', 'role': 'admin', 'view': 'Empresa'},
                   {'company': 'empresa_21', 'role': 'admin', 'view': 'RH'},
                   {'company': 'empresa_21', 'role': 'admin', 'view': 'Equipamento'},
                   {'company': 'empresa_21', 'role': 'admin', 'view': 'Fornecedor'},
                   {'company': 'empresa_21', 'role': 'admin', 'view': 'Almoxarifado'},
                   {'company': 'empresa_21', 'role': 'admin', 'view': 'Programação'},
                   {'company': 'empresa_21', 'role': 'admin', 'view': 'Manutenção'},
                   {'company': 'empresa_21', 'role': 'admin', 'view': 'Orçamento'},
                   {'company': 'empresa_21', 'role': 'admin', 'view': 'Indicadores'},

                   {'company': 'empresa_22', 'role': 'default', 'view': 'Plano'},
                   {'company': 'empresa_22', 'role': 'default', 'view': 'Empresa'},
                   {'company': 'empresa_22', 'role': 'default', 'view': 'RH'},
                   {'company': 'empresa_22', 'role': 'admin', 'view': 'Plano'},
                   {'company': 'empresa_22', 'role': 'admin', 'view': 'Empresa'},
                   {'company': 'empresa_22', 'role': 'admin', 'view': 'RH'},
                   {'company': 'empresa_22', 'role': 'admin', 'view': 'Equipamento'},
                   {'company': 'empresa_22', 'role': 'admin', 'view': 'Fornecedor'},
                   {'company': 'empresa_22', 'role': 'admin', 'view': 'Almoxarifado'},
                   {'company': 'empresa_22', 'role': 'admin', 'view': 'Programação'},
                   {'company': 'empresa_22', 'role': 'admin', 'view': 'Manutenção'},
                   {'company': 'empresa_22', 'role': 'admin', 'view': 'Orçamento'},
                   {'company': 'empresa_22', 'role': 'admin', 'view': 'Indicadores'},

                   {'company': 'empresa_3', 'role': 'default', 'view': 'Plano'},
                   {'company': 'empresa_3', 'role': 'default', 'view': 'Empresa'},
                   {'company': 'empresa_3', 'role': 'default', 'view': 'RH'},
                   {'company': 'empresa_3', 'role': 'admin', 'view': 'Plano'},
                   {'company': 'empresa_3', 'role': 'admin', 'view': 'Empresa'},
                   {'company': 'empresa_3', 'role': 'admin', 'view': 'RH'},
                   {'company': 'empresa_3', 'role': 'admin', 'view': 'Equipamento'},
                   {'company': 'empresa_3', 'role': 'admin', 'view': 'Fornecedor'},
                   {'company': 'empresa_3', 'role': 'admin', 'view': 'Almoxarifado'},
                   {'company': 'empresa_3', 'role': 'admin', 'view': 'Programação'},
                   {'company': 'empresa_3', 'role': 'admin', 'view': 'Manutenção'},
                   {'company': 'empresa_3', 'role': 'admin', 'view': 'Orçamento'},
                   {'company': 'empresa_3', 'role': 'admin', 'view': 'Indicadores'}
                   ]

user_lista = [{'username': 'admin', 'email': 'admin@admin.com',
               'password': 'aaa11111', 'role': 'admin',
               'date': '1980/05/10 12:45:10', 'company': 'empresa_1'},
              {'username': 'leandro', 'email': 'engleoluz@hotmail.com',
               'password': 'aaa11111', 'role': 'default',
               'date': '1980/05/10 12:45:10', 'company': 'empresa_1'},
              {'username': 'danylo', 'email': 'danylo@gmail.com',
               'password': '12345678', 'role': 'admin',
               'date': '1980/05/10 12:45:10', 'company': 'empresa_1'},

              {'username': 'admin_empresa_2', 'email': 'admin_empresa_2@admin.com',
               'password': 'aaa11111', 'role': 'admin',
               'date': '1980/05/10 12:45:10', 'company': 'empresa_2'},

              {'username': 'admin_empresa_21', 'email': 'admin_empresa_21@admin.com',
               'password': 'aaa11111', 'role': 'admin',
               'date': '1980/05/10 12:45:10', 'company': 'empresa_21'},

              {'username': 'admin_empresa_22', 'email': 'admin_empresa_22@admin.com',
               'password': 'aaa11111', 'role': 'admin',
               'date': '1980/05/10 12:45:10', 'company': 'empresa_22'},

              {'username': 'admin_empresa_3', 'email': 'admin_empresa_3@admin.com',
               'password': 'aaa11111', 'role': 'admin',
               'date': '1980/05/10 12:45:10', 'company': 'empresa_3'},

              ]

group_lista = [{'name': 'cadeira', 'company': 'empresa_1'},
               {'name': 'elevador', 'company': 'empresa_1'},
               {'name': 'mesa', 'company': 'empresa_1'}
               ]

asset_lista = [{'cod': '000.001', 'short': 'computador', 'company': 'empresa_1'},
               {'cod': '000.002', 'short': 'mesa', 'company': 'empresa_1'},
               {'cod': '000.003', 'short': 'chiller', 'company': 'empresa_1'},
               {'cod': '000.004', 'short': 'carro', 'company': 'empresa_1'}
               ]

system_lista = [{'name': 'elétrico', 'cod': '000.001'},
                {'name': 'alvenaria', 'cod': '000.002'},
                {'name': 'hidraulico', 'cod': '000.003'},
                {'name': 'combustão', 'cod': '000.004'}
                ]

supplier_lista = [{'name': 'Fornecedor_1', 'company': 'empresa_1'},
                  {'name': 'Fornecedor_2', 'company': 'empresa_1'}
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


def generate_plans():
    planlista = list()
    for item in plans_lista:
        plan = Plan.query.filter_by(name=item['name']).first()
        if plan:
            planlista.append(plan)
            continue
        plan = Plan()
        plan.name = item['name']
        planlista.append(plan)
        try:
            db.session.add(plan)
            db.session.commit()
            print('Plano inserido:', plan.name)
        except Exception as e:
            log.error("Erro ao inserir o plano: %s, %s" % (str(plan), e))
            db.session.rollback()
    return planlista


def generate_views():
    viewlista = list()
    for item in views_lista:
        view = View.query.filter_by(name=item['name']).first()
        if view:
            viewlista.append(view)
            continue
        view = View()
        view.name = item['name']
        view.icon = item['icon']
        view.url = item['url']
        try:
            db.session.add(view)
            db.session.commit()
            print('Tela inserida:', view.name)
        except Exception as e:
            log.error("Erro ao inserir a tela: %s, %s" % (str(view), e))
            db.session.rollback()
    return viewlista


def generate_viewplans():
    viewplanlista = list()
    for item in viewplans_lista:
        view = View.query.filter_by(name=item['view']).first()
        plan = Plan.query.filter_by(name=item['plan']).first()
        viewplan = ViewPlan.query.filter_by(view_id=view.id, plan_id=plan.id).first()

        if viewplan:
            viewplanlista.append(viewplan)
            continue

        viewplan = ViewPlan()
        viewplan.view_id = view.id
        viewplan.plan_id = plan.id
        viewplan.active = True
        try:
            db.session.add(viewplan)
            db.session.commit()
            print('Tela inserida: %s no plano: %s' % (view.name, plan.name))
        except Exception as e:
            log.error("Erro ao inserir a tela/plano: %s, %s" % (str(view), e))
            db.session.rollback()
    return viewplanlista


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
        plan = Plan.query.filter_by(name=item['plano']).one()
        manager = Company.query.filter_by(name=item['manager']).first()
        company.manager_company_id = 1
        if manager:
            company.manager_company_id = manager.id
        company.name = item['name']
        company.cnpj = item['cnpj']
        company.cep = item['cep']
        company.logradouro = item['logradouro']
        company.bairro = item['bairro']
        company.municipio = item['municipio']
        company.uf = item['uf']
        company.numero = item['numero']
        company.complemento = item['complemento']
        company.email = item['email']
        company.active = True
        company.member_since = item['date']

        company.subbusiness_id = subbusiness.id
        company.plan_id = plan.id
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
        role = Role(name=item['name'], description=item['description'], company_id=company.id)
        try:
            role.save()
            print("Regra inserida: %s na empresa: %s" % (role.name, company.name))
        except Exception as e:
            log.error("Erro ao inserir a regra: %s, %s" % (str(role), e))
            db.session.rollback()
    return roles


def generate_viewroles():
    viewrolelista = list()
    for item in viewroles_lista:
        company = Company.query.filter_by(name=item['company']).one()
        role = Role.query.filter_by(name=item['role'], company_id=company.id).one()
        view = View.query.filter_by(name=item['view']).one()
        viewrole = ViewRole.query.filter_by(view_id=view.id, role_id=role.id).first()

        if viewrole:
            viewrolelista.append(viewrole)
            continue

        viewrole = ViewRole(role_id=role.id, view_id=view.id, active=True)
        try:
            viewrole.save()
            print('Tela inserida: %s no perfil: %s' % (view.name, role.name))
        except Exception as e:
            log.error("Erro ao inserir a tela: %s erro: %s" % (str(viewrole), e))
            db.session.rollback()
    return viewrolelista


def generate_users():
    users = list()
    for item in user_lista:
        user = User.query.filter_by(username=item['username']).first()
        if user:
            users.append(user)
            continue
        user = User()
        company = Company.query.filter_by(name=item['company']).one()
        role = Role.query.filter_by(name=item['role'], company_id=company.id).one()
        user.username = item['username']
        user.email = item['email']
        user.password = item['password']
        user.member_since = item['date']
        user.confirmed = True
        user.active = True
        user.role_id = role.id
        user.company_id = company.id
        try:
            user.save()
            # db.session.add(user)
            # db.session.commit()
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
generate_views()
generate_plans()
generate_viewplans()
generate_companies()

# carregamento para os perfis e usuários
generate_roles()
generate_viewroles()
generate_users()

# carregamento para os equipamentos
generate_group()
generate_asset()
generate_system()

# carregamento para os fornecedores
generate_supplier()

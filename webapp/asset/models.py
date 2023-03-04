import logging
from webapp import db
from flask_login import current_user

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

class System(db.Model):
    """    Classe de sistemas dentro dos ativos   """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    asset_id = db.Column(db.Integer(), db.ForeignKey("asset.id"))
    asset = db.relationship("Asset", back_populates="system")

    def __repr__(self):
        return f'<System: {self.id}-{self.name}>'

    def change_attributes(self, form):
        """    Função para alterar os atributos do objeto    """
        self.name = form.name.data
        self.asset_id = form.asset.data

    def save(self) -> bool:
        """    Função para salvar no banco de dados o objeto"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False


class Group(db.Model):
    """    Classe de grupo de ativos    """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    company_id = db.Column(db.Integer(), nullable=False)
    asset = db.relationship("Asset", back_populates="group")

    def __repr__(self):
        return f'<Group: {self.id}-{self.name}>'

    def change_attributes(self, form):
        """    Função para alterar os atributos do objeto    """
        self.name = form.name.data
        self.company_id = form.company.data

    def save(self) -> bool:
        """    Função para salvar no banco de dados o objeto"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False


class Asset(db.Model):
    """    Classe do ativo    """
    file_name='padrão_equipamentos'
    titles=['Código','Descrição_Curta','Descrição_Longa','Fábrica','Marca','Modelo',
            'Número_Série','Largura','Comprimento','Altura','Peso','Ano_Fabricação',
            'Data_Aquisição','Data_Instalação','Custo_Aquisição','Taxa_Depreciação',
            'Tag','Centro_Custo','Grupo_Equipamentos','Sistema','Ativo']

    id = db.Column(db.Integer(), primary_key=True)
    cod = db.Column(db.String(50), nullable=True)
    short_description = db.Column(db.String(50), nullable=True)
    long_description = db.Column(db.String(50), nullable=True)
    manufacturer = db.Column(db.String(50), nullable=True)
    brand = db.Column(db.String(50), nullable=True)
    model = db.Column(db.String(50), nullable=True)
    ns = db.Column(db.String(50), nullable=True)
    dimension_x = db.Column(db.Integer(), nullable=True)
    dimension_y = db.Column(db.Integer(), nullable=True)
    dimension_z = db.Column(db.Integer(), nullable=True)
    weight = db.Column(db.Integer(), nullable=True)
    year_manufacture = db.Column(db.DateTime(), nullable=True)
    date_acquisition = db.Column(db.DateTime(), nullable=True)
    date_installation = db.Column(db.DateTime(), nullable=True)
    cost_acquisition = db.Column(db.Integer(), nullable=True)
    depreciation = db.Column(db.Integer(), nullable=True)
    tag = db.Column(db.Integer(), nullable=True)
    cost_center = db.Column(db.String(50), nullable=True)
    active = db.Column(db.Boolean, default=True)

    group_id = db.Column(db.Integer(), db.ForeignKey("group.id"))
    group = db.relationship("Group", back_populates="asset")
    company_id = db.Column(db.Integer(), db.ForeignKey("company.id"))
    company = db.relationship("Company", back_populates="asset")

    system = db.relationship("System", back_populates="asset")


    def __repr__(self):
        return f'<Asset: {self.id}-{self.name}>'

    def get_active(self):
        return self.active

    def set_active(self, active):
        self.active = active

    def change_attributes(self, form):
        """    Função para alterar os atributos do objeto    """
        self.cod = form.cod.data
        self.short_description = form.short_description.data
        self.long_description = form.long_description.data
        self.manufacturer = form.manufacturer.data
        self.brand = form.brand.data
        self.model = form.model.data
        self.ns = form.ns.data
        self.dimension_x = form.dimension_x.data
        self.dimension_y = form.dimension_y.data
        self.dimension_z = form.dimension_z.data
        self.weight = form.weight.data
        self.year_manufacture = form.year_manufacture.data
        self.date_acquisition = form.date_acquisition.data
        self.date_installation = form.date_installation.data
        self.cost_acquisition = form.cost_acquisition.data
        self.depreciation = form.depreciation.data
        self.tag = form.tag.data
        self.cost_center = form.cost_center.data
        self.active = form.active.data
        self.group_id = form.group.data
        self.company_id = current_user.company_id

    def change_active(self):
        if self.active:
            self.set_active(False)
        else:
            self.set_active(True)

    def save(self) -> bool:
        """    Função para salvar no banco de dados o objeto"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            log.error(f'Erro salvar no banco de dados: {self.__repr__()}:{e}')
            db.session.rollback()
            return False

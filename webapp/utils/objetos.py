import logging
from webapp import db

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)


def atributo_existe(objeto1, atributo, subatributo):
    """Função que realiza uma busca do objeto e do atributo vinculado ao modelo"""
    if hasattr(objeto1, atributo):
        objeto2 = getattr(objeto1, atributo)
        if hasattr(objeto2, subatributo):
            return getattr(objeto2, subatributo)
    return None


def atribuir_none_id(valor):
    """Função que retorna none ou o valor do id"""
    if valor == 0:
        return None
    else:
        return valor


def salvar_lote(lote):
    """Função para salvar em lote"""
    try:
        db.session.add_all(lote)
        db.session.commit()
        return True
    except Exception as e:
        log.error(f'Erro salvar ao tentar salvar o lote:{e}')
        db.session.rollback()
    return False

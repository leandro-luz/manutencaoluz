import logging
from webapp import db
from dateutil.parser import parse
from webapp.utils.tools import criptografar

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


def salvar(objetos) -> bool:
    """Função para salvar objetos no banco de dados"""
    try:
        if isinstance(objetos, list):
            db.session.add_all(objetos)
        else:
            db.session.add(objetos)

        db.session.commit()
        return True
    except Exception as e:
        log.error(f'Erro ao salvar no banco de dados: {e}')
        db.session.rollback()
        return False


def excluir(objetos) -> bool:
    """Função para excluir objetos no banco de dados"""
    try:
        if isinstance(objetos, list):
            for objeto in objetos:
                db.session.delete(objeto)
        else:
            db.session.delete(objetos)

        db.session.commit()
        return True
    except Exception as e:
        log.error(f'Erro ao excluir no banco de dados: {e}')
        db.session.rollback()
        return False


def preencher_objeto_atributos_semvinculo(objeto_model, dicionario, df, linha):
    """Função para preencher os atributos não vinculados a outros objetos/tabelas, sem consultar"""
    for chave, atributo in dicionario.items():
        # recupere o valor
        valor = df.at[linha, chave]
        if str(valor).isnumeric() or valor is None:
            # Salva o atributo se o valor e numerico ou nulo
            setattr(objeto_model, atributo, valor)
        else:
            # Salva o atributo quando texto
            setattr(objeto_model, atributo, valor)
    return objeto_model


def preencher_objeto_atributos_booleanos(objeto_model, dicionario, df, linha):
    """Função para preencher os atributos não vinculados a outros objetos/tabelas, sem consultar"""
    ativos = ['SIM', 'OK', 'POSITIVO', 'VERDADEIRO', 1, '1', 'TRUE', True, 'Ativo']
    for chave, atributo in dicionario.items():
        # Recupere o valor e valide
        valor = df.at[linha, chave]
        ativo = valor in ativos if valor is not None else False
        # Preenche o objeto
        setattr(objeto_model, atributo, ativo)
    return objeto_model


def extrairClasseTexto(texto):
    lista = texto.split("_")
    if len(lista) == 2:
        return str(lista[0]).capitalize()
    else:
        return str(lista[1]).capitalize()


def preencher_objeto_atributos_datas(objeto_model, dicionario, df, linha):
    """Função para preencher os atributos não vinculados a outros objetos/tabelas, sem consultar"""
    for chave, atributo in dicionario.items():
        valor = df.at[linha, chave]

        try:
            # Tenta fazer o parse da data
            data = parse(valor)
            setattr(objeto_model, atributo, data)
        except ValueError:
            # Se não for uma data válida, defina como None ou outro valor padrão
            setattr(objeto_model, atributo, None)  # ou 0 ou qualquer outro valor padrão

    return objeto_model


def criptografar_id_lista(objetos):
    for objeto in objetos:
        setattr(objeto, 'id_criptografado', criptografar(str(objeto.id)))

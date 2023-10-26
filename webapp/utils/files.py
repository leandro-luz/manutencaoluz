import logging
from pathlib import Path
from csv import writer
import pandas as pd
import numpy as np
import csv
from io import StringIO

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

downloads_path = str(Path.home() / "Downloads")

EXTENSOES_VALIDAS = {'csv'}


def arquivo_padrao(nome_arquivo, valores):
    """    Função que gera o arquivo padrão para o cadastro em lote de equipamentos    """
    try:
        # nome do arquivo
        nome = nome_arquivo + '.csv'
        # gerando os valores
        df = pd.DataFrame(valores)
        # excluindo a primeira linha
        df.columns = df.loc[0]
        df = df.drop(0)
        arquivo = df.to_csv(index=False)
        return True, nome, arquivo
    except Exception as e:
        log.error(f'Erro ao gerar o arquivo: {nome_arquivo}-{e}')
        return False


def verificar_extensao(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in EXTENSOES_VALIDAS


def lista_para_csv(lista, titulos):
    # Cria um objeto CSV em memória
    output = StringIO()
    csv_writer = csv.writer(output, dialect='excel')

    # Escreve os nomes dos titulos
    if titulos:
        csv_writer.writerow(titulos)

    # Escreve os dados da lista no objeto CSV
    for item in lista:
        csv_writer.writerow(item)

    # Retorna o objeto CSV como uma string
    return output.getvalue()





#
# from sqlalchemy.orm import class_mapper
# import sqlalchemy
# def attribute_names(cls):
#     return [prop.key for prop in class_mapper(cls).iterate_properties
#             if isinstance(prop, sqlalchemy.orm.ColumnProperty)]
# print(attribute_names(Empresa))

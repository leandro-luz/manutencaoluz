import csv
import logging
from io import StringIO
from pathlib import Path

import pandas as pd

from webapp.sistema.models import LogsEventos

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
        LogsEventos.registrar("erro", arquivo_padrao.__name__, erro=e)
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


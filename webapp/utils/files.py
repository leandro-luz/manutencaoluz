import logging
from pathlib import Path
from csv import writer

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

downloads_path = str(Path.home() / "Downloads")

EXTENSOES_VALIDAS = {'csv'}


def arquivo_padrao(nome_arquivo, valores):
    """    Função que gera o arquivo padrão para o cadastro em lote de equipamentos    """
    path = downloads_path + '\\' + nome_arquivo + '.csv'
    try:
        with open(path, 'w', newline='') as arquivo:
            escritor_csv = writer(arquivo, delimiter=';')
            escritor_csv.writerows(valores)
        return True, path
    except Exception as e:
        log.error(f'Erro ao gerar o arquivo: {nome_arquivo}-{e}')
        return False, path


def verificar_extensao(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in EXTENSOES_VALIDAS

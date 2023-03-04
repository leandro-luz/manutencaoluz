import logging
from pathlib import Path
from csv import writer

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
log = logging.getLogger(__name__)


downloads_path = str(Path.home() / "Downloads")


def file_standard(file_name, titles):
    """    Função que gera o arquivo padrão para o cadastro em lote de equipamentos    """
    path = downloads_path+'\\'+file_name+'.csv'
    try:
        with open(path, 'w') as arquivo:
            escritor_csv = writer(arquivo)
            escritor_csv.writerow(titles)
        return True, path
    except Exception as e:
        log.error(f'Erro ao gerar o arquivo: {file_name}-{e}')
        return False, path

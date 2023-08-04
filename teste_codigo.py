from datetime import datetime

# print(datetime.datetime.now())
# print(datetime.datetime.utcnow())


#
#
# name_of_file = input("What is the razao_social of the file: ")
# completeName = '/home/user/Documents/'+ name_of_file + ".txt"
# file1 = open(completeName , "w")
# toFile = input("Write what you want into the field")
# file1.write(toFile)
# file1.close()

# from pathlib import Path
# from csv import writer
#
# downloads_path = str(Path.home() / "Downloads")
#
#
# with open(downloads_path+'/teste.csv', 'w') as arquivo:
#     escritor_csv = writer(arquivo)
#     escritor_csv.writerow(['Código','Descrição_Curta','Descrição_Longa','Fábrica','Marca','Modelo',
#                            'Número_Série','Largura','Comprimento','Altura','Peso','Ano_Fabricação',
#                            'Data_Aquisição','Data_Instalação','Custo_Aquisição','Taxa_Depreciação',
#                            'Tag','Centro_Custo','Grupo_Equipamentos','Sistema','Ativo'])
#


# a = datetime.datetime.now()
# b = datetime.datetime.now() + datetime.timedelta(5)
# c = datetime.timedelta(30)
#
# if b-a < c:
#     print('menor')
# else:
#     print('maior')


# lista = [{'razao_social': 'admin_', 'email': 'email1'}, {'razao_social': 'adminluz_', 'email': 'email2'}]
#
# for x in lista:
#     print(x['razao_social'])
#     print(x['email'])

#
# import requests
#
# cep = "20.090-002"
#
# cep = cep.replace("-", "").replace(".", "").replace(" ", "")
#
# cnpj = "33291488000102"
# cnpj2 = "30722226000167"
#
#
# if len(cep) == 8:
#     # link = f'https://viacep.com.br/ws/{cep}/json/'
#     link = f'https://receitaws.com.br/v1/cnpj/{cnpj2}'
#     print(link)
#
#     requisicao = requests.get(link)
#
#     print(requisicao)
#
#     dic_requisicao = requisicao.json()
#
#     print(dic_requisicao['atividade_principal'])
#
#     print(dic_requisicao)
# else:
#     print("CEP Inválido")
# #


# valor = {'ultima_atualizacao': '2023-03-02T04:04:24.780Z'}
#
# valor2 = valor['ultima_atualizacao']
# print(valor2)
# print(type(valor2))
# tempo = datetime.strptime(valor2, "%Y-%m-%dT%H:%M:%S.%fZ")
# print(tempo)
# print(type(tempo))


# def programacao_ordem_servico():
#     """ Função que executa a verificação para a geração das OS dos planos de manutenção  """
#     # agenda a nova execução
#     programacao.enter(24 * 60 * 60, 1, programacao_ordem_servico)
#
#     # executa a verificação para gerar as OS
#     print(f"{datetime.now()}: teste")


# def data_futura(tempo, unidade):
#     """ Função que calcula e retorna uma data no futuro"""
#     # Verifica se a base do tempo é dia
#     if unidade in ["Diária", "Semanal"]:
#         return datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + \
#                datetime.timedelta(days=tempo)
#
#     # Verifica se a base do tempo é mensal
#     if unidade in ["Mensal", "Bimensal", "Trimensal", "Semestral", "Anual"]:
#         return datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + \
#                relativedelta(months=tempo)
#
#
# print(data_futura(1, "Diária"))
# print(data_futura(1, "Mensal"))
# print(data_futura(6, "Semestral"))
# print(data_futura(12, "Anual"))


from flask_apscheduler import APScheduler


sched = APScheduler()

def teste_1():
    print(f'teste_1: {datetime.now()}')

def teste_2():
    pass

print("a")
sched.add_job(id='te_1', func=teste_1, trigger='interval', seconds=5)
sched.start()
print("b")












# import datetime
# from dateutil.relativedelta import *
#
# agora = datetime.datetime.now()
# agora_ajustada = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
# amanha = agora_ajustada + datetime.timedelta(hours=22)
#
# print(f'agora: {agora}')
# print(f'amanhã: {amanha}')
# print(f'diferenca: {(amanha - agora).seconds}')





































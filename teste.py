# from dotenv import dotenv_values
import datetime
import os
from webapp import create_app
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python


from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# message = Mail(
#     from_email='engleoluz@hotmail.com',
#     to_emails='guguleo2019@gmail.com',
#     subject='Sending with Twilio SendGrid is Fun',
#     html_content='<strong>and easy to do anywhere, even with Python</strong>')
# try:
#     sg = SendGridAPIClient('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')
#     response = sg.send(message)
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
# except Exception as e:
#     print(e)


# print(environ.get('SENDGRID_API_KEY'))
# for a in os.environ:
#     print(a)

# config = dotenv_values("sendgrid.env", encoding="utf-8")
# print(config)


#
# def data_futura(tempo, nome):
#     """ Função que calcula e retorna uma data no futuro"""
#     # Fator basico
#     fator = 1
#     # Verifica qual a nome de tempo
#     if nome == "Mensal" or  \
#             nome == "Bimensal" or  \
#             nome == "Trimensal" or  \
#             nome == "Semestral":
#         fator = 30
#     if nome == "Anual":
#         fator  = 365
#
#     # retorna a data futura
#     return datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + \
#            datetime.timedelta(days=tempo * fator)
#
# print(data_futura(7, "Semanal"))
# print(data_futura(1, "Mensal"))
# print(data_futura(2, "Bimensal"))
# print(data_futura(3, "Trimensal"))
# print(data_futura(6, "Semestral"))
# print(data_futura(1, "Anual"))

from webapp.equipamento.models import Equipamento
from webapp.empresa.models import Empresa
from webapp.plano_manutencao.models import PlanoManutencao
from webapp.ordem_servico.models import OrdemServico
from webapp.contrato.models import Contrato
from webapp.usuario.models import Usuario
from webapp.supplier.models import Supplier

# titulos_doc = {'Código*': 'cod', 'Descrição_Curta*': 'descricao_curta','Tag*': 'tag',
#                'Subgrupo*': 'subgrupo_id','Descrição_Longa': 'descricao_longa','Fábrica': 'fabricante',
#                'Marca': 'marca','Modelo': 'modelo','Número_Série': 'ns','Largura': 'largura',
#                'Comprimento': 'comprimento','Altura': 'altura','Peso': 'peso','Potência': 'potencia',
#                'Tensão': 'tensao','Ano_Fabricação': 'data_fabricacao','Data_Aquisição': 'data_aquisicao',
#                'Data_Instalação': 'data_instalacao','Custo_Aquisição': 'custo_aquisicao',
#                'Taxa_Depreciação': 'depreciacao','Patrimônio': 'patrimonio','Localização': 'localizacao',
#                'Latitude': 'latitude','Longitude': 'longitude','Centro_Custo': 'centro_custo','Ativo': 'ativo'}
#

# env = os.environ.get('WEBAPP_ENV', 'dev')
# app = create_app('config.%sConfig' % env.capitalize())
# app.app_context().push()
#
# empresas = Empresa.query.all()
#
# cnpj = '07.233.546/0001-31'
# razao_social = 'RAZAOSOCIAL_EMPRESATESTE_1'
# nome_fantasia = 'NOMEFANTASIA_EMPRESATESTE_3'
#
# repetidos =[]
#
# for empresa in empresas:
#     if empresa.cnpj == cnpj:
#         repetidos.append([empresa.cnpj, 'cnpj repetido'])
#     if empresa.razao_social == razao_social:
#         repetidos.append([empresa.cnpj, 'razao social repetido'])
#     if empresa.nome_fantasia == nome_fantasia:
#         repetidos.append([empresa.cnpj, 'nome_fantasia repetido'])
#
# if len(repetidos)> 0:
#     for rep in repetidos:
#         print(rep)

import csv
from pathlib import Path
#
# downloads_path = str(Path.home() / "Downloads")
#
# path = downloads_path + '\\' + 'countries.csv'
#
# header = ['name', 'area', 'country_code2', 'country_code3']
# data = [
#     ['Albania', 28748, 'AL', 'ALB'],
#     ['Algeria', 2381741, 'DZ', 'DZA'],
#     ['American Samoa', 199, 'AS', 'ASM'],
#     ['Andorra', 468, 'AD', 'AND'],
#     ['Angola', 1246700, 'AO', 'AGO']
# ]
#
# header2 = ['tipo', 'cnpj', 'motivo']
#
# data2 = [
#     ['CNPJ:', '07.233.546/0001-31', 'rejeitado devido CNPJ já existir no banco de dados'],
#     ['CNPJ:', '07.233.546/0001-31', 'rejeitado devido RAZÃO SOCIAL já existir no banco de dados'],
#     ['CNPJ:', '07.233.546/0001-31', 'rejeitado devido NOME FANTASIA já existir no banco de dados'],
#     ['CNPJ:', '69.596.231/0001-06', 'rejeitado devido CNPJ já existir no banco de dados'],
#     ['CNPJ:', '69.596.231/0001-06', 'rejeitado devido RAZÃO SOCIAL já existir no banco de dados'],
#     ['CNPJ:', '69.596.231/0001-06', 'rejeitado devido NOME FANTASIA já existir no banco de dados'],
#     ['CNPJ:', '16.899.764/0001-09', 'rejeitado devido CNPJ já existir no banco de dados'],
#     ['CNPJ:', '16.899.764/0001-09', 'rejeitado devido RAZÃO SOCIAL já existir no banco de dados'],
#     ['CNPJ:', '16.899.764/0001-09', 'rejeitado devido NOME FANTASIA já existir no banco de dados'],
#     ['CNPJ:', '51.598.754/0001-26', 'rejeitado devido CNPJ já existir no banco de dados'],
#     ['CNPJ:', '51.598.754/0001-26', 'rejeitado devido RAZÃO SOCIAL já existir no banco de dados'],
#     ['CNPJ:', '51.598.754/0001-26', 'rejeitado devido NOME FANTASIA já existir no banco de dados'],
#     ['CNPJ:', '70.039.894/0001-09', 'rejeitado devido CNPJ já existir no banco de dados'],
#     ['CNPJ:', '70.039.894/0001-09', 'rejeitado devido RAZÃO SOCIAL já existir no banco de dados'],
#     ['CNPJ:', '70.039.894/0001-09', 'rejeitado devido NOME FANTASIA já existir no banco de dados'],
#     ['CNPJ:', '61.748.330/0001-54', 'rejeitado devido CNPJ já existir no banco de dados'],
#     ['CNPJ:', '61.748.330/0001-54', 'rejeitado devido RAZÃO SOCIAL já existir no banco de dados'],
#     ['CNPJ:', '61.748.330/0001-54', 'rejeitado devido NOME FANTASIA já existir no banco de dados'],
#     ['CNPJ:', '07.233.546/0001-31', 'rejeitado devido CNPJ já existir no banco de dados'],
#     ['CNPJ:', '07.233.546/0001-31', 'rejeitado devido RAZÃO SOCIAL já existir no banco de dados'],
#     ['CNPJ:', '07.233.546/0001-31', 'rejeitado devido NOME FANTASIA já existir no banco de dados']
# ]
#
# titulos_doc = {
#     'CNPJ*': 'cnpj', 'Razão_Social*': 'razao_social', 'Nome_Fantasia*': 'nome_fantasia',
#     'Tipo*': 'tipo', 'CEP*': 'cep', 'Logradouro*': 'logradouro', 'Número*': 'numero',
#     'Bairro*': 'bairro', 'Município*': 'municipio', 'UF*': 'uf',
#     'Email*': 'email', 'Telefone*': 'telefone', 'Contrato*': 'contrato_id',
#     'Data_Abertura': 'data_abertura',
#     'Situação': 'situacao', 'Porte': 'porte', 'Natureza_Jurídica': 'natureza_juridica',
#     'CNAE_P_Código': 'cnae_principal', 'CNAE_P_Texto': 'cnae_principal_texto',
#     'Inscrição_Estadual': 'inscricao_estadual', 'Inscrição_Municipal': 'inscricao_municipal',
#     'Localização': 'localizacao', 'Complemento': 'complemento', 'Nome_Responsável': 'nome_responsavel',
#     'Ativo': 'ativo'
# }
#
#
# titulos = [x for x in titulos_doc]
# print(titulos)

# with open(path, 'w', newline='') as f:
#     writer = csv.writer(f, delimiter=';')
#
#     # write the header
#     # writer.writerow(header2)
#
#     # write multiple rows
#     writer.writerows(titulos_doc)


# ativos = ['SIM', 'OK', 'POSITIVO', 'VERDADEIRO', 1, 'TRUE', True, 'Ativo']
#
# itens = ['sim', True, '', 'aa', 1]
#
# for item in itens:
#
#     if item in ativos:
#         print(f'{item}: presente')
#     else:
#         print(f'{item}: não presente')


import pandas as pd

# create a sample dataframe
# df = pd.DataFrame({
#     'Name': ['Alice', 'Bob', 'Charlie', 'David'],
#     'Age': [25, 30, 35, 40],
#     'Salary': [50000, 60000, 70000, 80000]
# })
# colunas_importada = df.columns
#
#
# colunas_base = {'Name': 'name', 'Nota': 'nota', 'Age': 'age', 'Endereco': 'endereco', 'Salary': 'salary'}
#
# nomes = []
# for i in colunas_base:
#     nomes.append(colunas_base[i])
#
# df_final = pd.DataFrame(columns=nomes)
#
# for col in colunas_importada:
#     df_final[colunas_base[col]] = df[col]
#
# print(df_final)

# nomes=['Name','Nota','Age','Endereco','Salary']
# df2 = pd.DataFrame(columns=nomes)
#
# print(df2)
#
# for a in df.columns:
#     print(a)

# from datetime import datetime, timezone, timedelta
#
# data_e_hora_atuais = datetime.now()
# fuso_horario = timezone('America/Sao_Paulo')
# print(fuso_horario)
#
# import pytz
# import datetime
#
# def data_atual_utc():
#     """Função que retorna a data atual corrigindo para o UTC"""
#     local_timezone = 'America/Sao_Paulo'
#     data_atual = datetime.datetime.now()
#     try:
#         tz = pytz.timezone(local_timezone)
#         utc_offset = tz.utcoffset(data_atual).total_seconds()/3600
#
#         # Retornar a data corrigida
#         return data_atual + datetime.timedelta(hours=utc_offset)
#     except pytz.UnknownTimeZoneError:
#         return data_atual


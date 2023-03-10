import datetime

# print(datetime.datetime.now())
# print(datetime.datetime.utcnow())


#
#
# name_of_file = input("What is the name of the file: ")
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



lista = [{'nome': 'admin_', 'email': 'email1'}, {'nome': 'adminluz_', 'email': 'email2'}]

for x in lista:
    print(x['nome'])
    print(x['email'])
import unittest
import os
from webapp import create_app

env = os.environ.get('WEBAPP_ENV', 'Test')
app = create_app('config.%sConfig' % env.capitalize())
app.app_context().push()

from webapp.usuario.models import PerfilAcesso, Senha, Usuario, TelaPerfilAcesso

from funcoes_sistema import criar_contrato
from webapp.contrato.models import Contrato

from webapp import db

print("Excluindo todas as tabelas")
db.drop_all()
print("Criando todas as tabelas")
db.create_all()


class Test_Auth(unittest.TestCase):
    # def test_role_change_atributes(self):
    #     form = PerfilForm
    #     name = 'regra_teste'
    #     descricao = 'testando a gravação de um regra'
    #     company = 1
    #     form.name.data = name
    #     form.description.data = descricao
    #     form.company.data = company
    #
    #     role = PerfilAcesso()
    #     role.alterar_atributos(form)
    #
    #     self.assertEqual(role.nome, name)
    #     self.assertEqual(role.descricao, descricao)
    #     self.assertEqual(role.empresa_id, company)

    def test_criar_contratos(self):
        contratos_lista = [
            {'nome': 'COMPLETO_1', 'ativo': True, 'empresa': None},
            {'nome': 'COMPLETO_2', 'ativo': True, 'empresa': None},
            {'nome': 'COMPLETO_3', 'ativo': True, 'empresa': None}
        ]

        # Inserindo os contratos na base de dados
        criar_contrato(contratos_lista)

        # Verificando se os contratos foram inseridos corretamente
        assert len(Contrato.query.all()) == 3

        # Tentando inserir os mesmos contratos novamente
        criar_contrato(contratos_lista)

        # Verificando se nenhum contrato foi inserido
        assert len(Contrato.query.all()) == 3


if __name__ == '__main__':
    unittest.main()

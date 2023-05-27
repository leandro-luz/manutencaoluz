import unittest
import os
from webapp import create_app


env = os.environ.get('WEBAPP_ENV', 'test')
app = create_app('config.%sConfig' % env.capitalize())
app.app_context().push()

from webapp.usuario.models import Perfil, Senha, Usuario, Telaperfil
from webapp.usuario.forms import PerfilForm
from dados_sistema import criar_contrato
from webapp.contrato.models import Contrato


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
    #     role = Perfil()
    #     role.alterar_atributos(form)
    #
    #     self.assertEqual(role.nome, name)
    #     self.assertEqual(role.descricao, descricao)
    #     self.assertEqual(role.empresa_id, company)


    contratos_lista = [{'nome': 'Contrato 1'}, {'nome': 'Contrato 2'}, {'nome': 'Contrato 3'}]

    def test_criar_contratos(self, contratos_lista):
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





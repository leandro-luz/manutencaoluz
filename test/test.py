import unittest
import os
from webapp import create_app


env = os.environ.get('WEBAPP_ENV', 'test')
app = create_app('config.%sConfig' % env.capitalize())
app.app_context().push()

from webapp.usuario.models import Perfil, Senha, Usuario, ViewRole
from webapp.usuario.forms import RoleForm


class Test_Auth(unittest.TestCase):
    def test_role_change_atributes(self):
        form = RoleForm
        name = 'regra_teste'
        descricao = 'testando a gravação de um regra'
        company = 1
        form.name.data = name
        form.description.data = descricao
        form.company.data = company

        role = Perfil()
        role.alterar_atributos(form)

        self.assertEqual(role.nome, name)
        self.assertEqual(role.descricao, descricao)
        self.assertEqual(role.empresa_id, company)



if __name__ == '__main__':
    unittest.main()





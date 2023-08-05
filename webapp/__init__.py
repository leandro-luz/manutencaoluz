from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
# debug_toolbar = DebugToolbarExtension()
mail = Mail()


def create_app(object_name: str) -> Flask:
    """Criar a aplicação com os recursos"""
    app = Flask(__name__)
    app.config.from_object(object_name)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    # debug_toolbar.init_app(app)

    from webapp.usuario import criar_modulo as criar_modulo_usuario
    from webapp.main import criar_modulo as criar_modulo_main
    from webapp.sistema import criar_modulo as criar_modulo_sistema
    from webapp.empresa import criar_modulo as criar_modulo_empresa
    from webapp.equipamento import criar_modulo as criar_modulo_equipamento
    from webapp.supplier import criar_modulo as criar_modulo_fornecedor
    from webapp.contrato import criar_modulo as criar_modulo_contrato
    from webapp.plano_manutencao import criar_modulo as criar_modulo_plano_manutencao
    from webapp.ordem_servico import criar_modulo as criar_modulo_ordem_servico

    criar_modulo_usuario(app)
    criar_modulo_main(app)
    criar_modulo_sistema(app)
    criar_modulo_empresa(app)
    criar_modulo_equipamento(app)
    criar_modulo_fornecedor(app)
    criar_modulo_contrato(app)
    criar_modulo_plano_manutencao(app)
    criar_modulo_ordem_servico(app)

    # app.register_error_handler(404, page_not_found)
    return app

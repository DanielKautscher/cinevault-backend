"""
Ponto de entrada da aplicação CineVault.

Este arquivo é responsável apenas por:
- criar a instância do Flask
- configurar CORS e Swagger
- registrar os controllers (blueprints)
- inicializar o banco de dados

Toda a lógica de negócio e acesso a dados fica nas camadas de
services e repositories, mantendo este arquivo enxuto.
"""
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

from database import init_db
from controllers.filme_controller import filme_bp
from controllers.avaliacao_controller import avaliacao_bp

app = Flask(__name__)
CORS(app)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/",
}

template = {
    "swagger": "2.0",
    "info": {
        "title": "CineVault API",
        "description": "API para gerenciamento de catálogo de filmes",
        "version": "1.0.0",
    },
    "basePath": "/",
    "schemes": ["http"],
}

swagger = Swagger(app, config=swagger_config, template=template)

# Registra as rotas de cada camada de controller
app.register_blueprint(filme_bp)
app.register_blueprint(avaliacao_bp)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)

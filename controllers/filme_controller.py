"""
Camada de controller (rotas) para filmes.

Responsável apenas por receber a requisição HTTP, repassar para a camada
de serviço e devolver a resposta. Não contém regra de negócio nem SQL.
"""
from flask import Blueprint, request, jsonify

from services import filme_service as service
from services.filme_service import ErroValidacao, ErroNaoEncontrado

filme_bp = Blueprint("filme", __name__)


@filme_bp.route("/cadastrar_filme", methods=["POST"])
def cadastrar_filme():
    """
    Cadastra um novo filme no catálogo
    ---
    tags:
      - Filmes
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - titulo
            - diretor
            - ano
            - genero
          properties:
            titulo:
              type: string
              example: "Duna"
            diretor:
              type: string
              example: "Denis Villeneuve"
            ano:
              type: integer
              example: 2021
            genero:
              type: string
              example: "Ficção Científica"
            sinopse:
              type: string
            nota:
              type: number
              example: 8.0
            poster_url:
              type: string
            duracao:
              type: integer
              example: 155
            idioma:
              type: string
              example: "Inglês"
    responses:
      201:
        description: Filme cadastrado com sucesso
      400:
        description: Dados inválidos
    """
    try:
        filme_id = service.cadastrar_filme(request.get_json())
        return jsonify({"mensagem": "Filme cadastrado com sucesso!", "id": filme_id}), 201
    except ErroValidacao as e:
        return jsonify({"erro": str(e)}), 400


@filme_bp.route("/buscar_filmes", methods=["GET"])
def buscar_filmes():
    """
    Retorna todos os filmes do catálogo
    ---
    tags:
      - Filmes
    parameters:
      - in: query
        name: genero
        type: string
        description: Filtrar por gênero
      - in: query
        name: ordem
        type: string
        enum: [nota, ano, titulo]
        description: Ordenar por campo
    responses:
      200:
        description: Lista de filmes
    """
    genero = request.args.get("genero")
    ordem = request.args.get("ordem", "titulo")
    filmes = service.listar_filmes(genero=genero, ordem=ordem)
    return jsonify(filmes), 200


@filme_bp.route("/buscar_filme/<int:filme_id>", methods=["GET"])
def buscar_filme(filme_id):
    """
    Busca um filme específico pelo ID
    ---
    tags:
      - Filmes
    parameters:
      - in: path
        name: filme_id
        type: integer
        required: true
    responses:
      200:
        description: Dados do filme
      404:
        description: Filme não encontrado
    """
    try:
        filme = service.obter_filme(filme_id)
        return jsonify(filme), 200
    except ErroNaoEncontrado as e:
        return jsonify({"erro": str(e)}), 404


@filme_bp.route("/buscar_filme_titulo", methods=["GET"])
def buscar_filme_titulo():
    """
    Busca filmes pelo título (pesquisa parcial)
    ---
    tags:
      - Filmes
    parameters:
      - in: query
        name: q
        type: string
        required: true
        description: Termo de busca
    responses:
      200:
        description: Filmes encontrados
      400:
        description: Parâmetro ausente
    """
    try:
        filmes = service.buscar_por_titulo(request.args.get("q", ""))
        return jsonify(filmes), 200
    except ErroValidacao as e:
        return jsonify({"erro": str(e)}), 400


@filme_bp.route("/atualizar_filme/<int:filme_id>", methods=["PUT"])
def atualizar_filme(filme_id):
    """
    Atualiza os dados de um filme
    ---
    tags:
      - Filmes
    parameters:
      - in: path
        name: filme_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            titulo:
              type: string
            diretor:
              type: string
            ano:
              type: integer
            genero:
              type: string
            sinopse:
              type: string
            nota:
              type: number
            duracao:
              type: integer
    responses:
      200:
        description: Filme atualizado com sucesso
      404:
        description: Filme não encontrado
    """
    try:
        service.atualizar_filme(filme_id, request.get_json())
        return jsonify({"mensagem": "Filme atualizado com sucesso!"}), 200
    except ErroNaoEncontrado as e:
        return jsonify({"erro": str(e)}), 404
    except ErroValidacao as e:
        return jsonify({"erro": str(e)}), 400


@filme_bp.route("/deletar_filme/<int:filme_id>", methods=["DELETE"])
def deletar_filme(filme_id):
    """
    Remove um filme do catálogo
    ---
    tags:
      - Filmes
    parameters:
      - in: path
        name: filme_id
        type: integer
        required: true
    responses:
      200:
        description: Filme removido com sucesso
      404:
        description: Filme não encontrado
    """
    try:
        service.deletar_filme(filme_id)
        return jsonify({"mensagem": "Filme removido com sucesso!"}), 200
    except ErroNaoEncontrado as e:
        return jsonify({"erro": str(e)}), 404

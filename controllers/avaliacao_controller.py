"""
Camada de controller (rotas) para avaliações e rotas utilitárias.

Responsável apenas por receber a requisição HTTP, repassar para a camada
de serviço e devolver a resposta. Não contém regra de negócio nem SQL.
"""
from flask import Blueprint, request, jsonify

from services import avaliacao_service
from services import filme_service
from services.filme_service import ErroValidacao, ErroNaoEncontrado

avaliacao_bp = Blueprint("avaliacao", __name__)


@avaliacao_bp.route("/avaliar_filme/<int:filme_id>", methods=["POST"])
def avaliar_filme(filme_id):
    """
    Adiciona uma avaliação a um filme
    ---
    tags:
      - Avaliações
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
          required:
            - usuario
            - nota
          properties:
            usuario:
              type: string
              example: "João Silva"
            nota:
              type: number
              example: 8.5
            comentario:
              type: string
    responses:
      201:
        description: Avaliação registrada
      400:
        description: Dados inválidos
      404:
        description: Filme não encontrado
    """
    try:
        avaliacao_service.avaliar_filme(filme_id, request.get_json())
        return jsonify({"mensagem": "Avaliação registrada com sucesso!"}), 201
    except ErroNaoEncontrado as e:
        return jsonify({"erro": str(e)}), 404
    except ErroValidacao as e:
        return jsonify({"erro": str(e)}), 400


@avaliacao_bp.route("/avaliacoes/<int:filme_id>", methods=["GET"])
def listar_avaliacoes(filme_id):
    """
    Lista todas as avaliações de um filme
    ---
    tags:
      - Avaliações
    parameters:
      - in: path
        name: filme_id
        type: integer
        required: true
    responses:
      200:
        description: Lista de avaliações
    """
    avaliacoes = avaliacao_service.listar_avaliacoes(filme_id)
    return jsonify(avaliacoes), 200


@avaliacao_bp.route("/generos", methods=["GET"])
def listar_generos():
    """
    Lista todos os gêneros disponíveis no catálogo
    ---
    tags:
      - Utilitários
    responses:
      200:
        description: Lista de gêneros
    """
    generos = filme_service.listar_generos()
    return jsonify(generos), 200


@avaliacao_bp.route("/estatisticas", methods=["GET"])
def estatisticas():
    """
    Retorna estatísticas gerais do catálogo
    ---
    tags:
      - Utilitários
    responses:
      200:
        description: Estatísticas do catálogo
    """
    total_avaliacoes = avaliacao_service.contar_total()
    stats = filme_service.montar_estatisticas(total_avaliacoes)
    return jsonify(stats), 200

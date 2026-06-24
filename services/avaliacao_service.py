"""
Camada de serviço (regra de negócio) para avaliações.

Responsável por validar dados, orquestrar o repositório de avaliações e
acionar o recálculo da nota do filme — sem nunca alterar a nota_original.
"""
from repositories import avaliacao_repository as repo
from repositories import filme_repository as filme_repo
from services.filme_service import ErroValidacao, ErroNaoEncontrado


def avaliar_filme(filme_id, data):
    """Valida e registra uma avaliação, recalculando a média do filme."""
    if not filme_repo.existe(filme_id):
        raise ErroNaoEncontrado("Filme não encontrado")

    usuario = data.get("usuario")
    nota = data.get("nota")
    if not usuario or nota is None:
        raise ErroValidacao("Campos 'usuario' e 'nota' são obrigatórios")

    nota = float(nota)
    if nota < 0 or nota > 10:
        raise ErroValidacao("Nota deve ser entre 0 e 10")

    repo.inserir(filme_id, usuario, nota, data.get("comentario"))

    # Recalcula a média das avaliações dos usuários.
    # Importante: a nota_original do cadastro nunca é sobrescrita aqui,
    # apenas o campo `nota`, que reflete a média da comunidade.
    media = repo.media_por_filme(filme_id)
    filme_repo.atualizar_nota(filme_id, round(media, 1))


def listar_avaliacoes(filme_id):
    """Retorna as avaliações de um filme."""
    return repo.listar_por_filme(filme_id)


def contar_total():
    """Retorna o total de avaliações no sistema, usado nas estatísticas."""
    return repo.contar_total()

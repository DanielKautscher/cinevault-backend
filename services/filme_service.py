"""
Camada de serviço (regra de negócio) para filmes.

Responsável por validar dados e orquestrar as chamadas ao repositório.
Não conhece detalhes de HTTP (isso fica no controller) nem SQL (isso fica
no repository).
"""
from repositories import filme_repository as repo

CAMPOS_OBRIGATORIOS = ["titulo", "diretor", "ano", "genero"]
CAMPOS_ATUALIZAVEIS = ["titulo", "diretor", "ano", "genero", "sinopse", "nota", "poster_url", "duracao", "idioma"]

ORDENS_VALIDAS = {
    "nota": "nota DESC",
    "ano": "ano DESC",
    "titulo": "titulo ASC",
}


class ErroValidacao(Exception):
    """Erro de negócio: dados inválidos enviados pelo cliente."""
    pass


class ErroNaoEncontrado(Exception):
    """Erro de negócio: recurso não existe."""
    pass


def cadastrar_filme(data):
    """Valida e cadastra um novo filme. Retorna o ID gerado."""
    for campo in CAMPOS_OBRIGATORIOS:
        if not data.get(campo):
            raise ErroValidacao(f"Campo '{campo}' é obrigatório")

    nota_inicial = data.get("nota", 0)
    return repo.inserir(
        titulo=data["titulo"],
        diretor=data["diretor"],
        ano=data["ano"],
        genero=data["genero"],
        sinopse=data.get("sinopse"),
        nota=nota_inicial,
        poster_url=data.get("poster_url"),
        duracao=data.get("duracao"),
        idioma=data.get("idioma", "Português"),
    )


def listar_filmes(genero=None, ordem="titulo"):
    """Retorna a lista de filmes, com filtro de gênero e ordenação opcionais."""
    order_clause = ORDENS_VALIDAS.get(ordem, "titulo ASC")
    return repo.listar_todos(genero=genero, order_clause=order_clause)


def obter_filme(filme_id):
    """Retorna um filme pelo ID ou lança ErroNaoEncontrado."""
    filme = repo.buscar_por_id(filme_id)
    if not filme:
        raise ErroNaoEncontrado("Filme não encontrado")
    return filme


def buscar_por_titulo(termo):
    """Valida o termo de busca e retorna os filmes encontrados."""
    termo = (termo or "").strip()
    if not termo:
        raise ErroValidacao("Parâmetro 'q' é obrigatório")
    return repo.buscar_por_titulo(termo)


def atualizar_filme(filme_id, data):
    """Valida e atualiza os campos de um filme existente."""
    if not repo.existe(filme_id):
        raise ErroNaoEncontrado("Filme não encontrado")

    updates = {k: v for k, v in data.items() if k in CAMPOS_ATUALIZAVEIS}
    if not updates:
        raise ErroValidacao("Nenhum campo válido para atualizar")

    repo.atualizar(filme_id, updates)


def deletar_filme(filme_id):
    """Remove um filme, validando se ele existe antes."""
    if not repo.existe(filme_id):
        raise ErroNaoEncontrado("Filme não encontrado")
    repo.deletar(filme_id)


def listar_generos():
    """Retorna a lista de gêneros distintos do catálogo."""
    return repo.listar_generos()


def montar_estatisticas(total_avaliacoes):
    """Monta o dicionário de estatísticas gerais do catálogo."""
    return {
        "total_filmes": repo.contar_total(),
        "media_notas": round(repo.media_geral_notas(), 1),
        "total_generos": repo.contar_generos_distintos(),
        "total_avaliacoes": total_avaliacoes,
        "filme_mais_bem_avaliado": repo.filme_mais_bem_avaliado(),
    }

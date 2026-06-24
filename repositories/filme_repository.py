"""
Camada de repositório (acesso a dados) para filmes.

Responsável apenas por executar queries SQL na tabela `filmes`.
Não contém validação nem regra de negócio — isso fica na camada de service.
"""
from database import get_db


def inserir(titulo, diretor, ano, genero, sinopse, nota, poster_url, duracao, idioma):
    """Insere um novo filme e retorna o ID gerado."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO filmes
           (titulo, diretor, ano, genero, sinopse, nota, nota_original, poster_url, duracao, idioma)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (titulo, diretor, ano, genero, sinopse, nota, nota, poster_url, duracao, idioma)
    )
    filme_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return filme_id


def listar_todos(genero=None, order_clause="titulo ASC"):
    """Retorna todos os filmes, opcionalmente filtrados por gênero."""
    conn = get_db()
    cursor = conn.cursor()
    if genero:
        cursor.execute(f"SELECT * FROM filmes WHERE genero = ? ORDER BY {order_clause}", (genero,))
    else:
        cursor.execute(f"SELECT * FROM filmes ORDER BY {order_clause}")
    filmes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return filmes


def buscar_por_id(filme_id):
    """Retorna um filme pelo ID, ou None se não existir."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM filmes WHERE id = ?", (filme_id,))
    filme = cursor.fetchone()
    conn.close()
    return dict(filme) if filme else None


def buscar_por_titulo(termo):
    """Busca filmes cujo título contenha o termo informado."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM filmes WHERE titulo LIKE ? ORDER BY nota DESC", (f"%{termo}%",))
    filmes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return filmes


def existe(filme_id):
    """Verifica se um filme com o ID informado existe."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM filmes WHERE id = ?", (filme_id,))
    encontrado = cursor.fetchone() is not None
    conn.close()
    return encontrado


def atualizar(filme_id, campos):
    """Atualiza os campos informados (dict) de um filme."""
    conn = get_db()
    cursor = conn.cursor()
    set_clause = ", ".join(f"{k} = ?" for k in campos)
    valores = list(campos.values()) + [filme_id]
    cursor.execute(f"UPDATE filmes SET {set_clause} WHERE id = ?", valores)
    conn.commit()
    conn.close()


def atualizar_nota(filme_id, nova_nota):
    """Atualiza apenas a nota (média de avaliações) de um filme."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE filmes SET nota = ? WHERE id = ?", (nova_nota, filme_id))
    conn.commit()
    conn.close()


def deletar(filme_id):
    """Remove um filme do banco."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM filmes WHERE id = ?", (filme_id,))
    conn.commit()
    conn.close()


def listar_generos():
    """Retorna a lista de gêneros distintos cadastrados."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT genero FROM filmes ORDER BY genero")
    generos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return generos


def contar_total():
    """Retorna o total de filmes cadastrados."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM filmes")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def media_geral_notas():
    """Retorna a média geral das notas de todos os filmes avaliados."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(nota) FROM filmes WHERE nota > 0")
    media = cursor.fetchone()[0] or 0
    conn.close()
    return media


def contar_generos_distintos():
    """Retorna a quantidade de gêneros distintos cadastrados."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT genero) FROM filmes")
    total = cursor.fetchone()[0]
    conn.close()
    return total


def filme_mais_bem_avaliado():
    """Retorna o filme com a maior nota cadastrada."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT titulo, nota FROM filmes ORDER BY nota DESC LIMIT 1")
    top = cursor.fetchone()
    conn.close()
    return dict(top) if top else None

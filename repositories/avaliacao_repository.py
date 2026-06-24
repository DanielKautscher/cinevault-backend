"""
Camada de repositório (acesso a dados) para avaliações.

Responsável apenas por executar queries SQL na tabela `avaliacoes`.
Não contém validação nem regra de negócio — isso fica na camada de service.
"""
from database import get_db


def inserir(filme_id, usuario, nota, comentario):
    """Insere uma nova avaliação para um filme."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO avaliacoes (filme_id, usuario, nota, comentario) VALUES (?, ?, ?, ?)",
        (filme_id, usuario, nota, comentario)
    )
    conn.commit()
    conn.close()


def listar_por_filme(filme_id):
    """Retorna todas as avaliações de um filme, da mais recente para a mais antiga."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM avaliacoes WHERE filme_id = ? ORDER BY criado_em DESC",
        (filme_id,)
    )
    avaliacoes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return avaliacoes


def media_por_filme(filme_id):
    """Calcula a média das notas de avaliação de um filme."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(nota) FROM avaliacoes WHERE filme_id = ?", (filme_id,))
    media = cursor.fetchone()[0]
    conn.close()
    return media


def contar_total():
    """Retorna o total de avaliações registradas no sistema."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM avaliacoes")
    total = cursor.fetchone()[0]
    conn.close()
    return total

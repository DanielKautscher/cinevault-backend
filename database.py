"""
Camada de infraestrutura do banco de dados.

Responsável apenas por abrir conexões com o SQLite e garantir que as
tabelas existam. Não contém regra de negócio nem lógica de rotas.
"""
import sqlite3

DB_PATH = "cinevault.db"


def get_db():
    """Abre e retorna uma conexão com o banco, já configurada com row_factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Cria as tabelas do banco (se não existirem) e popula dados de exemplo."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            diretor TEXT NOT NULL,
            ano INTEGER NOT NULL,
            genero TEXT NOT NULL,
            sinopse TEXT,
            nota REAL DEFAULT 0,
            nota_original REAL DEFAULT 0,
            poster_url TEXT,
            duracao INTEGER,
            idioma TEXT DEFAULT 'Português',
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filme_id INTEGER NOT NULL,
            usuario TEXT NOT NULL,
            nota REAL NOT NULL CHECK(nota >= 0 AND nota <= 10),
            comentario TEXT,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (filme_id) REFERENCES filmes(id) ON DELETE CASCADE
        )
    """)

    _seed_filmes(cursor)

    conn.commit()
    conn.close()


def _seed_filmes(cursor):
    """Popula a tabela de filmes com dados de exemplo, caso esteja vazia."""
    cursor.execute("SELECT COUNT(*) FROM filmes")
    if cursor.fetchone()[0] != 0:
        return

    filmes_seed = [
        ("Interestelar", "Christopher Nolan", 2014, "Ficção Científica",
         "Um grupo de astronautas viaja além das galáxias em busca de um novo lar para a humanidade.",
         9.2, "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg", 169, "Inglês"),
        ("Parasita", "Bong Joon-ho", 2019, "Thriller",
         "A família Kim, todos desempregados, se infiltra na vida da rica família Park.",
         9.0, "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg", 132, "Coreano"),
        ("A Origem", "Christopher Nolan", 2010, "Ficção Científica",
         "Um ladrão especializado em extrair segredos do subconsciente é contratado para plantar uma ideia.",
         8.8, "https://image.tmdb.org/t/p/w500/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg", 148, "Inglês"),
        ("Clube da Luta", "David Fincher", 1999, "Drama",
         "Um homem insatisfeito forma um clube de luta clandestino com um vendedor de sabão carismático.",
         8.8, "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg", 139, "Inglês"),
    ]

    cursor.executemany(
        """INSERT INTO filmes
           (titulo, diretor, ano, genero, sinopse, nota, nota_original, poster_url, duracao, idioma)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        [(t, d, a, g, s, n, n, p, du, i) for t, d, a, g, s, n, p, du, i in filmes_seed]
    )

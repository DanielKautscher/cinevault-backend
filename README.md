# CineVault — Back-end API

API REST para o catálogo de filmes CineVault, construída com Python, Flask e SQLite.

---

## Descricao

CineVault é um sistema de gerenciamento e descoberta de filmes. A API permite cadastrar, buscar, atualizar e remover filmes, além de gerenciar avaliações de usuários. O banco de dados é inicializado automaticamente na primeira execução com seis filmes clássicos pré-cadastrados.

---

## Arquitetura em camadas

O projeto é organizado em camadas, separando responsabilidades:

```
cinevault-backend/
├── app.py                          → cria o app Flask e registra as rotas
├── database.py                     → conexão com o banco e criação das tabelas
├── controllers/
│   ├── filme_controller.py         → rotas de filmes (request/response)
│   └── avaliacao_controller.py     → rotas de avaliações e utilitários
├── services/
│   ├── filme_service.py            → regras de negócio de filmes
│   └── avaliacao_service.py        → regras de negócio de avaliações
├── repositories/
│   ├── filme_repository.py         → queries SQL de filmes
│   └── avaliacao_repository.py     → queries SQL de avaliações
├── requirements.txt
└── README.md
```

**Controller** — recebe a requisição HTTP, repassa para o service e devolve a resposta. Não conhece SQL nem regra de negócio.

**Service** — valida os dados e aplica as regras de negócio (por exemplo: campos obrigatórios, faixa de nota válida, recálculo da média de avaliações). Não conhece detalhes de HTTP nem SQL.

**Repository** — executa as queries SQL no banco de dados. Não valida nada, apenas lê e escreve.

Essa separação evita misturar regra de negócio com acesso ao banco, facilitando manutenção e testes.

---

## Instalacao

### Pré-requisitos

- Python 3.8 ou superior
- pip

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/cinevault-backend.git
cd cinevault-backend

# 2. Crie e ative um ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie o servidor
python app.py
```

O servidor será iniciado em http://localhost:5000

---

## Documentacao Swagger

Com o servidor rodando, acesse a documentação interativa em:

```
http://localhost:5000/docs/
```

No Swagger é possível testar todas as rotas diretamente pelo navegador, sem precisar de ferramentas externas.

---

## Rotas disponíveis

### Filmes

| Método | Rota                      | Descricao                                      |
|--------|---------------------------|------------------------------------------------|
| POST   | /cadastrar_filme           | Cadastra um novo filme                         |
| GET    | /buscar_filmes             | Lista todos os filmes (filtro por genero e ordenacao) |
| GET    | /buscar_filme/id           | Busca um filme pelo ID                         |
| GET    | /buscar_filme_titulo?q=    | Busca filmes pelo titulo (pesquisa parcial)    |
| PUT    | /atualizar_filme/id        | Atualiza os dados de um filme                  |
| DELETE | /deletar_filme/id          | Remove um filme do catalogo                    |

### Avaliacoes

| Método | Rota                  | Descricao                          |
|--------|-----------------------|------------------------------------|
| POST   | /avaliar_filme/id      | Adiciona uma avaliacao a um filme  |
| GET    | /avaliacoes/id         | Lista todas as avaliacoes de um filme |

### Utilitarios

| Método | Rota           | Descricao                              |
|--------|----------------|----------------------------------------|
| GET    | /generos        | Lista os generos disponiveis no catalogo |
| GET    | /estatisticas   | Retorna estatisticas gerais do catalogo  |

---

## Banco de dados

O SQLite é gerado automaticamente no arquivo cinevault.db na primeira execucao.

Tabelas:

- filmes: armazena o catalogo de filmes com titulo, diretor, ano, genero, sinopse, nota, poster, duracao e idioma
- avaliacoes: armazena as avaliacoes dos usuarios com nota e comentario, vinculadas a um filme por chave estrangeira

A nota exibida em cada filme é recalculada automaticamente como média das avaliacoes recebidas.

# Catálogo de Filmes - Backend API

API RESTful para gerenciamento de catálogo de filmes, desenvolvida com Flask e utilizando SQLite como banco de dados.

## Funcionalidades

* Listar todos os filmes.
* Obter detalhes de um filme específico por ID.
* Adicionar um novo filme.
* Atualizar informações de um filme existente.
* Excluir um filme.

## Tecnologias Utilizadas

* **Python 3.x**
* **Flask:** Microframework web para Python.
* **SQLite:** Banco de dados leve, integrado.
* **Pipenv (Opcional, mas recomendado):** Gerenciador de dependências e ambientes virtuais.

## Pré-requisitos

Certifique-se de ter o [Python 3.x](https://www.python.org/downloads/) instalado em sua máquina.

## Instalação e Execução

Siga os passos abaixo para configurar e rodar a API localmente:

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/BrunoCouti/catalogo-filmes-backend.git](https://github.com/BrunoCouti/catalogo-filmes-backend.git)
    ```
    ```bash
    cd catalogo-filmes-backend
    ```

2.  **Crie e ative o ambiente virtual:**

    * **Usando Pipenv (Recomendado):**
        ```bash
        pip install pipenv
        pipenv install
        pipenv shell
        ```
    * **Usando venv padrão do Python:**
        ```bash
        python -m venv venv
        # No Windows:
        venv\Scripts\activate
       
        ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Inicialize o banco de dados (se for a primeira vez):**
    O banco de dados `filmes.db` será criado automaticamente na primeira execução, ou quando você adicionar o primeiro filme via API. Caso queira popular com dados iniciais ou garantir a criação da tabela, você pode executar o `app.py` uma vez.

5.  **Execute a API:**
    ```bash
    python app.py
    ```
    A API estará acessível em `http://127.0.0.1:5000` (ou `http://localhost:5000`).

## Endpoints da API

* `GET /filmes`: Retorna todos os filmes.
* `GET /filmes/<id>`: Retorna um filme por ID.
* `POST /filmes`: Adiciona um novo filme.
    ```json
    {
        "titulo": "Nome do Filme",
        "genero": "Gênero",
        "ano": 2023
    }
    ```
* `PUT /filmes/<id>`: Atualiza um filme por ID.
    ```json
    {
        "titulo": "Novo Título",
        "genero": "Novo Gênero",
        "ano": 2024
    }
    ```
* `DELETE /filmes/<id>`: Exclui um filme por ID.

---

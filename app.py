# app.py

from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_cors import CORS
import sqlite3
import os

# --- Configuração do Flask e Flask-RESTx ---
app = Flask(__name__)

# Configuração CORS para permitir requisições do frontend
CORS(app, resources={r"/filmes/*": {"origins": "http://127.0.0.1:5500", "methods": ["GET", "POST", "DELETE", "PUT", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"], "supports_credentials": True}})

# Configurações do Swagger (documentação da API)
api = Api(app,
          version='1.0',
          title='API do Catálogo de Filmes',
          description='Uma API simples para gerenciar filmes.',
          doc='/swagger-ui/')

# Namespace para organizar as rotas da API relacionadas a filmes
ns = api.namespace('filmes', description='Operações relacionadas a filmes')

# Modelo (schema) para o filme na documentação do Swagger
filme_model = api.model('Filme', {
    'id': fields.Integer(readOnly=True, description='ID único do filme'),
    'titulo': fields.String(required=True, description='Título do filme'),
    'diretor': fields.String(required=True, description='Diretor do filme'),
    'ano': fields.Integer(required=True, description='Ano de lançamento do filme'),
    'genero': fields.String(required=True, description='Gênero do filme')
})

# --- Configuração do Banco de Dados SQLite ---
DATABASE = 'filmes.db'

def get_db_connection():
    """Função para estabelecer conexão com o banco de dados."""
    conn = sqlite3.connect(os.path.join(app.root_path, DATABASE))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Função para inicializar o banco de dados e criar a tabela de filmes."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS filmes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                diretor TEXT NOT NULL,
                ano INTEGER NOT NULL,
                genero TEXT NOT NULL
            )
        ''')
        conn.commit()

with app.app_context():
    init_db()

# --- Rotas da API ---

@ns.route('')
class FilmesList(Resource):
    @ns.doc('listar_filmes')
    @ns.marshal_list_with(filme_model)
    def get(self):
        """Lista todos os filmes cadastrados."""
        conn = get_db_connection()
        filmes = conn.execute('SELECT * FROM filmes').fetchall()
        conn.close()
        return [dict(filme) for filme in filmes], 200

    @ns.doc('criar_filme')
    @ns.expect(filme_model)
    @ns.response(201, 'Filme criado com sucesso', filme_model)
    @ns.response(400, 'Dados inválidos')
    def post(self):
        """Cria um novo filme."""
        dados = request.json
        if not dados or not all(k in dados for k in ('titulo', 'diretor', 'ano', 'genero')):
            api.abort(400, "Dados do filme incompletos ou inválidos.")

        titulo = dados['titulo']
        diretor = dados['diretor']
        ano = dados['ano']
        genero = dados['genero']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO filmes (titulo, diretor, ano, genero) VALUES (?, ?, ?, ?)',
                           (titulo, diretor, ano, genero))
            conn.commit()
            novo_filme_id = cursor.lastrowid
            novo_filme = conn.execute('SELECT * FROM filmes WHERE id = ?', (novo_filme_id,)).fetchone()
            conn.close()
            return dict(novo_filme), 201
        except sqlite3.Error as e:
            api.abort(500, f"Erro ao inserir filme no banco de dados: {e}")

@ns.route('/<int:filme_id>')
@ns.param('filme_id', 'O identificador único do filme')
class Filme(Resource):
    @ns.doc('obter_filme')
    @ns.marshal_with(filme_model)
    @ns.response(200, 'Filme encontrado', filme_model)
    @ns.response(404, 'Filme não encontrado')
    def get(self, filme_id):
        """Obtém os detalhes de um filme específico pelo ID."""
        conn = get_db_connection()
        filme = conn.execute('SELECT * FROM filmes WHERE id = ?', (filme_id,)).fetchone()
        conn.close()
        if filme:
            return dict(filme), 200
        api.abort(404, f"Filme com ID {filme_id} não encontrado.")

    @ns.doc('deletar_filme')
    @ns.response(204, 'Filme excluído com sucesso')
    @ns.response(404, 'Filme não encontrado')
    def delete(self, filme_id):
        """Exclui um filme pelo ID."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM filmes WHERE id = ?', (filme_id,))
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            api.abort(404, f"Filme com ID {filme_id} não encontrado.")
        conn.close()
        return '', 204

# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)
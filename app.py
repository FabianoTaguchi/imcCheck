# Importação das biblioteca
from flask import Flask, render_template, request
from flask import redirect, url_for, flash, session
from functools import wraps
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, text
from sqlalchemy.exc import IntegrityError


#Criação do app e configuração do banco de dados
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'mysql+pymysql://root:root@localhost:3306/imccheck?charset=utf8mb4')
db = SQLAlchemy(app)


#Rota principal
@app.route('/index')
def index():
    return render_template('index.html', show_menu=True)


# CLasses do projeto
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_completo = db.Column(db.String(150), nullable= True)
    email = db.Column(db.String(150), nullable= True, unique=True)
    telefone = db.Column(db.String(40))
    email = db.Column(db.String(80))
    login = db.Column(db.String(80), nullable= True, unique=True)
    senha = db.Column(db.String(255), nullable= True)
    data_nascimento = db.Column(db.DateTime)
    peso = db.Column(db.Integer)
    altura = db.Column(db.Integer)
    sexo = db.Column(db.String(20))

   
class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    data_objetivo = db.Column(db.Date, nullable=False)
    peso_meta = db.Column(db.Numeric(5, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    
@app.route('/metas', methods=['GET', 'POST'])
def metas():
    return render_template('metas.html', show_menu=True)

@app.route('/metas/excluir', methods=['POST'])
def excluir_meta():
    return render_template('metas.html', show_menu=True)

@app.route('/registros', methods=['GET', 'POST'])
def registros():
    return render_template('registros.html', show_menu=True)

@app.route('/acompanhamento', methods=['GET'])
def acompanhamento():
    return render_template('acompanhamento.html', show_menu=True)

@app.route('/atividades', methods=['GET', 'POST'])
def atividades():
    return render_template('atividades.html', show_menu=True)

@app.route('/relatorio-atividades', methods=['GET'])
def relatorio_atividades():
    return render_template('relatorio_atividades.html', show_menu=True)

## Rotas antigas de gestão de fazenda removidas nesta etapa

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            flash('Informe usuário e senha.', 'warning')
            return redirect(url_for('login'))
        
        # Aceita qualquer combinação por enquanto
        flash('Login aceito.', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', show_menu=False)

# Rota responsável por abrir o formulário para cadastrar um usuário
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', show_menu=False)

# Rota para cadastrar o usuário
@app.route('/cadastro', methods=['POST'])
def cadastrar():
    nome_completo = (request.form.get('nome_completo') or '').strip()
    email = (request.form.get('email') or '').strip()
    telefone = (request.form.get('telefone') or '').strip()
    login = (request.form.get('login') or '').strip()
    senha = (request.form.get('senha') or '').strip()
    data_nascimento = (request.form.get('data_nascimento') or '').strip()
    peso = (request.form.get('peso') or '').strip()
    altura = (request.form.get('altura') or '').strip()
    sexo = (request.form.get('sexo') or '').strip()

    # Verifica se o nome, email, login ou senha não estão em branco
    if not nome_completo or not email or not login or not senha:
        flash('Nome, e-mail, login e senha são dados obrigatórios', 'warning')
        return redirect(url_for('index'))
        
@app.route('/cadastroMeta', methods=['GET', 'POST'])
def cadastroMetas():
    id = (request.form.get('id') or '').strip()
    user_id = (request.form.get('user_id') or '').strip()
    data_objetivo = (request.form.get('data_objetivo') or '').strip()
    peso_meta = (request.form.get('peso_meta') or '').strip()
  
    

    # Pega as variáveis e adiciona um novo usuário na tabela (Lista)
    try:
        u = Users(
            nome_completo=nome_completo,
            email=email,
            telefone=telefone or None,
            login=login,
            senha=senha,
            data_nascimento=data_nascimento,
            peso=peso or None,
            altura=altura or None, 
            sexo=sexo or None)
        db.session.add(u)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('index'))
    
    except IntegrityError:
        db.session.rollback()
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao cadastrar: {str(e)}', 'danger')
        return redirect(url_for('index'))

# Verifica se o arquivo é o principal do projeto
if __name__ == '__main__':
    # Runner da aplicação (configurável via env HOST/PORT)
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', '5600'))
    app.run(host=host, port=port, debug=True)

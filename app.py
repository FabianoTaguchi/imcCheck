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


# Classes do projeto
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
    peso = db.Column(db.Numeric(5,2))
    altura = db.Column(db.Numeric(3,2))
    sexo = db.Column(db.String(20))

# Classe Metas
class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    data_objetivo = db.Column(db.Date, nullable=False)
    peso_meta = db.Column(db.Numeric(5, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)



class WeightRecord(db.Model):
    __tablename__ = 'weight_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    data_registro = db.Column(db.Date, nullable=False)
    peso = db.Column(db.Numeric(5, 2), nullable=False)
    imc = db.Column(db.Numeric(5, 2))
    classificacao = db.Column(db.String(40))
    grau_obesidade = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


# Visualizar a meta salva  
@app.route('/metas', methods=['GET', 'POST'])
def metas():
    # Recuperar a sessão do usuário e define a meta como um campo vazio
    user_id = session.get('user_id')
    meta = None
    if user_id:
        # Busca um user_id com o mesmo valor que está logado na sessão
        meta = Goal.query.filter_by(user_id=user_id).first()
    return render_template('metas.html', show_menu=True, meta=meta)


# Excluir meta de um usuário logado
@app.route('/metas/excluir', methods=['POST'])
def excluir_meta():
    user_id = session.get('user_id')
    if not user_id:
        flash('Faça login para gerenciar metas.', 'warning')
        return redirect(url_for('login'))
    # Busca um user_id com o mesmo valor que está logado na sessão
    meta = Goal.query.filter_by(user_id=user_id).first()
    if not meta:
        flash('Nenhuma meta para excluir.', 'info')
        return redirect(url_for('metas'))
    # Exclui a meta
    db.session.delete(meta)
    db.session.commit()
    flash('Meta excluída.', 'success')
    return redirect(url_for('metas'))


@app.route('/registros', methods=['GET', 'POST'])
def registros():
    user_id = session.get('user_id')
    if not user_id:
        flash('Faça login para registrar dados.', 'warning')
        return redirect(url_for('login'))
    if request.method == 'POST':
        data_registro = (request.form.get('data_registro') or '').strip()
        peso_registro = (request.form.get('peso_registro') or '').strip()
        if not data_registro or not peso_registro:
            flash('Informe data e peso.', 'warning')
        else:
            try:
                data_obj = datetime.strptime(data_registro, '%Y-%m-%d').date()
                u = Users.query.get(user_id)
                altura = float(u.altura) if u and u.altura else None
                peso_val = float(peso_registro)
                imc_val = round(peso_val / (altura * altura), 2) if altura and altura > 0 else None
                classificacao = None
                grau = None
                if imc_val is not None:
                    if imc_val < 18.5:
                        classificacao = 'Abaixo do peso'
                    elif imc_val < 25:
                        classificacao = 'Peso normal'
                    elif imc_val < 30:
                        classificacao = 'Sobrepeso'
                    elif imc_val < 35:
                        classificacao = 'Obesidade'
                        grau = 'I'
                    elif imc_val < 40:
                        classificacao = 'Obesidade'
                        grau = 'II'
                    else:
                        classificacao = 'Obesidade'
                        grau = 'III'
                registro = WeightRecord(user_id=user_id, data_registro=data_obj, peso=peso_val, imc=imc_val, classificacao=classificacao, grau_obesidade=grau)
                db.session.add(registro)
                db.session.commit()
                flash('Registro salvo.', 'success')
            except Exception:
                db.session.rollback()
                flash('Erro ao salvar registro.', 'danger')
        return redirect(url_for('registros'))
    rows = WeightRecord.query.filter_by(user_id=user_id).order_by(WeightRecord.data_registro.desc()).all()
    registros = [{'data': r.data_registro, 'peso': float(r.peso), 'imc': float(r.imc) if r.imc is not None else None, 'classificacao': r.classificacao, 'grau': r.grau_obesidade} for r in rows]
    return render_template('registros.html', show_menu=True, registros=registros)


@app.route('/acompanhamento', methods=['GET'])
def acompanhamento():
    user_id = session.get('user_id')
    if not user_id:
        flash('Faça login para acompanhar registros.', 'warning')
        return redirect(url_for('login'))
    rows = WeightRecord.query.filter_by(user_id=user_id).order_by(WeightRecord.data_registro.desc()).all()
    meta = Goal.query.filter_by(user_id=user_id).first()
    registros = []
    for r in rows:
        imc_val = float(r.imc) if r.imc is not None else None
        classificacao = r.classificacao
        grau = r.grau_obesidade
        ok = (float(r.peso) <= float(meta.peso_meta)) if meta else None
        registros.append({'data': r.data_registro, 'peso': float(r.peso), 'imc': imc_val, 'classificacao': classificacao, 'grau': grau, 'ok': ok})
    return render_template('acompanhamento.html', show_menu=True, registros=registros)


@app.route('/atividades', methods=['GET', 'POST'])
def atividades():
    return render_template('atividades.html', show_menu=True)


@app.route('/relatorio-atividades', methods=['GET'])
def relatorio_atividades():
    return render_template('relatorio_atividades.html', show_menu=True)

# Rota para fazer o login na aplicação
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Recupera os dados do formulário
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            flash('Informe usuário e senha.', 'warning')
            return redirect(url_for('login'))
        # Faz a consulta a para saber se o campo login dos usuários é o mesmo recuperado do formulário
        user = Users.query.filter_by(login=username).first()
        # Recupera o login e o nome do usuário
        session['user_id'] = user.id
        session['user_name'] = user.nome_completo 
        session['user_telefone'] = user.telefone
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

    if not nome_completo or not email or not login or not senha:
        flash('Nome, e-mail, login e senha são dados obrigatórios', 'warning')
        return redirect(url_for('register'))
    try:
        user = Users(
            nome_completo=nome_completo,
            email=email,
            telefone=telefone or None,
            login=login,
            senha=senha,
            data_nascimento=datetime.strptime(data_nascimento, '%Y-%m-%d') if data_nascimento else None,
            peso=float(peso) if peso else None,
            altura=float(altura) if altura else None,
            sexo=sexo or None,)
        db.session.add(user)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!', 'success')
        session['user_id'] = user.id
        session['user_name'] = user.nome_completo 
        return redirect(url_for('index'))
    except IntegrityError:
        db.session.rollback()
        flash('Email ou login já cadastrado.', 'warning')
        return redirect(url_for('register'))
    except Exception:
        db.session.rollback()
        flash('Erro ao cadastrar usuário.', 'danger')
        return redirect(url_for('register'))


# Rota para cadastrar uma meta
@app.route('/cadastroMeta', methods=['GET', 'POST'])
def cadastroMetas():
    user_id = session.get('user_id')
    if not user_id:
        flash('Faça login para cadastrar meta.', 'warning')
        return redirect(url_for('login'))
    data_objetivo = (request.form.get('data_objetivo') or '').strip()
    peso_meta = (request.form.get('peso_meta') or '').strip()
    if not data_objetivo or not peso_meta:
        flash('Informe data objetivo e peso da meta.', 'warning')
        return redirect(url_for('metas'))
    existente = Goal.query.filter_by(user_id=user_id).first()
    if existente:
        flash('Já existe uma meta ativa para o usuário.', 'warning')
        return redirect(url_for('metas'))
    try:
        data_obj = datetime.strptime(data_objetivo, '%Y-%m-%d').date()
        meta = Goal(user_id=user_id, data_objetivo=data_obj, peso_meta=float(peso_meta))
        db.session.add(meta)
        db.session.commit()
        flash('Meta cadastrada com sucesso.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao cadastrar meta.', 'danger')
    return redirect(url_for('metas'))


# Verifica se o arquivo é o principal do projeto
if __name__ == '__main__':
    # Runner da aplicação (configurável via env HOST/PORT)
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', '5600'))
    app.run(host=host, port=port, debug=True)

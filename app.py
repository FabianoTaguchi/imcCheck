from flask import Flask, render_template, request
from flask import redirect, url_for, flash
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'

@app.route('/index')
def index():
    return render_template('index.html', show_menu=True)



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

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html', show_menu=False)

# Verifica se o arquivo é o principal do projeto
if __name__ == '__main__':
    # Runner da aplicação (configurável via env HOST/PORT)
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', '5600'))
    app.run(host=host, port=port, debug=True)

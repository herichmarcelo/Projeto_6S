import uuid
import csv
import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from auditorias_routes import auditorias_bp
from flask import send_file
from dashdados import app_dash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.register_blueprint(auditorias_bp)
app.secret_key = 'chave_secreta_super_segura'  # Certifique-se de alterar para uma chave segura em um ambiente de produção

# Dados do usuário administrador (substitua por uma solução mais segura em um ambiente de produção)
USUARIO_ADMIN = 'admin'
SENHA_ADMIN = '@bello'

# Dados de usuários (apenas para fins de demonstração)
usuarios = {'admin': {'senha': '@bello', 'tipo': 'administrador'}}

# Incorporar a aplicação Dash no aplicativo Flask
app_dash.server = app

# Rota para a dashboard Dash
@app.route('/dashboard')
def dashboard():
    return app_dash.index()


# Rota para fornecer o arquivo CSV
@app.route('/dados/arquivo_auditoria.csv')
def fornecer_csv():
    caminho_arquivo = 'dados/arquivo_auditoria.csv'
    return send_file(caminho_arquivo, as_attachment=True)

@app.route('/')
def index():
    if 'usuario' in session:
        return redirect(url_for('centro_usuario'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')

    # Lógica de autenticação (substitua pelo seu próprio sistema de autenticação)
    if usuario in usuarios and usuarios[usuario]['senha'] == senha:
        session['usuario'] = usuario
        return redirect(url_for('centro_usuario'))
    else:
        return render_template('login.html', mensagem='Credenciais inválidas. Tente novamente.')
    
@app.route('/centro_usuario')
def centro_usuario():
    usuario = session.get('usuario')
    tipo_usuario = usuarios[usuario]['tipo'] if usuario in usuarios else 'auditor' # type: ignore
    
    # Obtenha a referência à imagem do usuário da sessão
    foto_usuario = session.get('foto_usuario')

    return render_template('centro_usuario.html', usuario=usuario, tipo_usuario=tipo_usuario, foto_usuario=foto_usuario)

@app.route('/area_auditoria')
def area_auditoria():
    return render_template('area_auditoria.html')

@app.route('/logout')
def logout():
    usuario = session.get('usuario')
    if usuario:
        # Mantenha a referência à imagem associada ao usuário na sessão
        nome_arquivo = f'{usuario}_foto.jpg'
        session['foto_usuario'] = nome_arquivo

    # Limpe outros dados da sessão
    session.pop('usuario', None)

    return redirect(url_for('index'))

@app.route('/upload_foto', methods=['POST'])
def upload_foto():
    try:
        usuario = session.get('usuario')

        if usuario:
            setor_auditado = request.form.get('setor_auditado')  # Obtém o setor auditado do formulário HTML
            nome_arquivo = f'{setor_auditado}_foto.jpg'
            file = request.files.get('file')

            if file:
                # Salva o arquivo na pasta 'static/fotosauditorias'
                file.save(os.path.join('static', 'fotosauditorias', secure_filename(nome_arquivo)))
                return jsonify({'status': 'success', 'mensagem': 'Foto carregada com sucesso'})
            else:
                return jsonify({'status': 'error', 'mensagem': 'Erro ao carregar foto'})

        return jsonify({'status': 'error', 'mensagem': 'Usuário não autenticado'})

    except Exception as e:
        return jsonify({'status': 'error', 'mensagem': str(e)})

# Rota para cadastrar usuário (disponível apenas para administradores)
@app.route('/cadastrar_usuario', methods=['GET', 'POST'])
def cadastrar_usuario():
    if 'usuario' in session:
        usuario = session['usuario']
        tipo_usuario = usuarios[usuario]['tipo'] if usuario in usuarios else 'auditor'

        if tipo_usuario == 'administrador':
            if request.method == 'POST':
                novo_usuario = request.form.get('novo_usuario')
                nova_senha = request.form.get('nova_senha')
                tipo_novo_usuario = request.form.get('tipo_usuario')

                usuarios[novo_usuario] = {'senha': nova_senha, 'tipo': tipo_novo_usuario} # type: ignore
                mensagem = f'Usuário {novo_usuario} cadastrado com sucesso.'
                return render_template('cadastrar_usuario.html', usuario=usuario, tipo_usuario=tipo_usuario, mensagem=mensagem)
            
            return render_template('cadastrar_usuario.html', usuario=usuario, tipo_usuario=tipo_usuario)

        return redirect(url_for('centro_usuario'))

    return redirect(url_for('index'))

# Rota par a pagina auditorias/patio
@app.route('/auditorias/patio')
def patio():
    return render_template('auditorias/patio.html')

# Rota para consultar usuários (disponível apenas para administradores)
@app.route('/consultar_usuarios')
def consultar_usuarios():
    if 'usuario' in session:
        usuario = session['usuario']
        tipo_usuario = usuarios[usuario]['tipo'] if usuario in usuarios else 'auditor'

        if tipo_usuario == 'administrador':
            return render_template('consultar_usuarios.html', usuario=usuario, tipo_usuario=tipo_usuario, usuarios=usuarios)
        
        return redirect(url_for('centro_usuario'))

    return redirect(url_for('index'))
@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Recebe os dados do formulário
        data = request.form.to_dict()

        # Caminho para o arquivo CSV
        csv_path = os.path.join('dados', 'arquivo_auditoria.csv')

        # Verifica se o arquivo já existe
        file_exists = os.path.exists(csv_path)

        # Abre o arquivo CSV em modo de escrita, usando 'a' para adicionar ao final do arquivo
        with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            # Cria um objeto DictWriter
            csv_writer = csv.DictWriter(csvfile, fieldnames=list(data.keys()))

            # Se o arquivo não existir, escreve os cabeçalhos
            if not file_exists:
                csv_writer.writeheader()

            # Escreve os dados no arquivo CSV
            csv_writer.writerow(data)

        return 'Dados gravados com sucesso no arquivo CSV!'
    except Exception as e:
        return f'Ocorreu um erro ao processar a solicitação: {str(e)}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

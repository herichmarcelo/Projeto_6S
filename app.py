import pyodbc
import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_file, send_from_directory
from auditorias_routes import auditorias_bp
from dashdados import app_dash
from datetime import datetime
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.register_blueprint(auditorias_bp)
app.secret_key = 'chave_secreta_super_segura'  # Certifique-se de alterar para uma chave segura em um ambiente de produção

# Defina a pasta onde os arquivos serão carregados
UPLOAD_PATIO = 'static/patio'
app.config['UPLOAD_PATIO'] = UPLOAD_PATIO
UPLOAD_FOLDER = 'static/assets'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# String de conexão com o banco de dados Access
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=dados/base.accdb;'
    r'charset=utf-8;'
)
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
#Upar foto do Usuario
@app.route('/upload_foto', methods=['POST'])
def upload_foto():
    try:
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'Nenhum arquivo enviado'})

        file = request.files['file']
        nome_usuario = request.form.get('nome_usuario', '')

        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'Nome de arquivo vazio'})

        if file and allowed_file(file.filename):
            # Certifica-se de que o nome do arquivo é seguro
            filename = secure_filename(nome_usuario)
            # Salva o arquivo na pasta de upload
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'status': 'success', 'message': 'Arquivo enviado com sucesso', 'filename': filename})
        else:
            return jsonify({'status': 'error', 'message': 'Tipo de arquivo não permitido'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        form_data = request.form

        # Conecta-se ao banco de dados
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Insere os dados na tabela adequada
        val = [
            form_data['setor_auditado'],
            form_data['data_auditoria'],
            form_data['representante_setor'],
            form_data['auditores']
        ]

        for i in range(1, 17):
            val.append(form_data[f'pergunta_{i}'])
            val.append(form_data.get(f'comentario_pergunta_{i}', None))
            if f'upload_foto_pergunta_{i}' in request.files:
                upload_file = request.files[f'upload_foto_pergunta_{i},']
                if upload_file and allowed_file(upload_file.filename):
                    # Gera um nome de arquivo seguro com base no setor_auditado e um identificador único
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    filename = secure_filename(f"{form_data['setor_auditado']}_{timestamp}")

                    # Se o arquivo tiver uma extensão, adicione-a ao nome do arquivo seguro
                    if upload_file.filename:
                        filename += os.path.splitext(upload_file.filename)[1]

                    # Salva o arquivo
                    upload_file.save(os.path.join(UPLOAD_FOLDER, filename))
                    val.append(filename)
                else:
                    val.append(None)
            else:
                val.append(None)

        sql_columns = ", ".join([f'pergunta_{i}, comentario_pergunta_{i}, upload_foto_pergunta_{i}' for i in range(1, 17)])
        sql_values = ", ".join(['?'] * 52)  # 16 perguntas * 3 colunas + 4 colunas adicionais
        sql = f"INSERT INTO patio (setor_auditado, data_auditoria, representante_setor, auditores, {sql_columns}) VALUES ({sql_values})"
        
        cursor.execute(sql, val)

        # Confirma a transação e fecha a conexão
        conn.commit()
        cursor.close()
        conn.close()

        return 'Dados gravados com sucesso no banco de dados Access!'
    return 'Requisição GET recebida'

# Função auxiliar para verificar se a extensão do arquivo é permitida
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
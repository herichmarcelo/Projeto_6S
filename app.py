import pyodbc
import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file, send_from_directory
from auditorias_routes import auditorias_bp
from flask import send_file
from dashdados import app_dash
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.register_blueprint(auditorias_bp)
app.secret_key = 'chave_secreta_super_segura'  # Certifique-se de alterar para uma chave segura em um ambiente de produção

# Defina a pasta onde os arquivos serão carregados
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

@app.route('/submit', methods=['GET''POST'])
def submit():
    if request.method == 'POST':
        setor_auditado = request.form['setor_auditado']# Recebe os dados do formulário 
        data_auditoria = request.form['data_auditoria']
        representante_setor = request.form['representante_setor']
        auditores = request.form['auditores']
        pergunta_1 = request.form['pergunta_1']
        comentario_pergunta_1 =  request.form.get('comentario_pergunta_1', None)
        upload_foto_pergunta_1 = request.files.get('upload_foto_pergunta_1', None)
        pergunta_2 = request.form['pergunta_2']
        upload_foto_pergunta_2 = request.files.get('upload_foto_pergunta_2', None)
        comentario_pergunta_2 = request.form.get('comentario_pergunta_2', None)
        pergunta_3 = request.form['pergunta_3']
        upload_foto_pergunta_3 = request.files.get('upload_foto_pergunta_3', None)
        comentario_pergunta_3 = request.form.get('comentario_pergunta_3', None)
        pergunta_4 = request.form['pergunta_4']
        upload_foto_pergunta_4 = request.files.get('upload_foto_pergunta_4', None)
        comentario_pergunta_4 = request.form.get('comentario_pergunta_4', None)
        pergunta_5 = request.form['pergunta_5']
        upload_foto_pergunta_5 = request.files.get('upload_foto_pergunta_5', None)
        comentario_pergunta_5 = request.form.get('comentario_pergunta_5', None)
        pergunta_6 = request.form['pergunta_6']
        upload_foto_pergunta_6 = request.files.get('upload_foto_pergunta_6', None)
        comentario_pergunta_6 = request.form.get('comentario_pergunta_6', None)
        pergunta_7 = request.form['pergunta_7']
        upload_foto_pergunta_7 = request.files.get('upload_foto_pergunta_7', None)
        comentario_pergunta_7 = request.form.get('comentario_pergunta_7', None)
        pergunta_8 = request.form['pergunta_8']
        upload_foto_pergunta_8 = request.files.get('upload_foto_pergunta_8', None)
        comentario_pergunta_8 = request.form.get('comentario_pergunta_8', None)
        pergunta_9 = request.form['pergunta_9']
        upload_foto_pergunta_9 = request.files.get('upload_foto_pergunta_9', None)
        comentario_pergunta_9 = request.form.get('comentario_pergunta_9', None)
        pergunta_10 = request.form['pergunta_10']
        upload_foto_pergunta_10 = request.files.get('upload_foto_pergunta_10', None)
        comentario_pergunta_10 = request.form.get('comentario_pergunta_10', None)
        pergunta_11 = request.form['pergunta_11']
        upload_foto_pergunta_11 = request.files.get('upload_foto_pergunta_11', None)
        comentario_pergunta_11 = request.form.get('comentario_pergunta_11', None)
        pergunta_12 = request.form['pergunta_12']
        upload_foto_pergunta_12 = request.files.get('upload_foto_pergunta_12', None)
        comentario_pergunta_12 = request.form.get('comentario_pergunta_12', None)
        pergunta_13 = request.form['pergunta_13']
        upload_foto_pergunta_13 = request.files.get('upload_foto_pergunta_13', None)
        comentario_pergunta_13 = request.form.get('comentario_pergunta_13', None)
        pergunta_14 = request.form['pergunta_14']
        upload_foto_pergunta_14 = request.files.get('upload_foto_pergunta_14', None)
        comentario_pergunta_14 = request.form.get('comentario_pergunta_14', None)
        pergunta_15 = request.form['pergunta_15']
        upload_foto_pergunta_15 = request.files.get('upload_foto_pergunta_15', None)
        comentario_pergunta_15 = request.form.get('comentario_pergunta_15', None)
        pergunta_16 = request.form['pergunta_16']
        upload_foto_pergunta_16 = request.files.get('upload_foto_pergunta_16', None)
        comentario_pergunta_16 = request.form.get('comentario_pergunta_16', None)


        def save_image(setor_auditado, upload_file):
            if upload_file and allowed_file(upload_file.filename):
                filename = secure_filename(setor_auditado) + os.path.splitext(upload_file.filename)[1]
                upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return filename
            return None

        # Uso da função save_image
        filename_pergunta_1 = save_image(setor_auditado, upload_foto_pergunta_1)
        filename_pergunta_2 = save_image(setor_auditado, upload_foto_pergunta_2)
        # Conecta-se ao banco de dados
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Insere os dados na tabela adequada
        sql = "INSERT INTO patio (setor_auditado, data_auditoria, representante_setor, auditores, pergunta_1, comentario_pergunta_1, upload_foto_pergunta_1, pergunta_2, comentario_pergunta_2, upload_foto_pergunta_2, pergunta_3, comentario_pergunta_3, upload_foto_pergunta_3, pergunta_4, comentario_pergunta_4, upload_foto_pergunta_4, pergunta_5, comentario_pergunta_5, upload_foto_pergunta_5, pergunta_6, comentario_pergunta_6, upload_foto_pergunta_6, pergunta_7, comentario_pergunta_7, upload_foto_pergunta_7, pergunta_8, comentario_pergunta_8, upload_foto_pergunta_8, pergunta_9, comentario_pergunta_9, upload_foto_pergunta_9, pergunta_10, comentario_pergunta_10, upload_foto_pergunta_10, pergunta_11, comentario_pergunta_11, upload_foto_pergunta_11, pergunta_12, comentario_pergunta_12, upload_foto_pergunta_12, pergunta_13, comentario_pergunta_13, upload_foto_pergunta_13, pergunta_14, comentario_pergunta_14, upload_foto_pergunta_14, pergunta_15, comentario_pergunta_15, upload_foto_pergunta_15, pergunta_16, comentario_pergunta_16, upload_foto_pergunta_16) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val =  (setor_auditado, data_auditoria, representante_setor, auditores, pergunta_1, comentario_pergunta_1, filename, pergunta_2, comentario_pergunta_2, upload_foto_pergunta_2, pergunta_3, comentario_pergunta_3, upload_foto_pergunta_3, pergunta_4, comentario_pergunta_4, upload_foto_pergunta_4, pergunta_5, comentario_pergunta_5, upload_foto_pergunta_5, pergunta_6, comentario_pergunta_6, upload_foto_pergunta_6, pergunta_7, comentario_pergunta_7, upload_foto_pergunta_7, pergunta_8, comentario_pergunta_8, upload_foto_pergunta_8, pergunta_9, comentario_pergunta_9, upload_foto_pergunta_9, pergunta_10, comentario_pergunta_10, upload_foto_pergunta_10, pergunta_11, comentario_pergunta_11, upload_foto_pergunta_11, pergunta_12, comentario_pergunta_12, upload_foto_pergunta_12, pergunta_13, comentario_pergunta_13, upload_foto_pergunta_13, pergunta_14, comentario_pergunta_14, upload_foto_pergunta_14, pergunta_15, comentario_pergunta_15, upload_foto_pergunta_15, pergunta_16, comentario_pergunta_16, upload_foto_pergunta_16)
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
import os
import uuid
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from auditorias_routes import auditorias_bp
from dashdados import app_dash
from werkzeug.utils import secure_filename
import pyodbc
import base64
from datetime import datetime



app = Flask(__name__)
app.register_blueprint(auditorias_bp)
app.secret_key = 'chave_secreta_super_segura'  # Certifique-se de alterar para uma chave segura em um ambiente de produção

# Defina a pasta onde os arquivos serão carregados
UPLOAD_FOLDER = 'static/assets'
UPLOAD_PATIO = 'static/patio'
UPLOAD_EXTERNAS = 'static/externas'
UPLOAD_ADM = 'static/adm'
UPLOAD_APOIO = 'static/apoio' 
UPLOAD_PRODUCAO = 'static/producao'
UPLOAD_ASS = 'static/assinaturas' # Diretório para uploads de assinaturas
UPLOAD_USER = 'static/user'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_PATIO'] = UPLOAD_PATIO
app.config['UPLOAD_EXTERNAS'] = UPLOAD_EXTERNAS
app.config['UPLOAD_ADM'] = UPLOAD_ADM
app.config['UPLOAD_APOIO'] = UPLOAD_APOIO
app.config['UPLOAD_PRODUCAO'] = UPLOAD_PRODUCAO
app.config['UPLOAD_ASS'] = UPLOAD_ASS
app.config['UPLOAD_USER'] = UPLOAD_USER

# String de conexão com o banco de dados Access
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=dados/base.accdb;'
    r'charset=utf-8;'
)

# Dados de usuários (apenas para fins de demonstração)
#usuarios = {}

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

    try:
        # Conectar ao banco de dados
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Consultar o usuário no banco de dados
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
        usuario_info = cursor.fetchone()

        # Fechar a conexão com o banco de dados
        cursor.close()
        conn.close()

        if usuario_info:
            # Se o usuário existir e a senha estiver correta, inicie a sessão do usuário
            session['usuario'] = usuario
            return redirect(url_for('centro_usuario'))
        else:
            # Se as credenciais estiverem incorretas, exiba uma mensagem de erro
            return render_template('login.html', mensagem='Credenciais inválidas. Tente novamente.')

    except Exception as e:
        # Em caso de erro na consulta ao banco de dados, exiba uma mensagem de erro genérica
        return render_template('login.html', mensagem='Ocorreu um erro ao processar sua solicitação. Tente novamente mais tarde.')
    
@app.route('/centro_usuario')
def centro_usuario():
    usuario = session.get('usuario')

    # Conecta-se ao banco de dados Access
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Consulta o tipo de usuário na tabela de usuários
    cursor.execute("SELECT perfil, email FROM usuarios WHERE usuario = ?", (usuario,))
    row = cursor.fetchone()

    tipo_usuario = row[0] if row else 'auditor'
    email_usuario = row[1] if row else 'email'

    # Fecha a conexão com o banco de dados
    cursor.close()
    conn.close()

    # Obtenha a referência à imagem do usuário da sessão
    foto_usuario = session.get('foto_usuario')

    return render_template('centro_usuario.html', usuario=usuario, tipo_usuario=tipo_usuario,email_usuario=email_usuario, foto_usuario=foto_usuario)

@app.route('/area_auditoria')
def area_auditoria():
    return render_template('area_auditoria.html')

# Rota para cadastrar usuário (disponível apenas para administradores)
@app.route('/cadastrar_usuario')
def cadastrar_usuario():
    return render_template('cadastrar_usuario.html')

# Rota para consultar usuário (disponível apenas para administradores)
@app.route('/consultar_usuarios')
def consultar_usuarios():
    return render_template('consultar_usuarios.html')

# Rota para exibir o formulário HTML
@app.route('/cadastrar_usuario', methods=['GET'])
def mostrar_formulario():
    return render_template('cadastrar_usuario.html')

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

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
# Rota para receber os dados do formulário e cadastrá-los no banco de dados
@app.route('/cadastrarUser', methods=['POST'])
def submitUser():
    nome = request.form['nome']
    re = request.form['re']
    usuario = request.form['usuario']
    senha = request.form['senha']
    perfil = request.form['perfil']
    email = request.form['email']

    # Salvar a imagem na pasta static/user
    foto = request.files['foto']
    nome_foto = f"{usuario}_foto.jpg"  # Nome do arquivo de foto baseado no usuário
    foto.save(os.path.join(UPLOAD_USER, nome_foto))

    # Salvar a referência da imagem no banco de dados
    with pyodbc.connect(conn_str) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO usuarios (nome, re, usuario, senha, perfil, email, foto) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (nome, re, usuario, senha, perfil, email, nome_foto))
        connection.commit()

    return redirect(url_for('mostrar_formulario'))
# Rota para consultar usuários (disponível apenas para administradores)
@app.route('/consultUser', methods=['GET', 'POST'])
def submitconsult():
    if request.method == 'POST':
        termo_RE = request.form.get('termo_RE', '')
        termo_nome = request.form.get('termo_nome', '')

        # Conectar ao banco de dados
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Consulta SQL para buscar empresas com base nos critérios de consulta
        sql = "SELECT * FROM usuarios WHERE RE LIKE ? AND nome LIKE ?"

        try:
            # Executar a consulta com os parâmetros adequados
            cursor.execute(sql, ('%' + termo_RE + '%', '%' + termo_nome + '%'))

            # Obter os resultados da consulta
            usuarios = cursor.fetchall()

            # Fechar o cursor e a conexão com o banco de dados
            cursor.close()
            conn.close()

            # Renderizar o template HTML com os resultados da consulta
            return render_template('consultar_usuarios.html', usuarios=usuarios)

        except pyodbc.Error as e:
            # Tratar o erro aqui, como registrar e informar ao usuário
            print("Erro ao consultar usuarios:", e)
            return "Erro ao consultar usuarios. Por favor, tente novamente mais tarde."

    return render_template('consultar_usuarios.html')
@app.route('/trocar_Senha', methods=['POST'])
def trocar_Senha():
    # Obter o nome do arquivo da imagem clicada
    nome_imagem = request.form['nome_imagem']

    # Extrair o nome de usuário do nome do arquivo da imagem
    nome_usuario = nome_imagem.split('_')[0]

    # Obter a nova senha do formulário
    nova_senha = request.form['novaSenha']

    # Atualizar a senha na base de dados
    with pyodbc.connect(conn_str) as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE usuarios SET senha = ? WHERE usuario = ?", (nova_senha, nome_usuario))
        connection.commit()

    # Redirecionar o usuário de volta para onde estava
    return redirect(request.referrer)
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
    
    # Rota para lidar com o envio do formulário
@app.route('/patioAud', methods=['POST'])
def submit_patio():
    if request.method == 'POST':
        form_data = request.form

        # Conecta-se ao banco de dados
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        # 2. Insira o caminho da imagem da assinatura nos parâmetros SQL
        sql_columns = "setor_auditado, data_auditoria, representante_setor, auditores"
        sql_values = "?, ?, ?, ?"
        sql_params = [
            form_data['setor_auditado'],
            form_data['data_auditoria'],
            form_data['representante_setor'],
            form_data['auditores']
        
        ]
        for i in range(1, 17):
            pergunta_key = f'pergunta_{i}'
            comentario_key = f'comentario_pergunta_{i}'
            upload_key = f'upload_foto_pergunta_{i}'

            sql_columns += f", pergunta_{i}, comentario_pergunta_{i}, upload_foto_pergunta_{i}"
            sql_values += ", ?, ?, ?"

            sql_params.append(form_data.get(pergunta_key, ''))
            sql_params.append(form_data.get(comentario_key, ''))

            if upload_key in request.files:
                upload_file = request.files[upload_key]
                if upload_file and upload_file.filename and allowed_file(upload_file.filename):
                    # Gera um conjunto de 8 caracteres aleatórios
                    random_suffix = str(uuid.uuid4())[:8]
                    # Gera um nome de arquivo seguro com base no setor_auditado e um identificador único
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    # Obtém a extensão original do arquivo
                    _, extension = os.path.splitext(upload_file.filename)
                    # Gera o nome do arquivo com a extensão original
                    filename = secure_filename(f"{form_data['setor_auditado']}_{timestamp}_{random_suffix}{extension}")

                    # Salva o arquivo no sistema de arquivos
                    upload_file.save(os.path.join(UPLOAD_PATIO, filename))

                    # Salva apenas o caminho do arquivo no banco de dados
                    sql_params.append(os.path.join(UPLOAD_PATIO, filename))
                else:
                    sql_params.append('')
            else:
                sql_params.append('')

        sql = f"INSERT INTO patio ({sql_columns}) VALUES ({sql_values})"
        
        cursor.execute(sql, sql_params)

        # Confirma a transação e fecha a conexão
        conn.commit()
        cursor.close()
        conn.close()
                # Redireciona de volta para a mesma página
        return redirect(url_for('sucesso'))  # Substitua 'index' pelo nome da rota da página atual
        return 'Dados gravados com sucesso no banco de dados Access!'
    return 'Requisição GET recebida'
            # Rota para lidar com o envio do formulário
@app.route('/externasAud', methods=['POST'])
def submit_externas():
    if request.method == 'POST':
        form_data = request.form
        # Conecta-se ao banco de dados
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        # Insere os dados na tabela adequada
        sql_columns = "setor_auditado, data_auditoria, representante_setor, auditores"
        sql_values = "?, ?, ?, ?"
        sql_params = [
            form_data['setor_auditado'],
            form_data['data_auditoria'],
            form_data['representante_setor'],
            form_data['auditores']
        ]

        for i in range(1, 21):
            pergunta_key = f'pergunta_{i}'
            comentario_key = f'comentario_pergunta_{i}'
            upload_key = f'upload_foto_pergunta_{i}'

            sql_columns += f", pergunta_{i}, comentario_pergunta_{i}, upload_foto_pergunta_{i}"
            sql_values += ", ?, ?, ?"

            sql_params.append(form_data.get(pergunta_key, ''))
            sql_params.append(form_data.get(comentario_key, ''))

            if upload_key in request.files:
                upload_file = request.files[upload_key]
                if upload_file and upload_file.filename and allowed_file(upload_file.filename):
                    # Gera um conjunto de 8 caracteres aleatórios
                    random_suffix = str(uuid.uuid4())[:8]
                    # Gera um nome de arquivo seguro com base no setor_auditado e um identificador único
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    # Obtém a extensão original do arquivo
                    _, extension = os.path.splitext(upload_file.filename)
                    # Gera o nome do arquivo com a extensão original
                    filename = secure_filename(f"{form_data['setor_auditado']}_{timestamp}_{random_suffix}{extension}")

                    # Salva o arquivo no sistema de arquivos
                    upload_file.save(os.path.join(UPLOAD_EXTERNAS, filename))

                    # Salva apenas o caminho do arquivo no banco de dados
                    sql_params.append(os.path.join(UPLOAD_EXTERNAS, filename))
                else:
                    sql_params.append('')
            else:
                sql_params.append('')

        sql = f"INSERT INTO externas ({sql_columns}) VALUES ({sql_values})"
        
        cursor.execute(sql, sql_params)

        # Confirma a transação e fecha a conexão
        conn.commit()
        cursor.close()
        conn.close()
        

        return redirect(url_for('sucesso'))  # Substitua 'index' pelo nome da rota da página atual
        return 'Dados gravados com sucesso no banco de dados Access!'
    return 'Requisição GET recebida'

@app.route('/admAud', methods=['POST'])
def submit_adm():
    if request.method == 'POST':
        form_data = request.form
        # Conecta-se ao banco de dados
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        # Insere os dados na tabela adequada
        sql_columns = "setor_auditado, data_auditoria, representante_setor, auditores"
        sql_values = "?, ?, ?, ?"
        sql_params = [
            form_data['setor_auditado'],
            form_data['data_auditoria'],
            form_data['representante_setor'],
            form_data['auditores']
        ]

        for i in range(1, 35):
            pergunta_key = f'pergunta_{i}'
            comentario_key = f'comentario_pergunta_{i}'
            upload_key = f'upload_foto_pergunta_{i}'

            sql_columns += f", pergunta_{i}, comentario_pergunta_{i}, upload_foto_pergunta_{i}"
            sql_values += ", ?, ?, ?"

            sql_params.append(form_data.get(pergunta_key, ''))
            sql_params.append(form_data.get(comentario_key, ''))

            if upload_key in request.files:
                upload_file = request.files[upload_key]
                if upload_file and upload_file.filename and allowed_file(upload_file.filename):
                    # Gera um conjunto de 8 caracteres aleatórios
                    random_suffix = str(uuid.uuid4())[:8]
                    # Gera um nome de arquivo seguro com base no setor_auditado e um identificador único
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    # Obtém a extensão original do arquivo
                    _, extension = os.path.splitext(upload_file.filename)
                    # Gera o nome do arquivo com a extensão original
                    filename = secure_filename(f"{form_data['setor_auditado']}_{timestamp}_{random_suffix}{extension}")

                    # Salva o arquivo no sistema de arquivos
                    upload_file.save(os.path.join(UPLOAD_ADM, filename))

                    # Salva apenas o caminho do arquivo no banco de dados
                    sql_params.append(os.path.join(UPLOAD_ADM, filename))
                else:
                    sql_params.append('')
            else:
                sql_params.append('')

        sql = f"INSERT INTO adm ({sql_columns}) VALUES ({sql_values})"
        
        cursor.execute(sql, sql_params)

        # Confirma a transação e fecha a conexão
        conn.commit()
        cursor.close()
        conn.close()
        
        # Redireciona de volta para a mesma página
                # Redireciona de volta para a mesma página
        return redirect(url_for('sucesso'))  # Substitua 'index' pelo nome da rota da página atual
        return 'Dados gravados com sucesso no banco de dados Access!'
    return 'Requisição GET recebida'
@app.route('/apoioAud', methods=['POST'])
def submit_apoio():
    if request.method == 'POST':
        form_data = request.form
        # Conecta-se ao banco de dados
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        # Insere os dados na tabela adequada
        sql_columns = "setor_auditado, data_auditoria, representante_setor, auditores"
        sql_values = "?, ?, ?, ?"
        sql_params = [
            form_data['setor_auditado'],
            form_data['data_auditoria'],
            form_data['representante_setor'],
            form_data['auditores']
        ]

        for i in range(1, 35):
            pergunta_key = f'pergunta_{i}'
            comentario_key = f'comentario_pergunta_{i}'
            upload_key = f'upload_foto_pergunta_{i}'

            sql_columns += f", pergunta_{i}, comentario_pergunta_{i}, upload_foto_pergunta_{i}"
            sql_values += ", ?, ?, ?"

            sql_params.append(form_data.get(pergunta_key, ''))
            sql_params.append(form_data.get(comentario_key, ''))

            if upload_key in request.files:
                upload_file = request.files[upload_key]
                if upload_file and upload_file.filename and allowed_file(upload_file.filename):
                    # Gera um conjunto de 8 caracteres aleatórios
                    random_suffix = str(uuid.uuid4())[:8]
                    # Gera um nome de arquivo seguro com base no setor_auditado e um identificador único
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    # Obtém a extensão original do arquivo
                    _, extension = os.path.splitext(upload_file.filename)
                    # Gera o nome do arquivo com a extensão original
                    filename = secure_filename(f"{form_data['setor_auditado']}_{timestamp}_{random_suffix}{extension}")

                    # Salva o arquivo no sistema de arquivos
                    upload_file.save(os.path.join(UPLOAD_APOIO, filename))

                    # Salva apenas o caminho do arquivo no banco de dados
                    sql_params.append(os.path.join(UPLOAD_APOIO, filename))
                else:
                    sql_params.append('')
            else:
                sql_params.append('')

        sql = f"INSERT INTO apoio ({sql_columns}) VALUES ({sql_values})"
        
        cursor.execute(sql, sql_params)

        # Confirma a transação e fecha a conexão
        conn.commit()
        cursor.close()
        conn.close()
        
        # Redireciona de volta para a mesma página
                # Redireciona de volta para a mesma página
        return redirect(url_for('sucesso'))  # Substitua 'index' pelo nome da rota da página atual
        return 'Dados gravados com sucesso no banco de dados Access!'
    return 'Requisição GET recebida'
@app.route('/prodAud', methods=['POST'])
def submit_prod():
    if request.method == 'POST':
        form_data = request.form
        # Conecta-se ao banco de dados
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        # Insere os dados na tabela adequada
        sql_columns = "setor_auditado, data_auditoria, representante_setor, auditores"
        sql_values = "?, ?, ?, ?"
        sql_params = [
            form_data['setor_auditado'],
            form_data['data_auditoria'],
            form_data['representante_setor'],
            form_data['auditores']
        ]

        for i in range(1, 33):
            pergunta_key = f'pergunta_{i}'
            comentario_key = f'comentario_pergunta_{i}'
            upload_key = f'upload_foto_pergunta_{i}'

            sql_columns += f", pergunta_{i}, comentario_pergunta_{i}, upload_foto_pergunta_{i}"
            sql_values += ", ?, ?, ?"

            sql_params.append(form_data.get(pergunta_key, ''))
            sql_params.append(form_data.get(comentario_key, ''))

            if upload_key in request.files:
                upload_file = request.files[upload_key]
                if upload_file and upload_file.filename and allowed_file(upload_file.filename):
                    # Gera um conjunto de 8 caracteres aleatórios
                    random_suffix = str(uuid.uuid4())[:8]
                    # Gera um nome de arquivo seguro com base no setor_auditado e um identificador único
                    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                    # Obtém a extensão original do arquivo
                    _, extension = os.path.splitext(upload_file.filename)
                    # Gera o nome do arquivo com a extensão original
                    filename = secure_filename(f"{form_data['setor_auditado']}_{timestamp}_{random_suffix}{extension}")

                    # Salva o arquivo no sistema de arquivos
                    upload_file.save(os.path.join(UPLOAD_PRODUCAO, filename))

                    # Salva apenas o caminho do arquivo no banco de dados
                    sql_params.append(os.path.join(UPLOAD_PRODUCAO, filename))
                else:
                    sql_params.append('')
            else:
                sql_params.append('')

        sql = f"INSERT INTO producao ({sql_columns}) VALUES ({sql_values})"
        
        cursor.execute(sql, sql_params)

        # Confirma a transação e fecha a conexão
        conn.commit()
        cursor.close()
        conn.close()
        
        # Redireciona de volta para a mesma página
                # Redireciona de volta para a mesma página
        return redirect(url_for('sucesso'))  # Substitua 'index' pelo nome da rota da página atual
        return 'Dados gravados com sucesso no banco de dados Access!'
    return 'Requisição GET recebida'
# Função auxiliar para verificar se a extensão do arquivo é permitida
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
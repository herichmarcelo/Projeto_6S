from flask import Flask, request
from flask import Blueprint, render_template
import pyodbc
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Defina a pasta onde os arquivos serão carregados
UPLOAD_PATIO = 'static/patio'
app.config['UPLOAD_PATIO'] = UPLOAD_PATIO
# String de conexão com o banco de dados Access
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=dados/base.accdb;'
    r'charset=utf-8;'
)

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
                    upload_file.save(os.path.join(UPLOAD_PATIO, filename))
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
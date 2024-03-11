import pyodbc

# Configurações de conexão com o banco de dados Access
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=H:\Documentos\PYTHON\Projeto_6S\dados\base.accdb;'
)

# Conectar ao banco de dados
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# SQL para criar a tabela "patio" com os campos especificados
sql_create_table = '''
CREATE TABLE patio (
    setor_auditado TEXT,
    data_auditoria TEXT,
    representante_setor TEXT,
    auditores TEXT,
    pergunta_1 TEXT,
    comentario_pergunta_1 TEXT,
    upload_foto_pergunta_1 TEXT,
    pergunta_2 TEXT,
    comentario_pergunta_2 TEXT,
    upload_foto_pergunta_2 TEXT,
    pergunta_3 TEXT,
    comentario_pergunta_3 TEXT,
    upload_foto_pergunta_3 TEXT,
    pergunta_4 TEXT,
    comentario_pergunta_4 TEXT,
    upload_foto_pergunta_4 TEXT,
    pergunta_5 TEXT,
    comentario_pergunta_5 TEXT,
    upload_foto_pergunta_5 TEXT,
    pergunta_6 TEXT,
    comentario_pergunta_6 TEXT,
    upload_foto_pergunta_6 TEXT,
    pergunta_7 TEXT,
    comentario_pergunta_7 TEXT,
    upload_foto_pergunta_7 TEXT,
    pergunta_8 TEXT,
    comentario_pergunta_8 TEXT,
    upload_foto_pergunta_8 TEXT,
    pergunta_9 TEXT,
    comentario_pergunta_9 TEXT,
    upload_foto_pergunta_9 TEXT,
    pergunta_10 TEXT,
    comentario_pergunta_10 TEXT,
    upload_foto_pergunta_10 TEXT,
    pergunta_11 TEXT,
    comentario_pergunta_11 TEXT,
    upload_foto_pergunta_11 TEXT,
    pergunta_12 TEXT,
    comentario_pergunta_12 TEXT,
    upload_foto_pergunta_12 TEXT,
    pergunta_13 TEXT,
    comentario_pergunta_13 TEXT,
    upload_foto_pergunta_13 TEXT,
    pergunta_14 TEXT,
    comentario_pergunta_14 TEXT,
    upload_foto_pergunta_14 TEXT,
    pergunta_15 TEXT,
    comentario_pergunta_15 TEXT,
    upload_foto_pergunta_15 TEXT,
    pergunta_16 TEXT,
    comentario_pergunta_16 TEXT,
    upload_foto_pergunta_16 TEXT
)
'''

# Executar a consulta SQL para criar a tabela
cursor.execute(sql_create_table)

# Confirmar a transação
conn.commit()

# Fechar a conexão com o banco de dados
conn.close()

print("Tabela 'patio' criada com sucesso.")

import streamlit as st
import pandas as pd


def criar_formulario_auditoria():
    st.title('CHECKLIST AUDITORIA 6S PATIO')
    
    # Informações sobre o setor auditado
    setor_auditado = st.text_input('Setor Auditado:')
    data_auditoria = st.date_input('Data da Auditoria:')
    representante_setor = st.text_input('Representante do Setor:')
    auditores = st.text_input('Dupla de Auditores:')

    # Seção SENSO DE UTILIZAÇÃO

    st.subheader('SENSO DE UTILIZAÇÃO')

    # Pergunta 1
    st.write('1. Existem materiais ou equipamentos que não estão sendo utilizados sobre as mesas e bancadas?')
    resposta_seiri_1 = st.radio('Selecione (Pergunta 1):', ['😃 Bom', '😐 Médio', '😟 Ruim'], key='resposta_seiri_1')
    comentario_seiri_1_placeholder = st.empty()
    if resposta_seiri_1 == '😟 Ruim':
        comentario_seiri_1 = comentario_seiri_1_placeholder.text_area('Comentário (caso a resposta seja Ruim - Pergunta 1):', key='comentario_seiri_1')
        upload_foto_seiri_1 = st.file_uploader('Faça o upload de fotos (caso necessário):', type=['jpg', 'jpeg', 'png'], key='upload_foto_seiri_1')
  
    # Pergunta 2
    st.write('2. Existem equipamentos/mobiliários, ferramentas ou algum elemento de estrutura física do setor necessitando de reparo, enferrujados, velhos ou que precisa ser trocado?')
    resposta_seiri_2 = st.radio('Selecione (Pergunta 2):', ['😃 Bom', '😐 Médio', '😟 Ruim'], key='resposta_seiri_2')
    comentario_seiri_2_placeholder = st.empty()
    if resposta_seiri_2 == '😟 Ruim':
        comentario_seiri_2 = comentario_seiri_2_placeholder.text_area('Comentário (caso a resposta seja Ruim - Pergunta 2):', key='comentario_seiri_2')
        upload_foto_seiri_2 = st.file_uploader('Faça o upload de fotos (caso necessário):', type=['jpg', 'jpeg', 'png'], key='upload_foto_seiri_2')

    # Seção SENSO DE ORGANIZAÇÃO
    st.subheader('SENSO DE ORGANIZAÇÃO')

    # Pergunta 1 - SENSO DE ORGANIZAÇÃO
    st.write('1. Os materiais e objetos estão em locais adequados, organizados e identificados corretamente?')
    resposta_seiton_1 = st.radio('Selecione (Pergunta 1):', ['😃 Bom', '😐 Médio', '😟 Ruim'], key='resposta_seiton_1')
    comentario_seiton_1_placeholder = st.empty()
    if resposta_seiton_1 == '😟 Ruim':
        comentario_seiton_1 = comentario_seiton_1_placeholder.text_area('Comentário (caso a resposta seja Ruim - Pergunta 1):', key='comentario_seiton_1')
        upload_foto_seiton_1 = st.file_uploader('Faça o upload de fotos (caso necessário):', type=['jpg', 'jpeg', 'png'], key='upload_foto_seiton_1')

    # Pergunta 2 - SENSO DE ORGANIZAÇÃO
    st.write('2. De modo geral, o setor encontra-se organizado?')
    resposta_seiton_2 = st.radio('Selecione (Pergunta 2):', ['😃 Bom', '😐 Médio', '😟 Ruim'], key='resposta_seiton_2')
    comentario_seiton_2_placeholder = st.empty()
    if resposta_seiton_2 == '😟 Ruim':
        comentario_seiton_2 = comentario_seiton_2_placeholder.text_area('Comentário (caso a resposta seja Ruim - Pergunta 2):', key='comentario_seiton_2')
        upload_foto_seiton_2 = st.file_uploader('Faça o upload de fotos (caso necessário):', type=['jpg', 'jpeg', 'png'], key='upload_foto_seiton_2')

    # Seção SENSO DE LIMPEZA
    st.subheader('SENSO DE LIMPEZA')

    # Pergunta 1 - SENSO DE LIMPEZA
    st.write('1. Existe acumulo de água e excesso de resíduos?')
    resposta_seisan_1 = st.radio('Selecione (Pergunta 1):', ['😃 Bom', '😐 Médio', '😟 Ruim'], key='resposta_seisan_1')
    comentario_seisan_1_placeholder = st.empty()
    if resposta_seisan_1 == '😟 Ruim':
        comentario_seisan_1 = comentario_seisan_1_placeholder.text_area('Comentário (caso a resposta seja Ruim - Pergunta 1):', key='comentario_seisan_1')
        upload_foto_seisan_1 = st.file_uploader('Faça o upload de fotos (caso necessário):', type=['jpg', 'jpeg', 'png'], key='upload_foto_seisan_1')
    # Pergunta 2 - SENSO DE LIMPEZA
    st.write('2. O piso/grama da área encontra-se limpo, sem papéis, copos descartáveis ou resíduos?')
    resposta_seisan_2 = st.radio('Selecione (Pergunta 2):', ['😃 Bom', '😐 Médio', '😟 Ruim'], key='resposta_seisan_2')
    comentario_seisan_2_placeholder = st.empty()
    if resposta_seisan_2 == '😟 Ruim':
        comentario_seisan_2 = comentario_seisan_2_placeholder.text_area('Comentário (caso a resposta seja Ruim - Pergunta 2):', key='comentario_seisan_2')
        upload_foto_seisan_2 = st.file_uploader('Faça o upload de fotos (caso necessário):', type=['jpg', 'jpeg', 'png'], key='upload_foto_seisan_2')

    # Seção SENSO DE PADRONIZAÇÃO
    st.subheader('SENSO DE PADRONIZAÇÃO')

    # Pergunta 1 - SENSO DE PADRONIZAÇÃO
    st.write('1. As lâmpadas, luminárias estão limpas e em funcionamento?')
    resposta_seipan_1 = st.radio('Selecione (Pergunta 1):', ['😃 Bom', '😐 Médio', '😟 Ruim'], key='resposta_seipan_1')
    comentario_seipan_1_placeholder = st.empty()
    if resposta_seipan_1 == '😟 Ruim':
        comentario_seipan_1 = comentario_seipan_1_placeholder.text_area('Comentário (caso a resposta seja Ruim - Pergunta 1):', key='comentario_seipan_1')
        upload_foto_seipan_1 = st.file_uploader('Faça o upload de fotos (caso necessário):', type=['jpg', 'jpeg', 'png'], key='upload_foto_seipan_1')        

    # Pergunta 2 - SENSO DE PADRONIZAÇÃO
    st.write('2. Os equipamentos de combate à incêndios estão identificados, em boas condições e prontos para o uso?')
    resposta_seipan_2 = st.radio('Selecione (Pergunta 2):', ['😃 Bom', '😐 Médio', '😟 Ruim'], key='resposta_seipan_2')
    comentario_seipan_2_placeholder = st.empty()
    if resposta_seipan_2 == '😟 Ruim':
        comentario_seipan_2 = comentario_seipan_2_placeholder.text_area('Comentário (caso a resposta seja Ruim - Pergunta 2):', key='comentario_seipan_2')
        upload_foto_seipan_2 = st.file_uploader('Faça o upload de fotos (caso necessário):', type=['jpg', 'jpeg', 'png'], key='upload_foto_seipan_2')          

    # Seção SENSO DE AUTO DISCIPLINA
    st.subheader('SENSO DE AUTO DISCIPLINA')

    # Pergunta 1 - SENSO DE AUTO DISCIPLINA
    st.write('1. Existem materiais ou objetos impossibilitando trajeto, impedindo entrada de áreas ou setores?')
    resposta_seiad_1 = st.radio('Selecione (Pergunta 1):', ['😃 Bom', '😐 Médio', '😟 Ruim'], key='resposta_seiad_1')
    comentario_seiad_1_placeholder = st.empty()
    if resposta_seiad_1 == '😟 Ruim':
        comentario_seiad_1 = comentario_seiad_1_placeholder.text_area('Comentário (caso a resposta seja Ruim - Pergunta 1):', key='comentario_seiad_1')
        upload_foto_seiad_1 = st.file_uploader('Faça o upload de fotos (caso necessário):', type=['jpg', 'jpeg', 'png'], key='upload_foto_seiad_1')          

    # Pergunta 2 - SENSO DE AUTO DISCIPLINA
    st.write('2. São elaborados Planos de Ação para correção das Não Conformidades encontradas e os mesmos são gerenciados pelo setor? As ações da última auditoria.')
    resposta_seiad_2 = st.radio('Selecione (Pergunta 2):', ['😃 Bom', '😐 Médio', '😟 Ruim'], key='resposta_seiad_2')
    comentario_seiad_2_placeholder = st.empty()
    if resposta_seiad_2 == '😟 Ruim':
        comentario_seiad_2 = comentario_seiad_2_placeholder.text_area('Comentário (caso a resposta seja Ruim - Pergunta 2):', key='comentario_seiad_2')
        upload_foto_seiad_2 = st.file_uploader('Faça o upload de fotos (caso necessário):', type=['jpg', 'jpeg', 'png'], key='upload_foto_seiad_2')          

    # Pergunta 3 - SENSO DE AUTO DISCIPLINA
    st.write('3. O ambiente reflete a essência do Programa 6S? A área causa impacto, admiração? O setor cumpre com os demais Sensos?')
    resposta_seiad_3 = st.radio('Selecione (Pergunta 3):', ['😃 Bom', '😐 Médio', '😟 Ruim'], key='resposta_seiad_3')
    comentario_seiad_3_placeholder = st.empty()
    if resposta_seiad_3 == '😟 Ruim':
        comentario_seiad_3 = comentario_seiad_3_placeholder.text_area('Comentário (caso a resposta seja Ruim - Pergunta 3):', key='comentario_seiad_3')
        upload_foto_seiad_3 = st.file_uploader('Faça o upload de fotos (caso necessário):', type=['jpg', 'jpeg', 'png'], key='upload_foto_seiad_3')          

    # Seção SENSO DE SEGURANÇA DO ALIMENTO
    st.subheader('SENSO DE SEGURANÇA DO ALIMENTO')

    # Pergunta 1 - SENSO DE SEGURANÇA DO ALIMENTO
    st.write('1. Os colaboradores conhecem a Política da Qualidade? (Entrevistar colaboradores).')
    resposta_seisa_1 = st.radio('Selecione (Pergunta 1):', ['😃 Bom', '😐 Médio', '😟 Ruim'], key='resposta_seisa_1')
    comentario_seisa_1_placeholder = st.empty()
    if resposta_seisa_1 == '😟 Ruim':
          comentario_seisa_1 = comentario_seisa_1_placeholder.text_area('Comentário (caso a resposta seja Ruim - Pergunta 1):', key='comentario_seisa_1')
          upload_foto_seisa_1 = st.file_uploader('Faça o upload de fotos (caso necessário):', type=['jpg', 'jpeg', 'png'], key='upload_foto_seisa_1')            
                                                                      
    # Pergunta 2 - SENSO DE SEGURANÇA DO ALIMENTO
    st.write('2. Bancadas, mesas, armários, estantes, gavetas são mantidas organizadas durante a execução das tarefas?')
    resposta_seisa_2 = st.radio('Selecione (Pergunta 2):', ['😃 Bom', '😐 Médio', '😟 Ruim'], key='resposta_seisa_2')
    comentario_seisa_2_placeholder = st.empty()
    if resposta_seisa_2 == '😟 Ruim':
        comentario_seisa_2 = comentario_seisa_2_placeholder.text_area('Comentário (caso a resposta seja Ruim - Pergunta 2):', key='comentario_seisa_2')
        upload_foto_seisa_2 = st.file_uploader('Faça o upload de fotos (caso necessário):', type=['jpg', 'jpeg', 'png'], key='upload_foto_seisa_2')            

    # Pergunta 3 - SENSO DE SEGURANÇA DO ALIMENTO
    st.write('3. Os colaboradores entendem e praticam as Boas Práticas de Fabricação (BPF), (Colaborador com roupa civil por baixo do uniforme, usando adornos ou maquiagem, não fazendo uso das barreiras sanitárias, etc.).')
    resposta_seisa_3 = st.radio('Selecione (Pergunta 3):', ['😃 Bom', '😐 Médio', '😟 Ruim'], key='resposta_seisa_3')
    comentario_seisa_3_placeholder = st.empty()
    if resposta_seisa_3 == '😟 Ruim':
        comentario_seisa_3 = comentario_seisa_3_placeholder.text_area('Comentário (caso a resposta seja Ruim - Pergunta 3):', key='comentario_seisa_3')
        upload_foto_seisa_3 = st.file_uploader('Faça o upload de fotos (caso necessário):', type=['jpg', 'jpeg', 'png'], key='upload_foto_seisa_3')            

    # Pergunta 4 - SENSO DE SEGURANÇA DO ALIMENTO
    st.write('4. As lixeiras estão sendo utilizadas corretamente? (Todo lixo dentro da lixeira, lixeira padrão, resíduos separados corretamente).')
    resposta_seisa_4 = st.radio('Selecione (Pergunta 4):', ['😃 Bom', '😐 Médio', '😟 Ruim'], key='resposta_seisa_4')
    comentario_seisa_4_placeholder = st.empty()
    if resposta_seisa_4 == '😟 Ruim':
        comentario_seisa_4 = comentario_seisa_4_placeholder.text_area('Comentário (caso a resposta seja Ruim - Pergunta 4):', key='comentario_seisa_4')
        upload_foto_seisa_4 = st.file_uploader('Faça o upload de fotos (caso necessário):', type=['jpg', 'jpeg', 'png'], key='upload_foto_seisa_4')            

    # ... (código posterior)

    return {
        'Setor Auditado': setor_auditado,
        'Data da Auditoria': data_auditoria,
        'Representante do Setor': representante_setor,
        'Dupla de Auditores': auditores,
        'Senso de Utilização - Pergunta 1': {'Resposta': resposta_seiri_1, 'Comentário': comentario_seiri_1 if resposta_seiri_1 == '😟 Ruim' else '', 'Upload de Foto': upload_foto_seiri_1 if resposta_seiri_1 == '😟 Ruim' else None},
        'Senso de Utilização - Pergunta 2': {'Resposta': resposta_seiri_2, 'Comentário': comentario_seiri_2 if resposta_seiri_2 == '😟 Ruim' else '', 'Upload de Foto': upload_foto_seiri_2 if resposta_seiri_2 == '😟 Ruim' else None},
        'Senso de Organização - Pergunta 1': {'Resposta': resposta_seiton_1, 'Comentário': comentario_seiton_1 if resposta_seiton_1 == '😟 Ruim' else '', 'Upload de Foto': upload_foto_seiton_1 if resposta_seiton_1 == '😟 Ruim' else None},
        'Senso de Organização - Pergunta 2': {'Resposta': resposta_seiton_2, 'Comentário': comentario_seiton_2 if resposta_seiton_2 == '😟 Ruim' else '', 'Upload de Foto': upload_foto_seiton_2 if resposta_seiton_2 == '😟 Ruim' else None},
        'Senso de Limpeza - Pergunta 1': {'Resposta': resposta_seisan_1, 'Comentário': comentario_seisan_1 if resposta_seisan_1 == '😟 Ruim' else '', 'Upload de Foto': upload_foto_seisan_1 if resposta_seisan_1 == '😟 Ruim' else None},
        'Senso de Limpeza - Pergunta 2': {'Resposta': resposta_seisan_2, 'Comentário': comentario_seisan_2 if resposta_seisan_2 == '😟 Ruim' else '', 'Upload de Foto': upload_foto_seisan_2 if resposta_seisan_2 == '😟 Ruim' else None},
        'Senso de Padronização - Pergunta 1': {'Resposta': resposta_seipan_1, 'Comentário': comentario_seipan_1 if resposta_seipan_1 == '😟 Ruim' else '', 'Upload de Foto': upload_foto_seipan_1 if resposta_seipan_1 == '😟 Ruim' else None},
        'Senso de Padronização - Pergunta 2': {'Resposta': resposta_seipan_2, 'Comentário': comentario_seipan_2 if resposta_seipan_2 == '😟 Ruim' else '', 'Upload de Foto': upload_foto_seipan_2 if resposta_seipan_2 == '😟 Ruim' else None},
        'Senso de Auto Disciplina - Pergunta 1': {'Resposta': resposta_seiad_1, 'Comentário': comentario_seiad_1 if resposta_seiad_1 == '😟 Ruim' else '', 'Upload de Foto': upload_foto_seiad_1 if resposta_seiad_1 == '😟 Ruim' else None},
        'Senso de Auto Disciplina - Pergunta 2': {'Resposta': resposta_seiad_2, 'Comentário': comentario_seiad_2 if resposta_seiad_2 == '😟 Ruim' else '', 'Upload de Foto': upload_foto_seiad_2 if resposta_seiad_2 == '😟 Ruim' else None},
        'Senso de Auto Disciplina - Pergunta 3': {'Resposta': resposta_seiad_3, 'Comentário': comentario_seiad_3 if resposta_seiad_3 == '😟 Ruim' else '', 'Upload de Foto': upload_foto_seiad_3 if resposta_seiad_3 == '😟 Ruim' else None},
        'Senso de Segurança do Alimento - Pergunta 1': {'Resposta': resposta_seisa_1, 'Comentário': comentario_seisa_1 if resposta_seisa_1 == '😟 Ruim' else '', 'Upload de Foto': upload_foto_seisa_1 if resposta_seisa_1 == '😟 Ruim' else None},
        'Senso de Segurança do Alimento - Pergunta 2': {'Resposta': resposta_seisa_2, 'Comentário': comentario_seisa_2 if resposta_seisa_2 == '😟 Ruim' else '', 'Upload de Foto': upload_foto_seisa_2 if resposta_seisa_2 == '😟 Ruim' else None},
        'Senso de Segurança do Alimento - Pergunta 3': {'Resposta': resposta_seisa_3, 'Comentário': comentario_seisa_3 if resposta_seisa_3 == '😟 Ruim' else '', 'Upload de Foto': upload_foto_seisa_3 if resposta_seisa_3 == '😟 Ruim' else None},
        'Senso de Segurança do Alimento - Pergunta 4': {'Resposta': resposta_seisa_4, 'Comentário': comentario_seisa_4 if resposta_seisa_4 == '😟 Ruim' else '', 'Upload de Foto': upload_foto_seisa_4 if resposta_seisa_4 == '😟 Ruim' else None},
        # ... (continuação para os outros sensos)
    }

def criar_botao_csv(respostas_auditoria):
    csv_data = pd.DataFrame([respostas_auditoria])
    csv_file = csv_data.to_csv(index=False)

    # Adicionando botão de download para o CSV
    st.download_button(
        label="Baixar CSV",
        data=csv_file,
        key='csv_download_button',
        file_name=f'checklist_auditoria_6s_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.csv',
        mime='text/csv',
    )

def main():
    respostas_auditoria = criar_formulario_auditoria()
    criar_botao_csv(respostas_auditoria)

if __name__ == "__main__":
    main()
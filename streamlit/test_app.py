import streamlit as st
import numpy as numpy
import pandas as pd
import altair as alt

def main():
    '''TEXT'''
    st.title('Hello World')
    st.header('This a header')
    st.subheader('This a subheader')
    st.text('This a text')
    st.markdown('This a markdown')

    #st.balloons()

    #'''BOTOES E AFINS'''
    st.subheader('BOTOES E AFINS')
    #BOTAO
    st.subheader('Botao')
    botao = st.button('Botao')
    if botao:
        st.markdown('Clicado')

    #CHECKBOX
    st.subheader('Checkbox')
    caixa_check1 = st.checkbox('Checkbox01')
    caixa_check2 = st.checkbox('Checkbox02')
    if caixa_check1:
        st.markdown('Clicado01')
        st.balloons()
    if caixa_check2:
        st.markdown('Clicado02')

    #RADIO (Opção Única por Botão)
    st.subheader('Lista de Opções (Radio)')
    opcao_unica = st.radio('Selecione apenas UMA opção:',
     ('Opção 01', 'Opção 02', 'Opção 03'),
     index=2, key='nome alternativo')

    if opcao_unica == 'Opção 01':
        st.markdown('Clicado 01')
    else:
        st.write("Você não selecionou a opção 01!")

    if opcao_unica == 'Opção 02':
        st.markdown('Clicado 02')
    else:
        st.write("Você não selecionou a opção 02!")

    if opcao_unica == 'Opção 03':
        st.markdown('Clicado 03')
    else:
        st.write("Você não selecionou a opção 03!")    

    #SELECTBOX (Opção Única por Lista)
    st.subheader('Lista de Opções (Selectbox)')
    opcao_multipla = st.selectbox('Selecione apenas UMA opção:',
     ('Opção 01', 'Opção 02', 'Opção 03'),
     index=2, key='nome alternativo')

    if opcao_multipla == 'Opção 01':
        st.markdown('Clicado 01')
 
    if opcao_multipla == 'Opção 02':
        st.markdown('Clicado 02')

    if opcao_multipla == 'Opção 03':
        st.markdown('Clicado 03')

    #FILE UPLOAD
    st.subheader('Carregar Arquivo (File Uploader)')
    file = st.file_uploader('Selecione seu arquivo de dados tipo CSV', type='csv')
    if file is not None:
        st.markdown('Não está vazio!')

    #'''MIDIASMal ai. Internet zuada
    # '''
    st.subheader('MIDIA')
    #IMAGE
    st.subheader('Foto/Figura')
    st.image('BackGround Tech.jpg', width=400)
    
    #AUDIO
    st.subheader('Audio Dublagem do Video/Desenho')
    st.audio('Narracao Kawaii You Tube.mp4')

    #VIDEO
    st.subheader('Video Piano (Curto)')
    # Opcao 1 para video
    # video_file = open('Piano_keys.mp4', 'rb')
    #video_bytes = video_file.read()
    #st.video(video_bytes)
    # Opcao 2 para video
    st.video('Piano_keys.mp4', format='video/mp4', start_time=55)
    
if __name__ == '__main__':
    main()



def criar_histograma(coluna, df):
    chart = alt.Chart(df, width=600).mark_bar().encode(
        alt.X(coluna, bin=True),
        y='count()', tootip=[coluna, 'count()']
    ).interactive()
    return chart
import streamlit as st
import numpy as numpy
import pandas as pd
import altair as alt
import base64 # Para exportação / Cria link
from sklearn.preprocessing import LabelEncoder

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    #href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    href = f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'
    return href
#https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/12

def criar_histograma(coluna, df2):
    chart = alt.Chart(df2, width=600).mark_bar.encode(
        alt.X(coluna, bin=True),
        y='count', tooltip=[coluna, 'count()']
    ).interactive()
    return chart

#def criar_barras(coluna_num, coluna_cat, df2):
#    barra = alt.Chart(df2, width=600).mark_bar.encode(
#        x=alt.X(coluna_num, stack='zero'),
#        y=alt.Y(coluna_cat, tooltip=[coluna_cat, coluna_num]
#    ).interactive()
#    return barra

def criar_boxplot(coluna_num, coluna_cat, df2):
    boxplot = alt.Chart(df2, width=600).mark_boxplot.encode(
        x=coluna_num,
        y=coluna_cat
    )
    return boxplot

def criar_scatterplot(x, y, color, df2):
    scatter = alt.Chart(df2, width=600, height=600).mark_circle.encode(
        alt.X(x),
        alt.Y(y),
        color = color,
        tooltip = [x,y]
    ).interactive()
    return scatter

def criar_correlationplot(df2, colunas_numericas):
    cor_data = (df2[colunas_numericas]).corr().stack().reset_index().rename(columns={0: 'correlation', 'level_0': 'variable', 'level_1': 'variable2'})
    # The stacking results in an index on the correlation values, we need the index as normal columns for Altair
    cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format) # Round to 2 decimal
    base = alt.Chart(cor_data, width=600, height=600).encode(x='variable2:0', y='variable:0')
    # Text layer with correlation labels
    # Colors are for easier readability
    text = base.mark_text().encode(
        text='correlation_label',
        color=alt.condition(
            alt.datum.correlation > 0.5,
            alt.value('white'),
            alt.value('black')
        )
    )
    # The correlation heatmap itself
    cor_plot = base.mark_rect.encode(
        color='correlation:Q'
    )
    return cor_plot + text # The '+' means overlaying the text and rect layer

def main():
    #TITULO
    st.title('Interface de Exploração de Dados e Análise')
    st.header('**( I.E.D.A. )**')
    st.text('Por: Télio Mendes')
    #IMAGE
    st.image('BackGround Tech.jpg', width=400)
    #FILE UPLOAD
    file = st.file_uploader('Selecione o arquivo _CSV_ a ser analisado:', type='csv')
    if file is not None:
        df = pd.read_csv(file)
        st.subheader('**Observação geral dos dados**')
        # Seleciona quantidade de linhas
        n_linhas = df.shape[0]
        n_colunas = df.shape[1]
        st.write('*Total de linhas/colunas = *', n_linhas, '/', n_colunas)
        slider = st.slider('Quantidade de linhas', 1,20, 5)
        # Seleciona se início, fim ou aleatório
        posicao = st.selectbox('Posição no dataframe:',
        ('Início', 'Final', 'Aleatório'), index=0)
        if posicao == 'Início':
            st.dataframe(df.head(slider))
            #st.table(df.head(slider))
        if posicao == 'Final':
            st.dataframe(df.tail(slider))
            #st.table(df.tail(slider))
        if posicao == 'Aleatório':
            st.dataframe(df.sample(slider))
            #st.table(df.sample(slider))
        
        # Visão Geral das Informações do Banco de Dados 
        texto_colunas = 'Lista de Colunas (  total  ='+ str(df.shape[1])+ ')'
        st.subheader(texto_colunas)
        todas_colunas = [k for k in df.columns]
        todos_tipos = [str(df.dtypes[[k]]).split(" ")[4].split('\n')[0] for k in df.columns]
        df_todas_colunas = pd.DataFrame({"Coluna": todas_colunas, "Tipo": todos_tipos})
        st.dataframe(df_todas_colunas)
        
        # Info genérica
        st.write('* **Resumo estatísticos das colunas numéricas**')
        st.dataframe(df.describe())
        
        # Colunas (tipos)
        exploracao = pd.DataFrame({'nomes': df.columns, 'tipos': df.dtypes, 'NA %': (df.isna().sum() / df.shape[0]) * 100})
        st.write('* **Tipos de dados da colunas**', exploracao['tipos'].value_counts())
        # st.write('**Nomes das colunas tipo int64: **', exploracao[exploracao['tipos'] == 'int64']['nomes'].to_list())
        
        st.write('* **Colunas tipo int64**')
        for k in exploracao[exploracao['tipos'] == 'int64']['nomes']:
            st.write(k)
        
        st.write('* **Colunas tipo float64**')
        for k in exploracao[exploracao['tipos'] == 'float64']['nomes']:
            st.write(k)
        
        st.write('* **Colunas tipo object**')
        for k in exploracao[exploracao['tipos'] == 'object']['nomes']:
            st.write(k)
        categoricos = st.multiselect('-- Selecione as colunas que deseja adicionar Categórica Numérica --',
        exploracao[exploracao['tipos'] == 'object']['nomes'])
        #st.write('You selected:', categoricos)

        # Maneira menos eficiente de criar variáveis        
#        categorizar = set()
#        for k in exploracao[exploracao['tipos'] == 'object']['nomes']:
#            selecao_categoric = st.checkbox(f'{k} ', False)
#            if selecao_categoric:
#                categorizar.add(k)
#        st.write(categorizar)

        # Alteração de dados tipo object para categoric 
    #    for k in categoricos:
    #        df[k] = pd.Categorical(df[k])
    #        df[k] = df[k].cat.codes

        labelencoder = LabelEncoder()
        for k in categoricos:
            #df[k] = df[k].astype('category')
            df[f'{k}_Cat'] = labelencoder.fit_transform(df[k])

    #    st.write(df.dtypes)
    #    exploracao2 = pd.DataFrame({'nomes': df.columns, 'tipos': df.dtypes, 'NA %': (df.isna().sum() / df.shape[0]) * 100})
        
    #    for k in categoricos:
    #        df[k].apply(LabelEncoder().fit_transform)
    
    #    st.write('* **Colunas alteradas para tipo category**')
    #    for k in exploracao2[exploracao2['tipos'] == 'category']['nomes']:
    #        st.write(k)
        #st.table(df.head())
        #st.dataframe(df.head())

        # Dados faltantes
        st.write('* **Dados Faltantes (%)**')
        st.table(exploracao[exploracao['NA %'] != 0][['tipos', 'NA %']])

#        st.write('* **Consolidado - Tipos e NA %**')
#        st.table(exploracao[['tipos','NA %']])

#        # Correção de dados faltantes
#        st.write('* **Imputação de dados**')
#        percentual = st.slider('Escolha o limite percentual faltante máximo para as colunas que se deseja imputar dados',
#        max_value=100, min_value=0, value=0, format='%d')
#        lista_colunas = list(exploracao[exploracao['NA %'] < percentual]['nomes'])
#        st.write(lista_colunas)
#        select_method = st.radio('Escolha um método abaixo:', ('','Média', 'Mediana', 'Zero'))
#        st.markdown('Você selecionou:' + str(select_method))
#        #if select_method != '':
#        if select_method == 'Média':
#            df_imputado = df[lista_colunas].fillna(df[lista_colunas].mean())
#            exploracao_imputado = pd.DataFrame({'nomes': df_imputado.columns, 'tipos': df_imputado.dtypes,
#            'NA #': df_imputado.isna().sum(), 'NA %': (df_imputado.isna().sum() / df.shape[0]) * 100})
#            st.table(exploracao_imputado[exploracao_imputado['tipos'] != 'object']['NA %'])
#            st.subheader('Dados imputados, faça download abaixo')
#            st.markdown(get_table_download_link(df_imputado), unsafe_allow_html=True)
        
        st.write('**..............................................................**')
        # SUB DATAFRAME
        # Construção de um Banco de Dados apenas com as informações selecionadas
        st.subheader('Seleção de Dados para Exploração e Análise')
        st.write('* Selecione as colunas para construção de sua nova base de dados:')
        
#        # Option 01
# O      selecionados_opt1 = set()
# P      for k in df.columns:
# T          selecao = st.checkbox(f'{k}', False)
# I          if selecao:
# O              selecionados_opt1.add(k)
# N      #st.write(selecionados_opt1)
# 1      df2 = pd.DataFrame(df, columns=selecionados_opt1)
#        st.write(df2.head())
        
        # Option 02
        selecionados_opt2 = st.multiselect(
            'Selecione as colunas para construção de sua nova base de dados:', df.columns)
        #st.write('You selected:', selecionados_opt2)
        df2 = pd.DataFrame(df, columns = selecionados_opt2)
        st.write('Dados selecionados para análise:')
        st.write(df2.head())
        st.write(df2.dtypes)

        st.write('**.............................................................**')

        st.subheader('Estatística descritiva univariada')
        aux = pd.DataFrame({'colunas':df2.columns, 'tipos':df2.dtypes})
        colunas_numericas = list(aux[aux['tipos'] != 'object']['colunas'])
        colunas_object = list(aux[aux['tipos'] == 'object']['colunas'])
        colunas = list(df2.columns)
        col = st.selectbox('Selecione a coluna:', colunas_numericas)
        if col is not None:
            df3 = pd.DataFrame(df, columns = [col])
            st.table(df3.describe().transpose())
            #st.table(df[colunas_numericas].describe().transpose().loc[col])
            #st.write('**Média =**', df2[col].mean())
            #st.write('**Desvio padrão =**', df2[col].std())
            #st.write('**Mínimo/Máximo =**', df2[col].min(), '**/**', df2[col].max())
            #st.write('**1º/2º/3° quartil =**',
            #df2[col].quantile(0.25), '**/**',
            #df2[col].quantile(0.50), '**/**',
            #df2[col].quantile(0.75))
            #st.write('**Moda =**', df2[col].mode()[0])
            
            if df2[col].kurtosis() > 0:
                curtose = '*(Curtose* _**positiva**_*)* \n\n*Distribuição leptocúrtica - pico maior que a normal*'
            elif df2[col].kurtosis() < 0:
                curtose = '*(Curtose* _**negativa**_*)* \n\n*Distribuição platicúrtica - mais achatada em relação a normal*'
            else:
                curtose = '*(Distribuição normal)*'
            st.write('- *Curtose (Achatamento) =*', df2[col].kurtosis(), curtose)

            if df2[col].skew() > 0:
                assimetria = '*(Assimetria* _**positiva**_*)* \n\n*Perna a direita mais longa*'
            elif df2[col].skew() < 0:
                assimetria = '*(Assimetria* _**negativa**_*)* \n\n*Perna a esquerda mais longa*'
            else:
                assimetria = '*(Pernas simétricas)*'
            st.write('- *Assimetria =*', df2[col].skew(), assimetria)
        
        st.subheader('Visualização dos dados')
        st.markdown('Selecione a visualização')
        #
        histograma = st.checkbox('Histograma')
        if histograma:
            col_num = st.selectbox('Selecione a Coluna Numérica:', colunas_numericas, key='unique')
            st.markdown('Histograma da coluna:' + str(col_num))
            #st.write(criar_histograma(col_num, df2))
        #
        correlacao = st.checkbox('Correlação')
        if correlacao:
            st.write(criar_correlationplot(df2, colunas_numericas))

        st.subheader('Média da Pontuação de Crédito por Estado')
        st.table(df.groupby('estado_residencia')['pontuacao_credito'].mean())

if __name__ == '__main__':
    main()



def criar_histograma(coluna, df):
    chart = alt.Chart(df, width=600).mark_bar().encode(
        alt.X(coluna, bin=True),
        y='count()', tootip=[coluna, 'count()']
    ).interactive()
    return chart
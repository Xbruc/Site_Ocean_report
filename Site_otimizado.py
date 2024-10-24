
import streamlit as st
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px
import utm
from datetime import datetime
import calendar
import base64


imagem_path = '/Users/wesley.inovacao/Documents/Integra_dados_meteoceano/bercos.jpg'  # Substitua com o URL ou o caminho da sua imagem
imagem = st.image(imagem_path, use_column_width=True)


def carregar_imagem_base64(imagem_path):
    with open(imagem_path, "rb") as file:
        return base64.b64encode(file.read()).decode()

imagem_base64 = carregar_imagem_base64(imagem_path)

###################### CRIA ABAS DO SITE 
aba1, aba2 = st.tabs(["📊 Report", "🔍 Ensino"])
with aba1:
    ######################## GERA TAMPLATE DO SITE 
    logo_path = '/Users/wesley.inovacao/Documents/Integra_dados_meteoceano/logo_porto.png'
    st.sidebar.image(logo_path, use_column_width=True)

    st.title("OCEAN_REPORT")
    texto_justificado = """
    <div style='text-align: justify;'>
        O Porto do Itaqui é hub logístico comprometido não apenas com a eficiência operacional, mas também com o monitoramento das condições oceanográficas e meteorológicas. Este compromisso é evidenciado pela disponibilização de produtos observacionais e de modelagem. Nesse reporte, o Porto do Itaqui, stakeholders, pesquisadores e a comunidade em geral podem acessar os produtos de monitoramento. O Porto do Desenvolvimento promove uma gestão portuária sustentável e informada, que contribui para a segurança, eficiência e competitividade das operações portuárias.
    </div>
    """

    st.write(texto_justificado, unsafe_allow_html=True)

    st.sidebar.header(':blue[OCEAN_REPORT]', divider='blue')
    Dataset = st.sidebar.selectbox( 'Selecione o Dataset', ('Dados Observacionai')) #, 'Dados de Modelagem'))
    regiao = st.sidebar.selectbox( 'Baia', ('Baia de São Marcos'))
    variavel = st.sidebar.selectbox( 'Variáveis', ('Velocidade de Correntes', 'Batimetria', 'Marés', 'Granulometria', 'Meteorologia'))


    # ####################### CRIA DATA FRAME QUE DESCREVE AS ESTAÇÕES OCEANOGRÁFICAS 
    data = ({'lat': [570146.1, 570384.8, 569456, 569808.26, 569226.0, 569846.41, 570305.00],
            'lon': [9713875.8, 9711855.1, 9715527.3, 9714426.44, 9715805.3, 9715035, 9713825.00], 'Pontos': [1, 2, 3, 4, 5, 6, 8], 'Size': [8, 8, 8, 8, 8, 8, 8]})

    data = pd.DataFrame(data)
    data['lat'], data['lon'] = utm.to_latlon(data.lat, data.lon, 23, 'K')


    coord = ({'lat': [-2.324985, -2.342120, -2.343320, -2.345880, -2.355931, -2.32516, -2.302107, ],
            'lon': [-44.225178, -44.2238, -44.221977, -44.22298, -44.213013, -44.213299, -44.31534, ], 'Pontos': [1, 2, 3, 4, 5, 6, 7], 'Size': [8, 8, 8, 8, 8, 8, 8]})

    coord = pd.DataFrame(coord)

    ####################### DEFINE A FIGURA 
    fig_1 = px.scatter_mapbox(data, lat="lat", lon="lon", color='Pontos', size='Size',
                    color_continuous_scale=px.colors.cyclical.IceFire, size_max=8, zoom=12,
                    mapbox_style="open-street-map", hover_name="Pontos")
    fig_1.update_layout(
            title_text = 'Localização das estações oceanográficas', title_x=0.5,
            geo_scope='usa', font_color="black")


    fig = px.scatter_mapbox(coord, lat="lat", lon="lon", color='Pontos', size='Size',
                    color_continuous_scale=px.colors.cyclical.IceFire, size_max=12, zoom=10,
                    mapbox_style="open-street-map", hover_name="Pontos")
    fig.update_layout(
            title_text = 'Localização das estações oceanográficas', title_x=0.5,
            geo_scope='usa', font_color="black")

    ####################### GERA O MAPA DE LOCALIZAÇÃO DAS ESTAÇÕES 
    if Dataset == 'Dados Observacionai':
        if regiao == 'Baia de São Marcos':
            if variavel == 'Velocidade de Correntes':
                st.plotly_chart(fig_1, use_container_width=True)
            if variavel == 'Granulometria':
                st.plotly_chart(fig, use_container_width=True)

    # Função para filtrar os dados com base nas seleções
    def filtrar_por_estacao_mare(df, estacao_selecionada, mare_selecionada, ano_selecionado, mes_selecionado):
        # Filtrar com base nas seleções feitas
        filtro = df[
            (df['Station'] == estacao_selecionada) & 
            (df['Mare'] == mare_selecionada) & 
            (df['Time'].dt.year == ano_selecionado) & 
            (df['Time'].dt.month == mes_selecionado)
        ]
        return filtro

    def filtrar_BT(BT, ano_selecionado, mes_selecionado):
        # Filtrar com base nas seleções feitas
        filtro = BT[
            (BT['year_month_datetime'].dt.year == ano_selecionado) & 
            (BT['year_month_datetime'].dt.month == mes_selecionado)
        ]
        return filtro



    # Função para carregar os dados com cache para otimização
    @st.cache_data
    def carregar_dados():
        # Carregar os dados (substitua pelo caminho dos seus dados reais)
        df = pd.read_excel('/Users/wesley.inovacao/Documents/Integra_dados_meteoceano/corrente_porto_todos_pontos.xlsx')
        # Converter coluna de data para o formato datetime
        df['Time'] = pd.to_datetime(df['Time'])
        return df

    @st.cache_data
    def carregar_dados_Bt():
        # Carregar os dados (substitua pelo caminho dos seus dados reais)
        BT = pd.read_excel('/Users/wesley.inovacao/Documents/Integra_dados_meteoceano/Batimetria_22_23_r10.xlsx')
        return BT

    @st.cache_data
    def carregar_dados_MR():
        # Carregar os dados (substitua pelo caminho dos seus dados reais)
        MR = pd.read_excel('/Users/wesley.inovacao/Documents/Integra_dados_meteoceano/df_mare_hourly.xlsx')
        return MR

    @st.cache_data
    def carregar_dados_GR():
        # Carregar os dados (substitua pelo caminho dos seus dados reais)
        GR = pd.read_excel('/Users/wesley.inovacao/Documents/Integra_dados_meteoceano/Granolometria_14_23.xlsx')
        return GR

    @st.cache_data
    def carregar_dados_MT():
        # Carregar os dados (substitua pelo caminho dos seus dados reais)
        MT = pd.read_excel('/Users/wesley.inovacao/Documents/Integra_dados_meteoceano/Meteorologia_daily.xlsx')
        return MT

    # Função principal do Streamlit
    def app():
        if Dataset == 'Dados Observacionai':
            if regiao == 'Baia de São Marcos':
                if variavel == 'Velocidade de Correntes':
                    st.title("Datas das Campanhas Oceanográficas")
                    # Carregar os dados
                    df = carregar_dados()
                    table_data = []
                    for year in df['Time'].dt.year.unique():
                        # Iterate through unique stations
                        for station in df['Station'].unique():
                            # Iterate through unique mare types
                            for mare_type in df['Mare'].unique():
                                # Find the first date for each combination
                                first_date = df[(df['Time'].dt.year == year) & 
                                                (df['Station'] == station) & 
                                                (df['Mare'] == mare_type)]['Time'].min()

                                if pd.notna(first_date):
                                    table_data.append([station, mare_type, first_date])

                    # Create a DataFrame from the collected data
                    table_df = pd.DataFrame(table_data, columns=['Estação', 'Tipo de Maré', 'Data Inicial'])
                    table_df = table_df.set_index('Data Inicial')
                    st.write(table_df.T)

                    # Filtros interativos na barra lateral
                    st.sidebar.header("Filtros")
                    # Seleção de estação
                    estacao_selecionada = st.sidebar.selectbox("Selecione a Estação", df['Station'].unique())
                    # Seleção de maré
                    mare_selecionada = st.sidebar.selectbox("Selecione o Tipo de Maré", df['Mare'].unique())
                    # Seleção de ano com base nos anos presentes no DataFrame
                    ano_selecionado = st.sidebar.selectbox("Selecione o Ano", df['Time'].dt.year.unique())
                    # Seleção de mês com base nos meses disponíveis dentro do ano selecionado
                    meses_disponiveis = df[df['Time'].dt.year == ano_selecionado]['Time'].dt.month.unique()
                    mes_selecionado = st.sidebar.selectbox("Selecione o Mês", meses_disponiveis)
                    
                    # Filtrar os dados com base nas seleções
                    dados_filtrados = filtrar_por_estacao_mare(df, estacao_selecionada, mare_selecionada, ano_selecionado, mes_selecionado)
                    
                    # Verificar se há dados filtrados e mostrar o gráfico
                    if dados_filtrados.empty:
                        st.warning("Nenhum dado disponível para os filtros selecionados.")
                    else:
                        # Exibir o gráfico interativo usando Plotly
                        st.write(f"**Velocidade de Corrente no {estacao_selecionada}, {mare_selecionada}, {ano_selecionado}/{mes_selecionado}**")
                        
                        # Exibir gráfico usando Plotly
                        fig = px.scatter(
                            dados_filtrados,
                            x="Time",  # Assumindo que a coluna de tempo seja 'Time'
                            y="Depth",  # Assumindo que a coluna de velocidade seja 'Current_Speed'
                            color="Current_Speed",  # Para adicionar mais uma dimensão ao gráfico
                            color_continuous_scale="Portland",
                        )
                        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

                elif variavel == 'Batimetria':
                    # Carregar os dados
                    BT = carregar_dados_Bt()
                    
                    # Filtros interativos na barra lateral
                    #st.sidebar.header("Filtros")
                    # Seleção de ano com base nos anos presentes no DataFrame
                    # ano_selecionado = st.sidebar.selectbox("Selecione o Ano", BT['year_month_datetime'].dt.year.unique())
                    # Seleção de mês com base nos meses disponíveis dentro do ano selecionado
                    # meses_disponiveis = BT[BT['year_month_datetime'].dt.year == ano_selecionado]['year_month_datetime'].dt.month.unique()
                    # mes_selecionado = st.sidebar.selectbox("Selecione o Mês", meses_disponiveis)
                    
                    # Filtrar os dados com base nas seleções
                    # dados_filtrados = filtrar_BT(BT, ano_selecionado, mes_selecionado)
                    # Verificar se há dados filtrados e mostrar o gráfico
                    if BT.empty:
                        st.warning("Nenhum dado disponível para os filtros selecionados.")
                    else:
                        # Exibir o gráfico interativo usando Plotly
                        #st.write(f"**Batimetria dos Berços 99 a 108 no ano de {ano_selecionado}/{mes_selecionado}**")
                        
                        # Exibir gráfico usando Plotly
                        jet_scale = [   [0.0, 'rgb(0, 0, 255)'],  # Azul
                                        [0.2, 'rgb(0, 255, 255)'],  # Ciano
                                        [0.4, 'rgb(0, 255, 0)'],  # Verde
                                        [0.6, 'rgb(255, 255, 0)'],  # Amarelo
                                        [0.8, 'rgb(255, 165, 0)'],  # Laranja
                                        [1.0, 'rgb(255, 0, 0)']]  # Vermelho
                        fig = px.scatter_mapbox(
                        BT, lat="lat", lon="lon", color='z', size='z',
                        color_continuous_scale='Blues', size_max=5, zoom=12,
                        animation_frame="year_month" if "year_month" in BT.columns else None,
                        mapbox_style="open-street-map", hover_name="type"
                    )
                        fig.update_layout(
                            #title_text=f'{dados_filtrados["type"].iloc[0]}', title_x=0.5,
                            font_color="black", margin={"r":0,"t":0,"l":0,"b":0}
                        )
                        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                elif variavel == 'Marés':
                        MR = carregar_dados_MR()
                        # Create the plot
                        fig = go.Figure()
                        # Add the measured tide data with a specific color
                        fig.add_trace(go.Scatter(
                            x=MR['Data de leitura'],
                            y=MR['Maré medida (METRE)'],
                            mode='lines',
                            name='Maré medida (METRE)',
                            line=dict(color='black')))

                        # Add the predicted tide data with a different color
                        fig.add_trace(go.Scatter(
                            x=MR['Data de leitura'],
                            y=MR['Maré prevista (METRE)'],
                            mode='lines',
                            name='Maré prevista (METRE)',
                            line=dict(color='red')))

                        # Update the layout
                        fig.update_layout(
                            title='Maré medida vs Maré prevista - Berço 106',
                            xaxis_title='Data/Hora',
                            yaxis_title='Maré (metros)',
                            legend_title='Legenda',
                            xaxis=dict(
                            rangeselector=dict(
                            buttons=list([
                            dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                            dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                            dict(count=1,
                            label="YTD",
                            step="year",
                            stepmode="todate"),
                            dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                            dict(step="all")])),
                            rangeslider=dict(
                            visible=True),
                            type="date"))

                        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                        st.write("**O maregráfo está localizado no Berço 106, nas coordenadas 2°34'21.20''S  e  44°22'38''O**")

                elif variavel == 'Granulometria':
                    GR=carregar_dados_GR()
                    # Create a list of unique variable names (e.g., 'PM-01', 'PM-02', etc.)
                    variable_names = [col for col in GR.columns if col.startswith('Ponto')]
                    # Create a dropdown widget for selecting the variable
                    selected_variable = st.sidebar.selectbox("Select Variable", variable_names)

                    # Create the plot using Plotly Express
                    fig = px.bar(
                        GR,
                        x="Fração",
                        y=selected_variable,  # Use the selected variable for the y-axis
                        color="Fração",  # Assign different colors to each 'Fração'
                        animation_frame="Time" if "Time" in GR.columns else None,
                        labels={"Fração": "Fração granulométrica", selected_variable: "Value"},  # Customize labels
                        title="Distribuição Granulométrica")

                    # Customize the layout if needed
                    fig.update_layout(
                        xaxis_title="Fração granulométrica",
                        yaxis_title="Concentração (%)")
                    # Show the plot
                    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

                elif variavel == 'Meteorologia':
                    MT = carregar_dados_MT()
                    MT.set_index('Data')
                    # Create a list of available columns (for the dropdown filter)
                    available_columns = MT.columns.tolist()
                    available_columns.remove('Data') 
                    # Use streamlit to create a dropdown filter for selecting variables
                    colors = ["red", "blue", "green", "purple", "blue"]
                    selected_variable = st.selectbox("Select a variable", available_columns)
                    if selected_variable:
                        # Selecionar uma cor com base no índice da variável selecionada
                        color_index = available_columns.index(selected_variable) % len(colors)
                        selected_color = colors[color_index]
                        # Create the plot using plotly express
                        fig = px.line(MT, x=MT['Data'], y=selected_variable, title=f"Série Temporal de {selected_variable}")
                        fig.update_traces(line=dict(color=selected_color))
                        fig.update_layout(xaxis_title="Data", yaxis_title=selected_variable)
                        st.plotly_chart(fig)
                        
    # Executa a aplicação
    if __name__ == "__main__":
        app()

with aba2:

    # Exibindo o texto no Streamlit
    st.title("Complexo Estuarino de São Marcos")

    texto1 = """**Esta seção é dedicada aos entusiastas das ciências do mar e da atmosfera. Aqui, você encontra explicações sobre a dinâmica costeira do Complexo Estuarino de São Marcos (CESM).**

O Complexo Estuarino de São Marcos (CESM), localizado no estado do Maranhão, Brasil, está situado em uma área de transição climática entre o semiárido nordestino e a floresta amazônica. 
A região apresenta dois períodos climáticos distintos: uma estação chuvosa de janeiro a junho, e uma estação seca de agosto a dezembro, com uma precipitação média anual de 2.115 mm, influenciada pela Zona de Convergência Intertropical. 
O CESM recebe aportes fluviais principalmente da bacia do Mearim, além de contribuições de outras pequenas bacias. A descarga média anual de água doce é de 413 m³/s, com variações sazonais."""

# Exibir o texto formatado no Streamlit
    st.write(texto1)
    imagem_path = '/Users/wesley.inovacao/Documents/Integra_dados_meteoceano/Figura_1.png'  # Substitua com o URL ou o caminho da sua imagem
    imagem = st.image(imagem_path)

    texto2 = """
<p style='text-align: justify;'>
O rio Mearim exerce uma influência significativa nas correntes da Baía de São Marcos, especialmente nas proximidades do Porto do Itaqui. Suas descargas fluviais, principalmente durante a estação chuvosa, 
intensificam o regime hidrodinâmico da baía, criando um forte gradiente de salinidade e influenciando diretamente as correntes estuarinas. No Porto do Itaqui, essa interação entre as águas do rio, as marés e a geologia local resulta 
na formação de vórtices de correntes nas áreas adjacentes aos cais. Esses vórtices são gerados pela convergência de fluxos de maré com a corrente fluvial, criando zonas de circulação turbulenta 
nas bordas dos cais, que podem impactar a sedimentação, a erosão das margens e a manobrabilidade das embarcações. Um exemplo desses vórtices pode ser observado na figura abaixo.
</p>
"""

# Exibir o texto justificado no Streamlit
    st.markdown(texto2, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    # Caminhos dos vídeos
    video_1 = '/Users/wesley.inovacao/Documents/Integra_dados_meteoceano/Velocidade _Correntes_Ampliado.mp4'  # Substitua pelo caminho do seu primeiro vídeo
    video_2 = '/Users/wesley.inovacao/Documents/Integra_dados_meteoceano/Velocidade_Correntes_Local.mp4'  # Substitua pelo caminho do seu segundo vídeo
    # Carregar o primeiro vídeo na primeira coluna
    with col1:
        st.caption("### Velocidade de Correntes durante o mês de Outubro de 2016 - Menor resolução")
        st.video(video_1)

    # Carregar o segundo vídeo na segunda coluna
    with col2:
        st.caption("### Velocidade de Correntes durante o mês de Outubro de 2016 - Maior resolução")
        st.video(video_2)

    # Definir o texto corrigido
    texto3 = """
<p style='text-align: justify;'>
A Ilha de Guarapira desempenha um papel essencial na formação de vórtices anticiclônicos na Baía de São Marcos, especialmente nos berços 106 a 108 do Porto do Itaqui. 
Ao desviar as correntes de maré, a ilha cria zonas de baixa pressão que favorecem esses redemoinhos. De maneira geral, as ilhas interferem na hidrodinâmica local ao alterar a velocidade e a pressão das correntes, gerando vórtices. 
No caso de Guarapira, isso afeta tanto a circulação de água quanto a redistribuição de sedimentos e nutrientes, influenciando a erosão e a deposição no fundo marinho.
</p>
"""
# Exibir o texto justificado no Streamlit
    st.markdown(texto3, unsafe_allow_html=True)
    video_3 = '/Users/wesley.inovacao/Documents/Integra_dados_meteoceano/Velocidade_Corrente_de_mare_vazao_2024_10_18.mp4'  # Substitua pelo caminho do seu primeiro vídeo
    st.caption("### Vórtice anticiclônico formado na preamar em outubro de 2024.")
    st.video(video_3)

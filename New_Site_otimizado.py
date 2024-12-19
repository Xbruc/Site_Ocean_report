import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px
import utm
from datetime import datetime
#import calendar
import base64
import numpy as np
import matplotlib.pyplot as plt
import os 
st.set_page_config(layout="wide")

############################################## carrega imagens de cabeçalho #############################################################################

# Função para verificar e carregar uma imagem
def carregar_imagem(caminho, mensagem_erro, exibir_na_sidebar=False, use_column_width=True):
    """
    Carrega e exibe uma imagem no Streamlit.
    - caminho: Caminho da imagem
    - mensagem_erro: Mensagem de erro se a imagem não for encontrada
    - exibir_na_sidebar: Se True, exibe a imagem na barra lateral
    - use_column_width: Se True, ajusta a largura da imagem ao container
    """
    if os.path.exists(caminho):
        if exibir_na_sidebar:
            st.sidebar.image(caminho, use_column_width=use_column_width)
        else:
            st.image(caminho, use_column_width=use_column_width)
    else:
        if exibir_na_sidebar:
            st.sidebar.error(mensagem_erro)
        else:
            st.error(mensagem_erro)

# Função para carregar imagem em Base64
def carregar_imagem_base64(caminho):
    """
    Retorna uma string Base64 de uma imagem.
    - caminho: Caminho da imagem
    """
    if os.path.exists(caminho):
        with open(caminho, "rb") as file:
            return base64.b64encode(file.read()).decode()
    else:
        st.error(f"Erro: Arquivo '{caminho}' não encontrado")
        return None

# Define o diretório atual
diretorio_atual = os.getcwd()  # Use getcwd() ao invés de __file__ para maior compatibilidade

# Caminho da imagem principal
imagem_path = os.path.join(diretorio_atual, 'bercos.jpg')
carregar_imagem(imagem_path, f"Erro: Arquivo 'bercos.jpg' não encontrado em {imagem_path}")

# Caminho do logo
logo_path = os.path.join(diretorio_atual, 'logo_porto.png')
carregar_imagem(logo_path, f"Erro: Arquivo 'logo_porto.png' não encontrado em {logo_path}", exibir_na_sidebar=True)

# Carregar imagem em Base64 (caso necessário)
imagem_base64 = carregar_imagem_base64(imagem_path)

# Título do site
st.title("OCEAN_REPORT")

############################################# Cria abas do site, ex: Report, Ensino, Pesquisa #############################################################
aba1, aba2, aba3 = st.tabs(["📊 Report", "🔍 Pesquisa", "📚 Ensino"])
with aba1: ######################  ABA para Report 
    texto_justificado = """
    <div style='text-align: justify;'>
        O Porto do Itaqui é hub logístico comprometido não apenas com a eficiência operacional, mas também com o monitoramento das condições oceanográficas e meteorológicas. Este compromisso é evidenciado pela disponibilização de produtos observacionais e de modelagem. Nesse reporte, o Porto do Itaqui, stakeholders, pesquisadores e a comunidade em geral podem acessar os produtos de monitoramento. O Porto do Desenvolvimento promove uma gestão portuária sustentável e informada, que contribui para a segurança, eficiência e competitividade das operações portuárias.
    </div>
    """
    st.write(texto_justificado, unsafe_allow_html=True)
    ### Cria selectbox para especificar o caminho em que determinado dado está (FILTROS) 
    st.sidebar.header(':blue[OCEAN_REPORT]', divider='blue')
    Dataset = st.sidebar.selectbox( 'Selecione o Dataset', ('Dados Observacionai')) #, 'Dados de Modelagem'))
    regiao = st.sidebar.selectbox( 'Baia', ('Baia de São Marcos'))
    variavel = st.sidebar.selectbox( 'Variáveis', ('Velocidade de Correntes', 'Batimetria', 'Maré', 'Granulometria', 'Meteorologia',
                                                    'P. Físico-Químicos da Água', 'Material Orgânico da Água', 'Material Inorgânico da Água',
                                                    'Sedimentos Orgânicos', 'Sedimentos Inorgânicos'))


    ### Cria dataframe que contem a localização das estações oceanográficas  
    coord1 = ({'lat': [570146.1, 570384.8, 569456, 569808.26, 569226.0, 569846.41, 570305.00],
            'lon': [9713875.8, 9711855.1, 9715527.3, 9714426.44, 9715805.3, 9715035, 9713825.00], 'Estação': [1, 2, 3, 4, 5, 6, 8], 'Size': [8, 8, 8, 8, 8, 8, 8]})
    loc1 = pd.DataFrame(coord1)
    loc1['lat'], loc1['lon'] = utm.to_latlon(loc1.lat, loc1.lon, 23, 'K')

    coord2 = ({'lat': [-2.324985, -2.342120, -2.343320, -2.345880, -2.355931, -2.32516, -2.302107, ],
            'lon': [-44.225178, -44.2238, -44.221977, -44.22298, -44.213013, -44.213299, -44.31534, ], 'Estação': [1, 2, 3, 4, 5, 6, 7], 'Size': [8, 8, 8, 8, 8, 8, 8]})

    loc2 = pd.DataFrame(coord2)

    ### Define as figuras para plotar mapa da estações  
    loc1 = px.scatter_mapbox(loc1, lat="lat", lon="lon", color='Estação', size='Size',
                    color_continuous_scale=px.colors.cyclical.IceFire, size_max=8, zoom=12,
                    mapbox_style="open-street-map", hover_name="Estação")
    loc1.update_layout(
            title_text = 'Localização das estações oceanográficas', title_x=0.5,
            geo_scope='usa', font_color="black")

    loc2 = px.scatter_mapbox(loc2, lat="lat", lon="lon", color='Estação', size='Size',
                    color_continuous_scale=px.colors.cyclical.IceFire, size_max=12, zoom=10,
                    mapbox_style="open-street-map", hover_name="Estação")
    loc2.update_layout(
            title_text = 'Localização das estações oceanográficas', title_x=0.5,
            geo_scope='usa', font_color="black")

    # Função para carregar os dados com cache para otimização
    @st.cache_data
    def carregar_dados():
        # Carregar os dados (substitua pelo caminho dos seus dados reais)
        dados_corrente = pd.read_excel(os.path.join(diretorio_atual, 'corrente_porto_todos_pontos.xlsx'))
        # Converter coluna de data para o formato datetime
        dados_corrente['Time'] = pd.to_datetime(dados_corrente['Time'])
        return dados_corrente

    @st.cache_data
    def carregar_dados_Bt():
        # Carregar os dados (substitua pelo caminho dos seus dados reais)
        dados_batimetria = pd.read_excel(os.path.join(diretorio_atual, 'Batimetria_22_23_r10.xlsx'))
        return dados_batimetria

    @st.cache_data
    def carregar_dados_MR():
        # Carregar os dados (substitua pelo caminho dos seus dados reais)
        dados_mare = pd.read_excel(os.path.join(diretorio_atual, 'df_mare_hourly.xlsx'))
        return dados_mare

    @st.cache_data
    def carregar_dados_GR():
        # Carregar os dados (substitua pelo caminho dos seus dados reais)
        dados_granolometria = pd.read_excel(os.path.join(diretorio_atual, 'Granolometria_14_23.xlsx'))
        return dados_granolometria

    @st.cache_data
    def carregar_dados_MT():
        # Carregar os dados (substitua pelo caminho dos seus dados reais)
        dados_meteorologia = pd.read_excel(os.path.join(diretorio_atual, 'Meteorologia_daily.xlsx'))
        return dados_meteorologia

    @st.cache_data
    def carregar_dados_MT():
        # Carregar os dados (substitua pelo caminho dos seus dados reais)
        dados_p_fisico_quimicos = pd.read_excel(os.path.join(diretorio_atual, 'Parametros_fisico_quimicos.xlsx', engine="openpyxl", sheet_name='P_fisico_quimicos'))
        return dados_p_fisico_quimicos

    @st.cache_data
    def carregar_dados_MT():
        # Carregar os dados (substitua pelo caminho dos seus dados reais)
        dados_material_organico = pd.read_excel(os.path.join(diretorio_atual,  'Parametros_fisico_quimicos.xlsx', engine="openpyxl", sheet_name='Material_organico'))
        return dados_material_organico

    @st.cache_data
    def carregar_dados_MT():
        # Carregar os dados (substitua pelo caminho dos seus dados reais)
        dados_material_inorganico = pd.read_excel(os.path.join(diretorio_atual, 'Parametros_fisico_quimicos.xlsx', engine="openpyxl", sheet_name='Material_inorganico'))
        return dados_material_inorganico

    @st.cache_data
    def carregar_dados_MT():
        # Carregar os dados (substitua pelo caminho dos seus dados reais)
        dados_sedimento_organico = pd.read_excel(os.path.join(diretorio_atual, 'Parametros_fisico_quimicos.xlsx', engine="openpyxl", sheet_name='Sedimentos_Orgânicos'))
        return dados_sedimento_organico
        
    @st.cache_data
    def carregar_dados_MT():
        # Carregar os dados (substitua pelo caminho dos seus dados reais)
        dados_sedimento_inorganico = pd.read_excel(os.path.join(diretorio_atual, 'Parametros_fisico_quimicos.xlsx', engine="openpyxl", sheet_name='Sedimentos_Inorgânicos'))
        return dados_sedimento_inorganico

    # Função principal do Streamlit
    def app():
        if Dataset == 'Dados Observacionai':
            if regiao == 'Baia de São Marcos':
                if variavel == 'Velocidade de Correntes':
                    st.plotly_chart(loc1, use_container_width=True)
                    
                    st.sidebar.header("Filtros")

                    # Substituir valores ausentes por NaN explícito (não necessário, mas mantém claro)
                    dados_corrente["Current_Speed"] = dados_corrente["Current_Speed"].fillna(np.nan)

                    # Filtro da estação
                    estacao_selecionada = st.sidebar.selectbox("Selecione a Estação", dados_corrente["Station"].unique())

                    # Filtrar o DataFrame com base na estação selecionada
                    dados_filtrados_estacao = dados_corrente[dados_corrente["Station"] == estacao_selecionada]

                    # Filtro do tipo de maré disponível para a estação selecionada
                    tipos_mare_disponiveis = dados_filtrados_estacao["Mare"].unique()
                    mare_selecionada = st.sidebar.radio("Selecione o Tipo de Maré", tipos_mare_disponiveis)

                    # Filtrar o DataFrame com base na estação e no tipo de maré selecionados
                    dados_filtrados_mare = dados_filtrados_estacao[dados_filtrados_estacao["Mare"] == mare_selecionada]

                    # Filtrar as datas disponíveis para a estação e tipo de maré selecionados
                    datas_disponiveis = dados_filtrados_mare["Time"].dt.date.unique()
                    data_selecionada = st.sidebar.selectbox("Selecione a Data", datas_disponiveis)

                    # Aplicar todos os filtros no DataFrame
                    df_filtrado = dados_filtrados_mare[dados_filtrados_mare["Time"].dt.date == data_selecionada]

                    # Exibir o gráfico ou mensagem de aviso
                    if df_filtrado.empty:
                        st.warning("Nenhum dado disponível para os filtros selecionados.")
                    else:
                        st.write(f"**Velocidade de Corrente na {estacao_selecionada} - Maré: {mare_selecionada}**")
                        
                        # Dados válidos (não nulos)
                        dados_validos = df_filtrado.dropna(subset=["Current_Speed"])
                        
                        # Dados ausentes
                        dados_ausentes = df_filtrado[df_filtrado["Current_Speed"].isna()]
                        
                        # Configurar escala de cores
                        escala_cores = px.colors.sequential.Turbo
                        
                        # Gráfico para dados válidos
                        fig = px.scatter(
                            dados_validos,
                            x="Time",  # Coluna de tempo
                            y="Depth",  # Coluna de profundidade
                            color="Current_Speed",  # Para representar a velocidade da corrente
                            color_continuous_scale=escala_cores,  # Usa a escala de cores normal
                            labels={"Time": "Hora", "Depth": "Profundidade (m)", "Current_Speed": "Velocidade (m/s)"},
                        )
                        
                        # Adicionar camada para os valores ausentes (cor branca)
                        fig.add_scatter(
                            x=dados_ausentes["Time"],
                            y=dados_ausentes["Depth"],
                            mode="markers",
                            marker=dict(color="white", size=8, symbol="circle"),
                            name="Dados Ausentes",
                        )
                        
                        # Ajustar layout do gráfico
                        fig.update_layout(
                            title="Perfil da Velocidade de Corrente",
                            xaxis_title="Tempo",
                            yaxis_title="Profundidade (m)",
                            margin={"r": 0, "t": 40, "l": 0, "b": 0}
                        )
                        st.plotly_chart(fig, theme="streamlit", use_container_width=True)


                elif variavel == 'Batimetria':
                    if dados_batimetria.empty:
                        st.warning("Nenhum dado disponível para os filtros selecionados.")
                    else:
                        # Validar colunas necessárias
                        colunas_necessarias = {"lat", "lon", "z"}
                        if not colunas_necessarias.issubset(dados_batimetria.columns):
                            st.error("O conjunto de dados de batimetria está incompleto. Verifique as colunas.")
                        else:
                            # Garantir que year_month está no formato correto
                            if "year_month" in dados_batimetria.columns:
                                dados_batimetria["year_month"] = dados_batimetria["year_month"].astype(str)

                            # Exibir o gráfico
                            st.write("**Batimetria no Raio de 10m**")

                            fig = px.scatter_mapbox(
                                dados_batimetria,
                                lat="lat",
                                lon="lon",
                                color="z",
                                size="z",
                                color_continuous_scale="RdBu",
                                size_max=5,
                                zoom=12,
                                animation_frame="Data" if "Data" in dados_batimetria.columns else None,
                                mapbox_style="open-street-map",
                                hover_name="type",
                            )

                            # Layout do gráfico
                            fig.update_layout(
                                font_color="black",
                                margin={"r": 0, "t": 0, "l": 0, "b": 0}
                            )

                            # Renderizar o gráfico
                            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

                elif variavel == 'Maré':
                    
                    # Adicionar colunas auxiliares para mês, ano e nome do mês
                    dados_mare['mes'] = dados_mare['Data de leitura'].dt.month
                    dados_mare['ano'] = dados_mare['Data de leitura'].dt.year
                    dados_mare['mes_nome'] = dados_mare['Data de leitura'].dt.strftime('%B')  # Nome do mês

                    # Configuração do Streamlit
                    st.title("Visualização de Dados de Maré 🌊")
                    st.subheader("Marés Medidas e Previstas")

                    # Seletor de ano
                    ano_selecionado = st.selectbox(
                        "Selecione o ano:",
                        options=sorted(dados_mare['ano'].unique())
                    )

                    # Seletor de mês
                    mes_selecionado = st.selectbox(
                        "Selecione o mês:",
                        options=(dados_mare['mes_nome'].unique())
                    )
                    # Filtrar dados pelo mês e ano selecionados
                    dados_filtrados = dados_mare[
                        (dados_mare['ano'] == ano_selecionado) &
                        (dados_mare['mes_nome'] == mes_selecionado)
                    ]

                    # Verificar se há dados disponíveis
                    if dados_filtrados.empty:
                        st.warning("Não há dados disponíveis para o mês e ano selecionados.")
                    else:
                        # Ordenar os dados para garantir a progressão temporal
                        dados_filtrados = dados_filtrados.sort_values(by='Data de leitura')

                        # Criar uma lista de frames acumulativos
                        frames = []
                        for i in range(1, len(dados_filtrados) + 1):
                            frame_data = dados_filtrados.iloc[:i]
                            frames.append(
                                go.Frame(
                                    data=[
                                        go.Scatter(
                                            x=frame_data['Data de leitura'],
                                            y=frame_data['Maré medida (METRE)'],
                                            mode='lines',
                                            name='Maré medida',
                                            line=dict(color='blue')
                                        ),
                                        go.Scatter(
                                            x=frame_data['Data de leitura'],
                                            y=frame_data['Maré prevista (METRE)'],
                                            mode='lines',
                                            name='Maré prevista',
                                            line=dict(color='orange')
                                        ),
                                    ],
                                    name=str(frame_data['Data de leitura'].iloc[-1])
                                )
                            )

                        layout = go.Layout(
                        title=f"Marés Medidas e Previstas - {mes_selecionado} {ano_selecionado}",
                        xaxis=dict(title='Data'),
                        yaxis=dict(title='Nível de Maré (m)'),
                        updatemenus=[
                            dict(
                                type='buttons',
                                showactive=False,
                                buttons=[
                                    dict(
                                        label='Play',
                                        method='animate',
                                        args=[
                                            None,
                                            dict(frame=dict(duration=100, redraw=True), fromcurrent=True)
                                        ]
                                    ),
                                    dict(
                                        label='Pause',
                                        method='animate',
                                        args=[
                                            [None],
                                            dict(frame=dict(duration=2, redraw=True), fromcurrent=True)
                                        ]
                                    )
                                ]
                            )
                        ]
                    )

                    fig = go.Figure(
                        data=[
                            go.Scatter(
                                x=dados_filtrados['Data de leitura'],
                                y=dados_filtrados['Maré medida (METRE)'],
                                mode='lines',
                                name='Maré medida',
                                line=dict(color='blue')
                            ),
                            go.Scatter(
                                x=dados_filtrados['Data de leitura'],
                                y=dados_filtrados['Maré prevista (METRE)'],
                                mode='lines',
                                name='Maré prevista',
                                line=dict(color='orange')
                            )
                        ],
                        layout=layout,
                        frames=frames
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                elif variavel == 'Granulometria':
                    
                    # Create a list of unique variable names (e.g., 'PM-01', 'PM-02', etc.)
                    variable_names = [col for col in dados_granolometria.columns if col.startswith('Estação')]
                    # Create a dropdown widget for selecting the variable
                    selected_variable = st.sidebar.selectbox("Selecione a Variável", variable_names)

                    # Create the plot using Plotly Express
                    fig = px.bar(
                        dados_granolometria,
                        x="Fração",
                        y=selected_variable,  # Use the selected variable for the y-axis
                        color="Fração",  # Assign different colors to each 'Fração'
                        animation_frame="Time" if "Time" in dados_granolometria.columns else None,
                        labels={"Fração": "Fração granulométrica", selected_variable: "Value"},  # Customize labels
                        title="Distribuição Granulométrica")

                    # Customize the layout if needed
                    fig.update_layout(
                        xaxis_title="Fração granulométrica",
                        yaxis_title="Concentração (%)")
                    # Show the plot
                    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

                elif variavel == 'Meteorologia':
                   
                    # Título da aplicação
                    st.title("☀️🌧️ Condições do Tempo 🌬️🌡️")

                    df_clima = dados_meteorologia
                    # Seleção de data com um calendário
                    data_selecionada = st.date_input(
                        "Selecione a data para ver os detalhes:",
                        value=df_clima["Data"][0],
                        min_value=df_clima["Data"].min(),
                        max_value=df_clima["Data"].max()
                    )
                    data_selecionada = pd.Timestamp(data_selecionada)
                    # Verificar se a data está no intervalo
                    if data_selecionada not in df_clima['Data'].values:
                        st.error("Data selecionada não está no intervalo!")
                        st.stop()

                    # Filtrar os dados da data selecionada
                    dados_selecionados = df_clima[df_clima['Data'] == pd.Timestamp(data_selecionada)].iloc[0]

                    # Configurar gráficos lúdicos
                    fig = go.Figure()

                    # Adicionar temperatura
                    fig.add_trace(go.Indicator(
                        mode="gauge+number",
                        value=dados_selecionados['Temperatura (°C)'],
                        title={'text': "Temperatura (°C)"},
                        gauge={
                            'axis': {'range': [0, 50]},
                            'bar': {'color': "red"},
                            'steps': [
                                {'range': [0, 15], 'color': "lightblue"},
                                {'range': [15, 25], 'color': "lightgreen"},
                                {'range': [25, 35], 'color': "orange"},
                                {'range': [35, 50], 'color': "red"}
                            ],
                        },
                        domain={'x': [0.1, 0.4], 'y': [0.5, 0.9]}
                    ))

                    # Adicionar umidade
                    fig.add_trace(go.Indicator(
                        mode="gauge+number",
                        value=dados_selecionados['Umidade (%)'],
                        title={'text': "Umidade (%)"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "blue"},
                            'steps': [
                                {'range': [0, 30], 'color': "lightyellow"},
                                {'range': [30, 60], 'color': "lightgreen"},
                                {'range': [60, 100], 'color': "blue"}
                            ],
                        },
                        domain={'x': [0.6, 0.9], 'y': [0.5, 0.9]}
                    ))

                    # Adicionar velocidade do vento
                    fig.add_trace(go.Indicator(
                        mode="gauge+number",
                        value=dados_selecionados["Velocidade do Vento (m/s)"],
                        title={'text': "Velocidade do Vento (m/s)"},
                        gauge={
                            'axis': {'range': [0, 50]},
                            'bar': {'color': "purple"},
                            'steps': [
                                {'range': [0, 15], 'color': "lightgreen"},
                                {'range': [15, 30], 'color': "yellow"},
                                {'range': [30, 50], 'color': "red"}
                            ],
                        },
                        domain={'x': [0.3, 0.7], 'y': [0.0, 0.4]}
                    ))

                    # Layout do gráfico
                    fig.update_layout(
                        height=500,
                        width=800,
                        title_text=f"Condições do Tempo para {data_selecionada.strftime('%Y-%m-%d')}",
                        margin=dict(l=50, r=50, t=50, b=50)
                    )

                    # Exibir o gráfico
                    st.plotly_chart(fig)

                    # Mensagens divertidas
                    st.markdown(f"**🗓️ Data:** {data_selecionada.strftime('%Y-%m-%d')}")
                    st.markdown(f"**🌡️ Temperatura:** {dados_selecionados['Temperatura (°C)']:.1f}°C")
                    st.markdown(f"**💧 Umidade:** {dados_selecionados['Umidade (%)']:.1f}%")
                    st.markdown(f"**🌬️ Velocidade do Vento:** {dados_selecionados['Velocidade do Vento (m/s)']:.1f} m/s")

                    if dados_selecionados['Temperatura (°C)'] > 30:
                        st.markdown("🔥 **Está quente! Beba bastante água e evite o sol ao meio-dia!**")
                    elif dados_selecionados['Temperatura (°C)'] < 20:
                        st.markdown("❄️ **Fresco! Talvez você precise de um casaco leve.**")
                    else:
                        st.markdown("😊 **O clima está agradável. Aproveite o dia!**")
                    
                elif variavel == 'P. Físico-Químicos da Água':
                        # Criar o selectbox para selecionar a campanha
                    estacao_selecionada = st.sidebar.selectbox("Selecione a Campanha", dados_p_fisico_quimicos["Físico_Químicos"].unique())

                    # Filtrar o DataFrame com base na campanha selecionada
                    dados_filtrados = dados_p_fisico_quimicos[dados_p_fisico_quimicos["Físico_Químicos"] == estacao_selecionada]

                    # Transformar os dados para o formato longo usando `melt`
                    temp = dados_filtrados.melt(id_vars='Campanha', 
                                                var_name='Ponto', 
                                                value_name=f"{estacao_selecionada}")

                    # Plotar o gráfico de barras interativo
                    fig = px.bar(
                        temp,
                        x='Ponto',
                        y=f"{estacao_selecionada}",
                        color='Ponto',  # Cores distintas para cada ponto
                        animation_frame="Campanha" if "Campanha" in temp.columns else None,
                        labels=f"{estacao_selecionada}",
                        title= f"{estacao_selecionada}"
                    )

                    # Exibir o gráfico no Streamlit
                    st.plotly_chart(fig)

                elif variavel == 'Material Orgânico da Água':
                        # Criar o selectbox para selecionar a campanha
                    estacao_selecionada = st.sidebar.selectbox("Selecione a Campanha", dados_material_organico["Orgânicos"].unique())

                    # Filtrar o DataFrame com base na campanha selecionada
                    dados_filtrados = dados_material_organico[dados_material_organico["Orgânicos"] == estacao_selecionada]

                    # Transformar os dados para o formato longo usando `melt`
                    temp = dados_filtrados.melt(id_vars='Campanha', 
                                                var_name='Ponto', 
                                                value_name=f"{estacao_selecionada}")

                    # Plotar o gráfico de barras interativo
                    fig = px.bar(
                        temp,
                        x='Ponto',
                        y=f"{estacao_selecionada}",
                        color='Ponto',  # Cores distintas para cada ponto
                        animation_frame="Campanha" if "Campanha" in temp.columns else None,
                        labels=f"{estacao_selecionada}",
                        title= f"{estacao_selecionada}"
                    )
                    
                    st.plotly_chart(fig)

                elif variavel == 'Material Inorgânico da Água':
                        # Criar o selectbox para selecionar a campanha
                    estacao_selecionada = st.sidebar.selectbox("Selecione a Campanha", dados_material_inorganico["Inorgânicos"].unique())

                    # Filtrar o DataFrame com base na campanha selecionada
                    dados_filtrados = dados_material_inorganico[dados_material_inorganico["Inorgânicos"] == estacao_selecionada]

                    # Transformar os dados para o formato longo usando `melt`
                    temp = dados_filtrados.melt(id_vars='Campanha', 
                                                var_name='Ponto', 
                                                value_name=f"{estacao_selecionada}")

                    # Plotar o gráfico de barras interativo
                    fig = px.bar(
                        temp,
                        x='Ponto',
                        y=f"{estacao_selecionada}",
                        color='Ponto',  # Cores distintas para cada ponto
                        animation_frame="Campanha" if "Campanha" in temp.columns else None,
                        labels=f"{estacao_selecionada}",
                        title= f"{estacao_selecionada}"
                    )
                    
                    st.plotly_chart(fig)

                elif variavel == 'Sedimentos Orgânicos':
                        # Criar o selectbox para selecionar a campanha
                    estacao_selecionada = st.sidebar.selectbox("Selecione a Campanha", dados_sedimento_organico["Sedimentos_Organicos"].unique())

                    # Filtrar o DataFrame com base na campanha selecionada
                    dados_filtrados = dados_sedimento_organico[dados_sedimento_organico["Sedimentos_Organicos"] == estacao_selecionada]

                    # Transformar os dados para o formato longo usando `melt`
                    temp = dados_filtrados.melt(id_vars='Campanha', 
                                                var_name='Ponto', 
                                                value_name=f"{estacao_selecionada}")

                    # Plotar o gráfico de barras interativo
                    fig = px.bar(
                        temp,
                        x='Ponto',
                        y=f"{estacao_selecionada}",
                        color='Ponto',  # Cores distintas para cada ponto
                        animation_frame="Campanha" if "Campanha" in temp.columns else None,
                        labels=f"{estacao_selecionada}",
                        title= f"{estacao_selecionada}"
                    )

                    st.plotly_chart(fig)

                elif variavel == 'Sedimentos Inorgânicos':
                        # Criar o selectbox para selecionar a campanha
                    estacao_selecionada = st.sidebar.selectbox("Selecione a Campanha", dados_sedimento_inorganico["Sedimentos_Inorganicos"].unique())

                    # Filtrar o DataFrame com base na campanha selecionada
                    dados_filtrados = dados_sedimento_inorganico[dados_sedimento_inorganico["Sedimentos_Inorganicos"] == estacao_selecionada]

                    # Transformar os dados para o formato longo usando `melt`
                    temp = dados_filtrados.melt(id_vars='Campanha', 
                                                var_name='Ponto', 
                                                value_name=f"{estacao_selecionada}")

                    # Plotar o gráfico de barras interativo
                    fig = px.bar(
                        temp,
                        x='Ponto',
                        y=f"{estacao_selecionada}",
                        color='Ponto',  # Cores distintas para cada ponto
                        animation_frame="Campanha" if "Campanha" in temp.columns else None,
                        labels=f"{estacao_selecionada}",
                        title= f"{estacao_selecionada}"
                    )

                    st.plotly_chart(fig)

    # Executa a aplicação
    if __name__ == "__main__":
        app()

with aba2: ######################  ABA para Pesquisa

    st.title("Pesquisa Desenvolvimento e Inovação no Complexo Estuarino de São Marcos")
    
    Intro = """
    <div style='text-align: justify;'>
    O Porto do Itaqui, em parceria com a Fundação de Amparo à Pesquisa do Estado do Maranhão (FAPEMA), apoia projetos de Pesquisa, Desenvolvimento e Inovação (PD&I) voltados aos setores portuário, marítimo e logístico. Essa iniciativa fortalece vínculos com universidades e promove soluções inovadoras para os desafios do setor, além de estimular o desenvolvimento de produtos, processos e a capacitação de pessoas. O Porto financia e acompanha os projetos, oferecendo suporte aos pesquisadores, enquanto a FAPEMA é responsável pela gestão dos editais, concessão de bolsas e avaliação científica. A parceria também busca intensificar a relação Porto-Cidade e colaborar com os Objetivos de Desenvolvimento Sustentável (ODS) e o Plano Maranhão 2050, fomentando crescimento econômico, inovação, sustentabilidade e inclusão. Nesta página, apresentamos os resultados das pesquisas relacionadas à dinâmica do Complexo Estuarino da Baía de São Marcos (CEBS).
    </div>
    """
    st.write(Intro, unsafe_allow_html=True)

with aba3: ######################  ABA para Ensino 

    # Exibindo o texto no Streamlit
    st.title("Complexo Estuarino de São Marcos")

    texto1 = """**Esta seção é dedicada aos entusiastas das ciências do mar e da atmosfera. Aqui, você encontra explicações sobre a dinâmica costeira do Complexo Estuarino de São Marcos (CESM).**

O Complexo Estuarino de São Marcos (CESM), localizado no estado do Maranhão, Brasil, está situado em uma área de transição climática entre o semiárido nordestino e a floresta amazônica. 
A região apresenta dois períodos climáticos distintos: uma estação chuvosa de janeiro a junho, e uma estação seca de agosto a dezembro, com uma precipitação média anual de 2.115 mm, influenciada pela Zona de Convergência Intertropical. 
O CESM recebe aportes fluviais principalmente da bacia do Mearim, além de contribuições de outras pequenas bacias. A descarga média anual de água doce é de 413 m³/s, com variações sazonais."""

# Exibir o texto formatado no Streamlit
    st.write(texto1, unsafe_allow_html=True)
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


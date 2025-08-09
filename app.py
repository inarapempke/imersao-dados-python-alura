# Vamos importar as biblioteca dentro do nosso c[odigo]
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
# Define o título da página, o ícone e o layout para ocupar a largura inteira.
st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="📊",
    layout="wide",
)

# --- Carregamento dos dados ---
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

# Filtro de Ano
# Pegamos os "anos_disponiveis", nosso DataFrame, a coluna de "ano" e depois os valores únicos. O "sorted" vai organizar as informações para gente.
anos_disponiveis = sorted(df['ano'].unique())
# Aqui estamos colocando uma barra lateral com o "st.sidebar.multiselect" e a opção de selecionar cada um desses anos. Definimos essa opção como "Ano" e depois trouxemos os anos disponíveis.
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

# Filtro de Senioridade
# Pegamos os "senioridades_disponiveis", nosso DataFrame, a coluna de "ano" e depois os valores únicos. O "sorted" vai organizar as informações para gente.
senioridades_disponiveis = sorted(df['senioridade'].unique())
# Aqui estamos colocando uma barra lateral com o "st.sidebar.multiselect" e a opção de selecionar cada uma dessas senioridades. Definimos essa opção como "Senioridade" e depois trouxemos as senioridades disponíveis.
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

# Filtro por Tipo de Contrato
# Pegamos os "contratos_disponiveis", nosso DataFrame, a coluna de "contrato" e depois os valores únicos. O "sorted" vai organizar as informações para gente.
contratos_disponiveis = sorted(df['contrato'].unique())
# Aqui estamos colocando uma barra lateral com o "st.sidebar.multiselect" e a opção de selecionar cada um desses contratos. Definimos essa opção como "Tipo de Contrato" e depois trouxemos os contratos disponíveis.
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

# Filtro por Tamanho da Empresa
# Pegamos os "tamanhos_disponiveis", nosso DataFrame, a coluna de "tamanho_empresa" e depois os valores únicos. O "sorted" vai organizar as informações para gente.
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
# Aqui estamos colocando uma barra lateral com o "st.sidebar.multiselect" e a opção de selecionar cada um desses tamanhos de empresa. Definimos essa opção como "Tamanho da Empresa" e depois trouxemos os tamanhos disponíveis.
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

# --- Filtragem do DataFrame ---
# O dataframe principal é filtrado com base nas seleções feitas na barra lateral.
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(senioridades_selecionadas)) &
    (df['contrato'].isin(contratos_selecionados)) &
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
]

# --- Conteúdo Principal ---
# Aqui definimos o título do nosso Dashboard
st.title("🎲 Dashboard de Análise de Salários na Área de Dados")
# Aqui estamos colocando um texto explicativo / descrição de como o usuário deve utilizar esse Dashboard criado
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")

# --- Métricas Principais (KPIs) ---
st.subheader("Métricas gerais (Salário anual em USD)")

# Aqui adicionamos a lógica de "if" e "else" para dizer que, se o gráfico conseguir puxar os valores filtrados ele vai dar o resultado, mas caso ele não consiga ele retornará com o valor de "0, 0, 0"
if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado["cargo"].mode()[0]
else:
    salario_medio, salario_mediano, salario_maximo, total_registros, cargo_mais_comum = 0, 0, 0, ""

# Temos esses "col1, col2..." porque no "streamlit", a gente consegue dividir as informações em colunas dentro da página, sendo que cada coluna conterá uma métrica diferente.
col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown("---")

'''Da mesma forma que criamos métricas, separando em colunas, faremos a mesma coisa para os gráficos.
Então, podemos dividir um gráfico em duas colunas, depois fazer mais duas colunas, para ter a distribuição aparecendo corretamente nos gráficos na página.''' 


# --- Análises Visuais com Plotly ---
# Adicionando um subtítulo dentro do Dashboard
st.subheader("Gráficos")

# Começamos criando duas colunas para criar dois gráficos, um do lado do outro
col_graf1, col_graf2 = st.columns(2)

# O primeiro gráfico é do tipo de Barras, e ele traz o Top 10 Cargos por Salário Médio. Depois você pode filtrar essas informações e analisar por ano, por nível de experiência, etc.
with col_graf1:
    # Aqui estamos dizendo que se o nosso DF filtrado não estiver vazio, faremos um agrupamento por "salário médio" e pegaremos os 10 maiores salários e depois criaremos o gráficos de barras definindo todas informações do eixo X e Y, a orientação do gráfico.
    # Adicionamos a orientação do gráfico como "h" (horizontal), para ficar mais clara a visualização. Se fosse na vertical, era só não adicionar a orientação.
    # O ".nlargest(10)" pega os 10 maiores valores de "cargo" e "usd", ou seja, os maiores salários.
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='usd',
            y='cargo',
            orientation='h',
            title="Top 10 cargos por salário médio",
            labels={'usd': 'Média salarial anual (USD)', 'cargo': ''}
        )
        # O parâmetro ".update_layout(title_x=0.1)" serve para mover o título, não deixar ele tanto para a esquerda, mas mover ele um pouco para a direita.
        # Conforme você vai mexendo nesse valores, ele vai se deslocando mais.
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})

        # Para exibir o gráfico, nós utilizamos o "st.plotly_chart()" e utilizamos o parâmetro "use_container_width=True" também para exibir o gráfico
        st.plotly_chart(grafico_cargos, use_container_width=True)

        # Caso algum erro aconteça e o gráfico não seja gerado, exibiremos um aviso, o "st.warning()".
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")

# O segundo gráfico é do tipo de Histograma. Nós já tínhamos criado algo parecido, porém com o "seaborn", agora queremos fazer um gráfico interativo utilizando o "plotly".
# Esse gráfico trará a Distribuição de Salários Anuais.
with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='usd',
            nbins=30,
            title="Distribuição de salários anuais",
            labels={'usd': 'Faixa salarial (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    
    # Caso algum erro aconteça e o gráfico não seja gerado, exibiremos um aviso, o "st.warning()".
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

# Os gráficos 3 e 4 serão adicionados na linha de baixo
col_graf3, col_graf4 = st.columns(2)

# O terceiro gráfico será um gráfico de Rosca e ele trará a Proporção dos Tipos de Trabalho
with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)

        # Caso algum erro aconteça e o gráfico não seja gerado, exibiremos um aviso, o "st.warning()".
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

# O quarto gráfico seria a resposta do Desafio apresentado na Aula 03. Primeiro vamos criar esse gráfico lá no Colab.
# Os países que aparecem em Branco, são os que não temos dados.
with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
        grafico_paises = px.choropleth(media_ds_pais,
            locations='residencia_iso3',
            color='usd',
            color_continuous_scale='rdylgn',
            title='Salário médio de Cientista de Dados por país',
            labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")

# --- Tabela de Dados Detalhados ---
# Aqui trouxemos a tabela com os dados completos para caso alguém queira olhar a fundo, e também podemos filtrar alguma opção utilizano a lupa no lado superior direito da tabela.
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)

# Caso eu queira compartilhar o meu Dashboard com alguém, preciso colocar esse Dashboard em produção. Usaremos 2 ferramentas gratuitas:
# A primeira ferramenta será o GitHub, uma ferramenta muito importante para quem quer trabalhar com Data Science, Programação, porque é nela onde salvamos os códigos, gerenciamos versionamento. É nela que colocaremos o código online.
# Uma vez que o código estiver online, vamos utilizar o Streamlit (site), que vai colocar nosso site no ar.

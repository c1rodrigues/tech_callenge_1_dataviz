import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Títulos
st.write("# Tech-Challenge Expostação de Vinhos e Storytelling")

# importando dados
df_producao = pd.read_csv('ExpVinho22-Producao.csv', sep=';')
df_total = pd.read_csv('ExpVinho-Total.csv', sep=';')

# criando abas na aplicação
tab0, tab1, tab2, tab3, tab4 = st.tabs(['Exportação em Litros', 'Exportação em Dolares', 'Países Consumidores',
                                        'Fatores Econômicos', 'Conclusão'])

st.set_option('deprecation.showPyplotGlobalUse', False)

with tab0:
    # tratando os dados
    df_producao.reset_index(inplace=True)
    df_producao = df_producao.drop('index', axis=1)
    df_producao_usaveis = df_producao.set_index('País')
    df_producao_usaveis['Total'] = df_producao_usaveis.sum(axis=1)
    df_producao_usaveis = df_producao_usaveis.sort_values(by='Total', ascending=False)

    df_producao_outros = df_producao_usaveis.query('Total < 500000')
    total_outros = df_producao_outros.sum()
    total_outros = total_outros.to_frame().rename_axis('País')
    total_outros.rename(columns={0: 'Outros'}, inplace=True)
    total_outros = total_outros.T
    total_outros = total_outros.drop('Total', axis=1)

    df_producao_usaveis = df_producao_usaveis.query('Total >= 500000')
    df_producao_usaveis = df_producao_usaveis.drop('Total', axis=1)
    df_producao_usaveis = pd.concat([df_producao_usaveis, total_outros])

    st.write("# Valores Comercializados em Litros")
    df_producao_usaveis

    st.write('Para analisarmos melhor a evolução em cada país, podemos plotar um gráfico')
    fig = px.line(df_producao_usaveis.T, template='plotly_white')
    fig.update_layout(title="Evoluçaõ da Exportação",
                      xaxis_title=" ",
                      yaxis_title="Em Litros")
    st.plotly_chart(fig)

    """
    Podemos perceber dois picos de vendas para a Russia, sendo primeiro em 2009 e o segundo em 2013! A partir de 2015 vemos também um crescimento substancial por parte do Paraguai.
    Não menos importante, vale ressaltar que esses 11 países concentram 88,4% do total comercializado
    """

    st.write("# Concentração Total de Vendas")
    df_2 = pd.DataFrame(df_producao_usaveis.sum(axis=1), columns=['Total'])
    df_2.reset_index(inplace=True)
    df_2.rename(columns={'index': 'País'}, inplace=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_2['País'],
                         y=df_2['Total'],
                         name='Litros',
                         marker_color='rgb(26, 118, 255)'
                         ))
    fig.update_layout(
        title='Total vendido',
        yaxis=dict(
            title='Litros',
            titlefont_size=16,
            tickfont_size=14,
        ))
    st.plotly_chart(fig)

    '''
    Nesse gráfico vemos que a Russia e o Paraguai possuem o maior total de litros importados.
    Por outro lado, ao avaliarmos o gráfico a baixo vemos que esses dois países movimentam o total exportado em litros, sendo os outros países mais constantes!
    '''

    litros = df_producao_usaveis.sum(axis=0)
    litros = litros.to_frame()
    litros.reset_index(inplace=True)
    litros.rename(columns={'index': 'Ano', 0: 'Total'}, inplace=True)
    fig = px.line(litros, x='Ano', y='Total', template='plotly_white')
    st.plotly_chart(fig)

with tab1:
    # tratando dados
    df_total.reset_index(inplace=True)
    df_total.drop('index', axis=1, inplace=True)
    df_total.set_index('País', inplace=True)
    df_total['Total'] = df_total.sum(axis=1)
    df_total = df_total.sort_values(by='Total', ascending=False)
    df_total_usaveis = df_total.head(11)
    df_total_usaveis.drop('Total', axis=1, inplace=True)

    st.write("# Valores Comercializados em Dolares")
    df_total_usaveis

    """
    Esses 11 países representam 94,8% do total exportado em Dolares pelo Brasil!
    """

    st.write('Para analisarmos melhor a evolução em cada país, podemos plotar um gráfico')
    fig = px.line(df_total_usaveis.T, template='plotly_white')
    fig.update_layout(title="Evoluçaõ da Exportação",
                      xaxis_title=" ",
                      yaxis_title="Em Dolares")
    st.plotly_chart(fig)

    """
    Naturalmente pelo alto volumo importado, Russia e Paraguai representam grandes quantias importadas, e o restante dos países são mais constantes.
    """

    st.write("# Concentração Total de Vendas")

    df_1 = pd.DataFrame(df_total_usaveis.sum(axis=1), columns=['Total'])
    df_1.reset_index(inplace=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_1['País'],
                         y=df_1['Total'],
                         name='Dolares',
                         marker_color='rgb(55, 83, 109)'
                         ))
    fig.update_layout(
        title='Total vendido',
        yaxis=dict(
            title='Dolares',
            titlefont_size=16,
            tickfont_size=14,
        ))
    st.plotly_chart(fig)

    """
    Nesse momento, o Paraguai ultrapassa a Russia no total importado em dolares e movimenta de forma diferente
    a total exportado pelo Brasil em dolares! Estados Unidos e China permanecem em segundo e terceiro lugar respectivamente
    """

    dolares = df_total_usaveis.sum(axis=0)
    dolares = dolares.to_frame()
    dolares.reset_index(inplace=True)
    dolares.rename(columns={'index': 'Ano', 0: 'Total'}, inplace=True)
    fig = px.line(dolares, x='Ano', y='Total', template='plotly_white')
    st.plotly_chart(fig)

    st.write('# Comparação de exportação em Litros e Dolares')

    comparacao = pd.read_csv('Comparativo.csv', sep=';')
    comparacao.dropna(inplace=True)
    comparacao['Ano'] = comparacao['Ano'].astype(int).astype(str)
    comparacao.rename(columns={'Total Vendido por Ano': 'Total'}, inplace=True)

    df_dolar = comparacao[comparacao['Grupo'] == 'Dolares']
    df_litro = comparacao[comparacao['Grupo'] == 'Litros']

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_dolar['Ano'],
                         y=df_dolar['Total'],
                         name='Dolares',
                         marker_color='rgb(55, 83, 109)'
                         ))
    fig.add_trace(go.Bar(x=df_litro['Ano'],
                         y=df_litro['Total'],
                         name='Litros',
                         marker_color='rgb(26, 118, 255)'
                         ))

    fig.update_layout(
        title='Comparação Dolares / Litros',
        xaxis_tickfont_size=14,
        xaxis=dict(tickmode='array', tickvals=comparacao['Ano']),
        yaxis=dict(
            title='Comparação Dolares / Litros',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1
    )
    st.plotly_chart(fig)

with tab2:
    # tratando dados
    df_mundo = pd.read_excel('base_vinhos_mundo.xlsx')
    df_mundo['Year'] = df_mundo['Year'].fillna(0).astype(int)
    df_mundo = df_mundo[df_mundo['Region/Country'] != 'Global']
    df_vinho = df_mundo[df_mundo['Product'] == 'Wine']
    df_filtered_years = df_mundo[(df_mundo['Year'] >= 2008) & (df_mundo['Year'] <= 2022)]

    consumo_vinho = df_vinho[df_vinho['Variable'] == 'Consumption']
    grupo_consumo = consumo_vinho.groupby(['Region/Country', 'Year'])['Quantity'].sum().unstack(0)
    traducao_paises = {
        'Italy': 'Itália',
        'France': 'França',
        'United States of America': 'Estados Unidos da América',
        'Germany': 'Alemanha'
    }

    grupo_consumo = grupo_consumo.rename(columns=traducao_paises)
    top_5_consumo = grupo_consumo.sum().nlargest(5).index
    top_5_consumo = top_5_consumo.sort_values()
    df_3 = grupo_consumo[top_5_consumo].tail(15)

    """
    Para aprimorar nossa compreensão do mercado global e identificar possíveis destinos de exportação,
    buscamos os cinco principais países em termos de importação.

    Entre eles, pretendemos identificar potenciais mercados para nossos produtos.
    """

    st.write("# Cinco principais países Consumidores")
    fig = px.line(df_3, template='plotly_white')
    st.plotly_chart(fig)

    """
    Alemanha mantém um padrão de consumo de volume de vinho bastante constante,
    em contraste com os outros três países analisados, que mostram uma tendência de declínio. Enquanto isso, no caso dos EUA, 
    observamos um aumento acentuado no consumo de vinho.
    """

    importacao_vinho = df_vinho[df_vinho['Variable'] == 'Imports']
    grupo_importacao = importacao_vinho.groupby(['Region/Country', 'Year'])['Quantity'].sum().unstack(0)
    grupo_importacao = grupo_importacao.rename(columns=traducao_paises)
    df_5 = grupo_importacao[top_5_consumo]
    df_5 = df_5[13:28]

    fig = px.line(df_5, template='plotly_white')
    st.plotly_chart(fig)

    '''
    Entre os cinco principais países importadores de vinho, destacamos significativamente os EUA e a Alemanha.
    Ambas as nações são grandes importadoras de vinho, mas apresentam uma condição ainda mais notável do que os outros países quando analisamos o consumo e a produção.
    '''

    producao_vinho = df_vinho[df_vinho['Variable'] == 'Production']
    grupo_producao = producao_vinho.groupby(['Region/Country', 'Year'])['Quantity'].sum().unstack(0)
    grupo_producao = grupo_producao.rename(columns=traducao_paises)
    df_4 = grupo_producao[top_5_consumo]
    df_4 = df_4[13:28]

    fig = px.line(df_4, template='plotly_white')
    st.plotly_chart(fig)

    '''
    Além disso, outro ponto que os destaca como potenciais destinos de importação é a produção relativamente baixa e constante, 
    isso demonstra que, apesar da alta demanda, o mercado interno é insuficiente para suprir as necessidades domésticas.
    '''

with tab3:
    # tratando dados
    balanca = pd.read_csv('ISIC_ANUAL_EXP.csv', encoding='ISO-8859-1', sep=';')
    balanca['Agro'] = balanca['Agro'].str.replace(',', '.').astype(float)
    balanca['Ind.Extr.'] = balanca['Ind.Extr.'].str.replace(',', '.').astype(float)
    balanca['Ind.Transf.'] = balanca['Ind.Transf.'].str.replace(',', '.').astype(float)
    balanca['Outros'] = balanca['Outros'].str.replace(',', '.').astype(float)
    balanca['Total'] = balanca['Total'].str.replace(',', '.').astype(float)
    balanca.sort_values(by='Data', ascending=True, inplace=True)
    balanca['Data'] = balanca['Data'].apply(str)

    st.write("# Balança Comercial")

    lista = ['Agro', 'Ind.Extr.', 'Ind.Transf.', 'Outros', 'Total']
    fig = px.line(balanca, x='Data', y=lista, template='plotly_white')
    st.plotly_chart(fig)

    '''
    Podemos observar que na industria de transformação apresenta crescimento desde 2020, acompanhando o total os outros setores.
    Além disso, no acumulado dos 15 anos analisádos podemos observar crescimento de 31,45%! 
    '''

    # Tratando dados dolar
    # Dolar = pd.read_csv('Dolar.csv',  encoding ='ISO-8859-1',sep = ',')

    # st.write('#Cotação média dos últimos 15 anos')
    # fig = px.line(Dolar, x = 'Ano', y = 'Cotação', template='plotly_white')
    # st.plotly_chart(fig)

    '''
    Ao observarmos a evolução do Dolar comercial, podemos identificar que o saldo da balança comercial depende diretamente da cotação.
    Ou seja, uma valorização do Dolar frente ao Real favorece o saldo positívo, uma vez que aumenta as exportações (principalmente no setor das commodities) e de produtos
    que se relacionam ou dependem de mercadorias primárias.
    '''

    with tab4:
        '''
        Observando as informações aqui dispostas, e levando em consideração outros fatores como investimentos estatais no setor, crescimento e importancia dos Brics (25,5% do PIB mundial), 
        podemos concluir que os mercados mais promissores a serem explorados pela empresa são o mercado americano (Estados Unidos) e alemão.
        Ambos por estarem em crescimento no consumo e não possuírem produção que abasteça por completo a necessidade interna do país, criando assim a necessidade de importar o restante para satisfazer seus consumidores.
        '''
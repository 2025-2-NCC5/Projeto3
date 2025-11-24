from typing import List

from dash import dcc, html


def construir_layout(opcoes_canais: List[str], opcoes_lojas: List[str]) -> html.Div:
    return html.Div(
        className='pagina',
        children=[
            html.Header(
                className='cabecalho',
                children=[
                    html.Div(
                        [
                            html.Img(
                                src='/assets/logo-laranja.svg',
                                className='marca-logo',
                                alt='Foodlytics Dashboard',
                            ),
                            html.H1('Monitoramento operacional e estratégico'),
                            html.P('Visão unificada de pedidos, campanhas e alertas gerados automaticamente.'),
                        ]
                    )
                ],
            ),
            html.Section(
                className='painel-filtros',
                children=[
                    dcc.DatePickerRange(
                        id='filtro-periodo',
                        display_format='DD/MM/YYYY',
                        minimum_nights=0,
                        start_date_placeholder_text='Data inicial',
                        end_date_placeholder_text='Data final',
                    ),
                    dcc.Dropdown(
                        id='filtro-canais',
                        placeholder='Filtrar canais de venda',
                        multi=True,
                        options=[{'label': valor, 'value': valor} for valor in opcoes_canais],
                    ),
                    dcc.Dropdown(
                        id='filtro-lojas',
                        placeholder='Filtrar lojas',
                        multi=True,
                        options=[{'label': valor, 'value': valor} for valor in opcoes_lojas],
                    ),
                    html.Div(
                        className='botoes-exportacao',
                        children=[
                            html.Button('Exportar pedidos (CSV)', id='botao-exportar-pedidos'),
                            html.Button('Exportar campanhas (Excel)', id='botao-exportar-campanhas'),
                        ],
                    ),
                    dcc.Download(id='download-pedidos'),
                    dcc.Download(id='download-campanhas'),
                ],
            ),
            html.Section(
                className='grade-kpi',
                children=[
                    html.Div([html.P('Receita total'), html.H2(id='kpi-receita')], className='cartao-kpi'),
                    html.Div([html.P('Pedidos'), html.H2(id='kpi-pedidos')], className='cartao-kpi'),
                    html.Div([html.P('Ticket médio'), html.H2(id='kpi-ticket')], className='cartao-kpi'),
                    html.Div([html.P('Cancelamentos'), html.H2(id='kpi-cancelamento')], className='cartao-kpi'),
                    html.Div([html.P('Tempo médio de preparo'), html.H2(id='kpi-preparo')], className='cartao-kpi'),
                    html.Div([html.P('Satisfação média'), html.H2(id='kpi-satisfacao')], className='cartao-kpi'),
                ],
            ),
            html.Section(
                className='grade-graficos',
                children=[
                    dcc.Graph(id='grafico-receita'),
                    dcc.Graph(id='grafico-canais'),
                    dcc.Graph(id='grafico-lojas'),
                    dcc.Graph(id='grafico-satisfacao'),
                ],
            ),
            html.Section(
                className='painel-insights',
                children=[
                    html.Div(
                        className='cartao-insight',
                        children=[
                            html.H3('Alertas dinâmicos'),
                            html.Ul(id='lista-alertas'),
                            html.Button('Ver mais alertas', id='botao-alertas', n_clicks=0, className='botao-link'),
                        ],
                    ),
                    html.Div(
                        className='cartao-insight',
                        children=[
                            html.H3('Sugestões automáticas'),
                            html.Ul(id='lista-sugestoes'),
                        ],
                    ),
                ],
            ),
        ],
    )




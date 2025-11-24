from __future__ import annotations

import base64
from typing import List, Optional

import pandas as pd
from dash import Input, Output, State, callback_context, html, no_update

from src.servicos.exportacao import gerar_csv_pedidos, gerar_excel_campanhas
from src.servicos.indicadores import (
    FiltrosPainel,
    calcular_resumo_pedidos,
    gerar_alertas_variacao,
    gerar_desempenho_lojas,
    gerar_distribuicao_canais,
    gerar_satisfacao_lojas,
    gerar_serie_receita,
    gerar_sugestoes,
)


def _converter_data(valor: Optional[str]) -> Optional[pd.Timestamp]:
    if valor is None:
        return None
    return pd.to_datetime(valor)


def _criar_filtros(
    start: Optional[str],
    end: Optional[str],
    canais: Optional[List[str]],
    lojas: Optional[List[str]],
) -> FiltrosPainel:
    return FiltrosPainel(
        data_inicial=_converter_data(start),
        data_final=_converter_data(end),
        canais=canais,
        tipos_campanha=None,
        lojas=lojas,
    )


def _formata_moeda(valor: float) -> str:
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def registrar_callbacks(aplicacao):
    @aplicacao.callback(
        Output('kpi-receita', 'children'),
        Output('kpi-pedidos', 'children'),
        Output('kpi-ticket', 'children'),
        Output('kpi-cancelamento', 'children'),
        Output('kpi-preparo', 'children'),
        Output('kpi-satisfacao', 'children'),
        Output('grafico-receita', 'figure'),
        Output('grafico-canais', 'figure'),
        Output('grafico-lojas', 'figure'),
        Output('grafico-satisfacao', 'figure'),
        Output('lista-alertas', 'children'),
        Output('botao-alertas', 'children'),
        Output('lista-sugestoes', 'children'),
        Input('filtro-periodo', 'start_date'),
        Input('filtro-periodo', 'end_date'),
        Input('filtro-canais', 'value'),
        Input('filtro-lojas', 'value'),
        Input('botao-alertas', 'n_clicks'),
    )
    def atualizar_paineis(start_date, end_date, canais, lojas, n_clicks_alertas):
        filtros = _criar_filtros(start_date, end_date, canais, lojas)
        resumo = calcular_resumo_pedidos(filtros)
        grafico_receita = gerar_serie_receita(filtros)
        grafico_canais = gerar_distribuicao_canais(filtros)
        grafico_lojas = gerar_desempenho_lojas(filtros)
        grafico_satisfacao = gerar_satisfacao_lojas(filtros)

        alertas_completos = gerar_alertas_variacao(filtros)
        mostrar_todos = bool(n_clicks_alertas and n_clicks_alertas % 2 == 1)
        limite_alertas = 3
        if len(alertas_completos) > limite_alertas:
            if mostrar_todos:
                alertas_visiveis = alertas_completos
                texto_botao_alertas = 'Ver menos alertas'
            else:
                alertas_visiveis = alertas_completos[:limite_alertas]
                texto_botao_alertas = f"Ver mais alertas ({len(alertas_completos) - limite_alertas})"
        else:
            alertas_visiveis = alertas_completos
            texto_botao_alertas = 'Todos os alertas exibidos'

        alertas = [html.Li(texto) for texto in alertas_visiveis]
        sugestoes = [html.Li(texto) for texto in gerar_sugestoes(filtros)]

        satisfacao = resumo.get('satisfacao_media', 0) or 0
        tempo_preparo = resumo.get('tempo_medio_preparo', 0) or 0

        return (
            _formata_moeda(resumo['total_receita']),
            f"{resumo['total_pedidos']:,}".replace(',', '.'),
            _formata_moeda(resumo['ticket_medio']),
            f"{resumo['taxa_cancelamento']:.1f}%",
            f"{tempo_preparo:.0f} min",
            f"{satisfacao:.1f} / 5",
            grafico_receita,
            grafico_canais,
            grafico_lojas,
            grafico_satisfacao,
            alertas,
            texto_botao_alertas,
            sugestoes,
        )

    @aplicacao.callback(
        Output('download-pedidos', 'data'),
        Output('download-campanhas', 'data'),
        Input('botao-exportar-pedidos', 'n_clicks'),
        Input('botao-exportar-campanhas', 'n_clicks'),
        State('filtro-periodo', 'start_date'),
        State('filtro-periodo', 'end_date'),
        State('filtro-canais', 'value'),
        State('filtro-lojas', 'value'),
        prevent_initial_call=True,
    )
    def exportar_relatorios(n_csv, n_excel, start_date, end_date, canais, lojas):
        filtros = _criar_filtros(start_date, end_date, canais, lojas)
        disparo = callback_context.triggered
        if not disparo:
            return no_update, no_update
        prop_id = disparo[0]['prop_id']

        if prop_id.startswith('botao-exportar-pedidos'):
            conteudo = gerar_csv_pedidos(filtros)
            return (
                dict(content=conteudo.decode('utf-8'), filename='relatorio_pedidos.csv', type='text/csv'),
                no_update,
            )
        if prop_id.startswith('botao-exportar-campanhas'):
            conteudo = gerar_excel_campanhas(filtros)
            base64_bytes = base64.b64encode(conteudo).decode('utf-8')
            return (
                no_update,
                dict(
                    content=base64_bytes,
                    filename='relatorio_campanhas.xlsx',
                    type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    base64=True,
                ),
            )
        return no_update, no_update

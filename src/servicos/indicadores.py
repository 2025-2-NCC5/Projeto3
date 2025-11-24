from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from src.dados.carga_dados import carregar_campanhas, carregar_pedidos


@dataclass
class FiltrosPainel:
    data_inicial: Optional[pd.Timestamp]
    data_final: Optional[pd.Timestamp]
    canais: Optional[Iterable[str]]
    tipos_campanha: Optional[Iterable[str]]
    lojas: Optional[Iterable[str]]


COLORIR_CANAIS = {
    'APP': '#F97316',
    'WEB': '#55392B',
    'EPADOCA': '#FF6D38',
    '99FOOD': '#55312B',
    'WHATSAPP': '#25D366',
}


def _aplicar_filtros_pedidos(base: pd.DataFrame, filtros: FiltrosPainel) -> pd.DataFrame:
    dados = base.copy()
    if filtros.data_inicial is not None:
        dados = dados[dados['createdAt'] >= filtros.data_inicial]
    if filtros.data_final is not None:
        dados = dados[dados['createdAt'] <= filtros.data_final]
    if filtros.canais:
        dados = dados[dados['salesChannel'].isin(filtros.canais)]
    if filtros.lojas:
        dados = dados[dados['storeName'].isin(filtros.lojas)]
    return dados


def _aplicar_filtros_campanhas(base: pd.DataFrame, filtros: FiltrosPainel) -> pd.DataFrame:
    dados = base.copy()
    if filtros.tipos_campanha:
        dados = dados[dados['badge'].isin(filtros.tipos_campanha)]
    return dados


def filtrar_pedidos(filtros: FiltrosPainel) -> pd.DataFrame:
    return _aplicar_filtros_pedidos(carregar_pedidos(), filtros)


def filtrar_campanhas(filtros: FiltrosPainel) -> pd.DataFrame:
    return _aplicar_filtros_campanhas(carregar_campanhas(), filtros)


def _grafico_vazio(titulo: str, tipo: str = 'line'):
    grafico = getattr(px, tipo)(title=titulo)
    grafico.update_layout(margin=dict(l=20, r=20, t=50, b=30))
    return grafico


def _serie_receita_diaria(pedidos: pd.DataFrame) -> pd.DataFrame:
    if pedidos.empty:
        return pd.DataFrame(columns=['data', 'receita'])
    serie = (
        pedidos.groupby(pedidos['createdAt'].dt.date)['totalAmount']
        .sum()
        .rename_axis('data')
        .reset_index(name='receita')
    )
    serie['data'] = pd.to_datetime(serie['data'])
    return serie


def calcular_resumo_pedidos(filtros: FiltrosPainel) -> Dict[str, float]:
    pedidos = filtrar_pedidos(filtros)
    if pedidos.empty:
        return {chave: 0 for chave in (
            'total_receita',
            'total_pedidos',
            'ticket_medio',
            'taxa_cancelamento',
            'tempo_medio_preparo',
            'satisfacao_media',
        )}

    total_pedidos = len(pedidos)
    total_receita = pedidos['totalAmount'].sum()
    ticket_medio = total_receita / total_pedidos if total_pedidos else 0
    cancelados = (pedidos['statusLegivel'] == 'Cancelado').sum()
    taxa_cancelamento = cancelados / total_pedidos * 100

    preparo = pedidos.get('preparationTime')
    tempo_medio_preparo = float(preparo.mean()) if preparo is not None else 0

    avaliacao = pedidos.get('rating')
    satisfacao_media = float(avaliacao.dropna().mean()) if avaliacao is not None else 0

    return {
        'total_receita': float(total_receita),
        'total_pedidos': int(total_pedidos),
        'ticket_medio': float(ticket_medio),
        'taxa_cancelamento': float(taxa_cancelamento),
        'tempo_medio_preparo': tempo_medio_preparo,
        'satisfacao_media': satisfacao_media,
    }


def gerar_serie_receita(filtros: FiltrosPainel):
    serie = _serie_receita_diaria(filtrar_pedidos(filtros))
    if serie.empty:
        return _grafico_vazio('Sem dados para o período selecionado', 'line')

    figura = px.line(serie, x='data', y='receita', title='Receita diária')
    figura.update_traces(line_color='#FF6D38')
    figura.update_layout(margin=dict(l=20, r=20, t=50, b=30))
    return figura


def gerar_distribuicao_canais(filtros: FiltrosPainel):
    pedidos = filtrar_pedidos(filtros)
    if pedidos.empty:
        return _grafico_vazio('Sem pedidos para exibir', 'bar')

    distribuicao = (
        pedidos.groupby('salesChannel', as_index=False)['totalAmount']
        .sum()
        .rename(columns={'totalAmount': 'receita'})
        .sort_values('receita', ascending=False)
    )
    figura = px.bar(
        distribuicao,
        x='salesChannel',
        y='receita',
        title='Receita por canal',
        color='salesChannel',
        color_discrete_map=COLORIR_CANAIS,
    )
    figura.update_layout(showlegend=False, margin=dict(l=20, r=20, t=50, b=30))
    return figura


def gerar_desempenho_lojas(filtros: FiltrosPainel):
    pedidos = filtrar_pedidos(filtros)
    if pedidos.empty:
        return _grafico_vazio('Sem pedidos por loja para exibir', 'bar')

    resumo = (
        pedidos.groupby('storeName', as_index=False)
        .agg(receita=('totalAmount', 'sum'), pedidos=('id', 'count'))
        .assign(ticket=lambda df: df['receita'] / df['pedidos'])
        .sort_values('receita', ascending=False)
    )
    texto_pedidos = resumo['pedidos'].map(lambda valor: f"{valor:,}".replace(',', '.') + ' pedidos')
    maximo_receita = float(resumo['receita'].max()) if not resumo.empty else 0
    limite_direita = maximo_receita * 1.25 if maximo_receita else 0

    figura = px.bar(
        resumo,
        x='receita',
        y='storeName',
        orientation='h',
        title='Receita por loja',
        color='receita',
        color_continuous_scale=['#FFE5D5', '#FF6D38'],
        text=texto_pedidos,
        hover_data={'ticket': ':.2f'},
    )
    figura.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=20, r=40, t=60, b=40),
        xaxis=dict(automargin=True),
        yaxis=dict(automargin=True),
    )
    figura.update_traces(textposition='outside', cliponaxis=False)
    if limite_direita:
        figura.update_xaxes(range=[0, limite_direita])
    figura.update_yaxes(title='Loja')
    figura.update_xaxes(title='Receita (R$)')
    return figura


def gerar_satisfacao_lojas(filtros: FiltrosPainel):
    pedidos = filtrar_pedidos(filtros)
    if 'rating' not in pedidos or pedidos['rating'].dropna().empty:
        return _grafico_vazio('Sem avaliações registradas', 'bar')

    avaliacao = (
        pedidos.dropna(subset=['rating'])
        .groupby('storeName', as_index=False)
        .agg(media=('rating', 'mean'), volume=('id', 'count'))
        .sort_values('media', ascending=False)
    )

    figura = px.bar(
        avaliacao,
        x='storeName',
        y='media',
        color='volume',
        title='Satisfação média por loja',
        text=avaliacao['media'].round(2),
        color_continuous_scale=['#D1FAE5', '#16A34A'],
    )
    figura.update_layout(
        margin=dict(l=20, r=20, t=60, b=30),
        yaxis_title='Média de estrelas',
        xaxis_title='Loja',
        coloraxis_colorbar_title='Pedidos',
    )
    figura.update_traces(textposition='outside')
    return figura


def _detectar_anomalias_receita(serie: pd.DataFrame) -> pd.DataFrame:
    if len(serie) < 5:
        return serie.iloc[0:0]

    modelo = IsolationForest(contamination=0.12, random_state=42)
    previsoes = modelo.fit_predict(serie[['receita']])
    return serie[previsoes == -1]


def gerar_alertas_variacao(filtros: FiltrosPainel) -> List[str]:
    serie = _serie_receita_diaria(filtrar_pedidos(filtros))
    if serie.empty:
        return ['Sem dados suficientes para detectar anomalias.']

    anomalias = _detectar_anomalias_receita(serie)
    if anomalias.empty:
        return ['Nenhuma anomalia identificada pelo IsolationForest.']

    mediana = float(serie['receita'].median())
    alertas: List[str] = []
    for _, linha in anomalias.sort_values('data', ascending=False).iterrows():
        data_formatada = linha['data'].strftime('%d/%m/%Y')
        receita = float(linha['receita'])
        if receita >= mediana:
            alertas.append(
                f'{data_formatada}: receita fora do padrão (R$ {receita:,.2f}) e acima da mediana. Replique o que funcionou no dia.'
            )
        else:
            alertas.append(
                f'{data_formatada}: queda atípica de receita (R$ {receita:,.2f}). Revise estoques e campanhas ativas.'
            )
    return alertas[:5]


def _resumir_lojas_para_modelo(pedidos: pd.DataFrame) -> pd.DataFrame:
    if pedidos.empty:
        return pd.DataFrame()

    resumo = (
        pedidos.groupby('storeName', as_index=False)
        .agg(
            receita=('totalAmount', 'sum'),
            pedidos=('id', 'count'),
            cancelamentos=('statusLegivel', lambda serie: (serie == 'Cancelado').sum()),
            satisfacao=('rating', 'mean'),
        )
    )
    resumo['ticket'] = (resumo['receita'] / resumo['pedidos']).fillna(0)
    resumo['taxa_cancel'] = (resumo['cancelamentos'] / resumo['pedidos']).fillna(0)
    resumo['satisfacao'] = resumo['satisfacao'].fillna(0)
    return resumo[['storeName', 'receita', 'pedidos', 'ticket', 'taxa_cancel', 'satisfacao']]


def _segmentar_lojas(resumo: pd.DataFrame) -> pd.DataFrame:
    if len(resumo) < 2:
        return resumo

    k = min(4, max(2, len(resumo)))
    recursos = resumo[['receita', 'ticket', 'taxa_cancel', 'satisfacao']]
    matriz = StandardScaler().fit_transform(recursos)
    modelo = KMeans(n_clusters=k, n_init=10, random_state=42)
    resumo = resumo.copy()
    resumo['cluster'] = modelo.fit_predict(matriz)
    return resumo


def _sugestoes_por_cluster(resumo_segmentado: pd.DataFrame) -> List[str]:
    if 'cluster' not in resumo_segmentado:
        return []

    metricas = resumo_segmentado.groupby('cluster').agg(
        receita_media=('receita', 'mean'),
        cancel_media=('taxa_cancel', 'mean'),
        satisfacao_media=('satisfacao', 'mean'),
    )

    sugestoes: List[str] = []
    cluster_top = metricas['receita_media'].idxmax()
    lojas_top = resumo_segmentado.loc[resumo_segmentado['cluster'] == cluster_top, 'storeName']
    if not lojas_top.empty:
        sugestoes.append(
            f"Lojas {', '.join(lojas_top)} lideram receita. Documente as rotinas delas e compartilhe com o restante da rede."
        )

    cluster_risco = metricas['receita_media'].idxmin()
    if cluster_risco != cluster_top:
        lojas_risco = resumo_segmentado.loc[resumo_segmentado['cluster'] == cluster_risco, 'storeName']
        sugestoes.append(
            f"Lojas {', '.join(lojas_risco)} estão com receita baixa. Revise cardápio, estoque e escala para identificar gargalos."
        )

    cluster_cancel = metricas['cancel_media'].idxmax()
    lojas_cancel = (
        resumo_segmentado[resumo_segmentado['cluster'] == cluster_cancel]
        .sort_values('taxa_cancel', ascending=False)['storeName']
        .head(3)
    )
    if not lojas_cancel.empty and cluster_cancel not in {cluster_top, cluster_risco}:
        sugestoes.append(
            f"Cancelamentos elevados em {', '.join(lojas_cancel)}. Reforce conferência de pedidos e informe tempos com clareza."
        )

    cluster_satisf = metricas['satisfacao_media'].idxmin()
    lojas_satisf = (
        resumo_segmentado[resumo_segmentado['cluster'] == cluster_satisf]
        .sort_values('satisfacao')['storeName']
        .head(3)
    )
    if not lojas_satisf.empty:
        sugestoes.append(
            f"Satisfação baixa em {', '.join(lojas_satisf)}. Colete feedback dos clientes e trate os principais motivos."
        )

    return sugestoes


def _sugestoes_por_metricas(resumo: pd.DataFrame) -> List[str]:
    sugestoes: List[str] = []
    if resumo.empty:
        return sugestoes

    destaque = resumo.loc[resumo['satisfacao'].idxmax()]
    sugestoes.append(
        f"{destaque['storeName']} mantém satisfação média de {destaque['satisfacao']:.1f}. Replique o atendimento e processos dela."
    )

    abaixo_mediana = resumo.sort_values('ticket').head(1)
    mediana_ticket = float(resumo['ticket'].median())
    if not abaixo_mediana.empty and abaixo_mediana['ticket'].iat[0] < mediana_ticket:
        loja = abaixo_mediana.iloc[0]
        sugestoes.append(
            f"Ticket médio da loja {loja['storeName']} está abaixo da mediana. Ajuste preços, combos ou itens sugeridos."
        )

    return sugestoes


def gerar_sugestoes(filtros: FiltrosPainel) -> List[str]:
    pedidos = filtrar_pedidos(filtros)
    sugestoes: List[str] = []

    resumo_lojas = _resumir_lojas_para_modelo(pedidos)
    if not resumo_lojas.empty:
        segmentado = _segmentar_lojas(resumo_lojas)
        sugestoes.extend(_sugestoes_por_cluster(segmentado))
        sugestoes.extend(_sugestoes_por_metricas(resumo_lojas))

    if not pedidos.empty:
        receita_por_canal = pedidos.groupby('salesChannel')['totalAmount'].sum()
        if not receita_por_canal.empty:
            canal_top = receita_por_canal.idxmax()
            sugestoes.append(
                f'O canal {canal_top} concentrou a maior receita no período. Priorize monitoramento e ações nele.'
            )

    return sugestoes or ['Sem sugestões geradas pelo modelo neste período.']

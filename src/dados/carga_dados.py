from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Dict, Tuple

import pandas as pd

BASE_DADOS = Path(__file__).resolve().parents[2] / 'dados' / 'brutos'

MAPEAMENTO_STATUS_CAMPANHA = {
    '1': 'Rascunho',
    '2': 'Cancelada',
    '3': 'Publicada',
    '4': 'Concluida',
}

MAPEAMENTO_TIPO_CAMPANHA = {
    '1': 'Promocional',
    '2': 'Institucional',
}

MAPEAMENTO_STATUS_FILA = {
    '1': 'Agendada',
    '2': 'Enviada',
    '3': 'Recebida',
    '4': 'Lida',
    '5': 'Removida',
    '6': 'Pendente',
}

MAPEAMENTO_STATUS_CLIENTE = {
    '1': 'Ativo',
    '2': 'Inativo',
}

MAPEAMENTO_STATUS_PEDIDO = {
    'PENDING': 'Pendente',
    'PLACED': 'Registrado',
    'CONFIRMED': 'Confirmado',
    'DISPATCHED': 'Despachado',
    'CONCLUDED': 'Concluido',
    'CANCELED': 'Cancelado',
}


def _ler_csv(nome_arquivo: str) -> pd.DataFrame:
    caminho = BASE_DADOS / nome_arquivo
    if not caminho.exists():
        raise FileNotFoundError(f'Arquivo {caminho} nao encontrado')

    return pd.read_csv(
        caminho,
        sep=';',
        dtype=str,
        encoding='utf-8',
        engine='python',
    )


def _converter_para_data(coluna: pd.Series) -> pd.Series:
    return pd.to_datetime(coluna, dayfirst=True, errors='coerce')


def _ajustar_numero(texto: str) -> str:
    texto = texto.strip()
    if not texto:
        return ''
    if ',' in texto and '.' in texto:
        texto = texto.replace('.', '').replace(',', '.')
    elif ',' in texto:
        texto = texto.replace('.', '').replace(',', '.')
    else:
        texto = texto.replace(' ', '')
    return texto


def _converter_para_numero(coluna: pd.Series) -> pd.Series:
    return pd.to_numeric(coluna.fillna('').map(_ajustar_numero), errors='coerce')


@lru_cache
def carregar_campanhas() -> pd.DataFrame:
    dados = _ler_csv('Campaign_semicolon.csv')
    for campo in ('createdAt', 'updatedAt'):
        dados[campo] = _converter_para_data(dados[campo])
    dados['statusLegivel'] = dados['status'].map(MAPEAMENTO_STATUS_CAMPANHA).fillna(dados['status'])
    dados['tipoLegivel'] = dados['type'].map(MAPEAMENTO_TIPO_CAMPANHA).fillna(dados['type'])
    return dados


@lru_cache
def carregar_fila_campanhas() -> pd.DataFrame:
    dados = _ler_csv('CampaignQueue_semicolon.csv')
    dados['scheduledAt'] = _converter_para_data(dados['scheduledAt'])
    dados['sendAt'] = _converter_para_data(dados['sendAt'])
    dados['createdAt'] = _converter_para_data(dados['createdAt'])
    dados['updatedAt'] = _converter_para_data(dados['updatedAt'])
    dados['statusLegivel'] = dados['status'].map(MAPEAMENTO_STATUS_FILA).fillna(dados['status'])
    return dados


@lru_cache
def carregar_clientes() -> pd.DataFrame:
    dados = _ler_csv('Customer_semicolon.csv')
    for campo in ('enrichedAt', 'createdAt', 'updatedAt', 'dateOfBirth'):
        dados[campo] = _converter_para_data(dados[campo])
    dados['statusLegivel'] = dados['status'].map(MAPEAMENTO_STATUS_CLIENTE).fillna(dados['status'])
    return dados


@lru_cache
def carregar_pedidos() -> pd.DataFrame:
    dados = _ler_csv('Order_semicolon.csv')
    for campo in ('createdAt', 'updatedAt', 'scheduledAt'):
        dados[campo] = _converter_para_data(dados[campo])
    dados['totalAmount'] = _converter_para_numero(dados['totalAmount'])
    dados['preparationTime'] = _converter_para_numero(dados['preparationTime'])
    dados['takeOutTimeInSeconds'] = _converter_para_numero(dados['takeOutTimeInSeconds'])
    if 'rating' in dados.columns:
        dados['rating'] = _converter_para_numero(dados['rating'])
    dados['statusLegivel'] = dados['status'].map(MAPEAMENTO_STATUS_PEDIDO).fillna(dados['status'])
    return dados


def carregar_conjuntos() -> Dict[str, pd.DataFrame]:
    return {
        'campanhas': carregar_campanhas(),
        'fila_campanhas': carregar_fila_campanhas(),
        'clientes': carregar_clientes(),
        'pedidos': carregar_pedidos(),
    }

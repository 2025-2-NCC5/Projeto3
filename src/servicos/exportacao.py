from __future__ import annotations

import io

import pandas as pd

from src.servicos.indicadores import FiltrosPainel, filtrar_campanhas, filtrar_pedidos


def gerar_csv_pedidos(filtros: FiltrosPainel) -> bytes:
    pedidos = filtrar_pedidos(filtros)
    colunas = [
        'id',
        'companyId',
        'createdAt',
        'salesChannel',
        'orderType',
        'status',
        'totalAmount',
    ]
    csv_buffer = io.StringIO()
    pedidos[colunas].to_csv(csv_buffer, sep=';', index=False)
    return csv_buffer.getvalue().encode('utf-8')


def gerar_excel_campanhas(filtros: FiltrosPainel) -> bytes:
    campanhas = filtrar_campanhas(filtros)
    colunas = ['id', 'storeId', 'badge', 'type', 'status', 'createdAt']
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        campanhas[colunas].to_excel(writer, index=False, sheet_name='Campanhas')
    return excel_buffer.getvalue()

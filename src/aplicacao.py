from __future__ import annotations

from pathlib import Path

from dash import Dash

from src.dados.carga_dados import carregar_pedidos
from src.layout.callbacks import registrar_callbacks
from src.layout.componentes import construir_layout

GOOGLE_FONTS = 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'
ASSETS_PASTA = Path(__file__).resolve().parents[1] / 'assets'
FAVICON_ARQUIVO = ASSETS_PASTA / 'favicon.ico'


def _obter_opcoes() -> tuple[list[str], list[str]]:
    pedidos = carregar_pedidos()
    canais = sorted(pedidos['salesChannel'].dropna().unique())
    lojas = sorted(pedidos['storeName'].dropna().unique())
    return canais, lojas


def criar_aplicacao() -> Dash:
    canais, lojas = _obter_opcoes()
    app = Dash(
        __name__,
        suppress_callback_exceptions=True,
        title='Foodlytics Dashboard',
        external_stylesheets=[GOOGLE_FONTS],
        assets_folder=str(ASSETS_PASTA),
    )
    if FAVICON_ARQUIVO.exists():
        app._favicon = str(FAVICON_ARQUIVO)
    app.layout = construir_layout(canais, lojas)
    registrar_callbacks(app)
    return app


aplicacao = criar_aplicacao()
servidor = aplicacao.server

if __name__ == '__main__':
    aplicacao.run_server(debug=True)


from __future__ import annotations

import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker

BASE_PASTA = Path(__file__).resolve().parents[1] / 'dados' / 'brutos'
FAKE = Faker('pt_BR')
random.seed(42)
np.random.seed(42)

LOJAS = [
    {'companyId': 'LXK0A1', 'nome': 'Cantina Liberdade', 'cidade': 'Sao Paulo', 'canal_forte': 'APP', 'ticket_base': 42, 'satisfacao_media': 3.3, 'preparo_medio': 28},
    {'companyId': 'ZP930B', 'nome': 'Boteco Paulista', 'cidade': 'Sao Paulo', 'canal_forte': 'WEB', 'ticket_base': 55, 'satisfacao_media': 3.2, 'preparo_medio': 22},
    {'companyId': 'QW77C2', 'nome': 'Padaria Vila Nova', 'cidade': 'Campinas', 'canal_forte': 'EPADOCA', 'ticket_base': 31, 'satisfacao_media': 3.8, 'preparo_medio': 18},
    {'companyId': 'MN55D3', 'nome': 'Delivery do Centro', 'cidade': 'Rio de Janeiro', 'canal_forte': '99FOOD', 'ticket_base': 70, 'satisfacao_media': 3.1, 'preparo_medio': 30},
    {'companyId': 'AJ81E4', 'nome': 'Cantina Horizonte', 'cidade': 'Belo Horizonte', 'canal_forte': 'APP', 'ticket_base': 45, 'satisfacao_media': 3.6, 'preparo_medio': 26},
    {'companyId': 'BV62F5', 'nome': 'Restaurante Mar Azul', 'cidade': 'Salvador', 'canal_forte': '99FOOD', 'ticket_base': 90, 'satisfacao_media': 4.0, 'preparo_medio': 38},
    {'companyId': 'CP53G6', 'nome': 'Emporio Serra Verde', 'cidade': 'Curitiba', 'canal_forte': 'WEB', 'ticket_base': 98, 'satisfacao_media': 4.4, 'preparo_medio': 24},
    {'companyId': 'DQ44H7', 'nome': 'Sabores do Norte', 'cidade': 'Manaus', 'canal_forte': 'WHATSAPP', 'ticket_base': 62, 'satisfacao_media': 3.0, 'preparo_medio': 27},
    {'companyId': 'ER35J8', 'nome': 'Pizza do Porto', 'cidade': 'Porto Alegre', 'canal_forte': 'APP', 'ticket_base': 78, 'satisfacao_media': 3.7, 'preparo_medio': 35},
    {'companyId': 'FS26K9', 'nome': 'Casa do Chef Recife', 'cidade': 'Recife', 'canal_forte': 'WEB', 'ticket_base': 84, 'satisfacao_media': 3.9, 'preparo_medio': 33},
]
CANAIS = ['APP', 'WEB', 'EPADOCA', '99FOOD', 'WHATSAPP']
BADGES = ['loyalty', 'winback', 'delivery', 'migration']
STATUS_PEDIDO = ['CONCLUDED', 'CANCELED', 'DISPATCHED', 'PENDING']


def _escolher_canal(loja: dict) -> str:
    pesos = {canal: 1 for canal in CANAIS}
    pesos[loja['canal_forte']] = 3
    return random.choices(list(pesos.keys()), weights=list(pesos.values()))[0]


def gerar_pedidos(qtd: int = 500) -> pd.DataFrame:
    registros = []
    inicio = datetime(2025, 1, 1)
    for i in range(qtd):
        loja = random.choice(LOJAS)
        data = inicio + timedelta(days=random.randint(0, 120))
        canal = _escolher_canal(loja)
        base_ticket = loja.get('ticket_base', 65)
        desvio = max(5, base_ticket * 0.18)
        valor = float(np.clip(np.random.normal(base_ticket, desvio), 30, 100))
        nota_base = loja.get('satisfacao_media', 3.5)
        nota = float(np.clip(np.random.normal(nota_base, 0.25), 2.9, 4.5))
        preparo_base = loja.get('preparo_medio', 28)
        preparo = float(np.clip(np.random.normal(preparo_base, max(3, preparo_base * 0.2)), 10, 60))
        status = random.choices(STATUS_PEDIDO, weights=[0.65, 0.1, 0.15, 0.1])[0]
        registros.append(
            {
                'id': str(i + 1),
                'companyId': loja['companyId'],
                'storeName': loja['nome'],
                'storeCity': loja['cidade'],
                'containerId': FAKE.bothify(text='??????'),
                'createdAt': data.strftime('%d/%m/%Y %H:%M'),
                'customer': random.randint(1, 999),
                'displayId': FAKE.bothify(text='??##??'),
                'engineId': FAKE.bothify(text='######'),
                'engineName': 'DirectOrder',
                'engineType': 'POS',
                'extraInfo': FAKE.sentence(),
                'integrated': random.choice(['True', 'False']),
                'integrationId': random.randint(1000, 9999),
                'isTest': 'False',
                'orderTiming': random.choice(['IMMEDIATE', 'SCHEDULED']),
                'orderType': random.choice(['DELIVERY', 'INDOOR', 'TAKEOUT']),
                'salesChannel': canal,
                'scheduledAt': '',
                'status': status,
                'preparationTime': int(preparo),
                'takeOutTimeInSeconds': int(abs(np.random.normal(1200, 200))),
                'totalAmount': f'{valor:.2f}'.replace('.', ','),
                'rating': f'{nota:.1f}',
                'updatedAt': (data + timedelta(hours=2)).strftime('%d/%m/%Y %H:%M'),
                'version': 'v2.0.0',
            }
        )
    return pd.DataFrame(registros)


def gerar_clientes(qtd: int = 250) -> pd.DataFrame:
    registros = []
    for i in range(qtd):
        genero = random.choice(['M', 'F'])
        nascimento = FAKE.date_of_birth(minimum_age=18, maximum_age=70)
        registros.append(
            {
                'id': str(i + 1),
                'name': FAKE.name_male() if genero == 'M' else FAKE.name_female(),
                'taxId': FAKE.cpf() if genero == 'M' else FAKE.cnpj(),
                'gender': genero,
                'dateOfBirth': nascimento.strftime('%d/%m/%Y'),
                'status': random.choice(['1', '2']),
                'externalCode': '',
                'isEnriched': random.choice(['True', 'False']),
                'enrichedAt': '',
                'enrichedBy': '',
                'createdAt': FAKE.date_this_year(before_today=True, after_today=False).strftime('%d/%m/%Y %H:%M'),
                'createdBy': FAKE.user_name(),
                'updatedAt': '',
                'updatedBy': '',
                'phone': FAKE.msisdn(),
                'email': FAKE.email(),
            }
        )
    return pd.DataFrame(registros)


def gerar_campanhas(qtd: int = 90) -> pd.DataFrame:
    registros = []
    for i in range(qtd):
        data = FAKE.date_time_between(start_date='-180d', end_date='-5d')
        registros.append(
            {
                'id': str(i + 1),
                'segmentId': str(random.randint(1, 5)),
                'templateId': str(random.randint(1, 5)),
                'storeId': random.choice(LOJAS)['companyId'],
                'name': f'Campanha {FAKE.word().title()} {FAKE.bothify(text="??").upper()}',
                'description': FAKE.sentence(),
                'badge': random.choice(BADGES),
                'type': random.choice(['1', '2']),
                'status': random.choice(['1', '2', '3', '4']),
                'isDefault': random.choice(['True', 'False']),
                'createdAt': data.strftime('%Y-%m-%d %H:%M:%S'),
                'createdBy': FAKE.user_name(),
                'updatedAt': (data + timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S'),
                'updatedBy': FAKE.user_name(),
            }
        )
    return pd.DataFrame(registros)


def gerar_fila_campanhas(qtd: int = 220) -> pd.DataFrame:
    registros = []
    for i in range(qtd):
        campanha_id = random.randint(1, 90)
        agendado = FAKE.date_time_between(start_date='-90d', end_date='now')
        enviado = agendado + timedelta(minutes=random.randint(5, 60))
        status = random.choice(['1', '2', '3', '4', '5', '6'])
        registros.append(
            {
                'id': str(i + 1),
                'jobId': str(random.randint(1, 500)),
                'campaignId': campanha_id,
                'storeId': random.choice(LOJAS)['companyId'],
                'storeInstanceId': FAKE.bothify(text='########'),
                'customerId': random.randint(1, 250),
                'phoneNumber': FAKE.msisdn(),
                'scheduledAt': agendado.strftime('%d/%m/%Y %H:%M'),
                'sendAt': enviado.strftime('%d/%m/%Y %H:%M'),
                'status': status,
                'message': FAKE.sentence(),
                'response': '' if random.random() > 0.3 else FAKE.sentence(),
                'createdAt': (agendado - timedelta(hours=1)).strftime('%d/%m/%Y %H:%M'),
                'createdBy': FAKE.user_name(),
                'updatedAt': enviado.strftime('%d/%m/%Y %H:%M'),
                'updatedBy': FAKE.user_name(),
            }
        )
    return pd.DataFrame(registros)


def salvar(df: pd.DataFrame, nome: str):
    destino = BASE_PASTA / nome
    destino.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(destino, sep=';', index=False)
    print(f'Arquivo salvo: {destino}')


def main():
    salvar(gerar_pedidos(), 'Order_semicolon.csv')
    salvar(gerar_clientes(), 'Customer_semicolon.csv')
    salvar(gerar_campanhas(), 'Campaign_semicolon.csv')
    salvar(gerar_fila_campanhas(), 'CampaignQueue_semicolon.csv')


if __name__ == '__main__':
    main()



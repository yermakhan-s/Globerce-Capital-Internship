import asyncio

import aiohttp
import requests
import uplink
from uplink import Path

from config import settings
from fdc.client import FDCConsumer
from core.clent import CollectionCoreConsumer


async def update_credit(
        client: CollectionCoreConsumer,
        *,
        token: str,
        external_id: Path
):
    await client.update_daily(external_id=external_id, token=token)


async def main(loop):
    """Логика для исключения расхождения по задолженности и истории платежей
        1. Получаем все внешние идентификаторы кредитного соглашение из 1с.
        2. Запускаем цикл по всему кредитному соглашению. Внутри цикла отправляем
           запрос на обновление задолженности и истории платежей в collections_core.
    """
    session = requests.Session()
    session.verify = False

    # 1-шаг
    fdc_consumer = FDCConsumer(
        base_url=settings.URL_1C,
        auth=(settings.USERNAME_1C, settings.PASSWORD_1C),
        client=session
    )
    statements = fdc_consumer.get_statements(
            resp_format="json",
            filter_query="DeletionMark eq false"
        )["value"]

    len_statements = len(statements)
    step = 100 if len_statements > 100 else 1

    core_consumer = CollectionCoreConsumer(
        base_url=settings.COLLECTIONS_CORE_URL,
        client=uplink.AiohttpClient(connector=aiohttp.TCPConnector(ssl=False))
    )
    for i in range(0, len_statements, step):
        print(i, i+step)
        futures = [
            update_credit(
                core_consumer,
                token=settings.COLLECTION_CORE_TOKEN,
                external_id=statement["ДоговорЗайма"]) for statement in statements[i:i+step]
        ]
        await asyncio.gather(*futures)

event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main(event_loop))

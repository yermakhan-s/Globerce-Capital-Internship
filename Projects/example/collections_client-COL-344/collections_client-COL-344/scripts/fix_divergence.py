# import asyncio
# from typing import List, Union, Dict
#
# import aiohttp
# import requests
# import uplink
# import redis
# import json
#
# from uplink import Path
#
# from collections_client.config.config import settings
#
# from core.core_clent import CollectionCoreConsumer
# from fdc.odata_client import FDCOdataConsumer
#
#
# async def update_credit(
#         client: CollectionCoreConsumer,
#         *,
#         token: str,
#         external_id: Path
# ):
#     await client.update_daily(external_id=external_id, token=token)
#
#
# async def bipolar(
#         core_consumer: CollectionCoreConsumer,
#         statements: List[Union[str, Dict]],
#         is_cache: bool,
#         i: int,
#         step: int
# ):
#     if is_cache:
#         return [
#             update_credit(
#                 core_consumer,
#                 token=settings.COLLECTION_CORE_TOKEN,
#                 external_id=statement) for statement in statements[i:i + step]
#         ]
#     return [
#         update_credit(
#             core_consumer,
#             token=settings.COLLECTION_CORE_TOKEN,
#             external_id=statement["ДоговорЗайма"]) for statement in statements[i:i + step]
#     ]
#
#
# async def main(loop):
#     """Логика для исключения расхождения по задолженности и истории платежей
#         1. Получаем все внешние идентификаторы кредитного соглашение из 1с.
#            Получаем данные из исковых заявлений.
#         2. Запускаем цикл по всему кредитному соглашению. Внутри цикла отправляем
#            запрос на обновление задолженности и истории платежей в collections_core.
#     """
#     session = requests.Session()
#     session.verify = False
#
#     # 1-шаг
#     fdc_consumer = FDCOdataConsumer(
#         base_url=settings.URL_1C,
#         auth=(settings.USERNAME_1C, settings.PASSWORD_1C),
#         client=session
#     )
#     #  caching
#     r = redis.Redis()
#
#     is_cache = False
#
#     if r.exists("statements"):
#         statements = r.get("statements")
#         statements = json.loads(statements)
#         is_cache = True
#     else:
#         statements = fdc_consumer.get_statements(
#             resp_format="json",
#             filter_query="DeletionMark eq false")["value"]
#         cache_list = []
#         for i in statements:
#             cache_list.append(i["ДоговорЗайма"])
#         r.setex("statements", settings.EXP_TIME, json.dumps(cache_list))
#
#     r.close()
#
#     len_statements = len(statements)
#     step = 100 if len_statements > 100 else 1
#     # 2 - шаг
#     core_consumer = CollectionCoreConsumer(
#         base_url=settings.COLLECTIONS_CORE_URL,
#         client=uplink.AiohttpClient(connector=aiohttp.TCPConnector(ssl=False))
#     )
#
#     for i in range(0, len_statements, step):
#         print(i, i + step)
#         futures = await bipolar(core_consumer, statements, is_cache, i, step)
#         await asyncio.gather(*futures)
#
#
# event_loop = asyncio.get_event_loop()
# event_loop.run_until_complete(main(event_loop))

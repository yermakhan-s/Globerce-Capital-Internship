# import asyncio
# from typing import Dict
#
# import aiohttp
# import requests
# import uplink
#
# from collections_client.config.config import settings
# from fdc.odata_client import FDCOdataConsumer
# from helper import get_full_name
#
# from core.core_clent import CollectionCoreConsumer
#
#
# async def update_borrower_fio(
#         client: CollectionCoreConsumer,
#         *,
#         token: str,
#         data_in: Dict[str, str]
# ):
#     await client.borrower_fio_update(token=token, data_in=data_in)
#
#
# async def main(loop):
#     """Логика для исключения расхождения по задолженности и истории платежей
#         1. Получаем все внешние идентификаторы кредитного соглашение из 1с.
#            Получаем данные из исковых заявлений.
#         2. Запускаем цикл по всему кредитному соглашению. Внутри цикла отправляем
#            запрос на обновление ФИО заемщика в collections_core.
#     """
#     session = requests.Session()
#     session.verify = False
#
#     # 1-шаг
#     fdc_consumer = FDCOdataConsumer(
#         base_url=settings.URL_1C_ODATA,
#         auth=(settings.USERNAME_1C, settings.PASSWORD_1C),
#         client=session
#     )
#     statements = fdc_consumer.get_statements(
#             resp_format="json",
#             filter_query="DeletionMark eq false",
#             expand="Заемщик"
#         )["value"]
#
#     len_statements = len(statements)
#     step = 100 if len_statements > 100 else 1
#     # 2 - шаг
#     core_consumer = CollectionCoreConsumer(
#         base_url=settings.COLLECTIONS_CORE_URL,
#         client=uplink.AiohttpClient(connector=aiohttp.TCPConnector(ssl=False))
#     )
#     for i in range(0, len_statements, step):
#         print(i, i+step)
#         futures = []
#         for statement in statements[i:i+step]:
#             data_in = get_full_name(statement["Заемщик"]["Description"])
#             data_in["iin"] = statement["Заемщик"]["ИИН"]
#             print(data_in)
#             futures.append(update_borrower_fio(
#                 core_consumer,
#                 token=settings.COLLECTION_CORE_TOKEN,
#                 data_in=data_in))
#
#         await asyncio.gather(*futures)
#
# event_loop = asyncio.get_event_loop()
# event_loop.run_until_complete(main(event_loop))

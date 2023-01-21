import time

import requests
import logging

from config import settings
from fdc.client import FDCConsumer
from core.clent import CollectionCoreConsumer
from helper import get_full_name

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d; %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def import_data():
    session = requests.Session()
    session.verify = False

    # Core API client
    core_consumer = CollectionCoreConsumer(base_url=settings.COLLECTIONS_CORE_URL, client=session)
    credits_external_ids = core_consumer.credit_external_ids(token=settings.COLLECTION_CORE_TOKEN)
    credit_external_ids_set = set(credits_external_ids["credit_external_ids"])

    # FDC client
    consumer = FDCConsumer(
        base_url=settings.URL_1C,
        auth=(settings.USERNAME_1C, settings.PASSWORD_1C),
        client=session
    )
    statements = consumer.get_statements(
        resp_format="json",
        expand="Заемщик",
        filter_query="DeletionMark eq false")["value"]

    count = count_duplicate = count_success = count_fail = count_error = 0
    print(statements)
    # for statement_item in statements:
    #     agreement_key = statement_item["ДоговорЗайма"]
    #     if agreement_key in credit_external_ids_set:
    #         count_duplicate += 1
    #         continue
    #     borrower = statement_item["Заемщик"]
    #     if borrower["ТипКонтрагента"] == "ФизическоеЛицо":
    #         # Данные по задолженности
    #         # TODO: нужно переписать, будем брать данные от другого регистра
    #         # contract_data = {
    #         #     "external_id": statement_item["Ref_Key"],
    #         #     "main_debt": statement_item["ОстатокОсновногоДолга"],
    #         #     "reward": statement_item["ВознаграждениеПросроченное"],
    #         #     "recalc_reward": statement_item["Вознаграждение"],
    #         #     "fine": statement_item["ПеняПросроченная"],
    #         #     "commission": statement_item["КомиссияЗаОформление"],
    #         #     "tax": statement_item["Пошлина"],
    #         # }
    #         agreement_response = consumer.get_agreement_by_key(
    #             filter_query=f"Ref_Key eq guid'{agreement_key}'",
    #             resp_format="json",
    #             expand="НаименованиеКредитора,ЦельКредитования,ВидКредитногоПродукта,КредитныйПродукт"
    #         )["value"][0]
    #         contract_data = {
    #             "contract_amount": agreement_response["СуммаКредита"],
    #             "id_number": agreement_response["Number"],
    #             "issue_date": agreement_response["Date"].replace("T", " ")
    #         }
    #
    #         # Данные по заемщику
    #         borrower_data = get_full_name(borrower["Description"])
    #         borrower_data["iin"] = borrower["ИИН"]
    #         borrower_data["code"] = borrower["Code"]
    #
    #         # Адрес проживания заемщика
    #         borrower_info = borrower["КонтактнаяИнформация"]
    #         home_address = {}
    #         for borrower_item in borrower_info:
    #             if borrower_item["Тип"] == "Адрес" and borrower_item["LineNumber"] == "1":
    #                 home_address["country"] = borrower_item["Страна"]
    #                 # получаем адрес в виде строки, и оставляем только нужные данные
    #                 # хард код, так как адрес получаем в виде строки и не в виде dict
    #                 address_list = borrower_item["ЗначенияПолей"].split("\r\n")
    #                 if len(address_list) == 9:
    #                     home_address["country"] = borrower_item["Страна"]
    #                     home_address["district"] = address_list[1].split("=")[1]
    #                     home_address["city"] = address_list[2].split("=")[1]
    #                     home_address["street"] = address_list[3].split("=")[1]
    #                     home_address["building"] = address_list[4].split("=")[1]
    #                     home_address["flat"] = address_list[5].split("=")[1]
    #
    #         # УДЛ заемщика
    #         udl_key = borrower["ФизическоеЛицоГруппа"]
    #         document_resp = consumer.get_document(
    #             resp_format="json",
    #             expand="Физлицо",
    #             filter_query=f"Физлицо_Key eq guid'{udl_key}'"
    #         )["value"][0]
    #         document_data = {
    #             "id_number": document_resp["Номер"],
    #             "issued_date": document_resp["ДатаВыдачи"].split("T")[0],
    #             "validity": document_resp["СрокДействия"].split("T")[0],
    #             "issued_by": document_resp["КемВыдан"],
    #         }
    #
    #         # Номера телефона заемщика
    #         contact_datas = document_resp["Физлицо"]["КонтактнаяИнформация"]
    #
    #         phone_numbers = []
    #         for contact_data_item in contact_datas:
    #             if contact_data_item["Тип"] == "Телефон":
    #                 if contact_data_item["Представление"]:
    #                     phone_numbers.append({"phone_number": contact_data_item["Представление"]})
    #         creditor = agreement_response["НаименованиеКредитора"]
    #
    #         creditor_data = {
    #             "name": creditor["Description"],
    #             "iin": creditor["ИИН"]
    #         }
    #
    #         # Данные по кредиту
    #         params_data = {
    #             "period": agreement_response["СрокКредитования"],
    #             "cession_date": agreement_response["ДатаЗаключенияДоговораЦессии"].split("T")[0],
    #             "purpose":  agreement_response["ЦельКредитования"]["Description"],
    #             "product_type":  agreement_response["ВидКредитногоПродукта"]["Description"],
    #             "product":  agreement_response["КредитныйПродукт"]["Description"],
    #         }
    #
    #         # Данные по историю платежей
    #         borrower_key = statement_item["Заемщик_Key"]
    #         payment_history = consumer.get_payment_histories(
    #             borrower_key=f"Заемщик_Key eq guid'{borrower_key}'",
    #             resp_format="json"
    #         )["value"]
    #         payment_data = []
    #         # TODO: нужно переписать, будем брать данные от другого регистра
    #         # for payment in payment_history:
    #         #     if payment["ДоговорЗайма"] == agreement_key:
    #         #         break_payments = payment.get("РасшифровкаПлатежа")
    #         #         if break_payments:
    #         #             for break_payment in break_payments:
    #         #                 payment_dict = {
    #         #                     "external_id": break_payment["Ref_Key"],
    #         #                     "number": payment["Number"].strip(),
    #         #                     "repaid_amount": break_payment["Погашено"],
    #         #                     "debt_type": break_payment["ВидЗадолженности"],
    #         #                     "payment_date": break_payment["Платеж"].replace("T", " "),
    #         #                     "number_payout": break_payment["LineNumber"],
    #         #                 }
    #         #                 payment_data.append(payment_dict)
    #         core_request_data = {
    #             "external_id": agreement_key,
    #             "contract": contract_data,
    #             "params": params_data,
    #             "borrower": borrower_data,
    #             "creditor": creditor_data,
    #             "payment_histories": payment_data,
    #             "document": document_data,
    #             "phone_numbers": phone_numbers,
    #             "home_address": home_address,
    #         }
    #
    #         logging.info(f"Request body {core_request_data}")
    #         response = core_consumer.create_credit(
    #             token=settings.COLLECTION_CORE_TOKEN,
    #             borrower_data=core_request_data
    #         )
    #         status_code = response.status_code
    #         if 200 <= status_code < 400:
    #             count_success += 1
    #         elif 400 <= status_code < 500:
    #             count_fail += 1
    #         elif status_code >= 500:
    #             count_error += 1
    #         logging.info(f"Response {response.text}")
    #         print("---------------------------")
    #         count += 1
    #         time.sleep(1)

    logging.info(f"Общее количество данных: {len(statements)}")
    logging.info(f"Количество дубликатов: {count_duplicate}")
    logging.info(f"Количество отправленных запросов: {count}")
    logging.info(f"Количество успешных запросов: {count_success}")
    logging.info(f"Количество не валидных запросов: {count_fail}")
    logging.info(f"Количество ошибок во время запроса: {count_error}")


import_data()

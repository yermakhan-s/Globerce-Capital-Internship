import time
import logging

from collections_client.apps.collections_core.schemas import CreditLoadRequest
from collections_client.apps.collections_core.service import save_portfolio_history
from collections_client.apps.services.collections_core.client import CollectionCoreConsumer
from collections_client.apps.services.collections_core.helper import get_full_name
from collections_client.apps.services.collections_core.service import get_credit_external_id_set
from collections_client.apps.services.fdc_odata.client import FDCOdataConsumer
from collections_client.apps.services.fdc_service.client import FDCServiceConsumer
from collections_client.config.config import settings
from collections_client.config.log_config import init_logger


init_logger()
logger = logging.getLogger('collections_client')


async def load_data(
        db,
        *,
        data_in: CreditLoadRequest
):
    cession_date = data_in.cession_date.strftime("%Y-%m-%dT%H:%M:%S")

    core_consumer = CollectionCoreConsumer()
    credit_external_id_set = get_credit_external_id_set(core_consumer)
    consumer = FDCOdataConsumer()
    agreements_response = consumer.get_agreements(
        resp_format="json",
        expand="Заемщик,НаименованиеКредитора,ЦельКредитования,ВидКредитногоПродукта,КредитныйПродукт",
        filter_query=f"ДатаЗаключенияДоговораЦессии gt datetime'{cession_date}'",
    )
    agreements = agreements_response.json()["value"]
    count = count_duplicate = count_success = count_fail = count_error = 0
    for agreement in agreements:
        if agreement["DeletionMark"]:
            continue
        agreement_key = agreement["Ref_Key"]
        if agreement_key in credit_external_id_set:
            count_duplicate += 1
            continue
        borrower = agreement["Заемщик"]
        # Данные для кредитного контракта.Данные в основном будут из исковых.
        contract_data = {
            "contract_amount": agreement["СуммаКредита"],
            "id_number": agreement["Number"].strip(),
            "issue_date": agreement["Date"].replace("T", " ")
        }

        # Данные по заемщику
        borrower_data = get_full_name(borrower["Description"])
        borrower_data["iin"] = borrower["ИИН"]
        borrower_data["code"] = borrower["Code"]

        # Адрес проживания заемщика
        borrower_info = borrower["КонтактнаяИнформация"]
        home_address = {}
        for borrower_item in borrower_info:
            if borrower_item["Тип"] == "Адрес" and borrower_item["LineNumber"] == "1":
                home_address["country"] = borrower_item["Страна"]
                # получаем адрес в виде строки, и оставляем только нужные данные
                # хард код, так как адрес получаем в виде строки и не в виде dict
                address_list = borrower_item["ЗначенияПолей"].split("\r\n")
                if len(address_list) == 9:
                    home_address["country"] = borrower_item["Страна"]
                    home_address["district"] = address_list[1].split("=")[1]
                    home_address["city"] = address_list[2].split("=")[1]
                    home_address["street"] = address_list[3].split("=")[1]
                    home_address["building"] = address_list[4].split("=")[1]

                    home_address["flat"] = address_list[5].split("=")[1]

        # УДЛ заемщика
        udl_key = borrower["ФизическоеЛицоГруппа"]
        document_resp = consumer.get_document(
            resp_format="json",
            expand="Физлицо",
            filter_query=f"Физлицо_Key eq guid'{udl_key}'"
        )
        document = document_resp.json()["value"][0]
        document_data = {
            "id_number": document["Номер"].strip(),
            "issued_date": document["ДатаВыдачи"].split("T")[0],
            "validity": document["СрокДействия"].split("T")[0],
            "issued_by": document["КемВыдан"],
        }

        # Номера телефонов заемщика
        contact_data = document["Физлицо"]["КонтактнаяИнформация"]
        phone_numbers = []
        for contact_data_item in contact_data:
            if contact_data_item["Тип"] == "Телефон" and contact_data_item["Представление"]:
                phone_numbers.append({"phone_number": contact_data_item["Представление"]})

        # Данные кредитора
        creditor = agreement["НаименованиеКредитора"]
        creditor_data = {
            "name": creditor["Description"],
            "iin": creditor["ИИН"]
        }

        # Данные по кредитному параметру
        params_data = {
            "period": agreement["СрокКредитования"],
            "cession_date": agreement["ДатаЗаключенияДоговораЦессии"].split("T")[0],
            "purpose": agreement["ЦельКредитования"]["Description"],
            "product_type": agreement["ВидКредитногоПродукта"]["Description"],
            "product": agreement["КредитныйПродукт"]["Description"],
        }

        # Дополняем данные по контракту и истрии платажей из 1с сервиса
        fdc_service_consumer = FDCServiceConsumer()
        contract_payments_response = fdc_service_consumer.get_contract_payments(contract_id=agreement_key)
        contract_payments = contract_payments_response.json()

        contract = contract_payments["contract"]
        contract_data["external_id"] = contract["external_id"]
        contract_data["main_debt"] = contract["main_debt"]
        contract_data["reward"] = contract["reward"]
        contract_data["recalc_reward"] = contract["recalc_reward"]
        contract_data["fine"] = contract["fine"]
        contract_data["commission"] = contract["commission"]
        contract_data["tax"] = contract["tax"]

        payment_histories = contract_payments["payment_histories"]
        payment_data = []
        for payment in payment_histories:
            payment_dict = {
                "external_id": payment["external_id"],
                "number": payment["number"].strip(),
                "repaid_amount": payment["repaid_amount"],
                "debt_type": payment["debt_type"],
                "payment_date": payment["payment_date"].replace("T", " "),
                "number_payout": payment["number_payout"],
            }
            payment_data.append(payment_dict)

        core_request_data = {
            "external_id": agreement_key,
            "contract": contract_data,
            "params": params_data,
            "borrower": borrower_data,
            "creditor": creditor_data,
            "payment_histories": payment_data,
            "document": document_data,
            "phone_numbers": phone_numbers,
            "home_address": home_address,
        }

        logger.info(f"Request body {core_request_data}")
        response = core_consumer.create_credit(
            token=settings.COLLECTION_CORE_TOKEN,
            borrower_data=core_request_data
        )
        status_code = response.status_code
        if 200 <= status_code < 400: count_success += 1 # noqa
        elif 400 <= status_code < 500: count_fail += 1 # noqa
        elif status_code >= 500: count_error += 1 # noqa
        logger.info(f"Response {response.text}")
        print("---------------------------")
        count += 1
        time.sleep(1)

    await save_portfolio_history(db, data_in=data_in, total_request=count, success_request=count_success,
                                 fail_request=count_fail, error_request=count_error)
    logger.info(f"Общее количество заявок: {len(agreements)}")
    logger.info(f"Количество дубликатов: {count_duplicate}")
    logger.info(f"Количество отправленных запросов: {count}")
    logger.info(f"Количество успешных запросов: {count_success}")
    logger.info(f"Количество не валидных запросов: {count_fail}")
    logger.info(f"Количество ошибок во время запроса: {count_error}")

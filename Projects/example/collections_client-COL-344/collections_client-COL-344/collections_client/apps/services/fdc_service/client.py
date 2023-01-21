from uplink import get, Query, response_handler

from collections_client.apps.client.consumer import BaseConsumer
from collections_client.apps.client.exceptions import raise_for_status
from collections_client.config.config import settings


@response_handler(raise_for_status)
class FDCServiceConsumer(BaseConsumer):
    base_url = settings.URL_1C_SERVICE
    auth = (settings.USERNAME_1C, settings.PASSWORD_1C)

    @get("/mfo1/hs/TrafficExchange/GetClientInfo/")
    def get_contract_payments(self, contract_id: Query("ContractID")):
        """Запрос для получения данных по контракту и истроию платежей"""

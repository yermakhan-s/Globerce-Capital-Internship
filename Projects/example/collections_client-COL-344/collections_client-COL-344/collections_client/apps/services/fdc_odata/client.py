from uplink import get, Query, response_handler

from collections_client.apps.client.consumer import BaseConsumer
from collections_client.apps.client.exceptions import raise_for_status
from collections_client.config.config import settings


@response_handler(raise_for_status)
class FDCOdataConsumer(BaseConsumer):
    """A Python HTTP Client for the FDC REST API."""
    base_url = settings.URL_1C_ODATA
    auth = (settings.USERNAME_1C, settings.PASSWORD_1C)

    @get("Document_мфо_ИсковоеЗаявление")
    def get_statements(
            self,
            resp_format: Query("$format", encoded=True),
            filter_query: Query("$filter", encoded=True),
            expand: Query("$expand", encoded=True) = None
    ):
        """Список исковых заявлении."""

    @get("Document_мко_КредитноеСоглашение")
    def get_agreement_by_key(
            self,
            filter_query: Query("$filter", encoded=True),
            resp_format: Query("$format", encoded=True),
            expand: Query("$expand", encoded=True)):
        """Кредитное соглашение по идентификатору."""

    @get("InformationRegister_ДокументыФизическихЛиц")
    def get_document(
            self,
            resp_format: Query("$format", encoded=True),
            expand: Query("$expand", encoded=True),
            filter_query: Query("$filter", encoded=True)
    ):
        """УДЛ и номер телефона"""

    @get("Document_мко_ПогашениеЗайма")
    def get_payment_histories(
            self,
            borrower_key: Query("$filter", encoded=True),
            resp_format: Query("$format", encoded=True)):
        """История платежей по заемщику"""
        # TODO: нужно получить по кредиту, а не по заемщику.
        #  Если фильровать по кредиту выходит 500 или 200 с пустым значением

    @get("Document_мко_КредитноеСоглашение")
    def get_agreements(
            self,
            filter_query: Query("$filter", encoded=True),
            resp_format: Query("$format", encoded=True),
            expand: Query("$expand", encoded=True)
    ):
        """Список кредитных соглашений"""

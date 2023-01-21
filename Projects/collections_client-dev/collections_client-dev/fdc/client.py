from uplink import Consumer, get, Path, Query, returns


class FDCConsumer(Consumer):
    """A Python Client for the FDC REST API."""

    @returns.json
    @get("Document_мфо_ИсковоеЗаявление")
    def get_statements(
            self,
            resp_format: Query("$format", encoded=True),
            filter_query: Query("$filter", encoded=True),
            expand: Query("$expand", encoded=True) = None
    ):
        """Список исковых заявлении."""

    @returns.json
    @get("Document_мко_КредитноеСоглашение")
    def get_agreement_by_key(
            self,
            filter_query: Query("$filter", encoded=True),
            resp_format: Query("$format", encoded=True),
            expand: Query("$expand", encoded=True)):
        """Кредитное соглашение по идентификатору."""

    @returns.json
    @get("InformationRegister_ДокументыФизическихЛиц")
    def get_document(
            self,
            resp_format: Query("$format", encoded=True),
            expand: Query("$expand", encoded=True),
            filter_query: Query("$filter", encoded=True)
    ):
        """УДЛ и номер телефона"""

    @returns.json
    @get("Document_мко_ПогашениеЗайма")
    def get_payment_histories(
            self,
            borrower_key: Query("$filter", encoded=True),
            resp_format: Query("$format", encoded=True)):
        """История платежей по заемщику"""
        # TODO: нужно получить по кредиту, а не по заемщику.
        #  Если фильровать по кредиту выходит 500 или 200 с пустым значением

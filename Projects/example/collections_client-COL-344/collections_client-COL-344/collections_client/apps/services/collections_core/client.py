from uplink import post, Body, json, Header, get, put, Path

from collections_client.apps.client.consumer import BaseConsumer
from collections_client.apps.services.collections_core.schemas.borrowers import BorrowerFIOUpdateRequest
from collections_client.apps.services.collections_core.schemas.credits import CreditRequest
from collections_client.config.config import settings


class CollectionCoreConsumer(BaseConsumer):
    """A Python Client for the Collection Core API."""
    base_url = settings.COLLECTIONS_CORE_URL

    @json
    @post("credits/")
    async def create_credit(
            self,
            token: Header("x-api-token"),
            borrower_data: Body(type=CreditRequest),
    ):
        ...

    @get("credits/external_ids/")
    async def credit_external_ids(self, token: Header("x-api-token")):
        ...

    @put("credits/{external_id}/update-daily/")
    async def update_daily(self, external_id: Path, token: Header("x-api-token")):
        """Обновление данные по задолженности и история платажей по определенному кредиту"""

    @json
    @put("borrowers/fio-update/")
    async def borrower_fio_update(
            self,
            token: Header("x-api-token"),
            data_in: Body(type=BorrowerFIOUpdateRequest)
    ):
        """Обновляем ФИО заемщика по ИИН"""

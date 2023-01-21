from uplink import Consumer, post, Body, json, Header, get, returns, put, Path, delete, AiohttpClient

from core.models.credits import CreditRequest


class CollectionCoreConsumer(Consumer):
    """A Python Client for the Collection Core API."""

    @json
    @post("credits/")
    async def create_credit(
            self,
            token: Header("x-api-token"),
            borrower_data: Body(type=CreditRequest),
    ):
        ...

    @returns.json
    @get("credits/external_ids/")
    async def credit_external_ids(self, token: Header("x-api-token")):
        ...

    @put("credits/{external_id}/update-daily/")
    async def update_daily(self, external_id: Path, token: Header("x-api-token")):
        """Обновление данные по задолженности и история платажей по определенному кредиту"""



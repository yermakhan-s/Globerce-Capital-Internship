from typing import Set

from collections_client.apps.services.collections_core.client import CollectionCoreConsumer
from collections_client.config.config import settings


def get_credit_external_id_set(consumer: CollectionCoreConsumer) -> Set[str]:
    credits_external_ids_response = consumer.credit_external_ids(token=settings.COLLECTION_CORE_TOKEN)
    credits_external_ids = credits_external_ids_response.json()
    credit_external_id_set = set(credits_external_ids["credit_external_ids"])
    return credit_external_id_set

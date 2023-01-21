from fastapi import APIRouter
from collections_client.apps.collections_core import views as collections_core_view

router = APIRouter()

router.include_router(collections_core_view.router, prefix="/collections_core", tags=["collections_core"])

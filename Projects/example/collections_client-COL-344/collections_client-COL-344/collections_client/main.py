from fastapi import FastAPI
from collections_client import routers as base_router
from collections_client.config.config import settings


app = FastAPI(
    title=f"{settings.PROJECT_NAME} API"
)

app.include_router(base_router.router, prefix="", tags=["collections_client"])

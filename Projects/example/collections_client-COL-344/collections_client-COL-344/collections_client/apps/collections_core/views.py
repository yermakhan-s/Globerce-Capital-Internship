from datetime import datetime, timedelta

from fastapi import APIRouter, Body, BackgroundTasks, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from collections_client.apps.collections_core.schemas import CreditLoadRequest
from collections_client.apps.collections_core.selector import get_last_portfolio
from collections_client.apps.db import deps
from collections_client.apps.services.collections_core.scripts.load_fdc_data import load_data

from collections_client.config.config import settings
router = APIRouter()


@router.post("/load-credits/")
async def load_credits(
        db: AsyncSession = Depends(deps.get_db_session),
        *,
        background_tasks: BackgroundTasks,
        data_in: CreditLoadRequest = Body(...)
):
    """Выгрузка нового портфолио из 1С"""
    last_portfolio = await get_last_portfolio(db)
    if last_portfolio and last_portfolio.created_at + timedelta(settings.LIMIT_TO_LOAD_IN_DAYS) > datetime.now():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Лимит на загрузку")
    background_tasks.add_task(load_data, db, data_in=data_in)
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Request accepted"})

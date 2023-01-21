from sqlalchemy.ext.asyncio import AsyncSession

from collections_client.apps.collections_core.models import PortfolioHistory
from collections_client.apps.collections_core.schemas import CreditLoadRequest


async def save_portfolio_history(
        db: AsyncSession,
        *,
        data_in: CreditLoadRequest,
        total_request: int,
        success_request: int,
        fail_request: int,
        error_request: int
):
    portfolio_history = PortfolioHistory(
        created_by_fio=data_in.created_by_fio,
        cession_date=data_in.cession_date,
        total_request=total_request,
        success_request=success_request,
        fail_request=fail_request,
        error_request=error_request
    )
    db.add(portfolio_history)
    await db.commit()

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from collections_client.apps.collections_core.models import PortfolioHistory


async def get_last_portfolio(db: AsyncSession) -> PortfolioHistory:
    """Запрос для получение последего загруженного портфолио"""
    query = select(PortfolioHistory).order_by(PortfolioHistory.created_at.desc())
    portfolio_history = await db.execute(query)
    return portfolio_history.scalars().first()

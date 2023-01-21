from asyncio import current_task

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.orm import sessionmaker

from collections_client.config.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, echo=False)
Session = async_scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine,  expire_on_commit=False, class_=AsyncSession),
    scopefunc=current_task
)

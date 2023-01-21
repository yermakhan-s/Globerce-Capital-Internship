from sqlalchemy import (Column, Integer, String, DateTime)

from collections_client.apps.commons import timezone
from collections_client.apps.db.base_model import Model


class PortfolioHistory(Model):
    """История по загрузе портфолио"""
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=timezone.now)
    created_by_fio = Column(String(255))
    cession_date = Column(DateTime)
    total_request = Column(Integer)
    success_request = Column(Integer)
    fail_request = Column(Integer)
    error_request = Column(Integer)

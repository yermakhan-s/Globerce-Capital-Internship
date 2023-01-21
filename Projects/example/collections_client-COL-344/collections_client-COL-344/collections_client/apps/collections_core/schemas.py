from datetime import datetime
from pydantic import BaseModel, Field


class CreditLoadRequest(BaseModel):
    cession_date: datetime = Field(title="Дата цессии")
    created_by_fio: str = Field(title="ФИО пользователя")

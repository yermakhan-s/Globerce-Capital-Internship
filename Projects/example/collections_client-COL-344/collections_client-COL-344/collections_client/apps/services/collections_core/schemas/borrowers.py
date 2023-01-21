from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class BorrowerBase(BaseModel):
    iin: str = Field(title="ИИН заемщика")
    code: str = Field(title="Код заемщика")
    first_name: str = Field(title="Имя заещика")
    last_name: str = Field(title="Фамилия заемщика")
    middle_name: Optional[str] = Field(title="Отчество заемщика")


class DocumentCreate(BaseModel):
    id_number: str = Field(title="Номер удостоверение личности")
    issued_by: str = Field(title="Кем выдан")
    validity: date = Field(title="Срок действия")
    issued_date: date = Field(title="Дата выдачи")


class PhoneNumberCreate(BaseModel):
    phone_number: str = Field(title="Номер телефона")


class Address(BaseModel):
    country: Optional[str] = Field(default=None, title="Страна")
    region: Optional[str] = Field(default=None, title="Регион")
    region_code: Optional[str] = Field(default=None, title="Код региона")
    city: Optional[str] = Field(default=None, title="Город")
    district: Optional[str] = Field(default=None, title="Район")
    street: Optional[str] = Field(default=None, title="Улица")
    building: Optional[str] = Field(default=None, title="Здание")
    flat: Optional[str] = Field(default=None, title="Квартира")
    postal_code: Optional[str] = Field(default=None, title="Почтовый индекс")


class BorrowerFIOUpdateRequest(BaseModel):
    iin: str = Field(title="ИИН заемщика")
    first_name: str = Field(title="Имя заещика")
    last_name: str = Field(title="Фамилия заемщика")
    middle_name: Optional[str] = Field(title="Отчество заемщика")

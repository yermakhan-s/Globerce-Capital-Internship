from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, Field

from collections_client.apps.services.collections_core.schemas.borrowers import BorrowerBase, DocumentCreate, \
    PhoneNumberCreate, Address


class CreditContractCreate(BaseModel):
    external_id: Optional[str] = Field(title="Уникальный ключ контракта")
    main_debt: Optional[Decimal] = Field(title="Основной долг")
    reward: Optional[Decimal] = Field(title="Вознаграждение")
    recalc_reward: Optional[Decimal] = Field(title="Перерасчет вознаграждение")
    fine: Optional[Decimal] = Field(title="Пеня")
    commission: Optional[Decimal] = Field(title="Расходы по взысканию")
    tax: Optional[Decimal] = Field(title="Госпошлина")
    contract_amount: Decimal = Field(title="Cумма по договору")
    id_number: str = Field(title="Уникальный номер кредита")
    issue_date: datetime = Field(title="Дата договора")


class CreditParamsCreate(BaseModel):
    purpose: str = Field(title="Цель кредитование")
    product_type: str = Field(title="Вид кредитного продукта")
    product: str = Field(title="Кредитный продукт")
    period: int = Field(title="Срок кредита")
    cession_date: date = Field(title="Дата передачи в работу КА")


class CreditorCreate(BaseModel):
    iin: Optional[str] = Field(title="IIN кредитора")
    name: str = Field(title="Наименование кредитора")


class CreditPaymentHistoryCreate(BaseModel):
    external_id: Optional[str] = Field(title="Уникальный ключ")
    number: str = Field(title="Уникальный номер погашение займа")
    number_payout: int = Field(title="Номер выплаты")
    payment_date: str = Field(title="Дата платежа")
    debt_type: str = Field(title="Вид задолженности")
    repaid_amount: Decimal = Field(title="Погашено")


class CreditRequest(BaseModel):
    external_id: Optional[str] = Field(title="Уникальный ключ объекта")
    contract: CreditContractCreate = Field(title="Данные кредитного контракта")
    params: CreditParamsCreate = Field(title="Данные кредитного параметра")
    borrower: BorrowerBase = Field(title="Данные заемщика")
    creditor: CreditorCreate = Field(title="Данные кредитора")
    payment_histories: List[Optional[CreditPaymentHistoryCreate]] = Field(title="Данные история платежа")
    document: DocumentCreate = Field(title="Данные УДЛ")
    phone_numbers: List[PhoneNumberCreate] = Field(title="Номера телефонов заемщика")
    home_address: Optional[Address] = Field(title="Адресс проживания заемщика")

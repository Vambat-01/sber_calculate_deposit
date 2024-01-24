import re
from typing import Dict

from datetime import date
from pydantic import BaseModel, Field, field_validator, validator


def parse_custom_date_format(date_str: str) -> date:
    if not re.match(r'\d{2}\.\d{2}\.\d{4}', date_str):
        raise ValueError("Date must be in DD.MM.YYYY format")

    day, month, year = map(int, date_str.split('.'))

    return date(year, month, day)


class RequestDeposit(BaseModel):
    start_date: date = Field(..., description="Дата заявки(dd.mm.YYYY)", alias="date")
    periods: int = Field(..., ge=1, le=60, description="Количество месяцев по вкладу")
    amount: int = Field(..., ge=10_000, le=3_000_000, description="Сумма вклада")
    rate: float = Field(..., ge=1, le=8, description="Процент по вкладу")

    @validator('start_date', pre=True)
    def parse_date(cls, value):
        if isinstance(value, str):
            return parse_custom_date_format(value)
        elif isinstance(value, date):
            return value
        raise ValueError("Invalid date format")


class ResponseDeposit(BaseModel):
    profit_info: Dict = Field(..., description="Информация о прибыли")

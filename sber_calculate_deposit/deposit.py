from datetime import date
from typing import List, Tuple

from dateutil.relativedelta import relativedelta

from sber_calculate_deposit.models import RequestDeposit


def calculate_deposit(data: RequestDeposit) -> List[Tuple[date, float]]:
    """Подсчитывает дипозит и возвращает"""

    amount = data.amount
    coefficient = 1 + (data.rate / 12 / 100)
    values = []
    for month in range(data.periods):
        cur_date = data.start_date + relativedelta(months=month)
        cur_amount = round(coefficient * amount, 2)
        values.append((cur_date, cur_amount))
        amount = cur_amount

    return values

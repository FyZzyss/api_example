"""Схемы pydantic"""

# pylint:disable=too-few-public-methods, no-self-argument, no-self-use

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Union

from pydantic import BaseModel  # pylint:disable=no-name-in-module


class FileTypes(str, Enum):
    """Enum класс для валидации типов(возможно, будет пополняться в будущем)"""
    xlsx = 'xlsx'


class PeriodTypes(str, Enum):
    """Enum класс для валидации опции периодов(возможно, будет пополняться в будущем)"""
    quarter = 'quarter'
    month = 'month'


class UserTypes(str, Enum):
    """Enum класс для валидации опции периодов(возможно, будет пополняться в будущем)"""
    legal = 'legal'
    individual = 'individual'


class StatsOutput(BaseModel):
    """Модель статистики для отдачи данных по физ.лицам"""
    user: int
    s_name: str
    contract_n: Optional[int]
    contract_start: Optional[datetime]
    s_description: Optional[str]
    status: str
    total_sum: Decimal
    tax_deduction: int
    contract_ndfl: int
    ndfl_sum: int
    min_payment: int
    balance: Decimal
    to_pay: Decimal
    prorata: Decimal
    s_contract_dolgnost: Optional[str]
    is_rezident: int


class StatsOutputLegal(StatsOutput):
    """Модель статистики для отдачи данных по юр.лицам"""
    contract_nds: int
    child_users: Optional[str]


class StatsOutputList(BaseModel):
    """Модель статистики для отдачи данных"""
    users: List[Union[StatsOutputLegal, StatsOutput]]

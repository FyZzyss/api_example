"""Моделиpydantic"""

# pylint:disable=too-few-public-methods, no-self-argument, no-self-use
import re
from typing import Optional

from pydantic import BaseModel, validator  # pylint:disable=no-name-in-module
from fastapi import HTTPException

from app.schemas.stats import PeriodTypes


class ReportParams(BaseModel):
    """Модель обработки входящих данных"""
    user: Optional[int]
    s_name: Optional[str]
    period: Optional[str]
    period_date: Optional[str]
    file: Optional[str]
    user_type: Optional[str]

    @validator('period_date')
    def check_if_date_approach_to_period(cls, val, values):
        """Проверка на валидность даты, если есть и не нарушена ли логика опция-дата"""
        if val is not None:
            quarter = re.match(r'Q[1-4]_\d{4}', val)
            month = re.match(r'[A-Z][a-z]{2}_\d{4}', val)
            if not quarter and not month:
                raise HTTPException(
                    status_code=400,
                    detail='Date format must be like '
                           '\'Q2_2020\' for quarter and \'Sep_2020\' for month'
                )
            if values['period'] == PeriodTypes.quarter and not quarter:
                raise HTTPException(
                    status_code=400,
                    detail='With period \'quarter\' date must be like \'Q2_2020\''
                )
            if values['period'] == PeriodTypes.month and not month:
                raise HTTPException(
                    status_code=400,
                    detail='With period \'month\' date must be like \'Sep_2020\''
                )
        return val

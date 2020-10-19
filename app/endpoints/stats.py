"""Модуль stats"""

# pylint:disable=too-many-arguments

from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import ValidationError

from app.core.stats import Report
from app.models.stats import ReportParams
from app.schemas.stats import FileTypes, PeriodTypes, StatsOutputList, UserTypes

router = APIRouter()


@router.get("/payments/", response_model=StatsOutputList, response_description='Данные по физикам')
async def payments(
        user_type: UserTypes,
        period: PeriodTypes = None,
        period_date: str = None,
        user: int = None,
        s_name: str = None,
        file: FileTypes = None
):
    """Рендерит json или xlsx отчёт из монги по физикам.
    Args:
    - period: Настройка периода
    - period_date: Период, за который выбираем данные
    - user: Айди юзера, о котором нужна информация
    - s_name: ФИО(как в бд) юзера, о котором нужна информация
    - file: Тип файла, в который мы хотим положить данные(доступен только xlsx)
    """
    try:
        return await Report(
            params=ReportParams(
                period=period,
                period_date=period_date,
                user=user,
                s_name=s_name,
                user_type=user_type,
                file=file
            )
        ).get()
    except ValidationError as err:
        return HTTPException(status_code=400, detail=f"{err.errors()[0]['msg']}"
                                                     f"in {err.errors()[0]['loc']}")

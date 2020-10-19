"""Код под капотом"""
from fastapi import HTTPException

from app.core.utils import create_and_render_xlsx
from app.database import mongo
from app.models.stats import ReportParams
from app.schemas.stats import StatsOutputList, StatsOutput, FileTypes, UserTypes, StatsOutputLegal


class Report:
    """Класс отчёта"""

    def __init__(self, params: ReportParams):
        self.params = params
        self._report_list = None
        self.output_model_dict = {
            'legal': StatsOutputLegal,
            'individual': StatsOutput
        }

    def json(self):
        """Возвращает json"""
        return StatsOutputList(users=self._report_list)

    def xlsx(self):
        """Возвращает xlsx"""
        xlsx_columns = [
                'ID правообладателя', 'ФИО правообладателя',
                'Номер договора', 'Дата договора', 'Агентство', 'Статус',
                'Сумма по отчету, включая НДФЛ/НДС', 'Налоговый вычет', 'Ставка НДФЛ',
                'Сумма НДФЛ/НДС', 'Порог выплаты', 'Остаток', 'К оплате', 'Прората',
                'Гражданство/Должность', 'Резидентство',
            ]
        if self.params.user_type == UserTypes.legal.name:
            xlsx_columns.extend(['Ставка НДС', 'Дочерние ID'])
        return create_and_render_xlsx(
            self._report_list, xlsx_columns, self.output_model_dict[self.params.user_type],
            'report.xlsx'
        )

    async def get(self):
        """Получаем список отчётов по пользовательскому вводу"""
        async with mongo:
            self._report_list = [
                self.output_model_dict[self.params.user_type](**doc) async for doc in
                mongo.stats_payments.stats_payments.find(self.params.dict(
                    exclude_none=True, exclude={'file'}
                ), projection={'_id': False})
            ]
            # Если есть результат - выводим в нужном формате
            if self._report_list:
                return await self.__get_response()
            # Если ничего не было найдено, пытаемся найти ошибку юзера(если она есть)
            return await self.__validate_user_query(mongo)

    async def __validate_user_query(self, mongo_session):
        """
        Если в результате пользовательского ввода не было найдено ни одного отчёта, то:
        делаем доп. проверки, чтобы попытаться сказать юзеру, что он ввёл не так.
        """
        if self.params.user and self.params.s_name:
            check_user = await mongo_session.stats_payments.stats_payments.find_one(
                {"user": self.params.user},
                projection={'_id': False}
            )
            if not check_user:
                raise HTTPException(status_code=404, detail="Invalid person id")
            if self.params.s_name != check_user.get('s_name'):
                raise HTTPException(status_code=404, detail="Invalid person name")
        if (self.params.user or self.params.s_name) and self.params.period:
            check_user = await mongo_session.stats_payments.stats_payments.find_one(
                self.params.dict(
                    exclude_none=True, exclude={'period', 'period_date', 'file'}
                ),
                projection={'_id': False}
            )
            if check_user is not None:
                if check_user['period'] != self.params.period:
                    raise HTTPException(status_code=400, detail="Invalid period option")

        raise HTTPException(status_code=404, detail="Person not found")

    async def __get_response(self):
        """Выводим ответ в нужном фаормате"""
        if self.params.file == FileTypes.xlsx:
            # если передали file=xlsx - формируем и отдаём xlsx
            return self.xlsx()
        # если не формируем файл, то отдаём json
        return self.json()

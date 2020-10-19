"""Общие утилиты, которые могут пригодиться для всех эндпоинтов"""
from datetime import datetime
from typing import List
from io import BytesIO

import xlsxwriter
from fastapi.responses import StreamingResponse


def create_and_render_xlsx(tmp: List, headers: List, pydantic_model, file_name: str):
    """Создаём xlsx в памяти и отдаём"""
    get_cell_number = {key: number for number, key in enumerate(pydantic_model.__fields__)}
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    row_count = 1
    for number, value in enumerate(headers):
        worksheet.write(0, number, value)
    for row in tmp:
        row = row.dict()
        for key in row:
            if isinstance(row[key], datetime):
                row[key] = str(row[key])
            worksheet.write(row_count, get_cell_number[key], row[key])
        row_count += 1
    workbook.close()
    output.seek(0)
    return StreamingResponse(
        output,
        headers={
            'Content-Type': 'application/vnd.'
                            'openxmlformats-officedocument'
                            '.spreadsheetml.sheet',
            'Content-disposition':
                f'filename={file_name}'}
    )

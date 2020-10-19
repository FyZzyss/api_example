"""Главный модуль"""
from fastapi import FastAPI

from app.endpoints import stats

app = FastAPI()

app.include_router(stats.router, prefix="/stats", tags=["stats"])

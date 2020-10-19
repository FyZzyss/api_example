"""Модуль подключения к бд"""
from platformdb.engine import Engine
from lr.config import CONFIG

mongo = Engine(CONFIG).mongo

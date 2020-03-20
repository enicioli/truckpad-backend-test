import os
import importlib
from mongoframes import Frame
from pymongo import MongoClient
from mongomock import MongoClient as MongoClientMock
from abc import ABC


class AbstractConfig(ABC):
    config = None

    @staticmethod
    def get_config_class():
        if AbstractConfig.config is None:
            AbstractConfig.config = getattr(
                importlib.import_module('config.{}'.format(os.getenv('FLASK_ENV'))),
                'Config'
                )
        return AbstractConfig.config

    @staticmethod
    def set_up_db(mock=False):
        config = AbstractConfig.get_config_class()
        params = {
            'host': config.MONGO_HOST,
            'port': config.MONGO_PORT,
            'username': config.MONGO_USER,
            'password': config.MONGO_PASSWORD
        }

        client = MongoClient(**params) if not mock else MongoClientMock(**params)
        db = client[config.MONGO_DB]
        Frame._client = client

        return db

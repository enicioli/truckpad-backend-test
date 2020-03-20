import pymongo
from mongoframes import *
from api.odm.trucker import TruckerDocument
from config._abstract import AbstractConfig


class Coordinates(SubFrame):
    _fields = {
        'x',
        'y'
    }


class TruckType(SubFrame):
    TRUCK_TYPES = {
        1: 'Caminhão 3/4',
        2: 'Caminhão Tock',
        3: 'Caminhão Truck',
        4: 'Caminhão Simples',
        5: 'Caminhão Eixo Estendido'
    }

    _fields = {
        'code',
        'name'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = TruckType.TRUCK_TYPES[self.code] if self.code else None


class CheckInDocument(Frame):
    _db = AbstractConfig.get_config_class().MONGO_DB

    _collection = 'checkIns'

    _fields = {
        'trucker',
        'truckType',
        'origin',
        'destination',
        'isLoaded',
        'created',
        'checkedOut'
    }

    _default_projection = {
        'trucker': {'$ref': TruckerDocument},
        'origin': {'$sub': Coordinates},
        'destination': {'$sub': Coordinates},
        'truckType': {'$sub': TruckType}
    }

    _indexes = [
        IndexModel([('isLoaded', pymongo.ASCENDING)]),
        IndexModel([('truckType', pymongo.ASCENDING)]),
        IndexModel([('origin', pymongo.GEO2D)]),
        IndexModel([('destination', pymongo.GEO2D)]),
        IndexModel([('created', pymongo.ASCENDING)]),
        IndexModel([('checkedOut', pymongo.ASCENDING)])
    ]


CheckInDocument.listen('insert', CheckInDocument.timestamp_insert)

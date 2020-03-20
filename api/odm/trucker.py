import pymongo
from mongoframes import *
from config._abstract import AbstractConfig


class TruckerDocument(Frame):
    _db = AbstractConfig.get_config_class().MONGO_DB

    _collection = 'truckers'

    _fields = {
        '_id',
        'name',
        'birthDate',
        'sex',
        'licenseType',
        'isOwner',
        'created',
        'modified'
    }

    _indexes = [
        IndexModel([('name', pymongo.ASCENDING)]),
        IndexModel([('birthDate', pymongo.ASCENDING)]),
        IndexModel([('sex', pymongo.ASCENDING)]),
        IndexModel([('licenseType', pymongo.ASCENDING)]),
        IndexModel([('isOwner', pymongo.ASCENDING)]),
        IndexModel([('created', pymongo.ASCENDING)]),
        IndexModel([('modified', pymongo.ASCENDING)])
    ]


TruckerDocument.listen('insert', TruckerDocument.timestamp_insert)
TruckerDocument.listen('update', TruckerDocument.timestamp_update)

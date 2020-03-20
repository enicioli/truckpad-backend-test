from api.odm.check_in import CheckInDocument, TruckType
from api.odm.trucker import TruckerDocument
from bson.objectid import ObjectId
from datetime import datetime, timedelta


class CheckInModel:
    def __init__(self):
        pass

    @staticmethod
    def create_check_in(data: dict,
                        trucker: TruckerDocument):
        check_in = CheckInDocument(data)
        check_in.trucker = trucker
        check_in.truckType = TruckType(code=data['truckType'])
        check_in.insert()
        return check_in

    @staticmethod
    def get_check_in_by_id(check_in_id: str):
        return CheckInDocument.by_id(ObjectId(check_in_id))

    @staticmethod
    def checkout(check_in: CheckInDocument):
        if check_in.checkedOut is not None:
            return None
        check_in.checkedOut = datetime.now()
        check_in.update()
        return check_in

    @staticmethod
    def get_loaded_check_ins(days=0):
        return CheckInDocument.count({
            'isLoaded': True,
            'created': {
                '$gte': datetime.now() - timedelta(days=days)
            }
        })

    @staticmethod
    def get_checkout_distribution():
        return list(CheckInDocument.get_db().checkIns.aggregate([{
                '$group': {
                    '_id': {
                        'origin': '$origin',
                        'destination': '$destination',
                        'truckType': '$truckType'
                    },
                    'count': {
                        '$sum': 1
                    }
                }
            }]))

from api.odm.trucker import TruckerDocument
from api.odm.check_in import CheckInDocument
from bson.objectid import ObjectId


class TruckerModel:
    def __init__(self):
        pass

    @staticmethod
    def create_trucker(data: dict):
        trucker = TruckerDocument(data)
        trucker.insert()
        return trucker

    @staticmethod
    def update_trucker(trucker: TruckerDocument,
                       data: dict):
        for key, value in data.items():
            trucker.__setattr__(key, value)

        trucker.update()
        return trucker

    @staticmethod
    def get_trucker_by_id(trucker_id: str):
        return TruckerDocument.by_id(ObjectId(trucker_id))

    @staticmethod
    def delete_trucker(trucker: TruckerDocument):
        return trucker.delete()

    @staticmethod
    def get_available_truckers():
        return CheckInDocument.many({
            'isLoaded': False,
            'checkedOut': None
            })

    @staticmethod
    def get_owner_truckers():
        return TruckerDocument.many({
            'isOwner': True
            })

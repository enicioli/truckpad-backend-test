from api.routes.schemas._abstract import AbstractSchema
from api.odm.check_in import TruckType


class CheckInSchema(AbstractSchema):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": {
            "truckType": {
                "type": "number",
                "enum": list(TruckType.TRUCK_TYPES.keys()),
            },
            "origin": {
                "properties": {
                    "lng": {
                        "type": "number"
                    },
                    "lat": {
                        "type": "number"
                    },
                },
                "required": [
                    "lng",
                    "lat"
                ],
                "type": "object"
            },
            "destination": {
                "properties": {
                    "lng": {
                        "type": "number"
                    },
                    "lat": {
                        "type": "number"
                    },
                },
                "required": [
                    "lng",
                    "lat"
                ],
                "type": "object"
            },
            "isLoaded": {
                "type": "boolean"
            }
        },
        "required": [
            "truckType",
            "origin",
            "destination",
            "isLoaded"
        ],
        "type": "object"
    }

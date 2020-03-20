from api.routes.schemas._abstract import AbstractSchema


class TruckerSchema(AbstractSchema):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "properties": {
            "name": {
                "minLength": 3,
                "maxLength": 255,
                "type": "string",
            },
            "birthDate": {
                "type": "string",
                "format": "date"
            },
            "sex": {
                "type": "string",
                "enum": [
                    "F",
                    "M"
                ],
            },
            "licenseType": {
                "type": "string",
                "enum": [
                    "A",
                    "B",
                    "C",
                    "D",
                    "E"
                ],
            },
            "isOwner": {
                "type": "boolean"
            }
        },
        "required": [
            "name",
            "birthDate",
            "sex",
            "licenseType",
            "isOwner"
        ],
        "type": "object"
    }


class TruckerSchemaUpdate(TruckerSchema):

    def get_schema(self):
        schema = self.schema
        if 'required' in schema:
            schema.pop('required')

        return schema

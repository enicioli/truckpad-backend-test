from abc import ABC
from flask import jsonify
from bson import ObjectId


class AbstractRoute(ABC):

    @staticmethod
    def bad_request():
        return jsonify({'message': 'Bad request'}), 400

    @staticmethod
    def not_found():
        return jsonify({'message': 'Not found'}), 404

    @staticmethod
    def is_object_id(object_id):
        return ObjectId.is_valid(object_id)

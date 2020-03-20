from flask import Blueprint, request, jsonify
from api.routes._abstract import AbstractRoute
from api.routes.schemas.trucker import TruckerSchema, TruckerSchemaUpdate
from api.models.trucker import TruckerModel

TruckerController = Blueprint('trucker', __name__, url_prefix='/trucker')


@TruckerController.route('', methods=['POST'])
def route_create_trucker():
    json_data = request.get_json(force=True)
    result, message = TruckerSchema.validate(json_data)
    if result is False:
        return AbstractRoute.bad_request()

    trucker = TruckerModel.create_trucker(json_data)
    return jsonify(trucker.to_json_type()), 201


@TruckerController.route('/<trucker_id>', methods=['PUT', 'PATCH'])
def route_update_trucker(trucker_id: str):
    if not AbstractRoute.is_object_id(trucker_id):
        return AbstractRoute.bad_request()

    trucker = TruckerModel.get_trucker_by_id(trucker_id)
    if trucker is None:
        return AbstractRoute.not_found()

    json_data = request.get_json(force=True)

    if request.method == 'PATCH':
        result, message = TruckerSchemaUpdate.validate(json_data)
    else:
        result, message = TruckerSchema.validate(json_data)

    if result is False:
        return AbstractRoute.bad_request()

    trucker = TruckerModel.update_trucker(trucker, json_data)
    return jsonify(trucker.to_json_type())


@TruckerController.route('/<trucker_id>', methods=['GET'])
def route_get_trucker(trucker_id: str):
    if not AbstractRoute.is_object_id(trucker_id):
        return AbstractRoute.bad_request()

    trucker = TruckerModel.get_trucker_by_id(trucker_id)
    if trucker is None:
        return AbstractRoute.not_found()

    return jsonify(trucker.to_json_type())


@TruckerController.route('/<trucker_id>', methods=['DELETE'])
def route_delete_trucker(trucker_id: str):
    if not AbstractRoute.is_object_id(trucker_id):
        return AbstractRoute.bad_request()

    trucker = TruckerModel.get_trucker_by_id(trucker_id)
    if trucker is None:
        return AbstractRoute.not_found()

    TruckerModel.delete_trucker(trucker)
    return jsonify({'message': 'OK'})


@TruckerController.route('/available', methods=['GET'])
def route_get_available_truckers():
    check_ins = TruckerModel.get_available_truckers()
    return jsonify(list(map(lambda check_in: check_in.trucker.to_json_type(), check_ins)))


@TruckerController.route('/owner', methods=['GET'])
def route_get_owner_truckers():
    truckers = TruckerModel.get_owner_truckers()
    return jsonify(list(map(lambda trucker: trucker.to_json_type(), truckers)))

from flask import Blueprint, request, jsonify
from api.routes._abstract import AbstractRoute
from api.routes.schemas.check_in import CheckInSchema
from api.models.check_in import CheckInModel
from api.models.trucker import TruckerModel

CheckInController = Blueprint('check-in', __name__, url_prefix='/check-in')


@CheckInController.route('/trucker/<trucker_id>', methods=['POST'])
def route_create_check_in(trucker_id: str):
    if not AbstractRoute.is_object_id(trucker_id):
        return AbstractRoute.bad_request()

    json_data = request.get_json(force=True)
    result, message = CheckInSchema.validate(json_data)
    if result is False:
        return AbstractRoute.bad_request()

    trucker = TruckerModel.get_trucker_by_id(trucker_id)
    if trucker is None:
        return AbstractRoute.not_found()

    check_in = CheckInModel.create_check_in(json_data, trucker)
    return jsonify(check_in.to_json_type()), 201


@CheckInController.route('/<check_in_id>', methods=['GET'])
def route_get_check_in(check_in_id: str):
    if not AbstractRoute.is_object_id(check_in_id):
        return AbstractRoute.bad_request()

    check_in = CheckInModel.get_check_in_by_id(check_in_id)
    if check_in is None:
        return AbstractRoute.not_found()

    return jsonify(check_in.to_json_type())


@CheckInController.route('/<check_in_id>/checkout', methods=['PATCH'])
def route_checkout(check_in_id: str):
    if not AbstractRoute.is_object_id(check_in_id):
        return AbstractRoute.bad_request()

    check_in = CheckInModel.get_check_in_by_id(check_in_id)
    if check_in is None:
        return AbstractRoute.not_found()

    check_in = CheckInModel.checkout(check_in)
    if check_in is None:
        return AbstractRoute.bad_request()

    return jsonify(check_in.to_json_type())


@CheckInController.route('/loaded/<days>', methods=['GET'])
def route_get_loaded_check_ins(days: int):
    try:
        days = int(days)
    except ValueError:
        return AbstractRoute.bad_request()

    count = CheckInModel.get_loaded_check_ins(days)
    return jsonify(count)


@CheckInController.route('/distribution', methods=['GET'])
def route_get_checkout_distribution():
    check_ins = CheckInModel.get_checkout_distribution()
    return jsonify(check_ins)

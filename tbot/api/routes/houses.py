from flask import Blueprint, jsonify, request

from tbot.utils import list_house

house_api = Blueprint("house_api", __name__, url_prefix="/houses/")


@house_api.route("", methods=["GET"])
def root():
    if request.method == "GET":
        houses = list_house()
        data = [user.dict() for user in houses]
        return jsonify(data)

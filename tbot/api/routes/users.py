from flask import Blueprint, request, jsonify

from tbot.utils import list_user

user_api = Blueprint("user_api", __name__, url_prefix="/users/")


@user_api.route("", methods=["GET"])
def root():
    if request.method == "GET":
        users = list_user()
        data = [user.dict() for user in users]
        return jsonify(data)

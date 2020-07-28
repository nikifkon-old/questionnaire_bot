from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from tbot import schemas
from tbot.utils import create_event, delete_event, list_event, update_event

event_api = Blueprint("event_api", __name__, url_prefix="/events/")


@event_api.route("", methods=["GET", "PUT", "PATCH", "DELETE"])
def root():
    if request.method == "GET":
        events = list_event()
        data = [event.dict() for event in events]
        return jsonify(data)

    if not request.is_json:
        pass

    if request.method == "PUT":
        try:
            data = schemas.EventCreate(**request.json)
        except ValidationError as error:
            return error.json()
        data, status = create_event(data)
        return data, status

    if request.method == "PATCH":
        try:
            data = schemas.EventUpdate(**request.json)
        except ValidationError as error:
            return error.json()
        data, status = update_event(data)
        return data, status

    if request.method == "DELETE":
        try:
            id = request.json["id"]
        except KeyError:
            return jsonify(
                [{"loc": ["id"], "msg": "Missed required parameter"}])
        status = delete_event(id)
        return {}, status

from flask_restful import Resource, request

from .constants import HttpCodes
from .models import User, model_to_json


def make_response(data: dict, code: HttpCodes = HttpCodes.OK) -> tuple[dict, int]:
    return (data, code.value)


class Users(Resource):
    def get(self):
        users = [model_to_json(user) for user in User.select()]

        return make_response(users, HttpCodes.OK)

    def post(self):
        data = request.get_json(True)
        user = model_to_json(User.create(**data))

        return make_response(user, HttpCodes.CREATED)

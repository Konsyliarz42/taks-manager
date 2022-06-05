from flask_restful import Resource, request

from .constants import HttpCodes
from .forms import UserForm
from .models import User, model_to_json


def make_response(data: dict, code: HttpCodes = HttpCodes.OK):
    return (data, code.value)


class Users(Resource):
    @staticmethod
    def get():
        users = [model_to_json(user) for user in User.select()]
        return make_response(users, HttpCodes.OK)

    @staticmethod
    def post():
        data = request.get_json(True)
        form = UserForm(data=data)

        if form.validate():
            user = model_to_json(User.create(**data))
            return make_response(user, HttpCodes.CREATED)

        return make_response(form.errors, HttpCodes.BAD_REQUEST)

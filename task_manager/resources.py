from typing import Any, Union

from flask_restful import Resource as _Resource
from flask_restful import abort as _abort
from flask_restful import request
from werkzeug.security import generate_password_hash

from .constants import HttpCode
from .forms import TaskForm, UserForm
from .models import Task, User, model_to_json


def abort(code: HttpCode):
    _abort(code.value)


def make_response(data: dict, code: HttpCode = HttpCode.OK):
    return (data, code.value)


def get_or_404(model: Any, model_id: int) -> Union[User, Task]:
    records = model.select().where(model.id == model_id)
    return records[0] if records else abort(HttpCode.NOT_FOUND)


class Resource(_Resource):
    def whoami(self) -> str:
        return type(self).__name__


# ================================================================


class UserList(Resource):
    @staticmethod
    def get():
        users = [model_to_json(user) for user in User.select()]
        return make_response(users, HttpCode.OK)

    @staticmethod
    def post():
        data = request.get_json(True)
        form = UserForm(data=data)

        if form.validate():
            data["password"] = generate_password_hash(data["password"])
            user = model_to_json(User.create(**data))
            return make_response(user, HttpCode.CREATED)

        return make_response(form.errors, HttpCode.BAD_REQUEST)


class UserView(Resource):
    @staticmethod
    def get(user_id: int):
        user: User = get_or_404(User, user_id)
        user_json = model_to_json(user)

        return make_response(user_json, HttpCode.OK)


# ================================================================


class TaskList(Resource):
    @staticmethod
    def get():
        tasks = [model_to_json(task) for task in Task.select()]
        return make_response(tasks, HttpCode.OK)

    @staticmethod
    def post():
        data = request.get_json(True)
        data["status"] = Task().status  # When create it must be default
        form = TaskForm(data=data)

        if form.validate():
            task = model_to_json(Task.create(**data))
            return make_response(task, HttpCode.CREATED)

        return make_response(form.errors, HttpCode.BAD_REQUEST)


class TaskView(Resource):
    @staticmethod
    def get(task_id: int):
        task: Task = get_or_404(Task, task_id)
        task_json = model_to_json(task)

        return make_response(task_json, HttpCode.OK)

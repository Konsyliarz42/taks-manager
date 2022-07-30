from typing import Type, Union

from flask_restful import Resource
from flask_restful import abort as restful_abort
from flask_restful import request

from .constants import HttpCodes
from .forms import TaskForm, UserForm
from .models import Task, User, model_to_json


def abort(code: HttpCodes):
    restful_abort(code.value)


def make_response(data: dict, code: HttpCodes = HttpCodes.OK):
    return (data, code.value)


def get_or_404(model: Union[Type["User"], Type["Task"]], model_id: int) -> Union[User, Task]:
    records = model.select().where(model.id == model_id)
    return records[0] if records else abort(HttpCodes.NOT_FOUND)


# ================================================================


class UserList(Resource):
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


class UserView(Resource):
    @staticmethod
    def get(user_id: int):
        user: User = get_or_404(User, user_id)
        user_json = model_to_json(user)

        return make_response(user_json, HttpCodes.OK)


# ================================================================


class TaskList(Resource):
    @staticmethod
    def get():
        tasks = [model_to_json(task) for task in Task.select()]
        return make_response(tasks, HttpCodes.OK)

    @staticmethod
    def post():
        data = request.get_json(True)
        data["status"] = Task().status  # When create it must be default
        form = TaskForm(data=data)

        if form.validate():
            task = model_to_json(Task.create(**data))
            return make_response(task, HttpCodes.CREATED)

        return make_response(form.errors, HttpCodes.BAD_REQUEST)


class TaskView(Resource):
    @staticmethod
    def get(task_id: int):
        task: Task = get_or_404(Task, task_id)
        task_json = model_to_json(task)

        return make_response(task_json, HttpCodes.OK)

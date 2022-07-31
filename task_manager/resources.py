from typing import Any, Union

from flask_restful import Resource as _Resource
from flask_restful import abort, request
from werkzeug.security import generate_password_hash

from .constants import HttpCode
from .forms import AddTaskForm, AddUserForm
from .models import Task, User


def make_response(
    data: dict, code: HttpCode = HttpCode.OK
) -> tuple[dict[str, str], int]:
    "This method allow to use HTTP codes as enum type."
    return (data, code.value)


def make_response_bad_request(form: Any) -> tuple[dict[str, str], int]:
    "Returns the form's errors with `BAD_REQUEST` code."
    return make_response({"errors": form.errors}, HttpCode.BAD_REQUEST)


def get_or_404(model: Any, model_id: int) -> Union[User, Task]:
    try:
        record = model.get_by_id(model_id)
    except model.DoesNotExist:
        abort(HttpCode.NOT_FOUND)

    return record


class Resource(_Resource):
    def whoami(self) -> str:
        "This method was created for generate views in tests."
        return type(self).__name__


# ================================================================


class UserList(Resource):
    @staticmethod
    def get():
        users = [user.model_to_json() for user in User.select()]
        return make_response(users, HttpCode.OK)

    @staticmethod
    def post():
        data = request.get_json(True)
        form = AddUserForm(data=data)

        if form.validate():
            data["password"] = generate_password_hash(data["password"])
            user: User = User.create(**data)
            user_json = user.model_to_json()

            return make_response(user_json, HttpCode.CREATED)

        return make_response_bad_request(form)


class UserView(Resource):
    @staticmethod
    def get(user_id: int):
        user: User = get_or_404(User, user_id)
        user_json = user.model_to_json()

        return make_response(user_json, HttpCode.OK)

    @staticmethod
    def delete(user_id: int):
        user: User = get_or_404(User, user_id)

        if not user.is_active:
            abort(HttpCode.NOT_FOUND)

        user.is_active = False
        user.save()

        return make_response({}, HttpCode.OK)


# ================================================================


class TaskList(Resource):
    @staticmethod
    def get():
        tasks = [task.model_to_json() for task in Task.select()]
        return make_response(tasks, HttpCode.OK)

    @staticmethod
    def post():
        data = request.get_json(True)
        data["status"] = Task().status  # When create it must be default
        form = AddTaskForm(data=data)

        if form.validate():
            task: Task = Task.create(**data)
            task_json = task.model_to_json()

            return make_response(task_json, HttpCode.CREATED)

        return make_response_bad_request(form)


class TaskView(Resource):
    @staticmethod
    def get(task_id: int):
        task: Task = get_or_404(Task, task_id)
        task_json = task.model_to_json()

        return make_response(task_json, HttpCode.OK)

    @staticmethod
    def delete(task_id: int):
        task: Task = get_or_404(Task, task_id)
        task.delete_instance(True)

        return make_response({}, HttpCode.OK)

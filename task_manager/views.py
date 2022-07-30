from flask_restful import Resource

from .resources import TaskList, TaskView, UserList, UserView

API_VIEWS: dict[str, Resource] = {
    "/users/": UserList,
    "/user/<int:user_id>/": UserView,
    "/tasks/": TaskList,
    "/task/<int:task_id>/": TaskView,
}

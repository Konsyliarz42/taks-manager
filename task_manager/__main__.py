from argparse import ArgumentParser, MetavarTypeHelpFormatter

from . import api, app
from .resources import TaskList, TaskView, UserList, UserView


def main(host: str, port: int, debug: bool) -> None:
    api.add_resource(UserList, "/users/")
    api.add_resource(UserView, "/user/<int:user_id>/")

    api.add_resource(TaskList, "/tasks/")
    api.add_resource(TaskView, "/task/<int:task_id>/")

    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    parser = ArgumentParser(prog="task_manager")
    parser.set_defaults(cmd=parser.prog)
    subparsers = parser.add_subparsers()

    runserver_parser = subparsers.add_parser(
        "runserver",
        formatter_class=MetavarTypeHelpFormatter,
        description="Run flask server.",
    )
    runserver_parser.set_defaults(cmd=runserver_parser.prog)

    runserver_parser.add_argument(
        "--host",
        help="Server host | Default: 127.0.0.1",
        default="127.0.0.1",
        type=str,
        required=False,
    )
    runserver_parser.add_argument(
        "--port",
        help="Server port | Default: 5000",
        default=5000,
        type=int,
        required=False,
    )
    runserver_parser.add_argument(
        "--debug",
        help="Debug mode | Default: False",
        default=False,
        type=bool,
        required=False,
        choices=[True, False],
    )

    # --------------------------------

    args = parser.parse_args()
    main(host=args.host, port=args.port, debug=args.debug)

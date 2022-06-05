from argparse import ArgumentParser, MetavarTypeHelpFormatter
from datetime import date

from . import api, app, router
from .resources import TaskList, UserList


def main(host: str, port: int, debug: bool) -> None:
    api.add_resource(UserList, "/users/")
    api.add_resource(TaskList, "/tasks/")

    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    parser = ArgumentParser(prog="task_manager")
    parser.set_defaults(cmd=parser.prog)
    subparsers = parser.add_subparsers()

    # --------------------------------

    migrate_parser = subparsers.add_parser(
        "migrate",
        formatter_class=MetavarTypeHelpFormatter,
        description="Run all migrations or apply to selected migration.",
    )
    migrate_parser.set_defaults(cmd=migrate_parser.prog)

    migrate_parser.add_argument(
        "--selected-migration",
        help="Name of migration to apply",
        type=str,
        required=False,
    )

    # --------------------------------

    makemigrations_parser = subparsers.add_parser(
        "makemigrations",
        formatter_class=MetavarTypeHelpFormatter,
        description="Generate a new migration in your migrations folder or prepare template for your own migration.",
    )
    makemigrations_parser.set_defaults(cmd=makemigrations_parser.prog)

    makemigrations_parser.add_argument(
        "--migration-name",
        help="Name of migration | Default: migration_<date>",
        default=f"migrate_{date.today()}",
        type=str,
        required=False,
    )
    makemigrations_parser.add_argument(
        "--auto",
        help="Auto generated migration | Default: True",
        default=True,
        type=bool,
        required=False,
        choices=[True, False],
    )

    # --------------------------------

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

    if args.cmd == runserver_parser.prog:
        main(host=args.host, port=args.port, debug=args.debug)
    elif args.cmd == migrate_parser.prog:
        if args.selected_migration:
            router.run(name=args.selected_migration)
        else:
            router.run()
    elif args.cmd == makemigrations_parser.prog:
        router.create(
            name=args.migration_name,
            auto=args.auto,
        )
    else:
        parser.print_help()

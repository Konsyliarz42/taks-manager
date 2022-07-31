from argparse import ArgumentParser, MetavarTypeHelpFormatter

from . import app
from .models import BaseModel, db

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
    db.connect()
    db.create_tables(BaseModel.__subclasses__())
    app.run(host=args.host, port=args.port, debug=args.debug)
    db.close()

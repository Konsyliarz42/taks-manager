import re
from unittest import TestCase

from peewee import SqliteDatabase

from task_manager import api, app, views
from task_manager.models import BaseModel

MODELS = BaseModel.__subclasses__()
test_db = SqliteDatabase(":memory:")


def get_api_views():
    api_views = {}
    variable_pattern = re.compile(r"/<(.*)>/")

    for endpoint, resource in views.API_VIEWS.items():
        api_views[resource.whoami(resource())] = "/api" + re.sub(
            variable_pattern, "/{}/", endpoint
        )

    return api_views


class BasicTestCase(TestCase):
    class Config:
        TESTING = True
        DEBUG = True
        SECRET_KEY = "TestingSecretKey"
        ENV = "development"

    def setUp(self) -> None:
        app.config.from_object(BasicTestCase.Config())
        self.app = app
        self.api = api
        self.client = self.app.test_client()
        self.views = get_api_views()
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect(True)
        test_db.create_tables(MODELS)

    def tearDown(self) -> None:
        test_db.drop_tables(MODELS)
        test_db.close()

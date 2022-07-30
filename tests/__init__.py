import re
from unittest import TestCase

from task_manager import api, app, db, views
from task_manager.models import BaseModel


def get_all_views():
    all_views = {}
    variable_pattern = re.compile(r"/<(.*)>/")

    for endpoint, resource in views.API_VIEWS.items():
        all_views[resource.whoami(resource())] = "/api" + re.sub(
            variable_pattern, "/{}/", endpoint
        )

    return all_views


class BasicTestCase(TestCase):
    class Config:
        TESTING = True
        DATABASE_URL = ":memory:"
        SECRET_KEY = "TestingSecretKey"
        ENV = "development"

    def setUp(self) -> None:
        app.config.from_object(BasicTestCase.Config())
        self.app = app
        self.api = api
        self.client = self.app.test_client()
        self.views = get_all_views()

        self.tearDown()

    def tearDown(self) -> None:
        db.close()
        db.database = BasicTestCase.Config.DATABASE_URL
        db.connect()
        db.create_tables(BaseModel.__subclasses__())

from datetime import datetime

from werkzeug.test import TestResponse

from task_manager import constants
from task_manager.constants import HttpCode
from tests import BasicTestCase

# Use this variable to compare datetime
# Cut minutes and microseconds
MARKS_TO_CUT_DATETIME = 16
# Example:
# str(datetime.utcnow())[:MARKS_TO_CUT_DATETIME]
# 2022-07-31 17:36:43.046018 => 2022-07-31 17:36
USER_DATA = {
    "email": "test@test.com",
    "password": "testpassword",
    "confirm_password": "testpassword",
    "first_name": "Tester",
    "last_name": "Test",
}
TASK_DATA = {
    "title": "Test Task",
    "description": "This is a test task only for tests.",
    "assigned": None,
}


class AddUserFormTestCase(BasicTestCase):
    def post_response(self, data: dict) -> TestResponse:
        return self.client.post(self.views["UserList"], json=data)

    def test_correct_form(self):
        response = self.post_response(USER_DATA)
        assert response.status_code == HttpCode.CREATED

        # Check required fields in response
        assert "password" not in response.json
        assert "first_name" in response.json
        assert "last_name" in response.json
        assert "email" in response.json
        assert "is_admin" in response.json
        assert response.json["is_admin"] is False
        # TODO: Uncomment this assertion when add login mechanism
        # assert "is_active" not in response.json
        assert "registered_at" in response.json

        registered_at = response.json["registered_at"][:MARKS_TO_CUT_DATETIME]
        utc_now = str(datetime.utcnow())[:MARKS_TO_CUT_DATETIME]

        print(registered_at, utc_now)

        assert registered_at == utc_now

    # --------------------------------

    def test_emails_are_unique(self):
        json_data = USER_DATA.copy()
        response = self.post_response(json_data)
        assert response.status_code == HttpCode.CREATED

        response = self.post_response(json_data)
        assert response.status_code == HttpCode.BAD_REQUEST

    def test_email_is_valid(self):
        json_data = USER_DATA.copy()
        json_data["email"] = "xxxx@xxxx"
        response = self.post_response(json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_email_is_to_long(self):
        json_data = USER_DATA.copy()
        json_data["email"] = "x" * constants.STRING_FIELD_LENGTH["max"] + "x@test.com"
        response = self.post_response(json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_email_is_required(self):
        json_data = USER_DATA.copy()
        json_data.pop("email")
        response = self.post_response(json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    # --------------------------------

    def test_password_is_too_short(self):
        json_data = USER_DATA.copy()
        json_data["password"] = "x" * (constants.PASSWORD_FIELD_LENGTH["min"] - 1)
        response = self.post_response(json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_password_is_too_long(self):
        json_data = USER_DATA.copy()
        json_data["password"] = "x" * (constants.PASSWORD_FIELD_LENGTH["max"] + 1)
        response = self.post_response(json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_confirm_password_is_the_same_like_password(self):
        json_data = USER_DATA.copy()
        json_data["confirm_password"] = json_data["password"][::-1]
        response = self.post_response(json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_password_is_required(self):
        json_data = USER_DATA.copy()
        json_data.pop("password")
        response = self.post_response(json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_confirm_password_is_required(self):
        json_data = USER_DATA.copy()
        json_data.pop("confirm_password")
        response = self.post_response(json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    # --------------------------------

    def test_first_name_is_too_short(self):
        json_data = USER_DATA.copy()
        json_data["first_name"] = "x" * (constants.STRING_FIELD_LENGTH["min"] - 1)
        response = self.post_response(json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_first_name_is_too_long(self):
        json_data = USER_DATA.copy()
        json_data["first_name"] = "x" * (constants.STRING_FIELD_LENGTH["max"] + 1)
        response = self.post_response(json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_first_name_is_required(self):
        json_data = USER_DATA.copy()
        json_data.pop("first_name")
        response = self.post_response(json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    # --------------------------------

    def test_last_name_is_too_short(self):
        json_data = USER_DATA.copy()
        json_data["last_name"] = "x" * (constants.STRING_FIELD_LENGTH["min"] - 1)
        response = self.post_response(json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_last_name_is_too_long(self):
        json_data = USER_DATA.copy()
        json_data["last_name"] = "x" * (constants.STRING_FIELD_LENGTH["max"] + 1)
        response = self.post_response(json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_last_name_is_required(self):
        json_data = USER_DATA.copy()
        json_data.pop("last_name")
        response = self.post_response(json_data)

        assert response.status_code == HttpCode.BAD_REQUEST


# ================================================================


class AddTaskFormTestCase(BasicTestCase):
    def setUp(self) -> None:
        super().setUp()
        # Add User for tests
        self.client.post(self.views["UserList"], json=USER_DATA)

    def post_response(self, data: dict) -> TestResponse:
        return self.client.post(self.views["TaskList"], json=data)

    def test_correct_form(self):
        response = self.post_response(TASK_DATA)
        assert response.status_code == HttpCode.CREATED

        # Check required fields in response
        assert "title" in response.json
        assert "description" in response.json
        assert "status" in response.json
        assert "created_at" in response.json
        assert "assigned" in response.json

        created_at = response.json["created_at"][:MARKS_TO_CUT_DATETIME]
        utc_now = str(datetime.utcnow())[:MARKS_TO_CUT_DATETIME]

        assert created_at == utc_now

    # --------------------------------

    def test_title_is_too_short(self):
        json_data = TASK_DATA.copy()
        json_data["title"] = "x" * (constants.STRING_FIELD_LENGTH["min"] - 1)
        response = self.post_response(json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_title_is_too_long(self):
        json_data = TASK_DATA.copy()
        json_data["title"] = "x" * (constants.STRING_FIELD_LENGTH["max"] + 1)
        response = self.post_response(json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_title_is_required(self):
        json_data = TASK_DATA.copy()
        json_data.pop("title")
        response = self.post_response(json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    # --------------------------------

    def test_assigned_to_non_existing_user(self):
        json_data = TASK_DATA.copy()

        json_data["assigned"] = 2
        response = self.post_response(json_data)
        assert response.status_code == HttpCode.BAD_REQUEST

        json_data["assigned"] = 0
        response = self.post_response(json_data)
        assert response.status_code == HttpCode.BAD_REQUEST

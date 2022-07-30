from task_manager import constants
from task_manager.constants import HttpCode
from tests import BasicTestCase

JSON_DATA = {
    "email": "test@test.com",
    "password": "testpassword",
    "confirm_password": "testpassword",
    "first_name": "Test",
    "last_name": "Test",
}


class UserFormTestCase(BasicTestCase):
    def test_correct_form(self):
        response = self.client.post(self.views["UserList"], json=JSON_DATA)

        assert response.status_code == HttpCode.CREATED
        assert "password" not in response.json

    # --------------------------------

    def test_emails_are_unique(self):
        json_data = JSON_DATA.copy()
        response = self.client.post(self.views["UserList"], json=json_data)
        assert response.status_code == HttpCode.CREATED

        response = self.client.post(self.views["UserList"], json=json_data)
        assert response.status_code == HttpCode.BAD_REQUEST

    def test_email_is_valid(self):
        json_data = JSON_DATA.copy()
        json_data["email"] = "xxxx@xxxx"
        response = self.client.post(self.views["UserList"], json=json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_email_is_to_long(self):
        json_data = JSON_DATA.copy()
        json_data["email"] = "x" * constants.STRING_FIELD_LENGTH["max"] + "x@test.com"
        response = self.client.post(self.views["UserList"], json=json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_email_is_required(self):
        json_data = JSON_DATA.copy()
        json_data.pop("email")
        response = self.client.post(self.views["UserList"], json=json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    # --------------------------------

    def test_password_is_too_short(self):
        json_data = JSON_DATA
        json_data["password"] = "x" * (constants.PASSWORD_FIELD_LENGTH["min"] - 1)
        response = self.client.post(self.views["UserList"], json=json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_password_is_too_long(self):
        json_data = JSON_DATA
        json_data["password"] = "x" * (constants.PASSWORD_FIELD_LENGTH["max"] + 1)
        response = self.client.post(self.views["UserList"], json=json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_password_is_required(self):
        json_data = JSON_DATA
        json_data.pop("password")
        response = self.client.post(self.views["UserList"], json=json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    # --------------------------------

    def test_first_name_is_too_short(self):
        json_data = JSON_DATA
        json_data["first_name"] = "x" * (constants.STRING_FIELD_LENGTH["min"] - 1)
        response = self.client.post(self.views["UserList"], json=json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_first_name_is_too_long(self):
        json_data = JSON_DATA
        json_data["first_name"] = "x" * (constants.STRING_FIELD_LENGTH["max"] + 1)
        response = self.client.post(self.views["UserList"], json=json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_first_name_is_required(self):
        json_data = JSON_DATA
        json_data.pop("first_name")
        response = self.client.post(self.views["UserList"], json=json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    # --------------------------------

    def test_last_name_is_too_short(self):
        json_data = JSON_DATA
        json_data["last_name"] = "x" * (constants.STRING_FIELD_LENGTH["min"] - 1)
        response = self.client.post(self.views["UserList"], json=json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_last_name_is_too_long(self):
        json_data = JSON_DATA
        json_data["last_name"] = "x" * (constants.STRING_FIELD_LENGTH["max"] + 1)
        response = self.client.post(self.views["UserList"], json=json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

    def test_last_name_is_required(self):
        json_data = JSON_DATA
        json_data.pop("last_name")
        response = self.client.post(self.views["UserList"], json=json_data)

        assert response.status_code == HttpCode.BAD_REQUEST

from task_manager.constants import HttpCodes
from tests import BasicTestCase


class UserFormTestCase(BasicTestCase):
    def test_correct_add_new_user(self):
        json_data = {
            "email": "test@test.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "Test",
        }

        response = self.client.post(self.views["UserList"], json=json_data)
        assert response.status_code == HttpCodes.CREATED.value
        assert "password" not in response.json

    def test_emails_are_unique(self):
        json_data = {
            "email": "test@test.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "Test",
        }

        response = self.client.post(self.views["UserList"], json=json_data)
        assert response.status_code == HttpCodes.CREATED.value

        response = self.client.post(self.views["UserList"], json=json_data)
        assert response.status_code == HttpCodes.BAD_REQUEST.value

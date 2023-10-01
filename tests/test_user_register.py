import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
class TestUserRegister(BaseCase):
    def setup_method(self):
        self.base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{self.base_part}{random_part}@{domain}"

    def test_create_user_successfuly(self):
        data = {
            'password': '123',
            'username': self.base_part,
            'firstName': self.base_part,
            'lastName': self.base_part,
            'email': self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        #assert response.status_code == 200, f"Unexpected status code {response.status_code}"
        Assertions.assert_code_status(response, 200)
        print(response.content)

        expected_keys = ["id"]
        Assertions.assert_json_has_keys(response, expected_keys)


    def test_create_user_with_exist_email(self):
        url_user_c = "https://playground.learnqa.ru/api/user/"
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post(url_user_c, data=data)

        #print(response.status_code)
        #print(response.content)
        #assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"






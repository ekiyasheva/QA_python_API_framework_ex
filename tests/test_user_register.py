import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
class TestUserRegister(BaseCase):
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
        assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

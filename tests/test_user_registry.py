from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):

    def test_create_user_successfuly(self):
        data = self.prepare_registration_data()

        #response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        response = MyRequests.post("/user", data=data)

        #assert response.status_code == 200, f"Unexpected status code {response.status_code}"
        Assertions.assert_code_status(response, 200)
        print(response.content)

        expected_keys = ["id"]
        Assertions.assert_json_has_keys(response, expected_keys)


    def test_create_user_with_exist_email(self):
        #url_user_c = "https://playground.learnqa.ru/api/user/"
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        #response = requests.post(url_user_c, data=data)
        response = MyRequests.post("/user", data=data)

        #print(response.status_code)
        #print(response.content)
        #assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"






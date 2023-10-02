from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserGet(BaseCase):

    def test_get_user_details_not_auth(self):

        #response = requests.get("https://playground.learnqa.ru/api/user/2")
        response = MyRequests.get("/user/2")
        #print(response.content)

        expected_fields = ["username"]

        Assertions.assert_json_has_keys(response, expected_fields)
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        #response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        #response2 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        expected_fields1 = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields1)

    def test_get_user_details_another_user(self):
        #index = 1
        #list_id: list = []
        #for index in range (1, 100):
        #    response = MyRequests.get(f"/user/{index}")
        #    print(f"check user id {index}: response {response.text}")

        #    if response.text != "User not found":
        #        print(f"FIND USER in user id {index}!: {response.json()['username']}")

        #    index = index+1
        #response_data: list = BaseCase.authorization(self, "vinkotov@example.com", "1234")
        #print(response_data)

        expected_key_login: list = [
            ("id"),
            ("username"),
            ("email"),
            ("firstName"),
            ("lastName")
        ]
        response = BaseCase.authorization(self, "vinkotov@example.com", "1234")
        Assertions.assert_json_has_keys(response, expected_key_login)

        response2 = MyRequests.get("/user/2")
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_keys(response2, ["username"])
        Assertions.assert_json_has_not_key(response2,"id")





















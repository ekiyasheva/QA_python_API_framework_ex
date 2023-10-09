from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserGet(BaseCase):

    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        #print(response.content)

        expected_fields = ["username"]
        Assertions.assert_json_has_keys(response, expected_fields)
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        #PRECONDITION
        #== login
        log_data = self.api_login_user('vinkotov@example.com', '1234')
        #print(f"LOG DATA{log_data}")

        # TEST
        response_get = MyRequests.get(
            f"/user/{log_data.get('u_user_id')}",
            headers={"x-csrf-token": log_data.get('u_header')},
            cookies={"auth_sid": log_data.get('u_cookie')}
        )
        expected_fields1 = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response_get, expected_fields1)


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

        #PRECONDITION
        #== login
        log_data = self.api_login_user('vinkotov@example.com', '1234')
        #print(f"LOG DATA{log_data}")

        response2 = MyRequests.get("/user/2")
        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_keys(response2, ["username"])
        Assertions.assert_json_has_not_key(response2,"id")





















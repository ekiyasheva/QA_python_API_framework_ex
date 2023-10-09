import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    invalid_data_for_edit = [
        ({"firstName": BaseCase.random_string_t_len(1),
          "ErrorMessage": "{\"error\":\"Too short value for field firstName\"}"}),
        ({"email": "edit_email.example.com",
          "ErrorMessage": "Invalid email format"})
    ]

    def setup_method(self):
        self.registry_data = self.prepare_registration_data()


    def test_edit_just_created_user_lesson(self):
        # REGISTRY
        response1 = MyRequests.post("/user", data=self.registry_data)

        Assertions.assert_code_status(response1, 200)
        key_uid = ["id"]
        Assertions.assert_json_has_keys(response1, key_uid)

        email = self.registry_data['email']
        password = self.registry_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_name = "Change Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}

        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of user after edit"
        )

    def test_edit_unauthorized_user(self):
        response = MyRequests.put("/user/2", self.registry_data)

        Assertions.assert_code_status(response, 400)
        assert response.text == "Auth token not supplied", f"Unexpected response {response.text}"


    def test_edit_data_another_user(self):
        #PRECONDITION
        #== login
        log_data = self.api_login_user('vinkotov@example.com', '1234')
        #print(f"LOG DATA{log_data}")

        #TEST
        response_edit = MyRequests.put("/user/1", data=self.registry_data)
        Assertions.assert_code_status(response_edit, 400)
        assert response_edit.text == "Auth token not supplied", f"Unexpected response {response_edit.text}"


    @pytest.mark.parametrize('invalid_data', invalid_data_for_edit)
    def test_edit_user_on_invalid_data(self, invalid_data):
        # PRECONDITION
        #== registration
        reg_data = self.api_create_user()
        #print(f"REG DATA: {reg_data}")
        #== login
        log_data = self.api_login_user(reg_data.get("u_email"), reg_data.get("u_password"))
        #print(f"LOG DATA{log_data}")

        # TEST: edit firstName for invalid
        data = invalid_data

        response_edit = MyRequests.put(
            f"/user/{log_data.get('u_user_id')}",
            headers={"x-csrf-token": log_data.get('u_header')},
            cookies={"auth_sid": log_data.get('u_cookie')},
            data=data)
        #print(response_edit.text)

        Assertions.assert_code_status(response_edit, 400)
        assert response_edit.text == data.get("ErrorMessage"), \
            f"Unexpected response {response_edit.text}"
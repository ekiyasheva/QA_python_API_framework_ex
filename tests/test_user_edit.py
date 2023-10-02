from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTRY
        registry_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user", data=registry_data)

        Assertions.assert_code_status(response1, 200)
        key_uid = ["id"]
        Assertions.assert_json_has_keys(response1, key_uid)

        email = registry_data['email']
        password = registry_data['password']
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

    def test_edit_anauthorized_user(self):
        data_int = self.prepare_registration_data()
        response = MyRequests.put("/user/2", data_int)

        Assertions.assert_code_status(response, 400)
        assert response.text == "Auth token not supplied", f"Unexpected response {response.text}"


    def test_edit_data_another_user(self):
        #PRECONDITION
        response_login = self.authorization('vinkotov@example.com', '1234')

        Assertions.assert_code_status(response_login, 200)
        Assertions.assert_json_has_keys(response_login, ["id", "username", "email", "firstName", "lastName"])

        #TEST
        data_int = self.prepare_registration_data()
        response_edit = MyRequests.put("/user/2", data_int)

        Assertions.assert_code_status(response_edit, 400)
        assert response_edit.text == "Auth token not supplied", f"Unexpected response {response_edit.text}"

    def test_edit_user_invalid_email(self):
        # REGISTRY
        registry_data = self.prepare_registration_data()
        response_reg = MyRequests.post("/user", data=registry_data)

        Assertions.assert_code_status(response_reg, 200)
        Assertions.assert_json_has_keys(response_reg, ["id"])
        u_id = response_reg.json()["id"]
        u_email = registry_data.get("email")
        u_password = registry_data.get("password")

        #print(f"RESPONSE CODE REG: {response_reg.status_code}")
        #print(f"CONTENT REG: {response_reg.content}")
        #print(f"COOKIE REG: {response_reg.cookies.get('auth_sid')}")
        #print(f"HEADER REG: {response_reg.headers.get('x-csrf-token')}")
        #print(f"USER ID: {u_id}")
        #print(f"EMAIL: {u_email}")
        #print(f"PASSWORD: {u_password}")

        # LOGIN
        response_login = MyRequests.post("/user/login", data={"email": u_email, "password": u_password})

        #print(f"RESPONSE CODE LOG: {response_login.status_code}")
        #print(f"CONTENT LOG: {response_login.content}")
        #print(f"COOKIE LOG: {response_login.cookies.get('auth_sid')}")
        #print(f"HEADER LOG: {response_login.headers.get('x-csrf-token')}")

        Assertions.assert_code_status(response_login, 200)
        Assertions.assert_json_has_keys(response_login, ["user_id"])
        u_cookie = response_login.cookies.get("auth_sid")
        u_header = response_login.headers.get("x-csrf-token")

        # EDIT  EMAIL for INVALID
        data = {
            "email": "edit_email.example.com"
        }
        response_edit = MyRequests.put(
            f"/user/{u_id}",
            headers={"x-csrf-token": u_header},
            cookies={"auth_sid": u_cookie},
            data=data)
        #print(response_edit.url)
        #print(response_edit.status_code)
        #print(response_edit.text)

        Assertions.assert_code_status(response_edit, 400)
        assert response_edit.text == "Invalid email format", f"Unexpected response {response_edit.text}"


    def test_edit_user_invalid_first_name(self):
        # REGISTRY
        registry_data = self.prepare_registration_data()
        response_reg = MyRequests.post("/user", data=registry_data)

        Assertions.assert_code_status(response_reg, 200)
        Assertions.assert_json_has_keys(response_reg, ["id"])
        u_id = response_reg.json()["id"]
        u_email = registry_data.get("email")
        u_password = registry_data.get("password")

        #print(f"RESPONSE CODE REG: {response_reg.status_code}")
        #print(f"CONTENT REG: {response_reg.content}")
        #print(f"COOKIE REG: {response_reg.cookies.get('auth_sid')}")
        #print(f"HEADER REG: {response_reg.headers.get('x-csrf-token')}")
        #print(f"USER ID: {u_id}")
        #print(f"EMAIL: {u_email}")
        #print(f"PASSWORD: {u_password}")

        # LOGIN
        response_login = MyRequests.post("/user/login", data={"email": u_email, "password": u_password})

        #print(f"RESPONSE CODE LOG: {response_login.status_code}")
        #print(f"CONTENT LOG: {response_login.content}")
        #print(f"COOKIE LOG: {response_login.cookies.get('auth_sid')}")
        #print(f"HEADER LOG: {response_login.headers.get('x-csrf-token')}")

        Assertions.assert_code_status(response_login, 200)
        Assertions.assert_json_has_keys(response_login, ["user_id"])
        u_cookie = response_login.cookies.get("auth_sid")
        u_header = response_login.headers.get("x-csrf-token")

        # EDIT  FIRST NAME for invalid
        data = {
            "firstName": self.random_string_t_len(1)
        }
        response_edit = MyRequests.put(
            f"/user/{u_id}",
            headers={"x-csrf-token": u_header},
            cookies={"auth_sid": u_cookie},
            data=data)
        #print(response_edit.url)
        #print(response_edit.status_code)
        #print(response_edit.text)

        Assertions.assert_code_status(response_edit, 400)
        assert response_edit.text == "{\"error\":\"Too short value for field firstName\"}", f"Unexpected response {response_edit.text}"


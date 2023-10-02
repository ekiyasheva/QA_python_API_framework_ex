import pytest

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):
    exclude_params = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]

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

    def test_create_user_with_incorrect_email(self):
        email = f"{self.random_str_w_date()}.example.com"
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user", data=data)

        #print(response.status_code)
        #print(response.content)
        #print(response.text)

        Assertions.assert_code_status(response, 400)
        assert response.text == "Invalid email format", f"Unexpected response '{response.text}'"

    @pytest.mark.parametrize('condition', exclude_params)
    def test_create_user_without_parameters(self, condition):
        data_ext = self.prepare_registration_data()
        u_password = data_ext.get("password")
        u_username = data_ext.get("username")
        u_first_name = data_ext.get("firstName")
        u_last_name = data_ext.get("lastName")
        u_email = data_ext.get("email")

        #print(u_password)
        if condition == "password":
            data= {
                "username": u_username,
                "firstName": u_first_name,
                "lastName": u_last_name,
                "email": u_email
            }
        elif condition == "username":
            data = {
                "password": u_password,
                "firstName": u_first_name,
                "lastName": u_last_name,
                "email": u_email
            }
        elif condition == "firstName":
            data = {
                "password": u_password,
                "username": u_username,
                "lastName": u_last_name,
                "email": u_email
            }
        elif condition == "lastName":
            data = {
                "password": u_password,
                "username": u_username,
                "firstName": u_first_name,
                "email": u_email
            }
        elif condition == "email":
            data = {
                "password": u_password,
                "username": u_username,
                "firstName": u_first_name,
                "lastName": u_last_name
            }
        else:
            data = data_ext

        response = MyRequests.post("/user", data=data)

        #print(response.url)
        #print(response.status_code)
        #print(response.content)
        #print(response.text)

        Assertions.assert_code_status(response, 400)
        assert response.text == f"The following required params are missed: {condition}", \
            f"Unexpected response {response.text}"

    def test_create_user_short_username(self):
        u_username = self.random_string_t_len(1)
        data_ext = self.prepare_registration_data()
        data_int = {
            "password": data_ext.get("password"),
            "username": u_username,
            "firstName": data_ext.get("firstName"),
            "lastName": data_ext.get("lastName"),
            "email": data_ext.get("email")
        }
        #print(data_int)

        response = MyRequests.post("/user", data=data_int)
        #print(response.status_code)
        #print(response.text)
        #print(response.content)

        Assertions.assert_code_status(response, 400)
        assert response.text == "The value of 'username' field is too short", \
            f"Unexpected response {response.text}"

    def test_create_user_long_username(self):

        u_username = self.random_string_t_len(251)
        data_ext = self.prepare_registration_data()
        data_int = {
            "password": data_ext.get("password"),
            "username": u_username,
            "firstName": data_ext.get("firstName"),
            "lastName": data_ext.get("lastName"),
            "email": data_ext.get("email")
        }
        #print(data_int)

        response = MyRequests.post("/user", data=data_int)
        #print(response.status_code)
        #print(response.text)
        #print(response.content)

        Assertions.assert_code_status(response, 400)
        assert response.text == "The value of 'username' field is too long", f"Unexpected response {response.text}"





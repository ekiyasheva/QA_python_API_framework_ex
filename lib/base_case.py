import json.decoder
import random
import string

import requests.exceptions
from requests import Response
from datetime import datetime
from lib.my_requests import MyRequests


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Can't find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Can't find header with name {headers_name} in the last response"
        return response.headers[headers_name]
    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON formmat. Response test is {response.text}"
        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        return response_as_dict[name]



    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = self.random_str_w_date()
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': self.random_string_t_len(8),
            'username': self.random_string_t_len(15),
            'firstName': self.random_string_t_len(10),
            'lastName': self.random_string_t_len(10),
            'email': email
        }

    def random_str_w_date(self):
        random_str = datetime.now().strftime("%m%d%Y%H%M%S")
        return random_str

    @staticmethod
    def random_string_t_len(str_size: int):
        chars = string.ascii_letters
        return ''.join(random.choice(chars) for x in range(str_size))


    def api_create_user(self):
        registry_data = self.prepare_registration_data()
        try:
            response_reg = MyRequests.post("/user", data=registry_data)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        return_data = {
            "u_id": response_reg.json()["id"],
            "u_email": registry_data.get("email"),
            "u_password": registry_data.get("password")
        }

        return return_data

    def api_login_user(self, u_email: str, u_password: str):
        try:
            response_log = MyRequests.post("/user/login", data={"email": u_email, "password": u_password})
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        return_data = {
            "u_user_id": response_log.json()["user_id"],
            "u_cookie": response_log.cookies.get('auth_sid'),
            "u_header": response_log.headers.get('x-csrf-token')
        }

        return return_data







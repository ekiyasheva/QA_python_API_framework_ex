import json.decoder
import random
import string

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
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

    def random_str_w_date(self):
        random_str = datetime.now().strftime("%m%d%Y%H%M%S")
        return random_str

    def random_string_t_len(self, str_size):
        chars = string.ascii_letters
        return ''.join(random.choice(chars) for x in range(str_size))

    def authorization(self, email: str = None, password: str = None):
        data = {}
        if email is None and password is None:
            data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }
        elif email is not None and password is not None:
            data = {
                'email': email,
                'password': password
            }
        else:
            print("INVALID DATA: input email and password")

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        return response2






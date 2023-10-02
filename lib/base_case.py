import json.decoder
import random
import string

from requests import Response
from datetime import datetime


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





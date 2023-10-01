import requests

class TestCookies:

    def test_cokie_method_request(self):
        url_homework_cookie = "https://playground.learnqa.ru/api/homework_cookie"
        response_cookie = requests.get(url_homework_cookie)
        print(f"PRINT: your cookie is {dict(response_cookie.cookies)}")

        assert_cookie = response_cookie.cookies.get("HomeWork")
        assert assert_cookie == "hw_value", f"This cookie  'HomeWork'='{assert_cookie}', but expected 'HomeWork'='hw_value'"




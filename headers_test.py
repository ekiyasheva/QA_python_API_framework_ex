import requests

class TestHeaders:

    def test_header_method_request(self):
        url_homework_header = "https://playground.learnqa.ru/api/homework_header"
        response_header = requests.get(url_homework_header)
        print(f"PRINT: your header is {dict(response_header.headers)}")

        assert_header = response_header.headers.get("x-secret-homework-header")
        assert assert_header == "Some secret value", f"This header  'x-secret-homework-header'='{assert_header}', but expected 'x-secret-homework-header'='Some secret value'"


import pytest
import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("Работа с пользователем")
@allure.feature("Регистрация пользователя")
@allure.parent_suite("Тесты на регистрацию пользователя")
class TestUserRegister(BaseCase):
    exclude_params = [
        ("password"),
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]

    @allure.title("Успешное создание пользователя")
    @allure.description("Создание пользователя. Проверка корректности ответа от сервера.")
    def test_create_user_successfuly(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_keys(response, ["id"])
        #print(response.content)


    @allure.title("Ошибка регистрации пользователя - емейл дубликат")
    @allure.description("Попытка создать пользователя с уже существующим емейлом. Проверка сообщения об ошибке")
    def test_create_user_with_exist_email(self):
        data = self.prepare_registration_data('vinkotov@example.com')
        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email 'vinkotov@example.com' already exists", \
            f"Unexpected response content {response.content}"
        #print(response.status_code)
        #print(response.content)


    @allure.title("Ошибка регистрации пользователя - неверный формат емейла")
    @allure.description("Попытка создать пользователя с некорректным емейлом. Проверка сообщения об ошибке")
    def test_create_user_with_incorrect_email(self):
        data = self.prepare_registration_data(f"{self.random_str_w_date()}.example.com")
        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.text == "Invalid email format", \
            f"Unexpected response '{response.text}'"
        #print(response.status_code)
        #print(response.content)
        #print(response.text)


    @pytest.mark.parametrize('condition', exclude_params)
    @allure.title("Ошибка регистрации пользователя - нет обязательного параметра")
    @allure.description("Попытка создать пользователя без одного из обязательных параметров. Проверка сообщения об ошибке")
    def test_create_user_without_parameters(self, condition):
        data_ext = self.prepare_registration_data()
        u_password = data_ext.get("password")
        u_username = data_ext.get("username")
        u_first_name = data_ext.get("firstName")
        u_last_name = data_ext.get("lastName")
        u_email = data_ext.get("email")

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

        Assertions.assert_code_status(response, 400)
        assert response.text == f"The following required params are missed: {condition}", \
            f"Unexpected response {response.text}"
        #print(response.url)
        #print(response.status_code)
        #print(response.content)
        #print(response.text)

    @allure.title("Ошибка регистрации пользователя - недопустимо короткое имя")
    @allure.description("Попытка создать пользователя с именем из одной буквы. Проверка сообщения об ошибке")
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
        Assertions.assert_code_status(response, 400)
        assert response.text == "The value of 'username' field is too short", \
            f"Unexpected response {response.text}"
        # print(response.status_code)
        # print(response.text)
        # print(response.content)

    @allure.title("Ошибка регистрации пользователя - недопустимо длиное имя")
    @allure.description("Попытка создать пользователя с именем из 251 буквы. Проверка сообщения об ошибке")
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

        Assertions.assert_code_status(response, 400)
        assert response.text == "The value of 'username' field is too long", \
            f"Unexpected response {response.text}"
        #print(response.status_code)
        #print(response.text)
        #print(response.content)





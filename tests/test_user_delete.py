from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):

    def test_delete_user_impossible_to_remove(self):
        # PRECONDITION
        #== login
        log_data = self.api_login_user('vinkotov@example.com', '1234')
        #print(f"LOG DATA{log_data}")

        # TEST
        response_del = MyRequests.delete(
            f"/user/{log_data.get('u_user_id')}",
            headers={"x-csrf-token": log_data.get('u_header')},
            cookies={"auth_sid": log_data.get('u_cookie')}
        )

        Assertions.assert_code_status(response_del, 400)
        assert response_del.text == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", f"Unexpected response {response_del.text}"
        #print(f"RESPONSE CODE LOG: {response_del.status_code}")
        #print(f"CONTENT LOG: {response_del.content}")
        #print(f"COOKIE LOG: {response_del.cookies.get('auth_sid')}")
        #print(f"HEADER LOG: {response_del.headers.get('x-csrf-token')}")


    def test_delete_user(self):
        # PRECONDITION
        #== registration
        reg_data = self.api_create_user()
        #print(f"REG DATA: {reg_data}")
        #== login
        log_data = self.api_login_user(reg_data.get("u_email"), reg_data.get("u_password"))
        #print(f"LOG DATA{log_data}")

        # TEST
        #== get existing user
        response_get = MyRequests.get(
            f"/user/{log_data.get('u_user_id')}",
            headers={"x-csrf-token": log_data.get('u_header')},
            cookies={"auth_sid": log_data.get('u_cookie')}
        )
        Assertions.assert_code_status(response_get, 200)
        Assertions.assert_json_has_keys(response_get, ["id", "username", "email", "firstName", "lastName"])
        #print(f"RESPONSE CODE GET: {response_get.status_code}")
        #print(f"CONTENT GET: {response_get.content}")
        #print(f"COOKIE GET: {response_get.cookies.get('auth_sid')}")
        #print(f"HEADER GET: {response_get.headers.get('x-csrf-token')}")

        #== delete user
        response_del = MyRequests.delete(
            f"/user/{log_data.get('u_user_id')}",
            headers={"x-csrf-token": log_data.get('u_header')},
            cookies={"auth_sid": log_data.get('u_cookie')}
        )
        Assertions.assert_code_status(response_del, 200)
        #print(f"RESPONSE CODE DEL: {response_del.status_code}")
        #print(f"CONTENT DEL: {response_del.content}")
        #print(f"COOKIE DEL: {response_del.cookies.get('auth_sid')}")
        #print(f"HEADER DEL: {response_del.headers.get('x-csrf-token')}")

        #== get deleted user
        response_get_del = MyRequests.get(
            f"/user/{log_data.get('u_user_id')}",
            headers={"x-csrf-token": log_data.get('u_header')},
            cookies={"auth_sid": log_data.get('u_cookie')}
        )
        Assertions.assert_code_status(response_get_del, 404)
        assert response_get_del.text == "User not found", f"Unexpected response {response_get_del.text}"
        #print(f"RESPONSE CODE GET: {response_get_del.status_code}")
        #print(f"CONTENT GET: {response_get_del.content}")
        #print(f"COOKIE GET: {response_get_del.cookies.get('auth_sid')}")
        #print(f"HEADER GET: {response_get_del.headers.get('x-csrf-token')}")



    def test_delete_another_user(self):
        # REGISTER USER - 1
        registry_data1 = self.prepare_registration_data()
        response_reg1 = MyRequests.post("/user", data=registry_data1)

        Assertions.assert_code_status(response_reg1, 200)
        Assertions.assert_json_has_keys(response_reg1, ["id"])
        u_id_1 = response_reg1.json()["id"]
        u_email_1 = registry_data1.get("email")
        u_password_1 = registry_data1.get("password")
        #print(f"RESPONSE CODE REG_NEW_1: {response_reg1.status_code}")
        #print(f"CONTENT REG_NEW_1: {response_reg1.content}")
        #print(f"COOKIE REG_NEW_1: {response_reg1.cookies.get('auth_sid')}")
        #print(f"HEADER REG_NEW_1: {response_reg1.headers.get('x-csrf-token')}")
        #print(f"USER ID_NEW_1: {u_id_1}")
        #print(f"EMAIL_NEW_1: {u_email_1}")
        #print(f"PASSWORD_NEW_1: {u_password_1}")


        # LOGIN USER - 1
        login_data1 = {
            'email': u_email_1,
            'password': u_password_1
        }
        response_login1 = MyRequests.post("/user/login", data=login_data1)

        Assertions.assert_code_status(response_login1, 200)
        Assertions.assert_json_has_keys(response_login1, ["user_id"])
        u_cookie_1 = response_login1.cookies.get('auth_sid')
        u_header_1 = response_login1.headers.get('x-csrf-token')
        #print(f"RESPONSE CODE LOG_1: {response_login1.status_code}")
        #print(f"CONTENT LOG_1: {response_login1.content}")
        #print(f"COOKIE LOG_1: {response_login1.cookies.get('auth_sid')}")
        #print(f"HEADER LOG_1: {response_login1.headers.get('x-csrf-token')}")


        # REGISTER USER - 2
        registry_data2 = self.prepare_registration_data()
        response_reg2 = MyRequests.post("/user", data=registry_data2)

        Assertions.assert_code_status(response_reg2, 200)
        Assertions.assert_json_has_keys(response_reg2, ["id"])
        u_id_2 = response_reg2.json()["id"]
        u_email_2 = registry_data2.get("email")
        u_password_2 = registry_data2.get("password")
        #print(f"RESPONSE CODE REG_NEW_2: {response_reg1.status_code}")
        #print(f"CONTENT REG_NEW_2: {response_reg1.content}")
        #print(f"COOKIE REG_NEW_2: {response_reg1.cookies.get('auth_sid')}")
        #print(f"HEADER REG_NEW_2: {response_reg1.headers.get('x-csrf-token')}")
        #print(f"USER ID_NEW_2: {u_id_1}")
        #print(f"EMAIL_NEW_2: {u_email_1}")
        #print(f"PASSWORD_NEW_2: {u_password_1}")


        # LOGIN USER - 2
        login_data2 = {
            'email': u_email_2,
            'password': u_password_2
        }
        response_login2 = MyRequests.post("/user/login", data=login_data2)

        Assertions.assert_code_status(response_login2, 200)
        Assertions.assert_json_has_keys(response_login2, ["user_id"])
        u_cookie_2 = response_login2.cookies.get('auth_sid')
        u_header_2 = response_login2.headers.get('x-csrf-token')
        #print(f"RESPONSE CODE LOG_2: {response_login2.status_code}")
        #print(f"CONTENT LOG_2: {response_login2.content}")
        #print(f"COOKIE LOG_2: {response_login2.cookies.get('auth_sid')}")
        #print(f"HEADER LOG_2: {response_login2.headers.get('x-csrf-token')}")


        # DELETE USER w ID - USER 1 and HEADER & COOKIES USER 2
        id_del = u_id_1
        response_del = MyRequests.delete(
            f"/user/{id_del}",
            headers={"x-csrf-token": u_header_2},
            cookies={"auth_sid": u_cookie_2})

        Assertions.assert_code_status(response_del, 400)
        assert response_del.text == f"Auth token incorrect, you must log in as user ID {id_del}", \
            f"Unexpected response {response_del.text}"
        #print(f"RESPONSE CODE DEL: {response_del.status_code}")
        #print(f"CONTENT DEL: {response_del.content}")
        #print(f"COOKIE DEL: {response_del.cookies.get('auth_sid')}")
        #print(f"HEADER DEL: {response_del.headers.get('x-csrf-token')}")
        #assert u_id_1 != u_id_2, "Registration error - User_id must be unique"


        # GET USER IFO  - 1,2
        response_get_1 = MyRequests.get(f"/user/{u_id_1}", headers={"x-csrf-token": u_header_1}, cookies={"auth_sid": u_cookie_1})

        Assertions.assert_code_status(response_get_1, 200)
        Assertions.assert_json_has_keys(response_get_1, ["id", "username", "email", "firstName", "lastName"])
        #print(f"RESPONSE CODE GET-1: {response_get_1.status_code}")
        #print(f"CONTENT GET-1: {response_get_1.content}")
        #print(f"COOKIE GET-1: {response_get_1.cookies.get('auth_sid')}")
        #print(f"HEADER GET-1: {response_get_1.headers.get('x-csrf-token')}")


        response_get_2 = MyRequests.get(f"/user/{u_id_2}", headers={"x-csrf-token": u_header_2}, cookies={"auth_sid": u_cookie_2})

        Assertions.assert_code_status(response_get_2, 200)
        Assertions.assert_json_has_keys(response_get_2, ["id","username","email","firstName","lastName"])
        #print(f"RESPONSE CODE GET-2: {response_get_2.status_code}")
        #print(f"CONTENT GET-2: {response_get_2.content}")
        #print(f"COOKIE GET-2: {response_get_2.cookies.get('auth_sid')}")
        #print(f"HEADER GET-2: {response_get_2.headers.get('x-csrf-token')}")









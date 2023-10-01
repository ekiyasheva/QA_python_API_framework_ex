import json
import requests
import pytest

class TestUserAgent:

    uas = [
        '{"User_Agent": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30", "platform": "Mobile", "browser": "No", "device": "Android"}',
        '{"User_Agent": "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1", "platform": "Mobile", "browser": "Chrome", "device": "iOS"}',
        '{"User_Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)", "platform": "Googlebot", "browser": "Unknown", "device": "Unknown"}',
        '{"User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0", "platform": "Web", "browser": "Chrome", "device": "No"}',
        '{"User_Agent": "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1", "platform": "Mobile", "browser": "No", "device": "iPhone"}'
    ]

    @pytest.mark.parametrize('ua', uas)
    def test_user_agent(self, ua):

        url_ua = "https://playground.learnqa.ru/ajax/api/user_agent_check"

        json_ua = json.loads(ua)
        user_agent_ua = json_ua["User_Agent"]
        platform_ua = json_ua["platform"]
        browser_ua = json_ua["browser"]
        device_ua = json_ua["device"]
        #print(user_agent_ua)
        #print(platform_ua)
        #print(browser_ua)
        #print(device_ua)

        response = requests.get(url_ua, headers={"User-Agent": user_agent_ua})
        platform_resp = response.json()["platform"]
        browser_resp = response.json()["browser"]
        device_resp = response.json()["device"]
        #print(response.json())
        #print(platform_resp)
        #print(browser_resp)
        #print(device_resp)

        # Check PLATFORM
        assert platform_resp != "", f"NONE PLATFORM: in User-Agent '{user_agent_ua}' absent PLATFORM {platform_resp}"
        assert platform_resp == platform_ua, f"FAIL PLATFORM: in User-Agent '{user_agent_ua}', expected '{platform_ua}', but '{platform_resp}'"
        # Check BROWSER
        assert browser_resp != "", f"NONE BROWSER: in User-Agent '{user_agent_ua}' absent BROWSER {browser_resp}"
        assert browser_resp == browser_ua, f"FAIL BROWSER: in User-Agent '{user_agent_ua}', expected '{browser_ua}', but '{browser_resp}'"
        # Check DEVICE
        assert device_resp != "" f"NONE DEVICE: in User-Agent '{user_agent_ua}' absent BROWSER {device_resp}"
        assert device_resp == device_ua, f"FAIL DEVICE: in User-Agent '{user_agent_ua}', expected '{device_ua}', but '{device_resp}'"

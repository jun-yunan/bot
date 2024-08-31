import json
from selenium.webdriver.remote.webdriver import WebDriver


def save_cookies(file_path: str, cookies=None):
    try:
        with open(file_path, "w") as file:
            json.dump(cookies, file, indent=4)

    except Exception as e:
        print(f"An error occurred save cookies: {e}")


def load_cookies(driver: WebDriver, file_path: str):
    try:
        with open(file_path, "r") as file:
            cookies = json.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
                print(f"Cookie {cookie['name']} added.")
    except Exception as e:
        print(f"An error occurred load cookies: {e}")


def get_cookies(driver: WebDriver):
    # Lấy cookies từ trình duyệt
    cookies = driver.get_cookies()
    return cookies

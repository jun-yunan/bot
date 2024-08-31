import json
from selenium.webdriver.remote.webdriver import WebDriver


def get_local_storage(driver: WebDriver, key=None):
    if key:
        return driver.execute_script(f"return window.localStorage.getItem('{key}');")
    else:
        return driver.execute_script("return JSON.stringify(window.localStorage);")


def get_local_storages(driver: WebDriver):
    # Chèn mã JavaScript để lấy tất cả các mục từ localStorage
    try:
        local_storage = driver.execute_script(
            "return JSON.stringify(window.localStorage);"
        )
        return json.loads(local_storage)

    except Exception as e:
        print(f"An error occurred get local storage: {e}")
        local_storages = None
        return local_storages


def load_local_storage(driver, data):
    try:
        json_data = json.dumps(data)
        script = f"""
        var data = JSON.parse(arguments[0]);
        for (var key in data) {{
            localStorage.setItem(key, data[key]);
        }}
        """
        driver.execute_script(script, json_data)
    except Exception as e:
        print(f"An error occurred load local storage: {e}")


def get_session_storage(driver: WebDriver, key=None):
    if key:
        return driver.execute_script(f"return window.sessionStorage.getItem('{key}');")
    else:
        return driver.execute_script("return JSON.stringify(window.sessionStorage);")


def set_local_storage(driver: WebDriver, key, value):
    script = f"window.localStorage.setItem('{key}', '{value}');"
    driver.execute_script(script)


def set_session_storage(driver: WebDriver, key, value):
    script = f"window.sessionStorage.setItem('{key}', '{value}');"
    driver.execute_script(script)

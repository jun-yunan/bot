import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
)


def find_element(
    driver: WebDriver,
    by: By,
    value: str,
    timeout=10,
    condition=EC.presence_of_element_located,
) -> WebElement:
    try:
        return WebDriverWait(driver, timeout).until(condition((by, value)))
    except TimeoutException as e:
        print(
            f'The element with {by}="{value}" was not found within {timeout} seconds.'
        )
        return None
    except ElementClickInterceptedException as e:
        print(f'Element {by}="{value}" was found but could not be clicked.')
        # print(e)  # Nếu bạn muốn in ra thông tin chi tiết về lỗi
        return None


def save_to_file(data, filename):
    try:
        # async with aiofiles.open(filename, "w") as file:
        #     await file.write(json.dumps(data, indent=4))
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    except Exception as e:
        print(f"An error occurred save to file: {e}")


def read_json_file(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data

    except Exception as e:
        print(f"An error occurred read json file: {e}")
        return None


def switch_to_original_window(driver: WebDriver):
    original_window = driver.current_window_handle

    while True:
        current_windows = driver.window_handles
        if len(current_windows) == 1:
            print("Switched to original window")
            break

        for window in current_windows:
            if window != original_window:
                driver.switch_to.window(window)
                driver.close()
                driver.switch_to.window(original_window)
        time.sleep(1)

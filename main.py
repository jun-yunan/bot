import os
import json
import time
import threading
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from utils import find_element
from initialize_driver import initialize_driver
from anti_bot import undetected_browser
from utils import switch_to_original_window
from local_storage import get_local_storages
from local_storage import load_local_storage
from utils import read_json_file
from utils import save_to_file
from cookie import save_cookies
from cookie import load_cookies
from cookie import get_cookies


def set_window_screen(driver: WebDriver, num_threads: int, thread_name: str):
    window_width = 200
    window_height = 800
    window_x = (num_threads - int(thread_name.split("-")[1])) * (window_width + 10)
    window_y = 10
    driver.set_window_rect(window_x, window_y, window_width, window_height)


def get_and_save_local_storage(driver: WebDriver, thread_name: str):
    local_storage_data = get_local_storages(driver)
    save_to_file(
        local_storage_data, f"local_storage_data\\local_storage_{thread_name}.json"
    )


def read_and_load_local_storage(driver: WebDriver, thread_name: str):
    local_storage_data = read_json_file(
        f"local_storage_data\\local_storage_{thread_name}.json"
    )
    load_local_storage(driver, local_storage_data)
    print(f"Thread {thread_name} loaded local storage.")


def get_and_save_cookies(driver: WebDriver, thread_name: str):
    cookies = get_cookies(driver)
    save_cookies(file_path=f"cookies_data\\cookies_{thread_name}.json", cookies=cookies)
    print(f"Thread {thread_name} saved cookies.")


def get_query_id(driver: WebDriver):
    find_query_id = driver.execute_script(
        "return window.sessionStorage.getItem('__telegram__initParams');"
    )

    if find_query_id:
        return json.loads(find_query_id)["tgWebAppData"]
    else:
        print("Query id not found.")
        return None


# Đọc tệp JSON
def read_json_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def call_api(file_path: str, thread_name: str):
    try:
        data = read_json_file(file_path)
        print(json.dumps(data, indent=4))
        url = f"http://localhost:3000/api/v1/cookies"
        payload = {
            "name": thread_name,
            "cookie": json.dumps(data, indent=4),
        }
        headers = {}
        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            print(response.json())
        else:
            print("Failed to fetch api.")

    except Exception as e:
        print("Some thing went wrong!: ", e)


def read_dirs(main_directory: str):
    for root, dirs, files in os.walk(main_directory):
        break
    return dirs


def get_name_profiles(path: str):
    dirs = read_dirs(path)
    name_profiles = [f for f in dirs if f.startswith("Profile")]
    return name_profiles


def run_normal(driver: WebDriver, url: str, thread_name: str, actions: ActionChains):
    try:
        driver.get(url)
        driver.implicitly_wait(10)

        title = find_element(driver, By.TAG_NAME, "title")
        if not title:
            print("Title not found.")
            driver.quit()

        print(title.get_attribute("innerText") + " - " + thread_name)

        # time.sleep(2)
        # switch_to_original_window(driver=driver)
        # get_and_save_cookies(driver, thread_name)
        # get_and_save_local_storage(driver, thread_name)

        # call_api(
        #     file_path=f"cookies_data\\cookies_{thread_name}.json",
        #     thread_name=thread_name,
        # )

        load_cookies(driver, f"cookies_data\\cookies_thread_1.json")
        load_local_storage(
            driver,
            read_json_file(f"local_storage_data\\local_storage_thread_1.json"),
        )
        driver.refresh()

        print(f"Thread {thread_name} is visiting {url}")
        input("Press Enter to continue...")

    except Exception as e:
        print("Some thing went wrong!: ", e)

    finally:
        driver.quit()
        print(f"Thread {thread_name} is finished.")


def run_profile(
    url: str, thread_name: str, num_threads: int, profile_path: str, profile_name: str
):
    # get_name_profiles(r"C:\Users\JunYUNAN\AppData\Local\Google\Chrome\User Data")
    print(f"Thread {thread_name} is starting...")
    driver = initialize_driver(profile_path, profile_name)
    # set_window_screen(driver, num_threads, thread_name)
    undetected_browser(driver)
    actions = ActionChains(driver)
    run_normal(driver, url, thread_name, actions)


def main():
    path = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data")
    # url = "https://x.com/home"
    # url = "https://web.telegram.org/a/"
    url = "https://www.facebook.com/"

    # số luồng
    # num_threads = len(get_name_profiles(path))
    num_threads = 1

    profiles = [
        {
            "path": f"{path}\\Profile 19",
            "name": "Default",
        },
        # {
        #     "path": f"{path}\\Profile 20",
        #     "name": "Default",
        # }
        # {
        #     "path": path,
        #     "name": "Profile 7",
        # }
    ]
    # profile_name = get_name_profiles(path)
    # for profile in profile_name:
    #     profiles.append(
    #         {
    #             "path": path,
    #             "name": profile,
    #         }
    #     )

    # Tạo và khởi động các luồng
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(
            target=run_profile,
            args=(
                url,
                # f"{profile_name[i]}",
                f"thread_{i+1}",
                num_threads,
                profiles[i]["path"],
                profiles[i]["name"],
            ),
        )
        threads.append(thread)
        thread.start()
        time.sleep(3)

    # Chờ tất cả các luồng hoàn thành
    for thread in threads:
        thread.join()

    print("All threads have finished.")


if __name__ == "__main__":
    main()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def initialize_driver(profile_path, profile_name):
    options = webdriver.ChromeOptions()

    # options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument(f"--profile-directory={profile_name}")

    # undetected_chromedriver
    options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    # options.add_argument("--disable-extensions")
    # options.add_experimental_option("detach", True)
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--remote-debugging-port=9222")
    # options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")  # Vô hiệu hóa sandbox
    options.add_argument("--disable-dev-shm-usage")  # Vô hiệu hóa /dev/shm
    options.add_argument("--remote-allow-origins=*")
    options.add_argument("--disable-infobars")
    # options.add_argument("--enable-cookies")  # Cho phép cookie
    # options.add_argument("--headless")  # Chạy ẩn (không hiển thị trình duyệt)
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    # options.add_argument("--start-maximized")

    # options.add_extension(r"C:\Users\JunYUNAN\Downloads\Extenstion\0.0.42_0.crx")
    # options.add_extension(r"C:\Users\JunYUNAN\Downloads\Extenstion\4.8.0_0.crx")
    # options.add_extension(r"C:\Users\JunYUNAN\Desktop\Memefi_bot\Memefi_bot.crx")

    # driver_path = (
    #     r"C:\Users\JunYUNAN\Downloads\Chrome\chromedriver-win64\chromedriver.exe"
    # )
    # service = Service(ChromeDriverManager().install())
    # service = Service(executable_path=driver_path)
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome(options=options)
    return driver

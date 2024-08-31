from selenium.webdriver.remote.webdriver import WebDriver

from selenium_stealth import stealth


def undetected_browser(driver: WebDriver):
    # Sử dụng selenium-stealth để giảm khả năng bị phát hiện
    stealth(
        driver=driver,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6306.204 Safari/537.36",
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        run_on_insecure_origins=True,
    )

    # Vô hiệu hóa thuộc tính navigator.webdriver
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

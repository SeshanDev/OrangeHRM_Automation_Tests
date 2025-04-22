import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PageObjects.LeavePage import LeavePage
from PageObjects.LoginPage import Login
from PageObjects.DashboardPage import Dashboard
from Utilities.full_screenshot_util import take_fullscreen_screenshot
from Utilities.screenshot_util import take_screenshot


class Test_02_OrangeHRM:
    base_url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    username = "Admin"
    password = "admin123"

    @pytest.fixture(autouse=True)
    def setup(self, request):
        self.driver = webdriver.Chrome()
        self.driver.get(self.base_url)

        # Set the window size
        window_width = 1200  # Adjust the width
        window_height = 800  # Adjust the height
        screen_width = self.driver.execute_script("return screen.width;")
        screen_height = self.driver.execute_script("return screen.height;")

        # Positioning the browser in the top-right corner of the screen
        self.driver.set_window_position(screen_width - window_width, 0)
        self.driver.set_window_size(window_width, window_height)

        # Wait for the page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        def teardown():
            """Teardown after the test."""
            self.driver.quit()

            # Take the fullscreen screenshot after closing the browser
            take_fullscreen_screenshot("terminal_idle_view")  # Fullscreen screenshot when terminal is idle

        # Register the teardown function to be executed after the test
        request.addfinalizer(teardown)

        yield
        # After the test, the browser will be closed, and the finalizer will take the screenshot.

    def test_login_functionality(self):
        login = Login(self.driver)
        login.setUsername(self.username)
        login.setPassword(self.password)
        login.clickLogin()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h6[text()="Dashboard"]'))
        )
        take_screenshot(self.driver, "login_successful")  # ✅ Screenshot of browser
        take_fullscreen_screenshot("login_successful_terminal_view")  # Fullscreen terminal view

        assert "dashboard" in self.driver.current_url

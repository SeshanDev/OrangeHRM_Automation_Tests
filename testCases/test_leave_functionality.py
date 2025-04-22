import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from PageObjects.DashboardPage import Dashboard
from PageObjects.LeavePage import LeavePage
from PageObjects.LoginPage import Login
from Utilities.full_screenshot_util import take_fullscreen_screenshot
from Utilities.screenshot_util import take_screenshot


class Test_03_OrangeHRM:
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

    def test_leave_functionality(self):
        """Test to verify the leave functionality"""
        # Log in to the application
        login = Login(self.driver)
        login.setUsername(self.username)
        login.setPassword(self.password)
        login.clickLogin()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h6[text()="Dashboard"]'))
        )
        take_screenshot(self.driver, "after_login")  # ✅ Screenshot of browser
        take_fullscreen_screenshot("after_login_terminal_view")  # Fullscreen terminal view

        # Click on the "My Leave" button using the title attribute
        dashboard = Dashboard(self.driver)

        # Assuming the button has the title attribute with value "My Leave"
        my_leave_button_xpath = "//button[@title='My Leave']"

        # Wait for the button to be clickable and click it
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, my_leave_button_xpath))
        ).click()

        # Wait for the leave page to load and the necessary element to appear
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "oxd-layout")]'))
        )

        take_screenshot(self.driver, "leave_page")  # ✅ Screenshot of browser
        take_fullscreen_screenshot("leave_page_terminal_view")  # Fullscreen terminal view

        # Additional, check if the page header contains 'Leave'
        leave_page = LeavePage(self.driver)
        header_text = leave_page.get_leave_header()

        print(f"Header text found: '{header_text}'")

        # If the header text is 'Leave', it indicates the "My Leave" page is loaded
        assert header_text, "No header text found - element not located"
        assert "Leave" in header_text, f"Expected 'Leave' in header but got: '{header_text}'"

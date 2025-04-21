import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PageObjects.LeavePage import LeavePage
from PageObjects.LoginPage import Login
from PageObjects.DashboardPage import Dashboard



class Test_03_OrangeHRM:
    base_url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    username = "Admin"
    password = "admin123"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.base_url)
        self.driver.maximize_window()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        yield
        self.driver.quit()



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

        # Additional, check if the page header contains 'Leave'
        leave_page = LeavePage(self.driver)
        header_text = leave_page.get_leave_header()

        print(f"Header text found: '{header_text}'")

        # If the header text is 'Leave', it indicates the "My Leave" page is loaded
        assert header_text, "No header text found - element not located"
        assert "Leave" in header_text, f"Expected 'Leave' in header but got: '{header_text}'"


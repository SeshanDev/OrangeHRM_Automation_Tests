import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PageObjects.LeavePage import LeavePage
from PageObjects.LoginPage import Login
from PageObjects.DashboardPage import Dashboard



class Test_01_OrangeHRM:
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

    def test_login_page_title(self):
        assert self.driver.title == "OrangeHRM"

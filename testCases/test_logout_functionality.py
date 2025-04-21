import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PageObjects.LeavePage import LeavePage
from PageObjects.LoginPage import Login
from PageObjects.DashboardPage import Dashboard



class Test_04_OrangeHRM:
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


    def test_logout_functionality(self):
        login = Login(self.driver)
        login.setUsername(self.username)
        login.setPassword(self.password)
        login.clickLogin()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h6[text()="Dashboard"]'))
        )

        dashboard = Dashboard(self.driver)
        dashboard.clickProfileDropdown()
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//a[text()='Logout']"))
        )
        dashboard.clickLogout()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        assert "auth/login" in self.driver.current_url

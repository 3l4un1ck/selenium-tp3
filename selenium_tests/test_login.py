from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest


class TestAuthSelenium:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        yield
        self.driver.quit()

    def test_register_flow(self):
        self.driver.get('http://localhost:5000/auth/register')

        # Fill in registration form
        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        username_input.send_keys('seleniumuser')
        password_input.send_keys('seleniumpass123')
        submit_button.click()

        # Check if redirected to login page
        assert '/auth/login' in self.driver.current_url

        # Check success message
        flash_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
        )
        assert 'successfully registered' in flash_message.text

    def test_login_flow(self):
        self.driver.get('http://localhost:5000/auth/login')

        # Fill in login form
        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        username_input.send_keys('seleniumuser')
        password_input.send_keys('seleniumpass123')
        submit_button.click()

        # Check if redirected to index page
        assert '/todo_views/index' in self.driver.current_url

        # Check success message
        flash_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-success'))
        )
        assert 'successfully logged in' in flash_message.text

    def test_invalid_login(self):
        self.driver.get('http://localhost:5000/auth/login')

        # Try login with wrong credentials
        username_input = self.driver.find_element(By.NAME, 'username')
        password_input = self.driver.find_element(By.NAME, 'password')
        submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        username_input.send_keys('wronguser')
        password_input.send_keys('wrongpass')
        submit_button.click()

        # Check error message
        flash_message = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'alert-error'))
        )
        assert 'Incorrect username' in flash_message.text

    def test_logout_flow(self):
        # First login
        self.test_login_flow()

        # Find and click logout link
        logout_link = self.driver.find_element(By.XPATH, "//a[@href='/auth/logout']")
        logout_link.click()

        # Check if redirected to index page
        assert self.driver.current_url.endswith('/')
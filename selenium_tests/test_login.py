from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")

def test_login():
    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost:5000/login")
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin")
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(1)
    assert "Contacts" in driver.page_source
    driver.quit()
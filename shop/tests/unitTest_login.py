import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class LoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/accounts/login/")

    def test_login_form_entry(self):
        driver = self.driver

        username_box = driver.find_element(By.NAME, "username")
        password_box = driver.find_element(By.NAME, "password")

        username_box.send_keys("testuser")
        time.sleep(1)

        password_box.send_keys("testpassword123")
        time.sleep(1)

        self.assertEqual(username_box.get_attribute("value"), "testuser")
        self.assertEqual(password_box.get_attribute("value"), "testpassword123")

    def tearDown(self):
        time.sleep(2)
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
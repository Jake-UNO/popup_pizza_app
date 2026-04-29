import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time


class OrderConfirmationTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/")

    def test_place_order_and_send_confirmation_email(self):
        driver = self.driver

        # Click first product
        driver.find_element(By.CSS_SELECTOR, ".product-list a").click()
        time.sleep(1)

        # Add to cart
        driver.find_element(By.NAME, "quantity").send_keys("1")
        driver.find_element(By.XPATH, "//input[@value='Add Pizza to Order']").click()
        time.sleep(1)

        # Go to cart
        driver.get("http://127.0.0.1:8000/cart/")
        time.sleep(1)

        # Checkout
        driver.find_element(By.XPATH, "//a[contains(text(),'Checkout')]").click()
        time.sleep(1)

        # Fill form
        driver.find_element(By.NAME, "first_name").send_keys("Test")
        driver.find_element(By.NAME, "last_name").send_keys("User")
        driver.find_element(By.NAME, "email").send_keys("jakesorenson83@gmail.com")

        # Select first available pickup slot
        select = Select(driver.find_element(By.NAME, "pickup_slot"))
        select.select_by_index(1)

        time.sleep(1)

        # Submit order
        driver.find_element(By.XPATH, "//input[@type='submit']").click()
        time.sleep(3)

        # Confirm success page loaded
        self.assertIn("Thank you", driver.page_source)
        self.assertIn("successfully completed", driver.page_source)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
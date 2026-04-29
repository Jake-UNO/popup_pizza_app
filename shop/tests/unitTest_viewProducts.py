import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class ViewProductsTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:8000/")

    def test_view_products(self):
        driver = self.driver

        time.sleep(2)

        # Confirm homepage loaded
        self.assertIn("Popup Pizza", driver.page_source)

        # Scroll a bit (makes recording clearer)
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(2)

        # Click first product
        driver.find_element(By.CSS_SELECTOR, ".product-list a").click()
        time.sleep(2)

        # Confirm product page
        self.assertIn("Add Pizza to Order", driver.page_source)

        # Go back to menu
        driver.back()
        time.sleep(2)

    def tearDown(self):
        time.sleep(2)
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
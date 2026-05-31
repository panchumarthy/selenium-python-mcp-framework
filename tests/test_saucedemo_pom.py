"""
Standard POM-based Selenium tests for SauceDemo.
These run in CI without any AI/API dependency.
For AI-driven interactive testing, see test_goals.md.
"""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"


class TestLogin:
    def test_successful_login(self, driver):
        login = LoginPage(driver).open()
        login.login(VALID_USER, VALID_PASS)
        inventory = InventoryPage(driver)
        assert inventory.is_on_inventory_page(), "Should redirect to inventory after login"

    def test_invalid_credentials_show_error(self, driver):
        login = LoginPage(driver).open()
        login.login("wrong_user", "wrong_pass")
        assert login.get_error_message() != "", "Error message should be displayed"

    def test_locked_out_user_shows_error(self, driver):
        login = LoginPage(driver).open()
        login.login("locked_out_user", VALID_PASS)
        error = login.get_error_message()
        assert "locked out" in error.lower(), f"Expected locked-out error, got: {error}"

    def test_empty_username_shows_error(self, driver):
        login = LoginPage(driver).open()
        login.login("", VALID_PASS)
        assert login.get_error_message() != "", "Error message should appear for empty username"

    def test_empty_password_shows_error(self, driver):
        login = LoginPage(driver).open()
        login.login(VALID_USER, "")
        assert login.get_error_message() != "", "Error message should appear for empty password"


class TestInventory:
    @pytest.fixture(autouse=True)
    def login(self, driver):
        LoginPage(driver).open().login(VALID_USER, VALID_PASS)
        self.inventory = InventoryPage(driver)

    def test_inventory_page_loads(self, driver):
        assert self.inventory.is_on_inventory_page()

    def test_six_products_displayed(self, driver):
        names = self.inventory.get_item_names()
        assert len(names) == 6, f"Expected 6 products, got {len(names)}"

    def test_all_products_have_prices(self, driver):
        prices = self.inventory.get_item_prices()
        assert len(prices) == 6
        for price in prices:
            assert "$" in price, f"Price should contain '$': {price}"

    def test_add_first_item_to_cart(self, driver):
        self.inventory.add_item_by_index(0)
        assert self.inventory.get_cart_count() == 1

    def test_add_multiple_items_to_cart(self, driver):
        self.inventory.add_item_by_index(0)
        self.inventory.add_item_by_index(1)
        assert self.inventory.get_cart_count() == 2

    def test_sort_by_price_low_to_high(self, driver):
        self.inventory.sort_by("lohi")
        prices = self.inventory.get_item_prices()
        numeric = [float(p.replace("$", "")) for p in prices]
        assert numeric == sorted(numeric), "Prices should be in ascending order"

    def test_sort_by_name_z_to_a(self, driver):
        self.inventory.sort_by("za")
        names = self.inventory.get_item_names()
        assert names == sorted(names, reverse=True), "Names should be in descending order"


class TestCart:
    @pytest.fixture(autouse=True)
    def login_and_add_item(self, driver):
        LoginPage(driver).open().login(VALID_USER, VALID_PASS)
        inventory = InventoryPage(driver)
        inventory.add_item_to_cart("Sauce Labs Backpack")
        inventory.go_to_cart()
        self.cart = CartPage(driver)

    def test_cart_shows_added_item(self, driver):
        items = self.cart.get_cart_items()
        assert any("Backpack" in i for i in items), f"Backpack not found in cart: {items}"

    def test_cart_item_has_price(self, driver):
        prices = self.cart.get_cart_prices()
        assert len(prices) == 1
        assert "$" in prices[0]

    def test_remove_item_empties_cart(self, driver):
        self.cart.remove_item("Sauce Labs Backpack")
        items = self.cart.get_cart_items()
        assert len(items) == 0, "Cart should be empty after removal"

    def test_continue_shopping_returns_to_inventory(self, driver):
        self.cart.continue_shopping()
        inventory = InventoryPage(driver)
        assert inventory.is_on_inventory_page()


class TestCheckout:
    @pytest.fixture(autouse=True)
    def setup_checkout(self, driver):
        LoginPage(driver).open().login(VALID_USER, VALID_PASS)
        inventory = InventoryPage(driver)
        inventory.add_item_by_index(0)
        inventory.go_to_cart()
        self.cart = CartPage(driver)
        self.driver = driver

    def test_checkout_flow_completes(self, driver):
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        self.cart.proceed_to_checkout()

        def fill_react(el, value):
            driver.execute_script("""
                var s = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                s.call(arguments[0], arguments[1]);
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, el, value)

        wait = WebDriverWait(driver, 10)
        fill_react(wait.until(EC.presence_of_element_located((By.ID, "first-name"))), "John")
        fill_react(driver.find_element(By.ID, "last-name"), "Doe")
        fill_react(driver.find_element(By.ID, "postal-code"), "12345")

        continue_btn = driver.find_element(By.CSS_SELECTOR, "[data-test='continue']")
        driver.execute_script("arguments[0].click();", continue_btn)
        wait.until(lambda d: "checkout-step-two" in d.current_url)

        finish_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='finish']")))
        driver.execute_script("arguments[0].click();", finish_btn)

        confirmation = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".complete-header"))
        )
        assert "thank you" in confirmation.text.lower(), f"Unexpected confirmation: {confirmation.text}"

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEM_NAME = ".inventory_item_name"
    CART_ITEM_PRICE = ".inventory_item_price"
    REMOVE_BTN = "[data-test^='remove']"
    CHECKOUT_BTN = "[data-test='checkout']"
    CONTINUE_SHOPPING_BTN = "[data-test='continue-shopping']"

    def get_cart_items(self) -> list[str]:
        return [el.text for el in self.find_all(self.CART_ITEM_NAME)]

    def get_cart_prices(self) -> list[str]:
        return [el.text for el in self.find_all(self.CART_ITEM_PRICE)]

    def remove_item(self, item_name: str):
        items = self.find_all(self.CART_ITEM_NAME)
        buttons = self.find_all(self.REMOVE_BTN)
        count_before = len(items)
        for i, item in enumerate(items):
            if item_name.lower() in item.text.lower():
                self.driver.execute_script("arguments[0].click();", buttons[i])
                # Wait for the DOM to reflect the removal
                self.wait.until(
                    lambda d: len(d.find_elements(By.CSS_SELECTOR, self.CART_ITEM_NAME)) < count_before
                )
                return True
        raise ValueError(f"Item '{item_name}' not found in cart")

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BTN)
        self.wait.until(lambda d: "checkout-step-one" in d.current_url)

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING_BTN)
        self.wait.until(lambda d: "inventory" in d.current_url)

    def is_on_cart_page(self) -> bool:
        return "cart" in self.current_url

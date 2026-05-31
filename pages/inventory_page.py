from pages.base_page import BasePage


class InventoryPage(BasePage):
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    ADD_TO_CART_BTN = "[data-test^='add-to-cart']"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"
    SORT_DROPDOWN = "[data-test='product-sort-container']"
    PAGE_TITLE = ".title"

    def get_item_names(self) -> list[str]:
        return [el.text for el in self.find_all(self.ITEM_NAME)]

    def get_item_prices(self) -> list[str]:
        return [el.text for el in self.find_all(self.ITEM_PRICE)]

    def add_item_to_cart(self, item_name: str):
        names = self.find_all(self.ITEM_NAME)
        buttons = self.find_all(self.ADD_TO_CART_BTN)
        for i, item in enumerate(names):
            if item_name.lower() in item.text.lower():
                self.driver.execute_script("arguments[0].click();", buttons[i])
                return True
        raise ValueError(f"Item '{item_name}' not found on inventory page")

    def add_item_by_index(self, index: int = 0):
        buttons = self.find_all(self.ADD_TO_CART_BTN)
        self.driver.execute_script("arguments[0].click();", buttons[index])

    def get_cart_count(self) -> int:
        if self.is_visible(self.CART_BADGE):
            return int(self.text_of(self.CART_BADGE))
        return 0

    def go_to_cart(self):
        self.driver.get("https://www.saucedemo.com/cart.html")

    def sort_by(self, option: str):
        """Options: 'az', 'za', 'lohi', 'hilo'"""
        from selenium.webdriver.support.ui import Select
        select = Select(self.find(self.SORT_DROPDOWN))
        select.select_by_value(option)

    def is_on_inventory_page(self) -> bool:
        return "inventory" in self.current_url

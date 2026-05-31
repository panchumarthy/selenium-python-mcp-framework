from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com"

    USERNAME = "#user-name"
    PASSWORD = "#password"
    LOGIN_BTN = "#login-button"
    ERROR_MSG = "[data-test='error']"

    def open(self):
        self.driver.get(self.URL)
        return self

    def login(self, username: str, password: str):
        self.fill(self.USERNAME, username)
        self.fill(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def get_error_message(self) -> str:
        return self.text_of(self.ERROR_MSG) if self.is_visible(self.ERROR_MSG) else ""

    def is_on_login_page(self) -> bool:
        return "saucedemo.com" in self.current_url and self.is_visible(self.LOGIN_BTN)

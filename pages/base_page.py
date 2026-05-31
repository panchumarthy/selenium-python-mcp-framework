from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find(self, css):
        return self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css)))

    def find_all(self, css):
        return self.driver.find_elements(By.CSS_SELECTOR, css)

    def click(self, css):
        el = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
        self.driver.execute_script("arguments[0].click();", el)

    def fill(self, css, text):
        el = self.find(css)
        # Use React-compatible value setter so controlled inputs update their state
        self.driver.execute_script("""
            var s = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            s.call(arguments[0], arguments[1]);
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, el, text)

    def text_of(self, css) -> str:
        return self.find(css).text

    def is_visible(self, css) -> bool:
        try:
            return self.find(css).is_displayed()
        except Exception:
            return False

    @property
    def current_url(self) -> str:
        return self.driver.current_url

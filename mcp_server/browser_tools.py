"""
Selenium browser tool implementations called by the MCP server.
Each function maps directly to an MCP tool exposed to the Claude agent.
"""

import base64
import os
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils.driver_factory import create_driver

_driver: Optional[webdriver.Chrome] = None


def _get_driver() -> webdriver.Chrome:
    global _driver
    if _driver is None:
        raise RuntimeError("Browser not started. Call start_browser first.")
    return _driver


def start_browser(headless: bool = False) -> dict:
    global _driver
    _driver = create_driver(headless=headless)
    return {"status": "ok", "message": "Browser started"}


def stop_browser() -> dict:
    global _driver
    if _driver:
        _driver.quit()
        _driver = None
    return {"status": "ok", "message": "Browser stopped"}


def navigate_to(url: str) -> dict:
    driver = _get_driver()
    driver.get(url)
    return {"status": "ok", "title": driver.title, "url": driver.current_url}


def get_page_text() -> dict:
    driver = _get_driver()
    return {"status": "ok", "text": driver.find_element(By.TAG_NAME, "body").text}


def get_page_source() -> dict:
    driver = _get_driver()
    return {"status": "ok", "source": driver.page_source[:8000]}


def find_elements(selector: str, by: str = "css") -> dict:
    driver = _get_driver()
    by_map = {
        "css": By.CSS_SELECTOR,
        "xpath": By.XPATH,
        "id": By.ID,
        "name": By.NAME,
        "class": By.CLASS_NAME,
        "tag": By.TAG_NAME,
        "text": By.LINK_TEXT,
    }
    by_strategy = by_map.get(by.lower(), By.CSS_SELECTOR)
    elements = driver.find_elements(by_strategy, selector)
    results = []
    for i, el in enumerate(elements[:20]):
        results.append({
            "index": i,
            "tag": el.tag_name,
            "text": el.text[:200],
            "visible": el.is_displayed(),
            "enabled": el.is_enabled(),
        })
    return {"status": "ok", "count": len(elements), "elements": results}


def click_element(selector: str, by: str = "css", index: int = 0) -> dict:
    driver = _get_driver()
    by_map = {
        "css": By.CSS_SELECTOR,
        "xpath": By.XPATH,
        "id": By.ID,
        "name": By.NAME,
        "class": By.CLASS_NAME,
    }
    by_strategy = by_map.get(by.lower(), By.CSS_SELECTOR)
    try:
        wait = WebDriverWait(driver, 10)
        elements = wait.until(EC.presence_of_all_elements_located((by_strategy, selector)))
        target = elements[index]
        driver.execute_script("arguments[0].scrollIntoView(true);", target)
        driver.execute_script("arguments[0].click();", target)
        return {"status": "ok", "message": f"Clicked element [{index}] matching '{selector}'"}
    except TimeoutException:
        return {"status": "error", "message": f"Element not found: {selector}"}
    except IndexError:
        return {"status": "error", "message": f"Index {index} out of range for selector '{selector}'"}


def fill_input(selector: str, value: str, by: str = "css", clear_first: bool = True) -> dict:
    driver = _get_driver()
    by_map = {
        "css": By.CSS_SELECTOR,
        "xpath": By.XPATH,
        "id": By.ID,
        "name": By.NAME,
    }
    by_strategy = by_map.get(by.lower(), By.CSS_SELECTOR)
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((by_strategy, selector)))
        driver.execute_script("""
            var s = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
            s.call(arguments[0], arguments[1]);
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
        """, element, value)
        return {"status": "ok", "message": f"Filled '{selector}' with value"}
    except TimeoutException:
        return {"status": "error", "message": f"Input not found: {selector}"}


def press_key(selector: str, key: str, by: str = "css") -> dict:
    driver = _get_driver()
    by_map = {"css": By.CSS_SELECTOR, "xpath": By.XPATH, "id": By.ID}
    by_strategy = by_map.get(by.lower(), By.CSS_SELECTOR)
    key_map = {"enter": Keys.ENTER, "tab": Keys.TAB, "escape": Keys.ESCAPE}
    key_value = key_map.get(key.lower(), key)
    try:
        element = driver.find_element(by_strategy, selector)
        element.send_keys(key_value)
        return {"status": "ok", "message": f"Pressed {key} on '{selector}'"}
    except NoSuchElementException:
        return {"status": "error", "message": f"Element not found: {selector}"}


def get_element_attribute(selector: str, attribute: str, by: str = "css") -> dict:
    driver = _get_driver()
    by_map = {"css": By.CSS_SELECTOR, "xpath": By.XPATH, "id": By.ID, "name": By.NAME}
    by_strategy = by_map.get(by.lower(), By.CSS_SELECTOR)
    try:
        element = driver.find_element(by_strategy, selector)
        value = element.get_attribute(attribute)
        return {"status": "ok", "attribute": attribute, "value": value}
    except NoSuchElementException:
        return {"status": "error", "message": f"Element not found: {selector}"}


def take_screenshot(filename: str = "screenshot.png") -> dict:
    driver = _get_driver()
    screenshots_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    path = os.path.join(screenshots_dir, filename)
    driver.save_screenshot(path)
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return {"status": "ok", "path": path, "base64": encoded[:500] + "...(truncated)"}


def get_current_url() -> dict:
    driver = _get_driver()
    return {"status": "ok", "url": driver.current_url, "title": driver.title}


def wait_for_element(selector: str, by: str = "css", timeout: int = 10) -> dict:
    driver = _get_driver()
    by_map = {"css": By.CSS_SELECTOR, "xpath": By.XPATH, "id": By.ID}
    by_strategy = by_map.get(by.lower(), By.CSS_SELECTOR)
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by_strategy, selector))
        )
        return {"status": "ok", "message": f"Element '{selector}' is visible"}
    except TimeoutException:
        return {"status": "error", "message": f"Element '{selector}' not visible after {timeout}s"}

"""
Creates and configures a Selenium WebDriver instance.
Used by both the MCP server and the pytest fixtures.
"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_driver(headless: bool = None) -> webdriver.Chrome:
    if headless is None:
        headless = os.getenv("HEADLESS", "false").lower() == "true"

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    return driver

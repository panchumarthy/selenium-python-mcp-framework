import os
import pytest
from dotenv import load_dotenv
from utils.driver_factory import create_driver

load_dotenv()


@pytest.fixture(scope="function")
def driver():
    d = create_driver()
    yield d
    d.quit()


@pytest.fixture(scope="function")
def driver_headless():
    d = create_driver(headless=True)
    yield d
    d.quit()

import pytest  # pytest framework for test execution
from playwright.sync_api import sync_playwright  # playwright module for browser actions


@pytest.fixture(scope="session", params=["chromium"])
def browser(request):
    """Fixture to launch the browser based on the parameter"""
    with sync_playwright() as pw_obj:
        browser = pw_obj[request.param].launch(headless=False)
        yield browser
        browser.close()

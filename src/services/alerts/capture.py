"""
Selenium automation that goes to tradingview create_image_url (its a tradingview layout)
and submits a hotkey to generate a chart image url.
"""

import time

import pyperclip
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Capture:
    """
    Selenium automation
    """

    def __init__(self, chart_url) -> None:
        chrome_options = Options()
        # chrome_options.add_argument(argument="--headless")
        chrome_options.add_argument("--start-minimized")
        chrome_options.add_argument(argument="--no-sandbox")
        chrome_options.add_argument(argument="--force-dark-mode")
        chrome_options.add_argument(argument="--window-size=1920,1080")

        self.chart_url = chart_url
        self.driver = webdriver.Chrome(options=chrome_options)

    def capture_image_url(self) -> str:
        """
        Send keyboard shortcut and return the URL
        """
        image_url: str = ""
        try:
            self.driver.get(url=self.chart_url)
            self.wait_for_tradingview_chart()
            image_url = self.get_tradingview_image_link()

        finally:
            self.clean_up()

        return image_url

    def clean_up(self) -> None:
        """
        Close Browser
        """
        self.driver.quit()

    def send_shortcut(self) -> str:
        """
        Press ALT+S to have chart image url copied to clipboard
        """

        actions = ActionChains(driver=self.driver)
        actions.key_down(value=Keys.ALT).key_down(value="s").key_up(value=Keys.ALT)
        actions.perform()

        return pyperclip.paste()

    def wait_for_tradingview_chart(self) -> None:
        """
        Wait for the driver to load the tradingview chart
        """

        wait = WebDriverWait(driver=self.driver, timeout=10)
        wait.until(
            method=EC.presence_of_element_located(
                locator=(
                    By.CSS_SELECTOR,
                    "body > div.js-rootresizer__contents.layout-with-border-radius",
                )
            )
        )

    def get_tradingview_image_link(self) -> str:
        """
        Loop to see if the copied clipboard is the image URL

        Returns:
            str: Image URL or Empty if timeout
        """

        attempts = 10
        attempt = 0
        time.sleep(2)

        while attempt < attempts:
            clipboard: str = self.send_shortcut()
            if clipboard.startswith("https://www.tradingview.com/x/"):
                return clipboard

            time.sleep(0.5)
            attempt += 1

        return ""

import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class BrowserEngine:
    def __init__(self, headless=False):
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")

        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.binary_location = "/usr/bin/google-chrome"

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.options)

    def get_maps_data(self, search_query):
        try:
            self.driver.get("https://www.google.com/maps")

            # Handle cookie consent if present
            try:
                wait = WebDriverWait(self.driver, 5)
                accept_xpath = "//span[contains(text(), 'Accept') or contains(text(), 'Aceptar')]"
                self.driver.find_element(By.XPATH, accept_xpath).click()
            except:
                pass

            # Execute search
            wait = WebDriverWait(self.driver, 10)
            search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
            search_box.send_keys(search_query + Keys.ENTER)

            # Wait for results and scroll
            feed_selector = "div[role='feed']"
            scrollable_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, feed_selector)))
            self._scroll_sidebar(scrollable_div)

            return self.driver.page_source
        except Exception as e:
            print(f"Browser error: {e}")
            return None

    def _scroll_sidebar(self, scrollable_div):
        last_height = self.driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
        while True:
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scrollable_div)
            time.sleep(random.uniform(2.0, 4.0))
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
            if new_height == last_height:
                break
            last_height = new_height

    def visit_business_page(self, maps_url):
        try:
            self.driver.get(maps_url)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            time.sleep(1)
            return self.driver.page_source
        except Exception as e:
            return None
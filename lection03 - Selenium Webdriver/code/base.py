import pytest
from ui.locators import basic_locators
from selenium.common.exceptions import StaleElementReferenceException


CLICK_RETRY = 3


class BaseCase:
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver

    def find(self, locator):
        return self.driver.find_element(*locator)

    def search(self, query):
        elem = self.find(basic_locators.QUERY_LOCATOR_ID)
        elem.send_keys(query)
        go_button = self.find(basic_locators.GO_BUTTON_LOCATOR)
        go_button.click()

    def click(self, locator):
        for i in range(CLICK_RETRY):
            try:
                elem = self.find(locator)
                # if i < 2:
                #     self.driver.refresh()
                elem.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise

import time
import allure
import pytest
from web_tests.base import BaseCase


class TestWikipediaWeb(BaseCase):
    # @pytest.mark.skip(reason='TEMP')
    @pytest.mark.MWUI
    @pytest.mark.UI
    @allure.severity(allure.severity_level.NORMAL)
    @allure.epic("Awesome PyTest framework")
    @allure.title("Test login")
    @allure.description("Test for login")
    @allure.feature('Login tests')
    def test_login(self):
        self.login_page.login()



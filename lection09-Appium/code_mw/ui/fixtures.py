import os
import shutil

import allure
import pytest
from selenium import webdriver
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage
from ui.pages.login_page import LoginPage, LoginPageMW
from ui.pages.search_page import SearchPage
from ui.pages.title_page import TitlePage
from ui.pages.title_list_page import TitleListPage
from ui import pages

from webdriver_manager.chrome import ChromeDriverManager


class UnsupportedBrowserType(Exception):
    pass


def get_driver(browser_name):
    manager = ChromeDriverManager(version='latest')
    if browser_name == 'chrome':
        browser = webdriver.Chrome(executable_path=manager.install())
    else:
        raise UnsupportedBrowserType(f' Unsupported browser {browser_name}')
    return browser


@pytest.fixture(scope='function')
def driver(config, test_dir):
    url = config['url']
    browser_name = config['browser']
    browser = get_driver(browser_name)
    browser.get(url)
    yield browser
    browser.quit()


@pytest.fixture(scope='function')
def ui_report(driver, request, test_dir):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)

        browser_logfile = os.path.join(test_dir, 'browser.log')
        with open(browser_logfile, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

        with open(browser_logfile, 'r') as f:
            allure.attach(f.read(), 'browser.log', attachment_type=allure.attachment_type.TEXT)

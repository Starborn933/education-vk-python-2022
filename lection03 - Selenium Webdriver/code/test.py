import pytest
from base import BaseCase
from ui.locators import basic_locators


class TestExample(BaseCase):

    @pytest.mark.parametrize(
        'query',
        [
            pytest.param(
              'pycon'
            ),
            pytest.param(
                'python'
            ),
        ],
    )
    @pytest.mark.skip('skip')
    def test_search(self, query):
        self.search(query)
        assert 'No results found' not in self.driver.page_source

    @pytest.mark.skip('skip')
    def test_negative_search(self):
        self.search('adasdasdasdasdasda')
        assert 'No results found' not in self.driver.page_source

    @pytest.mark.UI
    def test_page_change(self):
        self.click(basic_locators.GO_BUTTON_LOCATOR)

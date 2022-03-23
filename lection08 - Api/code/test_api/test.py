import pytest

from api.client import InvalidLoginException
from test_api.base import BaseApi


class TestApi(BaseApi):

    def test_valid_login(self):
        # Проверка bStateError происхоидт в _request
        self.api_client.post_login()

    def test_invalid_login(self):
        self.api_client.user = 'User'
        self.api_client.password = 'Password'

        with pytest.raises(InvalidLoginException):
            self.api_client.post_login()
            pytest.fail(f'Login with {self.api_client.user} and {self.api_client.password} unexpectedly passed')

        res = self.api_client.post_login(set_session=False)
        assert res['bStateError'] is True


class TestTopicDraft(BaseApi):
    publish = False

    def test_topic_creation(self, topic):
        self.api_client.get_topic(topic.id)


class TestTopicPublish(TestTopicDraft):
    publish = True

    def test_topic_creation(self, topic):
        super(TestTopicPublish, self).test_topic_creation(topic)
        self.check_topic_in_feed(topic_id=topic, title=topic.title, text=topic.text)


########################################################################

class TestTopicDraftVar2(BaseApi):
    publish = False

    def check(self, topic):
        self.api_client.get_topic(topic.id)

    def test_topic_creation(self, topic):
        self.check(topic)


class TestTopicPublishVar2(TestTopicDraftVar2):
    publish = True

    def check(self, topic):
        self.check_topic_in_feed(topic_id=topic.id, title=topic.title, text=topic.text)

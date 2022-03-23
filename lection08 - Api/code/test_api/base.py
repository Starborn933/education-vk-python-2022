import pytest

from utils.builder import Builder


class BaseApi:
    BLOG_ID = 403

    authorize = True
    publish = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client
        self.builder = Builder()

        if self.authorize:
            self.api_client.post_login()

    @pytest.fixture(scope='function')
    def topic(self):
        topic_data = self.builder.topic()

        result = self.api_client.post_topic_create(blog_id=self.BLOG_ID, title=topic_data.title, text=topic_data.text,
                                                   publish=self.publish)
        topic_id = result.json()['redirect_url'].split('/')[-2]
        topic_data.id = int(topic_id)
        yield topic_data
        self.api_client.post_topic_delete(topic_id)

    def create_topic(self, title, text, publish=True):
        res = self.api_client.post_topic_create(self.BLOG_ID, title, text, publish=publish)

        return int(res['redirect_url'].split('/')[-2])

    def check_topic_in_feed(self, topic_id, title, text, feed_type='all'):
        all_topics = self.api_client.get_feed(feed_type=feed_type)

        topic = [i for i in all_topics['items'] if i['object']['id'] == topic_id]
        assert topic, f'Topic with id {topic_id} not present in feed_type {feed_type}'

        topic = topic[0]
        assert topic['object']['title'] == title
        assert topic['object']['text'] == text

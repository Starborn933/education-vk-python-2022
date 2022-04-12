from faker import Faker
from models.models import BannerModel


class MysqlBuilder:
    def __init__(self, client):
        self.client = client

    def create_banners(self, name=None, url=None):
        fake = Faker()
        banner_name = name or fake.job()
        banner_url = url or fake.url()

        banner = BannerModel(
            name=banner_name,
            url=banner_url
        )
        self.client.session.add(banner)
        self.client.session.commit()

        return banner

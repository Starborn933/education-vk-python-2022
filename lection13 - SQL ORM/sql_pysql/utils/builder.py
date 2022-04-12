from faker import Faker

class MysqlBuilder:
    def __init__(self, client):
        self.client = client

    def create_banners(self, name=None, url=None):
        fake = Faker()
        banner_name = name or fake.job()
        banner_url = url or fake.url()
        insert_query = f"""
            insert into `banner` (`name`, `url`) values ("{banner_name}", "{banner_url}")
            """
        self.client.execute_query(insert_query)

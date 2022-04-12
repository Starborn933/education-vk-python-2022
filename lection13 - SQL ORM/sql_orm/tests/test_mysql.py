import pytest
from mysql.client import MysqlClient
from utils.builder import MysqlBuilder
from models.models import BannerModel


class MyTest:

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql: MysqlClient = mysql_client
        self.builder: MysqlBuilder = MysqlBuilder(self.mysql)

        self.prepare()

    def get_banners(self, **filters):
        self.mysql.session.commit()
        res = self.mysql.session.query(BannerModel).filter_by(**filters)
        return res.all()


class TestMySql(MyTest):

    def prepare(self):
        banner = self.builder.create_banners()

    def test(self):
        count = self.get_banners()
        assert len(count) == 1

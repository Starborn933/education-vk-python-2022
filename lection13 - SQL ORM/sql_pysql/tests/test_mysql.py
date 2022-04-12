import pytest
from mysql.client import MysqlClient
from utils.builder import MysqlBuilder


class MyTest:

    def prepare(self):
        pass

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql: MysqlClient = mysql_client
        self.builder: MysqlBuilder = MysqlBuilder(self.mysql)

        self.prepare()

    def get_banners(self):
        res = self.mysql.execute_query("select * from `banner`", fetch=True)
        return res


class TestMySql(MyTest):

    def prepare(self):
        self.builder.create_banners()
        self.banner_id = self.mysql.connection.insert_id()

    def test(self):
        count = self.get_banners()
        assert len(count) == 1

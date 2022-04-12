import pymysql
from faker import Faker


# создать подключение к бд
connection = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='root',
                             password='0000',
                             db=None,  # бд не выбрана
                             charset='utf8',
                             )

connection.query('DROP database IF EXISTS `target`')
connection.query('CREATE database `target`')
connection.close()


connection = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='root',
                             password='0000',
                             db='target',
                             charset='utf8',
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor
                             )
create_banner = """
create table `banner`(
    `id` smallint(6) not null auto_increment,
    `name` char(50) not null,
    `url` char(50) not null,
    primary key (`id`)
 )
"""
connection.query(create_banner)

fake = Faker()
for _ in range(5):
    insert_query = f"""
    insert into `banner` (`name`, `url`) values ("{fake.job()}", "{fake.url()}")
    """
    connection.query(insert_query)

res = connection.query("select * from banner")
print(res)

cursor = connection.cursor()
cursor.execute("select * from banner")
print(cursor.fetchone())
connection.close()

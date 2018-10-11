
import unittest
import requests
import pymysql

class InterfaceTest(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.session = requests.session()
        memberID = ''

    def get_Member_Info(self):

        # 打开数据库连接
        db = pymysql.connect(host='56cbb9f62fac6.sh.cdb.myqcloud.com', port=6634, user='cdb_outerroot', password='@09ui%sbc09',
                 database="gic3_test")
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # SQL 查询语句
        sql = '''SELECT member_id FROM gic3_test.`tab_gic_member_0` WHERE third_nickname = '可乐' AND enterprise_id = 'ff8080815dacd3a2015dacd3ef5c0000'
UNION
SELECT member_id FROM gic3_test.`tab_gic_member_1` WHERE third_nickname = '可乐' AND enterprise_id = 'ff8080815dacd3a2015dacd3ef5c0000'
UNION
SELECT member_id FROM gic3_test.`tab_gic_member_2` WHERE third_nickname = '可乐' AND enterprise_id = 'ff8080815dacd3a2015dacd3ef5c0000'
UNION
SELECT member_id FROM gic3_test.`tab_gic_member_3` WHERE third_nickname = '可乐' AND enterprise_id = 'ff8080815dacd3a2015dacd3ef5c0000'
UNION
SELECT member_id FROM gic3_test.`tab_gic_member_4` WHERE third_nickname = '可乐' AND enterprise_id = 'ff8080815dacd3a2015dacd3ef5c0000'
UNION
SELECT member_id FROM gic3_test.`tab_gic_member_5` WHERE third_nickname = '可乐' AND enterprise_id = 'ff8080815dacd3a2015dacd3ef5c0000'
UNION
SELECT member_id FROM gic3_test.`tab_gic_member_6` WHERE third_nickname = '可乐' AND enterprise_id = 'ff8080815dacd3a2015dacd3ef5c0000'
UNION
SELECT member_id FROM gic3_test.`tab_gic_member_7` WHERE third_nickname = '可乐' AND enterprise_id = 'ff8080815dacd3a2015dacd3ef5c0000'
UNION
SELECT member_id FROM gic3_test.`tab_gic_member_8` WHERE third_nickname = '可乐' AND enterprise_id = 'ff8080815dacd3a2015dacd3ef5c0000'
UNION
SELECT member_id FROM gic3_test.`tab_gic_member_9` WHERE third_nickname = '可乐' AND enterprise_id = 'ff8080815dacd3a2015dacd3ef5c0000';'''
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                memberID = row[0]
                # 打印结果
                print(self.memberID)
        except:
            print("Error: unable to fetch data")

        # 关闭数据库连接
        db.close()
        return memberID

    def test_b_login_operations(self):
        login_data = {
            'loginName': '123456',
            'password': 'ywtest'
        }
        self.login_result = self.session.post(url='http://gicdev.demogic.com/gic-operations/login_process', data=login_data)
        print(self.login_result.content)


    def test_c_delAimMember(self):
        enterpriseID = "ff8080815dacd3a2015dacd3ef5c0000"
        del_data = {
            'eid': enterpriseID,
            'memberId': self.get_Member_Info(),
            'sex': '1',
            'dataReviseCode': '1108',
            'application': 'gic - webapp - admin',
            'cmqQueue': 'MemberCouponToErp - 1',
            'sycErpStatus': 'UPDATE_1',
            'checkBox': 'false'
        }
        self.result = self.session.post(url='http://gicdev.demogic.com/gic-operations/invok_date_revise', data=del_data)
        print(self)

    @classmethod
    def tearDownClass(cls):
        pass

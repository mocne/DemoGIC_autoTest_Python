
import unittest
import requests
import pymysql

class delMember(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = requests.session()
        global memberID
        memberID = ''

    def test_a_get_Member_Info(self):
        try:
            # 打开数据库连接
            self.db = pymysql.connect(host='56cbb9f62fac6.sh.cdb.myqcloud.com', port=6634, user='cdb_outerroot', password='@09ui%sbc09',
                     database="gic3_test")
            # 使用cursor()方法获取操作游标
            cursor = self.db.cursor()
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
                if len(results) == 0:return
                for row in results:
                    memberID = str(row[0])
                    self.db.close()
                    return True
            except Exception as e:
                print("Error: unable to fetch data")
                print(e)

            # 关闭数据库连接
            self.db.close()
            return False
        except Exception as e:
            print(e)
            print('can not get the memberId')


    def test_b_login_operations(self):
        login_data = {
            'loginName': '123456',
            'password': 'ywtest'
        }
        self.login_result = self.session.post(url='http://gicdev.demogic.com/gic-operations/login_process', data=login_data)

    def test_c_delAimMember(self):
        if memberID == '':
            print('\n\n###################################can not del with the blank value###################################\n\n')
        else:
            enterpriseID = "ff8080815dacd3a2015dacd3ef5c0000"
            del_data = {
                'eid': enterpriseID,
                'memberId': memberID,
                'sex': '1',
                'dataReviseCode': '1108',
                'application': 'gic - webapp - admin',
                'cmqQueue': 'MemberCouponToErp - 1',
                'sycErpStatus': 'UPDATE_1',
                'checkBox': 'false'
            }
            self.result = self.session.post(url='http://gicdev.demogic.com/gic-operations/invok_date_revise', data=del_data)

    @classmethod
    def tearDownClass(cls):
        pass

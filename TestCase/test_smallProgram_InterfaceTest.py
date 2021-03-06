#  -*- coding: utf-8 -*-
import json
import smtplib
import time
from email.mime.text import MIMEText

import pymysql
import requests
import unittest
import yaml
import sys

sys.path.append('E:\Code\DemoGIC_autoTest_Python')

from COMMON import HTMLTestRunner


class InterfaceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # tmpData = open("./MyData/test.yml", "rb")
        # cls.testData = yaml.load(tmpData.read())

        try:
            cls.db = pymysql.connect(host='212.64.10.76', port=3306, user='root', passwd='root', db='mocne_test',
                                     charset="utf8")
        except Exception as e:
            print(e.__context__)

    def setUp(self):
        if self._testMethodName == 'test_get_member_center_info':
            cursor = self.db.cursor()
            sql_select = "SELECT interface, note, protocol, host, port, path, method, get_params, post_params, check_sql, check_data FROM `mocne_test`.`interface_case` WHERE status = 1;"
            try:
                # 执行sql语句
                cursor.execute(sql_select)
                # 获取所有记录列表
                self.aimTestData = list(cursor.fetchall())
            except Exception as e:
                print(e)
                print("Error: unable to fecth data")
            cursor.close()
        self.session = requests.session()

    def test_interface_run(self):
        self.session.get('https://www.baidu.com')

    def test_get_member_center_info(self):
        self.session.get('https://www.baidu.com')
        tmpTestData = self.aimTestData
        for tmp in tmpTestData:
            if tmp[6] == 'GET':
                self.session.get(url=tmp[2] + '://' + tmp[3] + tmp[5] + '?' + tmp[7])
            elif tmp[6] == 'POST':
                responseStr = self.session.post(url=tmp[2] + '://' + tmp[3] + tmp[5],
                                                data=tmp[8])
                responseStatus = responseStr.status_code
                if responseStatus == 200:
                    aaa = json.dumps(responseStr.text)
                    print('pass')

    def tearDown(self):
        self.session.close()

    @classmethod
    def tearDownClass(cls):
        pass


#  ---发送邮件---
def send_email(report_file):
    sender = "811703707@qq.com"
    receiver = "917597939@qq.com"
    smtpserver = "smtp.qq.com"
    # 发送邮箱的账号密码,此处使用的是qq邮箱和第三方登录的授权码
    username = "811703707@qq.com"
    password = "xpodmmugjdonbfgb"

    # 定义邮件正文
    file = open(report_file, "rb")
    mail_body = file.read()
    file.close()

    msg = MIMEText(mail_body, _subtype="html", _charset="utf-8")
    msg["Subject"] = u"自动化测试报告"
    msg["From"] = "AutoTester<811703707@qq.com>"
    msg["To"] = "ReportReceiver<917597939@qq.com>"

    # att = MIMEText(open(report_file, 'rb').read(), 'base64', 'utf-8')
    # att["Content-Type"] = 'application/octet-stream'
    # # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    # att["Content-Disposition"] = 'attachment; filename="接口测试报告.html"'
    # msg.attach(att)

    smtp = smtplib.SMTP_SSL(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print("Email has send out !")


if __name__ == '__main__':
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    testunit = unittest.TestSuite()
    testunit.addTest(InterfaceTest("test_interface_run"))
    testunit.addTest(InterfaceTest('test_get_member_center_info'))
    HtmlFile = './Reports/' + now + "-InterfaceTest-HTMLtemplate.html"
    fp = open(HtmlFile, "ab+")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"接口测试报告", description=u"用例测试情况")
    runner.run(testunit)
    fp.close()
    send_email(HtmlFile)

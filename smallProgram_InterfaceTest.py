#  -*- coding: utf-8 -*-
import smtplib
import time
from email.mime.text import MIMEText

import requests
import unittest

import yaml

import HTMLTestRunner


class InterfaceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        tmpData = open("./myData/test.yml", "rb")
        cls.testData = yaml.load(tmpData.read())

    def setUp(self):
        self.session = requests.session()

    def test_interface_run(self):
        self.session.get('https://www.baidu.com')

    def test_get_member_center_info(self):
        self.session.get('https://www.baidu.com')
        tmpTestData = self.testData['smallProgram']['login']['get_member_center_info']
        for tmp in tmpTestData:
            if tmp['method'].equals('GET'):
                self.session.get(url=tmp['Protocol'] + '://' + tmp['Host'] + tmp['Path'] + '?' + tmp['params']['GET'])
            elif tmp['method'].equals('POST'):
                self.session.post(url=tmp['Protocol'] + '://' + tmp['Host'] + tmp['Path'], data=tmp['params']['POST'])
        print('admin')

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
    HtmlFile = './result/' + now + "-InterfaceTest-HTMLtemplate.html"
    fp = open(HtmlFile, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"接口测试报告", description=u"用例测试情况")
    runner.run(testunit)
    fp.close()
    send_email(HtmlFile)

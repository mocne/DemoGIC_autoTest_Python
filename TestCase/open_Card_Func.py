#  -*- coding: utf-8 -*-
import json
import os
import smtplib
import time
from email.mime.text import MIMEText
import requests
import unittest
import sys

sys.path.append('E:\Code\DemoGIC_autoTest_Python')

from COMMON import HTMLTestRunner

class open_Card_Func(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = requests.session()
        unittest.TextTestRunner().run(unittest.defaultTestLoader.discover(os.getcwd(), pattern="delMember.py", top_level_dir=None))

    def setUp(self):
        pass

    def test_a_check_Nginx(self):
        nginxResult = self.session.get(url='https://www.gicdev.com/').status_code
        assert nginxResult == 200
        return True

    @unittest.skipUnless(True, 'can not link to nginx')
    def test_b_get_ext_file(self):
        login_data = {
            'loginName': '123456',
            'password': 'ywtest'
        }
        self.login_result = self.session.post(url='http://gicdev.demogic.com/gic-operations/login_process',
                                              data=login_data).status_code
        if self.login_result == 200:
            extResult = self.session.post(url='http://gicdev.demogic.com/gic-operations/loadMiniProgramSetting', data={'eid': 'ff8080815dacd3a2015dacd3ef5c0000'})
            extJson = json.loads(extResult.text)
            extJsonRlt = extJson['msg']
            if extJsonRlt == '操作成功':
                extContent = extJson['data']['extJson']
                extJsonFile = json.loads(extContent)
                global extVersion
                extVersion = extJsonFile['ext']['build']
                tabBarList = extJsonFile['ext']['tabBar']['list']
                global tabBarLists
                tabBarLists = []
                for tabBar in tabBarList:
                    tabBarLists.append(tabBar['text'])
                print('')

    @unittest.skipUnless(True, 'can not link to nginx')
    def test_c_get_tabBar_menu(self):
        tabBar_data = {
            'appid': 'wx9d30a2aa1fc6d77a',
            'version': extVersion,
            'transId': 'wx9d30a2aa1fc6d77a2018 - 10 - 11 19: 43:36',
            'sign': '4da94030fe06b213891121cbb069f304',
            'timestamp': '2018 - 10 - 11 19: 43:36'
        }
        tabBarResult = self.session.post(url='https://www.gicdev.com/gic-wx-app/get-custom-guide-data.json', data=tabBar_data)
        tabBarInfo = json.loads(tabBarResult.text)
        assert tabBarResult.status_code == 200
        tabBars = tabBarInfo['response']['pages']
        for i in range(0,len(tabBars)):
            assert tabBars[i]['text'] == tabBarLists[i]
        print('')

    def tearDown(self):
        pass

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
    testunit.addTest(open_Card_Func("test_interface_run"))
    testunit.addTest(open_Card_Func('test_get_member_center_info'))
    HtmlFile = './Reports/' + now + "-InterfaceTest-HTMLtemplate.html"
    fp = open(HtmlFile, "ab+")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u"接口测试报告", description=u"用例测试情况")
    runner.run(testunit)
    fp.close()
    send_email(HtmlFile)

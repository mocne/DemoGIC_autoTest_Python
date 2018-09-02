#  -*- coding: utf-8 -*-

from email.mime.text import MIMEText

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os, sys

mail_host = 'xxxxx'
mail_from = 'xxxxx'
mail_pass = 'xxxxxx'


def addAttch(to_list, subject, content, path):
    msg = MIMEMultipart('related')                                      #  采用related定义内嵌资源的邮件体
    msgtext = MIMEText(content, _subtype='plain', _charset='utf-8')     #_subtype有plain,html等格式，避免使用错误

    msg.attach(msgtext)

    os.chdir(path)
    dir = os.getcwd()

    for fn in os.listdir(dir):                                          #  返回字符串文件名
        attach = MIMEText(open(fn, 'rb').read())
        attach["Content-Type"] = 'application/octet-stream'
        attach["Content-Disposition"] = 'attachment; filename=' + fn
        msg.attach(attach)
    msg['Subject'] = subject
    msg['From'] = mail_from
    msg['To'] = to_list

    server = smtplib.SMTP()
    server.connect(mail_host, 587)
    server.starttls()
    server.login(mail_from, mail_pass)
    server.sendmail(mail_from, msg['To'], msg.as_string())
    server.quit()


if __name__ == '__main__':
    msg = addAttch('shuqiang.yang@msxf.com', '对账', '对账数据', '/home/dbaops/Shell/finance_debt/AccountBalance')

# -*- coding: utf-8 -*-
import pymysql

# 打开数据库 （如果连接失败会报错）
db = pymysql.connect(host='127.0.0.1', port=3306, user='minbo', passwd='123456', db='pythontest', charset="utf8")

cursor = db.cursor()
sql_select1 = "select version()"

sql_select = '''select * from user'''
try:
    # 执行sql语句
    cursor.execute(sql_select)
    # 获取所有记录列表
    result = cursor.fetchall()
    for row in result:
        id = row[0]
        name = row[1]
        print("id = %d, name = %s" % (id, name))
except:
    print("Error: unable to fecth data")


db.close()

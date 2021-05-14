# coding:utf-8
# __author__ ='syx'

import re
import pymysql
import time
import requests

f1 = open('phone.txt', 'r')
#获取所有行数据
data1 = f1.read().splitlines()
# print data1
f1.close()
# 数据库连接
conn = pymysql.connect(host='192.168.100.70', port= 3306, user='root', password='mysqlHolder', db='qxh_island', charset='utf8')
print(conn)

def update_package_coupon(data):
    '''获取响应数据中的taxid参数'''
    url = f'https://zhuancan.holderzone.cn/island/api/designated_coupon_package?cpPackageId=279&platFormId=394&userIds={data}'
    print(url)
    r = requests.post(url, f'cpPackageId=279&platFormId=394&userIds={data}', )
    return r

# 设置函数
# listTemp 为列表 平分后每份列表的的个数n
def groupfunc(listTemp, n):
    result = []
    for i in range(0, len(listTemp), n):
        b = listTemp[i:i + n]
        result.append(b)
    return result
#使用cursor()方法创建一个游标对象
cursor = conn.cursor()

print(data1)
#获取每一行数据分组  数字代表每组的条数
data = groupfunc(data1, 10)

for line in data:
    print(tuple(line))
    # 使用execute()方法执行SQL查询
    cursor.execute(f'select group_concat(id) from island_user where phone in {tuple(line)} and platform_id = 394')
    # 使用fetchone()方法获取单条数据
    sqlData = ','.join(cursor.fetchone())
    # 打印
    print(sqlData)
    result = ''
    if sqlData :
        result = update_package_coupon(sqlData)
    else:
        print('没有查询到userids')
    print(result)
    time.sleep(5)

#关闭数据库连接
conn.close()
print('发放成功')
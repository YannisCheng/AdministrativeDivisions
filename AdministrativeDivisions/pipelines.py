# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql as pymysql

from AdministrativeDivisions.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB_NAME, ENCODE


class AdministrativeDivisionsPipeline(object):
    def insertIntoTable(self, sql):
        # 创建连接
        conn = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWORD,
            db=MYSQL_DB_NAME,
            charset=ENCODE)  # 要指定编码，否则中文可能乱码

        # 创建游标
        cursor = conn.cursor()

        # 执行查询语句
        cursor.execute(sql)

        # 提交，不然无法保存新建或者修改的数据
        conn.commit()

        # 关闭游标
        cursor.close()

        # 关闭连接
        conn.close()

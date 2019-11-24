# -*- coding: utf-8 -*-


import pymysql
import time
import hashlib
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings  #导入seetings配置


class DBHelper(object):

    def __init__(self):

        settings = get_project_settings()
        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )

        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)

        self.dbpool = dbpool

        def connect(self):
            return self.dbpool

        # 创建数据库
        def insert(self, item):
            sql = "insert into tech_courses(title,image,brief,course_url,created_at) values(%s,%s,%s,%s,%s)"
            # 调用插入的方法
            query = self.dbpool.runInteraction(self._conditional_insert, sql, item)
            # 调用异常处理方法
            query.addErrback(self._handle_error)

            return item

        # 写入数据库中
        def _conditional_insert(self, tx, sql, item):
            item['created_at'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                               time.localtime(time.time()))
            item['md5'] = hashlib.md5(item['title']).hexdigest()
            params = (item["title"], item['url'], item['date'])
            tx.execute(sql, params)

        # 错误处理方法

        def _handle_error(self, failue):
            print('--------------database operation exception!!-----------------')
            print(failue)

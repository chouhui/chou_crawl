# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql as pq
import hashlib
import time
from fish.email_.send_email import send_email


class FishPipeline(object):

    def __init__(self):
        self.conn = pq.connect(host='localhost', user='root',
                               passwd='Cyh920610.', db='WEB', charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):

        title = item.get('title')
        url = item.get('url')
        date_ = item.get('date_')
        title_md = title.encode('utf-8')
        md5 = hashlib.md5(title_md).hexdigest()
        a = time.gmtime()
        create_time = time.strftime('%Y-%m-%d', a)

        sql = "insert into ustc(title, url, date_, md5, create_time) VALUES (%s, %s, %s, %s, %s)"
        try:
            self.cur.execute(sql, (title, url, date_, md5, create_time))
            self.conn.commit()
            # send_email(title)
        except Exception as e:

            print('error:......%s' % e)


class FinanceNewsPipeline(object):

    def __init__(self):
        self.conn = pq.connect(host='localhost', user='root',
                               passwd='Cyh920610.', db='WEB', charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):

        title = item.get('title')
        url = item.get('url')
        content = item.get('content')
        create_time = item.get('create_time')
        source = item.get('source')
        url = url.encode('utf-8')
        title = title.encode('utf-8')
        print url
        md5 = hashlib.md5(title).hexdigest()

        sql = "insert into finance_news_negative(title, content, url, create_time, source, md5) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            self.cur.execute(sql, (title, content, url, create_time, source, md5))
            self.conn.commit()
            # send_email(title)
        except Exception as e:

            print('error:......%s' % e)




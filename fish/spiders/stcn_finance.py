# coding: utf-8
# 证券时报 http://news.stcn.com/
import scrapy
import json
import re
import time
from fish.items.items import FinanceNewsItem


def clear(data):

    c = re.sub('<[^<]+?>', '', data).replace('\n', '').strip()

    return c


def clear_body(x):
    return x.strip()


class UstcSpider(scrapy.Spider):

    name = 'stcn_finance'
    DOWNLOAD_DELAY = 1

    def start_requests(self):

        url_list = [
            'http://app.stcn.com/?app=search&controller=index&action=search&type=article&wd=%E8%82%A1%E4%BB%B7%E6%9A%B4%E8%B7%8C&catid=&before=&after=%3B&order=rel&page=100',
            'http://app.stcn.com/?app=search&controller=index&action=search&type=article&wd=%E8%82%A1%E4%BB%B7%E4%B8%8B%E6%BB%91&catid=&before=&after=%3B&order=rel&page=100',
            'http://app.stcn.com/?app=search&controller=index&action=search&type=article&wd=%E8%A3%81%E5%91%98&catid=&before=&after=%3B&order=rel&page=6',
            'http://app.stcn.com/?app=search&controller=index&action=search&type=article&wd=%E5%AF%92%E5%86%AC&catid=&before=&after=%3B&order=rel&page=100',
            'http://app.stcn.com/?app=search&controller=index&action=search&type=article&wd=%E8%BF%BD%E7%A9%B6%E8%B4%A3%E4%BB%BB&catid=&order=rel&before=&after=%3B',

        ]

        for i in range(3, 101):

            url = 'http://app.stcn.com/?app=search&controller=index&action=search&type=article&wd=%E8%82%A1%E4%BB%B7%E6%9A%B4%E8%B7%8C&catid=&before=&after=%3B&order=rel&page={}'.format(i)
            yield scrapy.Request(url)

    def parse(self, response):

        body = response.xpath('//div[@id="search_list"]/dl/dt/a/@href').extract()
        body = list(set(body))
        for i in body:
            yield scrapy.Request(i, callback=self.parse2)

    def parse2(self, response):

        if 'news' in response.url:

            body = response.xpath('//div[@class="txt_con"]//p/text()').extract()

            title = response.xpath('//div[@class="intal_tit"]/h2/text()').extract_first()
        elif 'stock' in response.url or 'company' in response.url:
            body = response.xpath('//div[@id="ctrlfscont"]//p//text()').extract()

            title = response.xpath('//div[@class="txt_hd"]/h1/text()').extract_first()
        elif 'kuaixun' in response.url:
            body = response.xpath('//div[@id="ctrlfscont"]//p//text()').extract()

            title = response.xpath('//div[@class="intal_tit"]/h2/text()').extract_first()
            if not title:
                title = response.xpath('//div[@')

        else:
            body = response.xpath('//div[@class="txt_con"]//p/text()').extract()

            title = response.xpath('//div[@class="intal_tit"]/h2/text()').extract_first()
        if not body:
            print 'hello'
            print response.url

        content = ''.join(map(clear_body, body))

        if content:

            item = FinanceNewsItem()

            item['title'] = title.strip()
            item['content'] = content.strip()
            item['url'] = response.url
            yield item

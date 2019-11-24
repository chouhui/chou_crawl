# coding: utf-8
# 中证网  http://search.cs.com.cn/
import scrapy
import json
import re
import time
from fish.items.items import FinanceNewsItem


def clear(data):

    c = re.sub('<[^<]+?>', '', data).replace('\n', '').strip()

    return c


class UstcSpider(scrapy.Spider):

    name = 'cs_finance'
    DOWNLOAD_DELAY = 1

    def start_requests(self):

        url_list = [
            'http://search.cs.com.cn/search?page=4&channelid=215308&searchword=%E9%80%80%E5%B8%82&keyword=%E9%80%80%E5%B8%82&token=12.1462412070719.47&perpage=10&outlinepage=5&&andsen=&total=&orsen=&exclude=&searchscope=&timescope=&timescopecolumn=&orderby=', #28126
            'http://search.cs.com.cn/search?page=5&channelid=215308&searchword=%E7%A0%B4%E5%8F%91&keyword=%E7%A0%B4%E5%8F%91&token=12.1462412070719.47&perpage=10&outlinepage=5&&andsen=&total=&orsen=&exclude=&searchscope=&timescope=&timescopecolumn=&orderby=', #5464
            # 'http://search.cs.com.cn/search?page=4&channelid=215308&searchword=%E5%85%AC%E5%8F%B8%E5%8D%B7%E5%85%A5&keyword=%E5%85%AC%E5%8F%B8%E5%8D%B7%E5%85%A5&token=12.1462412070719.47&perpage=10&outlinepage=5&&andsen=&total=&orsen=&exclude=&searchscope=&timescope=&timescopecolumn=&orderby=',#139
            'http://search.cs.com.cn/search?page=5&channelid=215308&searchword=%E8%B7%8C%E5%81%9C&keyword=%E8%B7%8C%E5%81%9C&token=12.1462412070719.47&perpage=10&outlinepage=5&&andsen=&total=&orsen=&exclude=&searchscope=&timescope=&timescopecolumn=&orderby=', #49503
            'http://search.cs.com.cn/search?page=5&channelid=215308&searchword=%E5%B8%82%E5%80%BC%E8%92%B8%E5%8F%91&keyword=%E5%B8%82%E5%80%BC%E8%92%B8%E5%8F%91&token=12.1462412070719.47&perpage=10&outlinepage=5&&andsen=&total=&orsen=&exclude=&searchscope=&timescope=&timescopecolumn=&orderby=', #2645
            'http://search.cs.com.cn/search?page=5&channelid=215308&searchword=%E4%B8%9A%E7%BB%A9%E4%B8%8B%E6%BB%91&keyword=%E4%B8%9A%E7%BB%A9%E4%B8%8B%E6%BB%91&token=12.1462412070719.47&perpage=10&outlinepage=5&&andsen=&total=&orsen=&exclude=&searchscope=&timescope=&timescopecolumn=&orderby=', #15923
            'http://search.cs.com.cn/search?page=5&channelid=215308&searchword=%E6%96%AD%E5%B4%96%E5%BC%8F%E4%B8%8B%E8%B7%8C&keyword=%E6%96%AD%E5%B4%96%E5%BC%8F%E4%B8%8B%E8%B7%8C&token=12.1462412070719.47&perpage=10&outlinepage=5&&andsen=&total=&orsen=&exclude=&searchscope=&timescope=&timescopecolumn=&orderby=', #2693
            'http://search.cs.com.cn/search?page=4&channelid=215308&searchword=%E5%85%A8%E5%B9%B4%E4%BA%8F%E6%8D%9F&keyword=%E5%85%A8%E5%B9%B4%E4%BA%8F%E6%8D%9F&token=12.1462412070719.47&perpage=10&outlinepage=5&&andsen=&total=&orsen=&exclude=&searchscope=&timescope=&timescopecolumn=&orderby=', #2068
            'http://search.cs.com.cn/search?page=5&channelid=215308&searchword=%E5%87%80%E5%88%A9%E4%B8%8B%E6%BB%91&keyword=%E5%87%80%E5%88%A9%E4%B8%8B%E6%BB%91&token=12.1462412070719.47&perpage=10&outlinepage=5&&andsen=&total=&orsen=&exclude=&searchscope=&timescope=&timescopecolumn=&orderby=', #1735
            # 'http://search.cs.com.cn/search?page=2&channelid=215308&searchword=%E9%94%80%E5%94%AE%E9%A2%9D%E4%B8%8B%E6%BB%91&keyword=%E9%94%80%E5%94%AE%E9%A2%9D%E4%B8%8B%E6%BB%91&token=12.1462412070719.47&perpage=10&outlinepage=5&&andsen=&total=&orsen=&exclude=&searchscope=&timescope=&timescopecolumn=&orderby=' #301

        ]

        for i in range(1, 15):

            url = 'http://search.cs.com.cn/search?page={}&channelid=215308&searchword=%E5%85%AC%E5%8F%B8%E5%8D%B7%E5%85%A5&keyword=%E5%85%AC%E5%8F%B8%E5%8D%B7%E5%85%A5&token=12.1462412070719.47&perpage=10&outlinepage=5&&andsen=&total=&orsen=&exclude=&searchscope=&timescope=&timescopecolumn=&orderby='.format(i)
            yield scrapy.Request(url)

    def parse(self, response):

        body = response.xpath('//td[@class="searchresult"]/table//a/@href').extract()
        body = list(set(body))
        for i in body:
            if 'hk' not in i or 'overseas' not in i:
                yield scrapy.Request(i, callback=self.parse2)

    def parse2(self, response):

        body = response.xpath('//div[@class="article-t hidden"]//p/text()').extract()

        title = response.xpath('//div[@class="article"]/h1/text()').extract_first()
        if not body:
            print 'hello'
            body = response.xpath('//div[@class="artical_c"]//p/text()').extract()
            title = response.xpath('//div[@class="artical_t"]/h1/text()').extract_first()
            print body
            print title

        content = ''.join(body)

        if content and title:

            item = FinanceNewsItem()

            item['title'] = title.strip()
            item['content'] = content.strip()
            item['url'] = response.url
            yield item

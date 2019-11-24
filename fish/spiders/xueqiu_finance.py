# coding: utf-8
import scrapy
import json
import re
import time
from fish.items.items import FinanceNewsItem


def clear(data):

    c = re.sub('<[^<]+?>', '', data).replace('\n', '').strip()

    return c


class UstcSpider(scrapy.Spider):

    name = 'xueqiu_finance'
    DOWNLOAD_DELAY = 2
    # allowed_domains = ['xueqiu.com']
    headers = {
        'Host': 'xueqiu.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'DNT': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
    }

    cookie = 'aliyungf_tc=AQAAANEA52/YyQAAStrTOsPPZxzARZtA; acw_tc=2760820e15710438380616570e085f8ef178620287ddef7c4cfbd8a919a61b; device_id=24700f9f1986800ab4fcc880530dd0ed; s=bx114l6phd; __utma=1.1016718050.1571062812.1571062812.1571062812.1; __utmc=1; __utmz=1.1571062812.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_1db88642e346389874251b5a1eded6e3=1571043840,1571062170,1571103484; remember=1; remember.sig=K4F3faYzmVuqC0iXIERCQf55g2Y; xq_a_token=b93ed7bd9348a079f6b17cbe6e04d0d8b714b4e8; xq_a_token.sig=fzeyb14nftfE7T34kaKz3zD7dnA; xqat=b93ed7bd9348a079f6b17cbe6e04d0d8b714b4e8; xqat.sig=tHH2cDZmUeqT4AK_jtF-pWOvMdc; xq_r_token=e7177cf884ac1fca0dbac82696911c80bd91e32e; xq_r_token.sig=siWFvpWUpV1LkVHoA4Dy4l4o2lE; xq_is_login=1; xq_is_login.sig=J3LxgPVPUzbBg3Kee_PquUfih7Q; u=2579192882; u.sig=tCp2zcJupVj7mjmnmHdd0mZw47Y; bid=54203089bacf058624717b6966307eb3_k1r845uu; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1571107148'
    cookie_l = cookie.split('; ')
    cookies = {}
    for i in cookie_l:
        k, v = i.split('=', 1)
        cookies[k] = v

    # start_urls = ['https://xueqiu.com/statuses/search.json?sort=reply&source=user&q=%E8%A3%81%E5%91%98&count=20&page=1', ]

    def start_requests(self):

        for i in range(72, 101):
            # https://xueqiu.com/statuses/search.json?sort=time&source=all&q=%E8%82%A1%E4%BB%B7%E4%B8%8B%E8%B7%8C&count=10&page=1
            # https://xueqiu.com/statuses/search.json?sort=time&source=all&q=%E8%A3%81%E5%91%98&count=10&page=1
            # https://xueqiu.com/statuses/search.json?sort=reply&source=user&q=%E8%A3%81%E5%91%98&count=20&page=1
            # https://xueqiu.com/statuses/search.json?sort=reply&source=all&q=%E8%A3%81%E5%91%98&count=10&page={}
            url = 'https://xueqiu.com/statuses/search.json?q=涨&page={}&uid=5124430882&sort=time&comment=0&_=1571106282'
            yield scrapy.Request(url.format(i), cookies=self.cookies, headers=self.headers)

    def parse(self, response):

        body = response.body
        cons = json.loads(body)
        lists = cons['list']
        # lists = cons['statuses']
        for list in lists:

            item = FinanceNewsItem()

            o_time = list['created_at']
            c_time = time.localtime(int(o_time)/1000)
            t_time = time.strftime("%Y-%m-%d %H:%M:%S", c_time)

            item['title'] = clear(list['title'])
            item['content'] = clear(list['text'])

            # item['title'] = ''
            # item['content'] = clear(list['description'])
            item['url'] = 'https://xueqiu.com' + list['target']
            item['create_time'] = t_time
            item['source'] = 'xueqiu'

            # print item
            if u'跌' not in item['content']:

                yield item


        # print item

        # for bo in body:
        #
        #     url_raw = bo.xpath('./a/@href').extract_first()
        #     url_pre = 'https://sse.ustc.edu.cn/'
        #     title = bo.xpath('./a/text()').extract_first().strip()
        #     date_ = bo.xpath('./a/em/text()').extract_first()
        #
        #
        #     item['url'] = url_pre + url_raw
        #     item['title'] = title
        #     item['date_'] = date_
        #
        #     yield item
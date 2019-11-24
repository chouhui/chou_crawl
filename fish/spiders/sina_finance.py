# coding: utf-8
import scrapy
from ..items.items import FinanceNewsItem


class UstcSpider(scrapy.Spider):

    name = 'sina_finance'
    DOWNLOAD_DELAY = 0.5

    # allowed_domains = ['https://search.sina.com.cn']
    headers = {
        ':authority': 'search.sina.com.cn',
        ':method': 'GET',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'referer': 'https://search.sina.com.cn/?q=%B2%C3%D4%B1&range=all&c=news&sort=time&page=1&col=&source=&from=&country=&size=&time=&a=&pf=0&ps=0&dpc=1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'DNT': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    }
    cookie = 'U_TRS1=000000b4.6b5b338c.5d39598e.9c837716; U_TRS2=000000b4.6b65338c.5d39598e.e86077f9; UOR=,baby.sina.com.cn,; SINAGLOBAL=60.221.28.180_1564039687.561314; Apache=60.221.28.180_1564039687.561316; UM_distinctid=16c2807c21a223-04ef0dd7734ac-37637c02-fa000-16c2807c21caa; lxlrttp=1560672234; SCF=AoHacE_ZphjBf8jZ4NtObjUJUAm2BYl80Fa4yy9J7eFwUKUgvxjpOB4o0l6viennXwuYWd9FuKxOmoZyNUbFyYQ.; ULV=1564042039168:2:2:2:60.221.28.180_1564039687.561316:1564039688588; SGUID=1564061267359_5574604; sso_info=v02m6alo5qztKWRk5iljpOIpY6TiKWRk5ClkKSEpY6DmKWRk5ilkJSMpZCTiKWRk5SljoOQpZCkmKWRk5yljpSEpY6DkKWRk5yljpOkpZCkkKWRk5iljpOcpZCTlKWRk5ilkJOIpZCTmKadlqWkj5OMuYyTpLSMg6CxjIOAwA==; SessionID=d9difrtf9vahk2a01uliala1d3; gr_user_id=b61b3d48-1296-4512-9b2e-bcd42a4d4694; grwng_uid=713feecc-c67f-4308-a2ae-b7697a99b55d; vjuids=914d7b35b.16da1b92efa.0.b6fede8f92f39; vjlast=1570376331.1570376331.30; SINABLOGNUINFO=1000000000.3b9aca00.v5sinalogtest; ULOGIN_IMG=gz-82f52f553b880dd210b61cc27eef6985388c'

    cookie_l = cookie.split('; ')
    cookies = {}
    for i in cookie_l:
        k, v = i.split('=', 1)
        cookies[k] = v
    # print cookies

    def start_requests(self):

        for i in range(1, 20):
            #https://search.sina.com.cn/?q=%B2%C3%D4%B1&range=rel&c=news&sort=time&col=&source=&from=&country=&size=&time=&a=&page={}&pf=0&ps=0&dpc=1

            #
            url = 'http://search.sina.com.cn/?q=%B9%C9%BC%DB%B1%A9%D5%C7&range=title&c=news&sort=rel&col=&source=&from=&country=&size=&time=&a=&page={}&pf=0&ps=0&dpc=1'

            yield scrapy.Request(url.format(i), headers=self.headers, cookies=self.cookies)

    def parse(self, response):

        # item = FishItem()

        body = response.xpath('//div[@id="result"]/div[@class="box-result clearfix"]')

        for res in body:
            item = FinanceNewsItem()
            titles = res.xpath('.//h2/a//text()').extract()
            title = ''.join(titles)
            url = res.xpath('.//h2/a/@href').extract_first()
            time = res.xpath('.//h2/span/text()').extract_first().split(' ', 1)[-1]

            item['title'] = title
            item['url'] = url
            item['create_time'] = time

            yield scrapy.Request(url, headers=self.headers, meta={'item': item}, callback=self.parse2)

    def parse2(self, response):

        item = response.meta['item']

        body = response.xpath('//div[@class="article"]//p//text()').extract()
        content = ''.join(body).strip()
        if content == '':
            body = response.xpath('//div[@id="artibody"]//text()').extract()
            content = ''.join(body).strip()
        if 'blog' in item['url']:
            body = response.xpath('//div[@id="sina_keyword_ad_area2"]//text()').extract()
            content = ''.join(body).strip()
        if u'免责声明' in content:
            print 'yes'
            content = content.rsplit(u'免责声明', 1)[0]
        if u'参考文献' in content:
            print 'yes'
            content = content.rsplit(u'参考文献', 1)[0]
        if u'特别声明' in content:
            print 'yes'
            content = content.rsplit(u'特别声明', 1)[0]

        item['content'] = content
        item['source'] = 'sina'
        # if u'股价' or u'上涨' in item['title']:

        yield item


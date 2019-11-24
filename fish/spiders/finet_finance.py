# coding: utf-8
import scrapy
from ..items.items import FinanceNewsItem


def clear(t):
    return t.strip()


class UstcSpider(scrapy.Spider):

    name = 'finet_finance'
    DOWNLOAD_DELAY = 1

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

    def start_requests(self):

        for i in range(100, 150):
            #https://search.sina.com.cn/?q=%B2%C3%D4%B1&range=rel&c=news&sort=time&col=&source=&from=&country=&size=&time=&a=&page={}&pf=0&ps=0&dpc=1

            #
            url = 'https://www.finet.com.cn/news/hushenjiaodian/list_40_{}.html'

            yield scrapy.Request(url.format(i), headers=self.headers)

    def parse(self, response):


        body = response.xpath('//*[@id="main"]/div[2]/div[2]/div[2]/ul/li')

        for res in body:
            titles = res.xpath('./a//text()').extract()[0]
            url_raw = res.xpath('./a/@href').extract_first()
            url = 'https://www.finet.com.cn' + url_raw
            time_raw = res.xpath('./span/text()').extract_first()
            time = time_raw.split(' ')[0]

            if u'涨' in titles or u'增' in titles or u'净利润' in titles or u'走强' in titles or u'强势' in titles or u'拉升' in titles:
                print titles
                item = FinanceNewsItem()

                item['title'] = titles
                item['url'] = url
                item['create_time'] = time

                yield scrapy.Request(url, headers=self.headers, meta={'item': item}, callback=self.parse2)

    def parse2(self, response):

        item = response.meta['item']

        body = response.xpath('//div[@class="news_text"]//p//text()').extract()
        body = map(clear, body)

        content = ''.join(body).strip()

        if u'来源' in content:
            print 'yes'
            content = content.rsplit(u'来源', 1)[0]
        if u'(责任编辑' in content:

            content = content.rsplit(u'(责任编辑', 1)[0]

        item['content'] = content
        item['source'] = 'finet'
        # if u'股价' or u'上涨' in item['title']:

        yield item


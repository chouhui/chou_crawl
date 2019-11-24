# coding: utf-8
import scrapy
from ..items.items import FinanceNewsItem


class UstcSpider(scrapy.Spider):

    name = 'jiemian_finance'
    DOWNLOAD_DELAY = 1

    # allowed_domains = ['https://search.sina.com.cn']
    headers = {
        'Referer': 'None',
    }
    cookie = 'app_qrcode_hide=1; br-resp-key="g:191111145748d1400000004ef5930a526a"'

    cookie_l = cookie.split('; ')
    cookies = {}
    for i in cookie_l:
        k, v = i.split('=', 1)
        cookies[k] = v
    # print cookies

    def start_requests(self):

        for i in range(1, 5):
            #https://search.sina.com.cn/?q=%B2%C3%D4%B1&range=rel&c=news&sort=time&col=&source=&from=&country=&size=&time=&a=&page={}&pf=0&ps=0&dpc=1

            #
            url = 'https://a.jiemian.com/index.php?m=search&a=index&msg=%E7%BD%A2%E5%B7%A5&type=news&page={}'.format(i)
            # url = 'https://www.jiemian.com/article/3640323.html'
            yield scrapy.Request(url)

    def parse(self, response):

        body = response.xpath('//div[@class="news-header"]//a/@href').extract()

        for res in body:

            yield scrapy.Request(res,headers=self.headers, callback=self.parse2)

    def parse2(self, response):

        body = response.xpath('//div[@class="article-content"]/p//text()').extract()
        content = ''.join(body).strip()
        title = response.xpath('//div[@class="article-header"]/h1/text()').extract_first()
        item = FinanceNewsItem()

        item['title'] = title
        item['content'] = content
        item['source'] = 'jiemian'
        item['url'] = response.url
        # print item

        yield item

